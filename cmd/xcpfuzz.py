import re
import sys
import json
import time
import itertools
import argparse
import asyncio
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import aiohttp
from playwright.async_api import async_playwright, Page, Browser


PORTAL_BASE  = "https://portaldatransparencia.gov.br"
SEARCH_URL   = "https://busca.portaldatransparencia.gov.br/busca/pessoa-fisica"
TOKEN_FILE   = Path(__file__).resolve().parent / "token.txt"
REPO_URL     = "https://github.com/ravenastar-js/xcpfuzz"
MIRROR_URL   = "https://ravenastar.com/cmd/xcpfuzz.py"

_API_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
    "Referer": f"{PORTAL_BASE}/pessoa-fisica/busca/lista",
    "Origin": PORTAL_BASE,
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
}

_BLOCK_TYPES = {"image", "media", "font"}

_STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', {get: () => false, configurable: true});
Object.defineProperty(navigator, 'plugins', {get: () => [
    {name:'Chrome PDF Plugin', filename:'internal-pdf-viewer', description:'Portable Document Format'},
    {name:'Chrome PDF Viewer', filename:'mhjfbmdgcfjbbpaeojofohoefgiehjai', description:''},
    {name:'Native Client', filename:'internal-nacl-plugin', description:''}
]});
Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR','pt','en-US','en']});
Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
window.chrome = {runtime: {}, app: {isInstalled: false}};
"""


def _enable_ansi():
    if sys.platform == "win32":
        try:
            import ctypes
            k = ctypes.windll.kernel32
            k.SetConsoleMode(k.GetStdHandle(-11), 7)
        except Exception:
            pass
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass


_enable_ansi()

ANSI = sys.stdout.isatty()

C_GREEN  = "\033[32m"
C_YELLOW = "\033[33m"
C_RED    = "\033[31m"
C_CYAN   = "\033[36m"
C_MAGENTA= "\033[35m"
C_DIM    = "\033[90m"
C_BOLD   = "\033[1m"
C_RESET  = "\033[0m"
C_CLEAR  = "\r\033[K"
C_JADE   = "\033[38;2;136;216;176m"

BANNER = r"""
██╗  ██╗ ██████╗██████╗ ███████╗██╗   ██╗███████╗███████╗
╚██╗██╔╝██╔════╝██╔══██╗██╔════╝██║   ██║╚══███╔╝╚══███╔╝
 ╚███╔╝ ██║     ██████╔╝█████╗  ██║   ██║  ███╔╝   ███╔╝
 ██╔██╗ ██║     ██╔═══╝ ██╔══╝  ██║   ██║ ███╔╝   ███╔╝
██╔╝ ██╗╚██████╗██║     ██║     ╚██████╔╝███████╗███████╗
╚═╝  ╚═╝ ╚═════╝╚═╝     ╚═╝      ╚═════╝ ╚══════╝╚══════╝
"""

_debug_saved = asyncio.Event()


def _fmt_time(sec: float) -> str:
    sec = int(sec)
    if sec < 60:
        return f"{sec}s"
    m, s = divmod(sec, 60)
    if m < 60:
        return f"{m}m{s:02d}s"
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m"


def _calc_digit(partial: str, weight: int) -> int:
    soma = sum(int(d) * w for d, w in zip(partial, range(weight, 1, -1)))
    resto = (soma * 10) % 11
    return 0 if resto >= 10 else resto


def _build_cpf(base9: str) -> str | None:
    if len(set(base9)) == 1:
        return None
    d1 = _calc_digit(base9, 10)
    d2 = _calc_digit(base9 + str(d1), 11)
    return base9 + str(d1) + str(d2)


def fmt(cpf: str) -> str:
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def generate_candidates(mask: str) -> list[str]:
    clean = re.sub(r"[^0-9Xx]", "", mask).upper()
    if len(clean) != 11:
        print(f"{C_RED}[ERRO]{C_RESET} Máscara inválida: '{mask}'. Use formato como XXX.680.938-XX")
        sys.exit(1)

    prefix = list(clean[:9])
    x_pos = [i for i, c in enumerate(prefix) if c == "X"]

    out = []
    for combo in itertools.product(range(10), repeat=len(x_pos)):
        if x_pos and x_pos[0] == 0 and all(x_pos[k] == k for k in range(len(x_pos))) and combo == (0,) * len(x_pos):
            continue
        base = prefix.copy()
        for pos, digit in zip(x_pos, combo):
            base[pos] = str(digit)
        cpf = _build_cpf("".join(base))
        if cpf:
            out.append(cpf)
    return out


def _matches_name(name: str, filter_name: str) -> bool:
    if not filter_name:
        return True
    return filter_name.lower() in (name or "").lower()


def _parse_json(data: dict) -> tuple[bool, str]:
    total = data.get("totalRegistros", 0)
    records = data.get("registros", [])
    name = ""
    if records:
        raw = records[0].get("nome", "")
        name = raw.title() if raw else ""
    return (total > 0 or bool(records), name)


def _print_banner() -> None:
    if not ANSI:
        print(BANNER.strip("\n"))
        return
    for line in BANNER.strip("\n").split("\n"):
        print(f"  {C_JADE}{line}{C_RESET}")


def _print_guide() -> None:
    sep = f"  {C_DIM}{'─' * 56}{C_RESET}"

    print()
    _print_banner()
    print(sep)
    print(f"  {C_DIM}Repo   :{C_RESET} {C_BOLD}{REPO_URL}{C_RESET}")
    print(f"  {C_DIM}Mirror :{C_RESET} {C_DIM}{MIRROR_URL}{C_RESET}")
    print(sep)
    print()

    print(f"  {C_YELLOW}{C_BOLD}⚠  DISCLAIMER{C_RESET}")
    print(f"  {C_DIM}O Portal da Transparência não é um buscador de CPFs da Receita Federal.{C_RESET}")
    print(f"  {C_DIM}Ele só exibe pessoas com vínculo com o governo federal (servidor,{C_RESET}")
    print(f"  {C_DIM}beneficiário de programa social, fornecedor etc.). Sem esse vínculo,{C_RESET}")
    print(f"  {C_DIM}nenhum dado será retornado, mesmo para CPFs válidos.{C_RESET}")
    print()

    print(f"  {C_CYAN}{C_BOLD}» INSTALAÇÃO{C_RESET}  {C_DIM}(PowerShell){C_RESET}")
    for cmd in [
        'winget install -e --id Python.Python.3.12',
        '',
        'Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force',
        'python -m venv .venv',
        '.\\.venv\\Scripts\\Activate.ps1',
        '',
        'python -m pip install --upgrade pip',
        'python -m pip install aiohttp playwright',
        'playwright install chromium',
    ]:
        print(f"    {C_GREEN}{cmd}{C_RESET}")
    print()

    print(f"  {C_CYAN}{C_BOLD}» USO{C_RESET}")
    for cmd in [
        'python xcpfuzz.py "XXX.680.938-XX"',
        'python xcpfuzz.py "XXX.680.938-XX" --nome "Silva"',
        'python xcpfuzz.py "XXX.680.938-XX" --workers 30',
        'python xcpfuzz.py "XXX.680.938-XX" --force-playwright',
        'python xcpfuzz.py --help',
    ]:
        print(f"    {C_GREEN}{cmd}{C_RESET}")
    print()

    print(f"  {C_CYAN}{C_BOLD}» EXECUÇÃO VIA PIPE{C_RESET}  {C_DIM}(sem clonar o repo){C_RESET}")
    print(f"    {C_GREEN}(Invoke-WebRequest -Uri \"{MIRROR_URL}\" -UseBasicParsing).Content | python - \"XXX.680.938-XX\"{C_RESET}")
    print()

    print(sep)
    print()


class ResultWriter:
    def __init__(self, mask: str, name_filter: str) -> None:
        prefix = "target-" if name_filter else ""
        self.path = f"{prefix}{mask}.txt"
        self.count = 0
        self._f = open(self.path, "w", encoding="utf-8")
        self._f.write("xCPFuzz — busca por máscara\n")
        self._f.write(f"Máscara : {mask}\n")
        if name_filter:
            self._f.write(f"Nome    : {name_filter}\n")
        self._f.write(f"Início  : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        self._f.write("=" * 60 + "\n\n")
        self._f.flush()

    def add(self, record: dict) -> None:
        line = record["cpf"] + (f" — {record['nome']}" if record["nome"] else "")
        self._f.write(line + "\n")
        self._f.flush()
        self.count += 1

    def close(self, total: int) -> None:
        self._f.write("\n" + "=" * 60 + "\n")
        self._f.write(f"Total encontrado: {self.count}/{total}\n")
        self._f.write(f"Fim     : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        self._f.close()


class Progress:
    def __init__(self, total: int) -> None:
        self.total = total
        self.done = 0
        self.found = 0
        self.start = time.monotonic()
        self._bar_on_screen = False
        self.active = ANSI

    def _bar_line(self) -> str:
        elapsed = max(time.monotonic() - self.start, 1e-6)
        rate = self.done / elapsed
        remaining = self.total - self.done
        eta_str = _fmt_time(remaining / rate) if rate > 0 and remaining > 0 else "—"
        pct = (self.done / self.total * 100) if self.total else 0.0
        width = 28
        filled = int(width * self.done / self.total) if self.total else 0
        bar = "█" * filled + "░" * (width - filled)
        return (
            f"{C_CLEAR}  {C_CYAN}[{bar}]{C_RESET} "
            f"{C_BOLD}{pct:5.1f}%{C_RESET}  "
            f"{self.done:>5}/{self.total}  "
            f"{C_GREEN}✓ {self.found}{C_RESET}  "
            f"{C_DIM}{_fmt_time(elapsed)} · {rate:5.1f}/s · ETA {eta_str}{C_RESET}"
        )

    def draw(self) -> None:
        if not self.active:
            return
        sys.stdout.write(self._bar_line())
        sys.stdout.flush()
        self._bar_on_screen = True

    def _log(self, msg: str) -> None:
        if not self.active:
            return
        if self._bar_on_screen:
            sys.stdout.write(C_CLEAR)
        sys.stdout.write(msg + "\n")
        self.draw()

    def match(self, cpf: str, name: str) -> None:
        self.done += 1
        self.found += 1
        label = name if name else f"{C_DIM}nome não disponível{C_RESET}"
        self._log(f"  {C_GREEN}{C_BOLD}✓{C_RESET} {C_BOLD}{cpf}{C_RESET} — {label}")

    def miss(self, cpf: str, name: str = "") -> None:
        self.done += 1
        if not self.active:
            return
        if name:
            self._log(f"  {C_YELLOW}·{C_RESET} {C_DIM}{cpf} — nome '{name}' não corresponde{C_RESET}")
        else:
            self._log(f"  {C_DIM}· {cpf}{C_RESET}")

    def error(self, cpf: str) -> None:
        self.done += 1
        if not self.active:
            return
        self._log(f"  {C_RED}× {cpf} — erro{C_RESET}")

    def finish(self) -> None:
        if self.active and self._bar_on_screen:
            sys.stdout.write(C_CLEAR)
            sys.stdout.flush()
            self._bar_on_screen = False


def _print_header(mode: str, mask: str, name: str, total: int, workers: int, output: str) -> None:
    sep = f"  {C_DIM}{'─' * 56}{C_RESET}"
    print()
    _print_banner()
    print(sep)
    print(f"  {C_DIM}Modo      :{C_RESET} {C_MAGENTA}{mode}{C_RESET}")
    print(f"  {C_DIM}Máscara   :{C_RESET} {mask}")
    if name:
        print(f"  {C_DIM}Nome      :{C_RESET} {C_YELLOW}{C_BOLD}{name}{C_RESET}")
    print(f"  {C_DIM}Candidatos:{C_RESET} {total:,}")
    print(f"  {C_DIM}Workers   :{C_RESET} {workers}")
    print(f"  {C_DIM}Saída     :{C_RESET} {output}")
    print(sep)
    print()


async def _extract_token() -> str | None:
    token: str | None = None

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=True,
                channel="chrome",
                args=["--disable-blink-features=AutomationControlled"],
            )
        except Exception:
            browser = await p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"],
            )

        context = await browser.new_context(
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            viewport={"width": 1366, "height": 768},
        )
        await context.add_init_script(_STEALTH_JS)
        page = await context.new_page()

        def on_request(req):
            nonlocal token
            if token is not None:
                return
            if "busca.portaldatransparencia.gov.br" not in req.url:
                return
            qs = parse_qs(urlparse(req.url).query)
            if "t" in qs:
                token = qs["t"][0]

        page.on("request", on_request)

        try:
            await page.goto(
                f"{PORTAL_BASE}/pessoa-fisica/busca/lista",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            await page.wait_for_timeout(4000)

            if token is None:
                html = await page.content()
                m = re.search(r"let\s+token\s*=\s*['\"]&?t=([A-Za-z0-9]+)['\"]", html)
                if m:
                    token = m.group(1)

            if token is None:
                try:
                    await page.fill("#termo", "14345221722")
                    btn = await page.query_selector(
                        'button[aria-label="Enviar dados do formulário de busca"]'
                    )
                    if btn:
                        await btn.click()
                        await page.wait_for_timeout(8000)
                except Exception:
                    pass
        finally:
            await browser.close()

    return token


def _load_token() -> str | None:
    try:
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
        return token or None
    except FileNotFoundError:
        return None
    except Exception:
        return None


def _save_token(token: str) -> None:
    TOKEN_FILE.write_text(token, encoding="utf-8")


async def _ensure_token() -> str:
    cached = _load_token()
    if cached:
        print(f"  {C_DIM}Token     :{C_RESET} {C_GREEN}carregado de {TOKEN_FILE.name}{C_RESET}")
        return cached

    print(f"  {C_DIM}Token     :{C_RESET} {C_YELLOW}gerando novo token...{C_RESET}")
    token = await _extract_token()

    if not token:
        print(f"  {C_RED}[ERRO]{C_RESET} Não foi possível obter o token.")
        sys.exit(1)

    _save_token(token)
    print(f"  {C_DIM}Token     :{C_RESET} {C_GREEN}gerado e salvo em {TOKEN_FILE.name}{C_RESET}")
    return token


async def _probe_api(session: aiohttp.ClientSession, token: str) -> bool:
    try:
        async with session.get(
            SEARCH_URL,
            params={"termo": "14345221722", "pagina": 1, "tamanhoPagina": 1, "t": token},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as resp:
            if resp.status == 200:
                ct = resp.headers.get("Content-Type", "")
                if "json" in ct:
                    data = await resp.json()
                    return "registros" in data or "totalRegistros" in data
    except Exception:
        pass
    return False


async def _probe_with_spinner(session: aiohttp.ClientSession, token: str) -> bool:
    if not ANSI:
        result = await _probe_api(session, token)
        print(f"  {C_DIM}API direta:{C_RESET} {'disponível' if result else 'indisponível'}")
        return result

    frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    stop = asyncio.Event()

    async def spin():
        i = 0
        while not stop.is_set():
            sys.stdout.write(f"{C_CLEAR}  {C_CYAN}{frames[i % len(frames)]}{C_RESET} Verificando API direta...")
            sys.stdout.flush()
            i += 1
            await asyncio.sleep(0.08)
        sys.stdout.write(C_CLEAR)
        sys.stdout.flush()

    spinner = asyncio.create_task(spin())
    try:
        result = await _probe_api(session, token)
    finally:
        stop.set()
        await spinner

    status = f"{C_GREEN}{C_BOLD}disponível ✓{C_RESET}" if result else f"{C_YELLOW}indisponível — usando Playwright{C_RESET}"
    print(f"  {C_DIM}API direta:{C_RESET} {status}")
    return result


async def _ticker(progress: Progress, stop: asyncio.Event) -> None:
    if not ANSI:
        return
    while not stop.is_set():
        try:
            await asyncio.wait_for(stop.wait(), timeout=0.5)
            return
        except asyncio.TimeoutError:
            progress.draw()


async def _query_api(
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    cpf: str,
    writer: ResultWriter,
    progress: Progress,
    name_filter: str,
    token: str,
) -> None:
    async with sem:
        formatted = fmt(cpf)
        found, name = False, ""
        try:
            async with session.get(
                SEARCH_URL,
                params={
                    "termo": cpf,
                    "letraInicial": "",
                    "pagina": 1,
                    "tamanhoPagina": 10,
                    "t": token,
                },
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 200:
                    ct = resp.headers.get("Content-Type", "")
                    if "json" in ct:
                        found, name = _parse_json(await resp.json())
        except Exception:
            progress.error(formatted)
            return

        matched = found and _matches_name(name, name_filter)

        if matched:
            writer.add({"cpf": formatted, "nome": name})
            progress.match(formatted, name)
        elif found:
            progress.miss(formatted, name)
        else:
            progress.miss(formatted)


async def run_api(
    candidates: list[str],
    workers: int,
    name_filter: str,
    writer: ResultWriter,
    progress: Progress,
    token: str,
) -> None:
    conn = aiohttp.TCPConnector(limit=workers * 2, ssl=False)
    sem = asyncio.Semaphore(workers)
    stop_ticker = asyncio.Event()
    ticker = asyncio.create_task(_ticker(progress, stop_ticker))

    try:
        async with aiohttp.ClientSession(headers=_API_HEADERS, connector=conn) as session:
            tasks = [
                _query_api(session, sem, cpf, writer, progress, name_filter, token)
                for cpf in candidates
            ]
            await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        stop_ticker.set()
        await ticker


async def _query_playwright(
    browser: Browser,
    cpf: str,
    sem: asyncio.Semaphore,
    debug: bool,
) -> tuple[bool, str]:
    async with sem:
        captured: dict = {}
        ready = asyncio.Event()

        context = await browser.new_context(
            user_agent=_API_HEADERS["User-Agent"],
            viewport={"width": 1280, "height": 800},
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            extra_http_headers={"Accept-Language": "pt-BR,pt;q=0.9"},
        )
        await context.add_init_script(_STEALTH_JS)
        page: Page = await context.new_page()

        async def block_route(route):
            if route.request.resource_type in _BLOCK_TYPES:
                await route.abort()
            else:
                await route.continue_()

        await page.route("**/*", block_route)

        async def on_response(response):
            if "busca.portaldatransparencia.gov.br" not in response.url:
                return
            if response.status != 200:
                return
            if f"termo={cpf}" not in response.url:
                return
            try:
                captured["json"] = await response.json()
                ready.set()
            except Exception:
                pass

        page.on("response", on_response)

        try:
            await page.goto(
                f"{PORTAL_BASE}/pessoa-fisica/busca/lista",
                wait_until="domcontentloaded",
            )

            try:
                await page.fill("#termo", cpf)
                btn = await page.wait_for_selector(
                    'button[aria-label="Enviar dados do formulário de busca"]',
                    timeout=10_000,
                )
                await btn.click()
            except Exception:
                pass

            try:
                await asyncio.wait_for(ready.wait(), timeout=20.0)
            except asyncio.TimeoutError:
                pass

            if debug and not _debug_saved.is_set():
                _debug_saved.set()
                html = await page.content()
                with open("debug.html", "w", encoding="utf-8") as f:
                    f.write(html)
                if "json" in captured:
                    with open("debug.json", "w", encoding="utf-8") as f:
                        json.dump(captured["json"], f, ensure_ascii=False, indent=2)
        finally:
            await page.close()
            await context.close()

        if "json" in captured:
            return _parse_json(captured["json"])

        return (False, "")


async def run_playwright(
    candidates: list[str],
    workers: int,
    debug: bool,
    name_filter: str,
    writer: ResultWriter,
    progress: Progress,
) -> None:
    sem = asyncio.Semaphore(workers)
    stop_ticker = asyncio.Event()
    ticker = asyncio.create_task(_ticker(progress, stop_ticker))

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True, channel="chrome")
        except Exception:
            browser = await p.chromium.launch(headless=True)

        async def process(cpf: str):
            formatted = fmt(cpf)
            try:
                found, name = await _query_playwright(browser, cpf, sem, debug)
            except Exception:
                progress.error(formatted)
                return

            matched = found and _matches_name(name, name_filter)
            if matched:
                writer.add({"cpf": formatted, "nome": name})
                progress.match(formatted, name)
            elif found:
                progress.miss(formatted, name)
            else:
                progress.miss(formatted)

        try:
            await asyncio.gather(*[process(cpf) for cpf in candidates], return_exceptions=True)
        finally:
            stop_ticker.set()
            await ticker
            await browser.close()


async def _run_async(args, candidates: list[str], writer: ResultWriter) -> None:
    total = len(candidates)

    if args.force_playwright:
        token = ""
        use_api = False
        print(f"  {C_DIM}Token     :{C_RESET} {C_YELLOW}ignorado (--force-playwright){C_RESET}")
        print(f"  {C_DIM}API direta:{C_RESET} {C_YELLOW}ignorada (--force-playwright){C_RESET}")
    else:
        token = await _ensure_token()
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(headers=_API_HEADERS, connector=conn) as session:
            use_api = await _probe_with_spinner(session, token)

    workers = args.workers if use_api else min(args.workers, 5)
    mode = "API direta" if use_api else "Playwright (reCAPTCHA)"

    _print_header(mode, args.mask, args.nome, total, workers, writer.path)

    progress = Progress(total)
    try:
        if use_api:
            await run_api(candidates, workers, args.nome, writer, progress, token)
        else:
            await run_playwright(candidates, workers, args.debug, args.nome, writer, progress)
    finally:
        progress.finish()


def main() -> None:
    if len(sys.argv) == 1:
        _print_guide()
        sys.exit(0)

    parser = argparse.ArgumentParser(
        prog="xcpfuzz",
        description="xCPFuzz — busca CPFs no Portal da Transparência via máscara.",
    )
    parser.add_argument("mask", help="Máscara do CPF. Ex: XXX.680.938-XX")
    parser.add_argument("--nome", default="", metavar="NOME",
                        help="Filtra pelo nome (substring, case-insensitive). Saída em target-<mask>.txt")
    parser.add_argument("--workers", type=int, default=20, metavar="N",
                        help="Concorrência (padrão: 20 API / 5 Playwright)")
    parser.add_argument("--debug", action="store_true",
                        help="Salva debug.html / debug.json da primeira consulta")
    parser.add_argument("--force-playwright", action="store_true",
                        help="Força Playwright mesmo se API direta funcionar")
    args = parser.parse_args()

    if args.workers < 1:
        print(f"{C_RED}[ERRO]{C_RESET} --workers deve ser >= 1")
        sys.exit(1)

    candidates = generate_candidates(args.mask)
    total = len(candidates)
    writer = ResultWriter(args.mask, args.nome)

    interrupted = False
    try:
        asyncio.run(_run_async(args, candidates, writer))
    except KeyboardInterrupt:
        interrupted = True
        print(f"\n  {C_YELLOW}⚠  Interrompido pelo usuário{C_RESET}")
    finally:
        writer.close(total)
        print(f"  {C_DIM}{'─' * 56}{C_RESET}")
        if writer.count:
            print(f"  {C_GREEN}{C_BOLD}✓ {writer.count}{C_RESET} resultado(s) encontrado(s) de {total}")
        else:
            print(f"  {C_DIM}Nenhum resultado encontrado de {total} candidato(s){C_RESET}")
        print(f"  {C_DIM}Salvo em:{C_RESET} {C_BOLD}{writer.path}{C_RESET}")
        print()

    if interrupted:
        sys.exit(130)


if __name__ == "__main__":
    main()