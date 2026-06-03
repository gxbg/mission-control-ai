"""setup.py - gera a estrutura e os arquivos da Fase 1 da Mission Control AI (EnviroSat).

Como usar:
    1. Coloque este arquivo dentro da pasta do seu projeto (ex.: a pasta mission-control-ai).
    2. Abra o CMD nessa pasta e rode:  py setup.py
    3. O script cria as pastas e escreve os arquivos.
       Arquivos que ja existem sao preservados (nao sobrescreve seu trabalho).

Depois, crie o .env com a sua OLLAMA_API_KEY e siga os passos que o script imprime no final.
"""
from pathlib import Path

ARQUIVOS = {
    'main.py': r'''"""Mission Control AI — ponto de entrada do sistema."""
from src.ui import run_cli
from src.engine import MissionEngine

if __name__ == "__main__":
    engine = MissionEngine()
    run_cli(engine)
''',
    'requirements.txt': r'''# Dependências mínimas — versões fixadas para reprodutibilidade.
ollama==0.6.2
python-dotenv==1.2.2
rich==15.0.0
prompt-toolkit==3.0.52
pyfiglet==1.0.4

# Opcionais (descomente se quiser incrementar):
# textual==6.4.0        # TUI completa, estilo aplicativo
# pandas==2.2.3         # séries temporais da telemetria
# matplotlib==3.9.2     # gráficos
''',
    '.gitignore': r'''# Credenciais — NUNCA versionar
.env

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
env/

# IDEs
.vscode/
.idea/

# Sistema operacional
.DS_Store
Thumbs.db
''',
    '.env.example': r'''# Arquivo: .env.example  (template — copie para .env e preencha)
#
# IMPORTANTE:
#   - O arquivo .env REAL nunca deve ser versionado.
#   - Confirme que ".env" está no .gitignore ANTES do primeiro commit.
#   - Se a chave vazar no histórico do Git, gere uma nova no painel da Ollama.

OLLAMA_API_KEY=sua_chave_aqui_sem_aspas
''',
    'README.md': r'''# 🚀 Mission Control AI — EnviroSat

Sistema de monitoramento e análise de telemetria de satélite por IA generativa.
Trilha **EnviroSat** (observação ambiental) — Global Solution 2026.1 · FIAP ·
Prompt Engineering and Artificial Intelligence.

> 🚧 Em desenvolvimento. As seções completas (integrantes e RM, persona,
> cenários de teste, limitações conhecidas e proposta de valor / modelo de
> negócio) serão preenchidas na fase final.

## O que o projeto faz
Recebe dados simulados de telemetria de um satélite de observação ambiental,
detecta anomalias por lógica em Python e usa o modelo `gpt-oss:120b` (via
Ollama Cloud) para interpretar o estado da missão em linguagem natural,
traduzindo cada alerta em impacto terrestre (desmatamento e focos de incêndio).

## Tecnologias utilizadas
- Python 3.10+
- Ollama Cloud API (modelo `gpt-oss:120b`)
- Bibliotecas: `ollama`, `python-dotenv`, `rich`, `prompt-toolkit`, `pyfiglet`

## Como executar
1. Clone o repositório.
2. Crie o ambiente virtual: `python -m venv .venv && source .venv/bin/activate`
   (no Windows: `.venv\Scripts\activate`).
3. Instale as dependências: `pip install -r requirements.txt`
4. Crie um arquivo `.env` na raiz com:
   ```
   OLLAMA_API_KEY=sua_chave_aqui
   ```
5. Execute: `python main.py`

## Estrutura
```
mission-control-ai/
├── main.py              # ponto de entrada
├── banner_ascii.py      # gerador de banner ASCII
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── ui.py            # interface CLI (Rich + prompt-toolkit)
│   ├── engine.py        # motor de análise + função llm()
│   ├── telemetria.py    # geração dos dados simulados
│   └── alertas.py       # thresholds e regras de decisão
└── prompts/
    └── system_prompt.md # system prompt da IA
```
''',
    'banner_ascii.py': r'''"""Gerador de banner ASCII da Mission Control AI (trilha EnviroSat).

Uso:
    python banner_ascii.py                       # banner padrão
    python banner_ascii.py --fonts               # lista as fontes do PyFiglet
    python banner_ascii.py --font slant --text "Mission Control AI"
    python banner_ascii.py --demo                # compara algumas fontes
"""
import argparse

import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()


def render_banner(linha1_txt="Global Solution",
                  linha2_txt="Mission Control AI",
                  font="ansi_shadow"):
    """Gera e imprime o banner em ASCII art, no estilo da CLI."""
    linha1 = pyfiglet.figlet_format(linha1_txt, font=font)
    linha2 = pyfiglet.figlet_format(linha2_txt, font=font)
    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
             style="italic #8484A0")
    ))


def listar_fontes():
    """Imprime todas as fontes disponíveis no PyFiglet."""
    for fonte in sorted(pyfiglet.FigletFont.getFonts()):
        console.print(fonte)


def demo():
    """Mostra a frase em algumas fontes diferentes para comparação."""
    fontes = ["ansi_shadow", "slant", "standard", "small",
              "big", "banner3", "doom", "isometric1"]
    for fonte in fontes:
        console.rule(f"[bold #06B6D4]{fonte}")
        try:
            console.print(pyfiglet.figlet_format("Mission Control", font=fonte))
        except Exception as e:
            console.print(f"(fonte indisponível: {e})", style="red")


def main():
    parser = argparse.ArgumentParser(
        description="Banner ASCII da Mission Control AI"
    )
    parser.add_argument("--fonts", action="store_true",
                        help="lista as fontes disponíveis")
    parser.add_argument("--font", default="ansi_shadow",
                        help="fonte do PyFiglet a usar")
    parser.add_argument("--text", default="Mission Control AI",
                        help="texto da segunda linha")
    parser.add_argument("--demo", action="store_true",
                        help="compara várias fontes lado a lado")
    args = parser.parse_args()

    if args.fonts:
        listar_fontes()
    elif args.demo:
        demo()
    else:
        render_banner(linha2_txt=args.text, font=args.font)


if __name__ == "__main__":
    main()
''',
    'src/__init__.py': r'''# Marca o diretório src/ como um pacote Python.
''',
    'src/engine.py': r'''"""Motor de análise da Mission Control AI."""
import os
from pathlib import Path

from ollama import Client
from dotenv import load_dotenv

load_dotenv()

# Identificação da trilha escolhida pelo grupo.
TRILHA = "envirosat"  # "agrosat" | "envirosat" | "connectsat" | "mobilitysat"

# Cliente Ollama Cloud (mesmo padrão dos Checkpoints 02 e 03).
client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")},
)

# Aviso de sanidade ao iniciar: confirma se a chave foi carregada do .env.
_api = os.environ.get("OLLAMA_API_KEY")
if not _api:
    print("⚠ OLLAMA_API_KEY não encontrada — verifique o arquivo .env.")


def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia o prompt ao gpt-oss:120b via Ollama Cloud e retorna o texto.

    Este é o ÚNICO ponto de contato do projeto com o modelo.
    Toda chamada à IA passa por aqui — não reescreva esta função,
    chame-a de dentro de MissionEngine.analyze().
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        return client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md."""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente."  # fallback genérico


class MissionEngine:
    """Motor de análise — os métodos abaixo são completados nas próximas fases."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()

    def is_ready(self):
        # Trocar para True quando analyze() estiver implementado (Fase 4).
        return False

    def status_snapshot(self):
        """Retorna um texto resumindo o estado atual da telemetria."""
        # TODO (Fase 4): chamar telemetria.coletar() e formatar de forma legível.
        return "🛠 status_snapshot() ainda não implementado."

    def analyze(self, pergunta_usuario):
        """Analisa a pergunta com base na telemetria + alertas + IA."""
        # TODO (foco do trabalho — Fases 2 a 4):
        #   1. Coletar dados via src.telemetria.coletar()
        #   2. Avaliar alertas via src.alertas.avaliar(dados)
        #   3. Montar o prompt com dados + alertas + a pergunta do usuário
        #   4. Chamar llm(prompt, system=self.system_prompt)
        #   5. Retornar a resposta
        return (
            "🛠 Implementação pendente.\n\n"
            "Olá! A interface CLI está funcionando, mas a lógica\n"
            "de análise ainda não foi conectada. Falta:\n\n"
            "  1. Completar src/telemetria.py\n"
            "  2. Completar src/alertas.py\n"
            "  3. Escrever o system prompt em prompts/system_prompt.md\n"
            "  4. Sobrescrever analyze() em src/engine.py"
        )
''',
    'src/ui.py': r'''"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""
from datetime import datetime

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))


def show_banner():
    """Exibe o banner ASCII colorido no início da sessão."""
    banner = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    console.print(Text(banner, style="bold #06B6D4"))
    console.print(Panel.fit(
        "Bem-vindo à interface da Mission Control AI — trilha EnviroSat.\n"
        "Sistema de monitoramento e análise de telemetria por IA generativa.\n"
        "Use /help para ver os comandos · /exit para sair.\n"
        "Modelo: gpt-oss:120b via Ollama Cloud",
        title="◆ MISSION CONTROL",
        border_style="#06B6D4",
        subtitle="connected",
    ))


def show_response(text):
    """Renderiza a resposta da IA em um painel com timestamp."""
    now = datetime.now().strftime("%H:%M")
    console.print(Panel(text, title="◆ Mission Control",
                        subtitle=now, border_style="#06B6D4"))


def show_help():
    """Lista os comandos disponíveis."""
    console.print(Panel(
        "/help    mostra esta ajuda\n"
        "/status  resumo do estado atual da telemetria\n"
        "/about   sobre o projeto e a trilha\n"
        "/clear   limpa a tela\n"
        "/exit    encerra a sessão",
        title="◆ Comandos", border_style="#A855F7",
    ))


def show_about():
    """Mostra informações sobre o projeto e a trilha."""
    console.print(Panel(
        "Mission Control AI — Global Solution 2026.1 · FIAP\n"
        "Trilha EnviroSat (observação ambiental).\n\n"
        "Simula a telemetria de um satélite de monitoramento ambiental\n"
        "(estilo Amazônia-1 / Landsat) e usa IA generativa para traduzir\n"
        "o estado da missão em impacto terrestre: combate ao desmatamento\n"
        "e resposta rápida a focos de incêndio.",
        title="◆ Sobre", border_style="#A855F7",
    ))


def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()
    if not engine.is_ready():
        console.print("\n⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n", style="yellow")

    while True:
        try:
            user_input = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\nEncerrando a Mission Control. Até logo.", style="#06B6D4")
            break

        if not user_input:
            continue
        if user_input == "/exit":
            console.print("Encerrando a Mission Control. Até logo.", style="#06B6D4")
            break
        if user_input == "/help":
            show_help()
            continue
        if user_input == "/about":
            show_about()
            continue
        if user_input == "/status":
            show_response(engine.status_snapshot())
            continue
        if user_input == "/clear":
            console.clear()
            show_banner()
            continue

        # Qualquer outra entrada vai para o motor de análise.
        resposta = engine.analyze(user_input)
        show_response(resposta)
''',
    'src/telemetria.py': r'''"""Geração da telemetria simulada do satélite EnviroSat.

Implementação completa na Fase 2. Por enquanto, apenas o esqueleto.
"""


def coletar():
    """Coleta (simula) os parâmetros atuais da telemetria.

    Retornará um dicionário com os parâmetros monitorados da trilha
    EnviroSat: sensor térmico (detecção de focos), sensor óptico RGB+NIR,
    buffer de imagens não transmitidas, precisão de geolocalização e
    energia disponível.
    """
    # TODO (Fase 2): gerar valores plausíveis, variando por ciclo.
    raise NotImplementedError("telemetria.coletar() será implementado na Fase 2.")
''',
    'src/alertas.py': r'''"""Regras de alerta e decisão para a telemetria do EnviroSat.

Implementação completa na Fase 2. Por enquanto, apenas o esqueleto.
"""


def avaliar(dados):
    """Avalia a telemetria e retorna os alertas e ações automatizadas.

    Aplicará os thresholds em Python (Fase 2) e devolverá quais
    parâmetros estão críticos, a severidade de cada um e a resposta
    automatizada disparada em situação de crise.
    """
    # TODO (Fase 2): implementar thresholds e respostas automatizadas.
    raise NotImplementedError("alertas.avaliar() será implementado na Fase 2.")
''',
    'prompts/system_prompt.md': r'''# System Prompt — Mission Control AI (EnviroSat)

> 🚧 PLACEHOLDER. O system prompt definitivo é escrito na Fase 3
> (papel + escopo + restrições + tom + formato de saída +
> a amarra obrigatória entre análise técnica e impacto terrestre).

Você é um assistente da Mission Control AI.
''',
}


def main():
    criados = []
    mantidos = []
    for caminho, conteudo in ARQUIVOS.items():
        p = Path(caminho)
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            mantidos.append(caminho)
            continue
        p.write_text(conteudo, encoding="utf-8")
        criados.append(caminho)

    print("=" * 54)
    print(" Mission Control AI - Fase 1: estrutura gerada")
    print("=" * 54)
    for c in criados:
        print("  [criado]  " + c)
    for m in mantidos:
        print("  [mantido] " + m + "  (ja existia, preservado)")
    print()
    print("Proximos passos:")
    print("  1. Crie um arquivo .env na raiz com a sua chave Ollama:")
    print("       OLLAMA_API_KEY=sua_chave_aqui")
    print("  2. py -m venv .venv")
    print("     .venv\\Scripts\\activate")
    print("  3. pip install -r requirements.txt")
    print("  4. py main.py   (rode em um terminal/CMD de verdade)")
    print()
    print("Voce deve ver o banner ciano e o aviso AGUARDANDO IMPLEMENTACAO.")


if __name__ == "__main__":
    main()
