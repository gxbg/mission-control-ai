"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""
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
