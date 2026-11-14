<div align="center">

<h1>
  <img src="https://api.iconify.design/mdi/account-search.svg?color=%236effa8" width="42" height="42" style="vertical-align: middle;" />
  xCPFuzz
</h1>
<h3>
  <img src="https://api.iconify.design/mdi/magnify-scan.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Gerador e verificador de CPFs via máscara
</h3>

[![Python](https://img.shields.io/badge/Python_3.12+-000000?style=for-the-badge&logo=python&logoColor=6effa8&labelColor=0c1a13)](#)
[![curl_cffi](https://img.shields.io/badge/curl__cffi-000000?style=for-the-badge&logo=python&logoColor=6effa8&labelColor=0c1a13)](https://github.com/lexiforest/curl_cffi)
[![Playwright](https://img.shields.io/badge/Playwright-000000?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzZlZmZhOCIgZD0iTTEyIDJDMi4yIDIgMiAyLjIgMiAxMnMyLjIgMTAgMTAgMTAgMTAtMi4yIDEwLTEwUzIxLjggMiAxMiAyem0wIDE4Yy00LjQgMC04LTMuNi04LThzMy42LTggOC04IDggMy42IDggOC0zLjYgOC04IDh6Ii8+PC9zdmc+&logoColor=6effa8&labelColor=0c1a13)](https://playwright.dev/python/)
[![Windows PowerShell](https://img.shields.io/badge/Windows_PowerShell-000000?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzZlZmZhOCIgZD0iTTMsNS41VjExSDEwLjVWM0gzVjUuNU0zLDE4LjVWMTNIMTAuNVYyMUgzVjE4LjVNMTEuNSwyMUgyMVYxM0gxMS41VjIxTTExLjUsM1YxMUgyMVYzSDExLjVaIi8+PC9zdmc+&logoColor=6effa8&labelColor=0c1a13)](https://learn.microsoft.com/pt-br/powershell/scripting/install/install-powershell)
[![License](https://img.shields.io/badge/License-MIT-000000?style=for-the-badge&logo=opensourceinitiative&logoColor=6effa8&labelColor=0c1a13)](#)

[![Download xcpfuzz.py](https://img.shields.io/badge/Download-xcpfuzz.py-6effa8?style=for-the-badge&logo=python&logoColor=6effa8&labelColor=0c1a13)](cmd/xcpfuzz.py)

*💚 Gera CPFs válidos por máscara e verifica vínculos no Portal da Transparência*

</div>

---

<div align="center">
  <img src="img/bg.png" alt="xCPFuzz Banner" width="100%"/>
</div>

<br>

---

<h2>
  <img src="https://api.iconify.design/mdi/bullseye-arrow.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Visão Geral
</h2>

O **xCPFuzz** é uma CLI em Python que **gera CPFs válidos a partir de uma máscara** (`XXX.680.938-XX`) e **consulta cada um** na API pública do Portal da Transparência. O objetivo é **verificar** se um CPF com um padrão específico aparece na base pública do governo federal. Útil para **pesquisa OSINT**, **jornalismo investigativo**, **auditoria**, **verificação de identidade**, **investigação forense**, **perícia digital** e demais usos legítimos de análise de dados públicos.

> [!IMPORTANT]
> <img src="https://api.iconify.design/mdi/microsoft-windows.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" />
> **Feito para Windows PowerShell.** O xCPFuzz foi **desenvolvido e testado no PowerShell do Windows** (Windows 10/11) usando **Python 3.12+**. Os comandos de instalação, ativação de venv e execução via pipe foram escritos especificamente para o **PowerShell**, e podem não funcionar sem adaptação em `cmd.exe`, Bash, Zsh ou outros shells. Em **Linux/macOS**, os comandos `python` → `python3` e `.\.venv\Scripts\Activate.ps1` → `source .venv/bin/activate` precisam ser trocados, mas o script em si roda normalmente.
>
> <img src="https://api.iconify.design/mdi/information.svg?color=%236effa8" width="18" height="18" style="vertical-align: middle;" /> **Não tem o PowerShell instalado?** Siga as instruções oficiais: [Instalar o PowerShell](https://learn.microsoft.com/pt-br/powershell/scripting/install/install-powershell).

Cada consulta retorna se o CPF existe na base e, quando disponível, o **nome associado**. O resultado é salvo em arquivo `.txt` formatado com data, máscara, total encontrado e os nomes quando disponíveis.

> [!WARNING]
> **O xCPFuzz NÃO é um buscador de CPFs da Receita Federal.** <img src="https://api.iconify.design/mdi/alert-octagon.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" />
>
> O Portal da Transparência só exibe pessoas que possuem **algum vínculo com o governo federal** (servidores, beneficiários de programas sociais, fornecedores, pensionistas etc.). Se a pessoa não tiver esse tipo de vínculo, **nenhum dado será retornado**, mesmo que o CPF exista e seja válido na Receita.
>
> A ferramenta **não descobre CPFs**: ela **verifica** se CPFs gerados a partir de uma máscara aparecem no Portal da Transparência. Uso destinado exclusivamente a **pesquisa legítima**. Respeite os termos de uso do Portal e a LGPD.

> [!NOTE]
> **Este projeto começou como um experimento.** <img src="https://api.iconify.design/mdi/flask.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" />
> O xCPFuzz foi desenvolvido para automatizar uma verificação tediosa e repetitiva, que seria cansativa de executar manualmente. O escopo é simples e não há planos de expandir para algo massivo.

<h3>
  <img src="https://api.iconify.design/mdi/creation.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Por que usar?
</h3>

- <img src="https://api.iconify.design/mdi/rocket-launch.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Rápido** - Concorrência assíncrona com `curl_cffi` (padrão: 20 workers paralelos)
- <img src="https://api.iconify.design/mdi/incognito.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Bypass do AWS WAF** - Extrai o cookie `aws-waf-token` via Playwright e reutiliza em sessão `curl_cffi` com fingerprint TLS de Chrome real
- <img src="https://api.iconify.design/mdi/speedometer.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Rate limit adaptativo** - Respeita os limites oficiais da API (400 req/min diurno, 700 req/min 00:00–06:00) com jitter, backoff em 429/403 e recuperação automática
- <img src="https://api.iconify.design/mdi/refresh.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Fallback inteligente** - Se a API for bloqueada, cai automaticamente para Playwright
- <img src="https://api.iconify.design/mdi/palette.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Interface colorida** - Progress bar ao vivo com ETA, taxa de consultas e logs em cores
- <img src="https://api.iconify.design/mdi/filter.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Filtro por nome** - Retorna só CPFs cujo titular contenha o nome buscado
- <img src="https://api.iconify.design/mdi/cloud-download.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Execução via pipe** - Roda direto da URL espelhada, sem clonar o repositório
- <img src="https://api.iconify.design/mdi/microsoft-windows.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **PowerShell-first** - Instalação e comandos escritos para o PowerShell do Windows (compatível com Linux/macOS via adaptação)

---

<h2>
  <img src="https://api.iconify.design/mdi/lightning-bolt.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Recursos Principais
</h2>

- <img src="https://api.iconify.design/mdi/format-list-numbered.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Máscara com wildcard** - Use `X` em qualquer posição (`XXX.680.938-XX` gera 100¹·⁵ CPFs válidos)
- <img src="https://api.iconify.design/mdi/check-decagram.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Dígitos verificadores automáticos** - Os dois últimos dígitos são calculados pelo algoritmo oficial do CPF
- <img src="https://api.iconify.design/mdi/shield-lock.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Bypass do AWS WAF** - Playwright resolve o desafio do WAF e extrai o cookie `aws-waf-token`; a API direta roda em `curl_cffi` com `impersonate="chrome"` (fingerprint TLS/JA3 real) e headers consistentes (`Sec-CH-UA`, `Sec-Fetch-*`)
- <img src="https://api.iconify.design/mdi/incognito.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Stealth JS** - Sobrescreve `navigator.webdriver`, plugins, languages e platform para evitar detecção no Playwright
- <img src="https://api.iconify.design/mdi/speedometer.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Rate limit adaptativo** - Classe `AdaptiveRateLimiter` com taxa configurável (`--rate`), jitter de até 25%, penalização multiplicativa em 429/403 (respeita `Retry-After`) e recuperação de 3% por sucesso
- <img src="https://api.iconify.design/mdi/swap-horizontal.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Modo duplo** - API direta (rápida, com WAF token) ou Playwright headless (contorna reCAPTCHA)
- <img src="https://api.iconify.design/mdi/file-document-multiple.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Saída persistente** - Arquivo `.txt` com cabeçalho, data, máscara, total e nomes encontrados
- <img src="https://api.iconify.design/mdi/bug.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Debug** - Flag `--debug` salva `debug.html` e `debug.json` da primeira consulta

---

<details>
<summary>
  <img src="https://api.iconify.design/mdi/tools.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  <b>Stack de Tecnologias (Clique para expandir)</b>
</summary>
<br>
<div align="center">

[![Python](https://img.shields.io/badge/Python_3.12-000000?style=flat-square&logo=python&logoColor=6effa8&labelColor=0c1a13)](https://python.org/)
[![curl_cffi](https://img.shields.io/badge/curl__cffi-000000?style=flat-square&logo=python&logoColor=6effa8&labelColor=0c1a13)](https://github.com/lexiforest/curl_cffi)
[![Playwright](https://img.shields.io/badge/Playwright-000000?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzZlZmZhOCIgZD0iTTEyIDJDMi4yIDIgMiAyLjIgMiAxMnMyLjIgMTAgMTAgMTAgMTAtMi4yIDEwLTEwUzIxLjggMiAxMiAyem0wIDE4Yy00LjQgMC04LTMuNi04LThzMy42LTggOC04IDggMy42IDggOC0zLjYgOC04IDh6Ii8+PC9zdmc+&logoColor=6effa8&labelColor=0c1a13)](https://playwright.dev/python/)
[![asyncio](https://img.shields.io/badge/asyncio-000000?style=flat-square&logo=python&logoColor=6effa8&labelColor=0c1a13)](https://docs.python.org/3/library/asyncio.html)
[![Windows PowerShell](https://img.shields.io/badge/Windows_PowerShell-000000?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzZlZmZhOCIgZD0iTTMsNS41VjExSDEwLjVWM0gzVjUuNU0zLDE4LjVWMTNIMTAuNVYyMUgzVjE4LjVNMTEuNSwyMUgyMVYxM0gxMS41VjIxTTExLjUsM1YxMUgyMVYzSDExLjVaIi8+PC9zdmc+&logoColor=6effa8&labelColor=0c1a13)](https://learn.microsoft.com/pt-br/powershell/scripting/install/install-powershell)
[![Git](https://img.shields.io/badge/Git-000000?style=flat-square&logo=git&logoColor=6effa8&labelColor=0c1a13)](https://git-scm.com/)

</div>
</details>

---

<h2>
  <img src="https://api.iconify.design/mdi/rocket-launch.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Como Usar
</h2>

> [!TIP]
> <img src="https://api.iconify.design/mdi/microsoft-windows.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" />
> **Ambiente recomendado:** Windows 10/11 com **PowerShell 7+** (ou Windows PowerShell 5.1). Os passos abaixo assumem esse ambiente. Em Linux/macOS, substitua `python` por `python3` e ajuste a ativação do venv.
>
> <img src="https://api.iconify.design/mdi/information.svg?color=%236effa8" width="18" height="18" style="vertical-align: middle;" /> Precisa instalar o PowerShell? Consulte o guia oficial: [Instalar o PowerShell](https://learn.microsoft.com/pt-br/powershell/scripting/install/install-powershell).

<h3>
  <img src="https://api.iconify.design/mdi/download.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Download
</h3>

O script fica em [`cmd/xcpfuzz.py`](https://github.com/ravenastar-js/xcpfuzz/blob/main/cmd/xcpfuzz.py) nesse repositório. 

Baixe direto:

[![Download xcpfuzz.py](https://img.shields.io/badge/Download-xcpfuzz.py-6effa8?style=for-the-badge&logo=python&logoColor=6effa8&labelColor=0c1a13)](cmd/xcpfuzz.py)

Ou use o espelho: [https://ravenastar.com/cmd/xcpfuzz.py](https://ravenastar.com/cmd/xcpfuzz.py)

<h3>
  <img src="https://api.iconify.design/mdi/download.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Instalação (Windows PowerShell)
</h3>

Requer **Python 3.12+**. No **PowerShell** (Windows):

```powershell
winget install -e --id Python.Python.3.12

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install curl_cffi playwright
playwright install chromium
```

> O `playwright install chromium` baixa o navegador headless usado para extrair o cookie `aws-waf-token` e, se necessário, operar em modo fallback contra o reCAPTCHA.
>
> <img src="https://api.iconify.design/mdi/microsoft-windows.svg?color=%236effa8" width="18" height="18" style="vertical-align: middle;" /> **Somente PowerShell:** o comando `Set-ExecutionPolicy -Scope Process` é necessário para permitir a ativação do venv. Em `cmd.exe`, use `.\.venv\Scripts\activate.bat`; em Linux/macOS, `source .venv/bin/activate`.
>
> <img src="https://api.iconify.design/mdi/information.svg?color=%236effa8" width="18" height="18" style="vertical-align: middle;" /> **Não tem o PowerShell?** Instale seguindo o guia oficial: [Instalar o PowerShell](https://learn.microsoft.com/pt-br/powershell/scripting/install/install-powershell).

<h3>
  <img src="https://api.iconify.design/mdi/terminal.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Guia Rápido
</h3>

```powershell
python xcpfuzz.py
```

Sem argumentos, o script mostra o **guia completo com banner, link do repositório, instruções de instalação e exemplos de uso**. Depois é só rodar com uma máscara.

<h3>
  <img src="https://api.iconify.design/mdi/play.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Execução
</h3>

| Comando | Descrição |
| :--- | :--- |
| `python xcpfuzz.py "XXX.680.938-XX"` | Gera todos os CPFs válidos e consulta cada um |
| `python xcpfuzz.py "XXX.680.938-XX" --nome "Silva"` | Filtra por nome (case-insensitive) |
| `python xcpfuzz.py "XXX.680.938-XX" --workers 30` | Aumenta a concorrência (padrão: 20) |
| `python xcpfuzz.py "XXX.680.938-XX" --rate 10` | Ajusta a taxa de requisições por segundo (padrão: 6.6) |
| `python xcpfuzz.py "XXX.680.938-XX" --no-api` | Força modo Playwright (ignora API direta) |
| `python xcpfuzz.py "XXX.680.938-XX" --debug` | Salva `debug.html`/`debug.json` da primeira consulta |
| `python xcpfuzz.py --help` | Help resumido das flags |

> **Formato da máscara:** exatamente **11 posições**, com `X` nas posições que devem ser variadas. Pontos e hífen são opcionais (`XXX.680.938-XX` ou `XXX680938XX`).
>
> **Sobre `--rate`:** alinhado aos limites oficiais da API do Portal da Transparência (400 req/min diurno = 6.6 req/s, 700 req/min entre 00:00 e 06:00 = 11.6 req/s, APIs restritas a 180 req/min = 3 req/s). O rate limiter adaptativo reduz automaticamente a taxa em caso de `429`/`403` e a recupera após sucessos.

<h3>
  <img src="https://api.iconify.design/mdi/pipe.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Execução via pipe (sem clonar)
</h3>

Roda direto da URL espelhada **usando `Invoke-WebRequest` do PowerShell**:

```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new(); (Invoke-WebRequest -Uri "https://ravenastar.com/cmd/xcpfuzz.py" -UseBasicParsing).Content | python -X utf8 - "XXX.680.938-XX"
```

Com filtro de nome:

```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new(); (Invoke-WebRequest -Uri "https://ravenastar.com/cmd/xcpfuzz.py" -UseBasicParsing).Content | python -X utf8 - "XXX.680.938-XX" --nome "Silva"
```

> <img src="https://api.iconify.design/mdi/information.svg?color=%236effa8" width="18" height="18" style="vertical-align: middle;" /> O `-UseBasicParsing` evita dependência do Internet Explorer no Windows PowerShell 5.1. No PowerShell 7+ ele é opcional (mas inofensivo). Em Linux/macOS, use `curl -s https://ravenastar.com/cmd/xcpfuzz.py | python3 - "XXX.680.938-XX"`.

---

<h2>
  <img src="https://api.iconify.design/mdi/file-document.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Saída
</h2>

Para cada execução é gerado um arquivo `.txt` no diretório atual:

| Cenário | Arquivo |
| :--- | :--- |
| Sem filtro de nome | `XXX.680.938-XX.txt` |
| Com `--nome` | `target-XXX.680.938-XX.txt` |

Formato:

```text
xCPFuzz - busca por máscara
Máscara : XXX.680.938-XX
Nome    : Silva
Início  : 11/11/2026 14:32:07
============================================================

123.680.938-45 - João da Silva
987.680.938-12 - Maria Silva Souza

============================================================
Total encontrado: 2/100¹·⁵
Fim     : 11/11/2026 14:33:12
```

---

<h2>
  <img src="https://api.iconify.design/mdi/wrench.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Solução de Problemas
</h2>

| Sintoma | Causa provável | Correção |
| :--- | :--- | :--- |
| `API direta: indisponível` | WAF bloqueou a requisição de probe | Tente novamente em alguns minutos; ou use `--no-api` para forçar Playwright |
| Erros `429` recorrentes | Rate limit atingido | Reduza `--rate` (ex: `--rate 3`) e aguarde |
| Erros `403` recorrentes | WAF bloqueou após excesso de requisições | Aguarde 5–10 min, reduza `--rate` e `--workers` |
| Progresso para em 0% | Requisições bloqueadas | Tente `--workers 3 --rate 2` e aguarde alguns minutos |
| `Não foi possível obter aws-waf-token` | Playwright não resolveu o desafio do WAF | Rode `playwright install chromium` novamente; tente `--no-api` |
| `Máscara inválida` | Faltou dígito ou caractere estranho | Use formato `XXX.680.938-XX` (11 posições) |
| `Rate limit adaptativo reduzindo taxa muito rápido` | Muitos bloqueios em sequência | Reduza `--workers` (ex: `--workers 5`) para diminuir concorrência |
| Mojibake (`Ã¡`, `â€"`) no terminal | Console em CP1252 ou pipe sem UTF-8 | Rode `chcp 65001` antes, use Windows Terminal ou aplique `$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new()` antes do comando |
| `... não pode ser carregado porque a execução de scripts foi desabilitada` | ExecutionPolicy restritiva no PowerShell | Rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force` |
| `.\.venv\Scripts\Activate.ps1 : não reconhecido` | Venv não criado ou PowerShell em modo restrito | Verifique se `python -m venv .venv` rodou e reabra o terminal |
| `python: command not found` | Python não instalado ou fora do PATH | Reinstale via `winget install -e --id Python.Python.3.12` e reabra o terminal |
| `ModuleNotFoundError: No module named 'curl_cffi'` | Dependência não instalada | Rode `python -m pip install curl_cffi` |

---

<h2>
  <img src="https://api.iconify.design/mdi/scale-balance.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Licença e Uso Responsável
</h2>

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para detalhes.

> **Uso responsável:** esta ferramenta consulta dados **públicos** já expostos pelo Portal da Transparência. Não faça uso ilícito e, em caso de dúvida jurídica, procure orientação antes de usar...

---

<h3>
  <img src="https://api.iconify.design/mdi/scale-balance.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Base legal e normas de referência
</h3>

- **Constituição Federal, art. 5º, XXXIII** – direito de acesso a informações de interesse público.
- **Constituição Federal, art. 5º, X** – inviolabilidade da intimidade, da vida privada, da honra e da imagem.
- **Lei nº 12.527/2011 (Lei de Acesso à Informação)** e **Lei Complementar nº 131/2009 (Lei da Transparência)** – fundamento da divulgação de dados no Portal da Transparência.
- **Lei nº 13.709/2018 (LGPD), art. 7º, §3º** – o tratamento de dados pessoais de acesso público deve considerar a finalidade, a boa-fé e o interesse público que justificaram sua disponibilização.
- **LGPD, art. 6º** – princípios da finalidade, adequação e necessidade.
- **LGPD, art. 7º, §7º** – o uso posterior desses dados exige propósito legítimo e específico.
- **Lei nº 13.432/2017, arts. 2º e 10** – quando usado por profissional de investigação particular, restringe-se à coleta de dados de natureza não criminal, sendo vedado participar diretamente de diligências policiais.

> Ferramenta de produção de inteligência e suporte técnico, sem usurpação de função pública. O uso deve respeitar a finalidade legítima, a LGPD e a legislação pertinente. A responsabilidade pelo uso é de quem o executa.

---

## <img src="https://api.iconify.design/mdi/star.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" />  Star History

<a href="https://www.star-history.com/?repos=ravenastar-js%2Fxcpfuzz&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ravenastar-js/xcpfuzz&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ravenastar-js/xcpfuzz&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ravenastar-js/xcpfuzz&type=date&legend=top-left" />
 </picture>
</a>

---

<div align="center">

<h2>
  Feito com 
  <img src="https://api.iconify.design/mdi/heart.svg?color=%236effa8" width="24" height="24" style="vertical-align: middle;" /> 
  por <a href="https://linktr.ee/ravenastar">RavenaStar</a>
</h2>

</div>