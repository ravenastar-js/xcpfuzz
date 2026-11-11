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
[![aiohttp](https://img.shields.io/badge/aiohttp-000000?style=for-the-badge&logo=python&logoColor=6effa8&labelColor=0c1a13)](#)
[![Playwright](https://img.shields.io/badge/Playwright-000000?style=for-the-badge&logo=playwright&logoColor=6effa8&labelColor=0c1a13)](#)
[![License](https://img.shields.io/badge/License-MIT-000000?style=for-the-badge&logo=opensourceinitiative&logoColor=6effa8&labelColor=0c1a13)](#)

[![Download xcpfuzz.py](https://img.shields.io/badge/Download-xcpfuzz.py-6effa8?style=for-the-badge&logo=python&logoColor=0c1a13&labelColor=0c1a13)](cmd/xcpfuzz.py)

*💚 Gera CPFs válidos por máscara e verifica vínculos no Portal da Transparência*

</div>

---

<div align="center">
  <img src="img/bg.png" alt="XNAJA Banner" width="100%" />
</div>

<br>

---

<h2>
  <img src="https://api.iconify.design/mdi/bullseye-arrow.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Visão Geral
</h2>

O **xCPFuzz** é uma CLI em Python que **gera CPFs válidos a partir de uma máscara** (`XXX.680.938-XX`) e **consulta cada um** na API pública do Portal da Transparência. O objetivo é **verificar** se um CPF com um padrão específico aparece na base pública do governo federal. Útil para **pesquisa OSINT**, **jornalismo investigativo**, **auditoria**, **verificação de identidade**, **investigação forense**, **perícia digital** e demais usos legítimos de análise de dados públicos.

Cada consulta retorna se o CPF existe na base e, quando disponível, o **nome associado**. O resultado é salvo em arquivo `.txt` formatado com data, máscara, total encontrado e os nomes quando disponíveis.

> [!WARNING]
> **O xCPFuzz NÃO é um buscador de CPFs da Receita Federal.** <img src="https://api.iconify.design/mdi/alert-octagon.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" />
>
> O Portal da Transparência só exibe pessoas que possuem **algum vínculo com o governo federal** (servidores, beneficiários de programas sociais, fornecedores, pensionistas etc.). Se a pessoa não tiver esse tipo de vínculo, **nenhum dado será retornado**, mesmo que o CPF exista e seja válido na Receita.
>
> A ferramenta **não descobre CPFs**: ela **verifica** se CPFs gerados a partir de uma máscara aparecem no Portal da Transparência. Uso destinado exclusivamente a **pesquisa legítima**. Respeite os termos de uso do Portal e a LGPD.

> [!NOTE]
> **Este projeto começou como um experimento.** <img src="https://api.iconify.design/mdi/flask.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" />
> O xCPFuzz foi feito para automatizar uma verificação chata de fazer manualmente. O escopo é simples e não há planos de expandir para algo massivo.

<h3>
  <img src="https://api.iconify.design/mdi/creation.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Por que usar?
</h3>

- <img src="https://api.iconify.design/mdi/rocket-launch.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Rápido** - Concorrência assíncrona com `aiohttp` (padrão: 20 workers paralelos)
- <img src="https://api.iconify.design/mdi/refresh.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Fallback inteligente** - Se a API for bloqueada, cai automaticamente para Playwright
- <img src="https://api.iconify.design/mdi/palette.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Interface colorida** - Progress bar ao vivo com ETA, taxa de consultas e logs em cores
- <img src="https://api.iconify.design/mdi/filter.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Filtro por nome** - Retorna só CPFs cujo titular contenha o nome buscado
- <img src="https://api.iconify.design/mdi/cloud-download.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Execução via pipe** - Roda direto da URL espelhada, sem clonar o repositório

---

<h2>
  <img src="https://api.iconify.design/mdi/lightning-bolt.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Recursos Principais
</h2>

- <img src="https://api.iconify.design/mdi/format-list-numbered.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Máscara com wildcard** - Use `X` em qualquer posição (`XXX.680.938-XX` gera 100 CPFs válidos)
- <img src="https://api.iconify.design/mdi/check-decagram.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Dígitos verificadores automáticos** - Os dois últimos dígitos são calculados pelo algoritmo oficial do CPF
- <img src="https://api.iconify.design/mdi/shield-lock.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Token automático** - Extrai o token `?t=` do Portal via Playwright e cacheia em `token.txt`
- <img src="https://api.iconify.design/mdi/stealth.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Stealth JS** - Sobrescreve `navigator.webdriver`, plugins, languages e platform para evitar detecção
- <img src="https://api.iconify.design/mdi/swap-horizontal.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> **Modo duplo** - API direta (rápida) ou Playwright headless (contorna reCAPTCHA)
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
[![aiohttp](https://img.shields.io/badge/aiohttp-000000?style=flat-square&logo=python&logoColor=6effa8&labelColor=0c1a13)](https://docs.aiohttp.org/)
[![Playwright](https://img.shields.io/badge/Playwright-000000?style=flat-square&logo=playwright&logoColor=6effa8&labelColor=0c1a13)](https://playwright.dev/python/)
[![asyncio](https://img.shields.io/badge/asyncio-000000?style=flat-square&logo=python&logoColor=6effa8&labelColor=0c1a13)](https://docs.python.org/3/library/asyncio.html)
[![Cloudflare](https://img.shields.io/badge/Cloudflare_Pages-000000?style=flat-square&logo=cloudflare&logoColor=6effa8&labelColor=0c1a13)](https://pages.cloudflare.com/)
[![Git](https://img.shields.io/badge/Git-000000?style=flat-square&logo=git&logoColor=6effa8&labelColor=0c1a13)](https://git-scm.com/)

</div>
</details>

---

<h2>
  <img src="https://api.iconify.design/mdi/rocket-launch.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Como Usar
</h2>

<h3>
  <img src="https://api.iconify.design/mdi/download.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Download
</h3>

O script fica em [`cmd/xcpfuzz.py`](https://github.com/ravenastar-js/xcpfuzz/blob/main/cmd/xcpfuzz.py) no repositório. Baixe direto:

[![Download xcpfuzz.py](https://img.shields.io/badge/Download-xcpfuzz.py-6effa8?style=for-the-badge&logo=python&logoColor=0c1a13&labelColor=0c1a13)](https://ravenastar.com/cmd/xcpfuzz.py)

Ou use o espelho: [https://ravenastar.com/cmd/xcpfuzz.py](https://ravenastar.com/cmd/xcpfuzz.py)

<h3>
  <img src="https://api.iconify.design/mdi/download.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Instalação
</h3>

Requer **Python 3.12+**. No **PowerShell** (Windows):

```powershell
winget install -e --id Python.Python.3.12

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install aiohttp playwright
playwright install chromium
```

> O `playwright install chromium` baixa o navegador headless usado para extrair o token e, se necessário, operar em modo fallback contra o reCAPTCHA.

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
| `python xcpfuzz.py "XXX.680.938-XX" --force-playwright` | Força modo Playwright (contorna bloqueio de API) |
| `python xcpfuzz.py "XXX.680.938-XX" --debug` | Salva `debug.html`/`debug.json` da primeira consulta |
| `python xcpfuzz.py --help` | Help resumido das flags |

> **Formato da máscara:** exatamente **11 posições**, com `X` nas posições que devem ser variadas. Pontos e hífen são opcionais (`XXX.680.938-XX` ou `XXX680938XX`).

<h3>
  <img src="https://api.iconify.design/mdi/pipe.svg?color=%236effa8" width="22" height="22" style="vertical-align: middle;" />
  Execução via pipe (sem clonar)
</h3>

Roda direto da URL espelhada em Cloudflare Pages:

```powershell
(Invoke-WebRequest -Uri "https://ravenastar.com/cmd/xcpfuzz.py" -UseBasicParsing).Content | python - "XXX.680.938-XX"
```

Com filtro de nome:

```powershell
(Invoke-WebRequest -Uri "https://ravenastar.com/cmd/xcpfuzz.py" -UseBasicParsing).Content | python - "XXX.680.938-XX" --nome "Silva"
```

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
Total encontrado: 2/100
Fim     : 11/11/2026 14:33:12
```

---

<h2>
  <img src="https://api.iconify.design/mdi/wrench.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Solução de Problemas
</h2>

| Sintoma | Causa provável | Correção |
| :--- | :--- | :--- |
| `Não foi possível obter o token` | Portal mudou HTML ou bloqueou IP | Use `--force-playwright`, apague `token.txt` e tente novamente |
| `API direta: indisponível` | Token expirou ou rate limit | Apague `token.txt` para gerar novo token |
| Progresso para em 0% | Requisições bloqueadas | Tente `--workers 3` e aguarde alguns minutos |
| `Máscara inválida` | Faltou dígito ou caractere estranho | Use formato `XXX.680.938-XX` (11 posições) |
| Mojibake (`Ã¡`, `â€"`) no terminal | Console em CP1252 | Rode `chcp 65001` antes ou use Windows Terminal |

---

<h2>
  <img src="https://api.iconify.design/mdi/scale-balance.svg?color=%236effa8" width="28" height="28" style="vertical-align: middle;" />
  Licença e Uso Responsável
</h2>

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para detalhes.

> **Uso responsável:** esta ferramenta consulta dados **públicos** já expostos pelo Portal da Transparência. Não faça uso ilícito e, em caso de dúvida jurídica, procure orientação antes de usar...

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

<a href="#">
  <img src="https://api.iconify.design/mdi/arrow-up-bold.svg?color=%236effa8" width="20" height="20" style="vertical-align: middle;" /> 
  Voltar ao topo
</a>

</div>