"""escrever_fase4.py - grava engine.py e ui.py finais (Fase 4 - integracao).

Rode na pasta do projeto:  py escrever_fase4.py
Conecta a telemetria + alertas + IA no MissionEngine e habilita os
comandos /status /ciclo /normal /critico na CLI.
"""
from pathlib import Path

ARQUIVOS = {
    'src/engine.py': r'''"""Motor de análise da Mission Control AI."""
import os
from pathlib import Path

from ollama import Client
from dotenv import load_dotenv

from src import telemetria, alertas

load_dotenv()

# Identificação da trilha escolhida pelo grupo.
TRILHA = "envirosat"  # "agrosat" | "envirosat" | "connectsat" | "mobilitysat"

# Cliente Ollama Cloud (mesmo padrão dos Checkpoints 02 e 03).
client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")},
)

_api = os.environ.get("OLLAMA_API_KEY")
if not _api:
    print("⚠ OLLAMA_API_KEY não encontrada — verifique o arquivo .env.")


def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia o prompt ao gpt-oss:120b via Ollama Cloud e retorna o texto.

    Único ponto de contato do projeto com o modelo. Toda chamada à IA passa
    por aqui.
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


def _formatar_status(dados, resultado):
    """Monta um texto legível do estado atual da missão (sem chamar a IA)."""
    linhas = [f"Trilha: EnviroSat  |  Nível geral: {resultado['nivel_geral'].upper()}", ""]
    linhas.append("Telemetria atual:")
    for chave, valor in dados.items():
        linhas.append(f"  - {chave}: {valor}")

    if resultado["alertas"]:
        linhas.append("")
        linhas.append("Alertas:")
        for a in resultado["alertas"]:
            linhas.append(f"  - [{a['nivel'].upper()}] {a['rotulo']}: {a['valor']}{a['unidade']}")
    else:
        linhas.append("")
        linhas.append("Alertas: nenhum, todos os parâmetros dentro do normal.")

    if resultado["acoes"]:
        linhas.append("")
        linhas.append("Ações automáticas acionadas:")
        for acao in resultado["acoes"]:
            linhas.append(f"  - {acao}")
    return "\n".join(linhas)


def _montar_prompt(dados, resultado, pergunta):
    """Monta o texto enviado à IA, injetando dados + alertas + a pergunta."""
    linhas = ["TELEMETRIA ATUAL DO SATÉLITE:"]
    for chave, valor in dados.items():
        linhas.append(f"  - {chave}: {valor}")

    linhas.append("")
    linhas.append(f"NÍVEL GERAL (calculado pelo sistema): {resultado['nivel_geral'].upper()}")

    if resultado["alertas"]:
        linhas.append("ALERTAS DETECTADOS:")
        for a in resultado["alertas"]:
            linhas.append(
                f"  - [{a['nivel'].upper()}] {a['rotulo']}: "
                f"{a['valor']}{a['unidade']} | impacto: {a['impacto']}"
            )
    else:
        linhas.append("ALERTAS: nenhum, todos os parâmetros dentro do normal.")

    if resultado["acoes"]:
        linhas.append("AÇÕES AUTOMÁTICAS JÁ ACIONADAS PELO SISTEMA:")
        for acao in resultado["acoes"]:
            linhas.append(f"  - {acao}")

    linhas.append("")
    linhas.append(f"PERGUNTA DO OPERADOR: {pergunta}")
    return "\n".join(linhas)


class MissionEngine:
    """Motor de análise da missão — combina telemetria, alertas e IA."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self.cenario = "aleatorio"
        # Leitura inicial da telemetria ao ligar o sistema.
        self.dados = telemetria.coletar(self.cenario)

    def is_ready(self):
        return True

    def novo_ciclo(self, cenario=None):
        """Gera uma nova leitura de telemetria e devolve o status formatado.

        Se 'cenario' for informado ("normal" | "critico" | "aleatorio"),
        ele passa a valer para as próximas leituras (útil para a demonstração).
        """
        if cenario:
            self.cenario = cenario
        self.dados = telemetria.coletar(self.cenario)
        resultado = alertas.avaliar(self.dados)
        return _formatar_status(self.dados, resultado)

    def status_snapshot(self):
        """Resumo legível do estado atual (sem IA) — usado pelo comando /status."""
        resultado = alertas.avaliar(self.dados)
        return _formatar_status(self.dados, resultado)

    def analyze(self, pergunta_usuario):
        """Analisa a pergunta com base na telemetria atual + alertas + IA."""
        resultado = alertas.avaliar(self.dados)
        prompt = _montar_prompt(self.dados, resultado, pergunta_usuario)
        return llm(prompt, system=self.system_prompt)
''',
    'src/ui.py': r'''"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""
from datetime import datetime

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
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


def show_response(text, markdown=False):
    """Renderiza uma resposta em painel com timestamp.

    Se markdown=True, o texto é interpretado como Markdown (negrito, listas),
    deixando a análise da IA mais legível.
    """
    now = datetime.now().strftime("%H:%M")
    conteudo = Markdown(text) if markdown else text
    console.print(Panel(conteudo, title="◆ Mission Control",
                        subtitle=now, border_style="#06B6D4"))


def show_help():
    """Lista os comandos disponíveis."""
    console.print(Panel(
        "/help     mostra esta ajuda\n"
        "/status   estado atual da telemetria (sem IA)\n"
        "/ciclo    gera uma nova leitura de telemetria\n"
        "/normal   força um cenário de operação normal\n"
        "/critico  força um cenário de crise (ótimo para a demonstração)\n"
        "/about    sobre o projeto e a trilha\n"
        "/clear    limpa a tela\n"
        "/exit     encerra a sessão\n\n"
        "Qualquer outra frase é enviada à IA para análise da missão.",
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
        if user_input == "/ciclo":
            show_response(engine.novo_ciclo("aleatorio"))
            continue
        if user_input == "/normal":
            show_response(engine.novo_ciclo("normal"))
            continue
        if user_input == "/critico":
            show_response(engine.novo_ciclo("critico"))
            continue
        if user_input == "/clear":
            console.clear()
            show_banner()
            continue

        # Qualquer outra entrada vai para o motor de análise (IA).
        console.print("Analisando a missão...", style="#8484A0")
        resposta = engine.analyze(user_input)
        show_response(resposta, markdown=True)
''',
}


def main():
    if not Path('src').exists():
        print('ERRO: rode este script DENTRO da pasta do projeto (onde fica a pasta src).')
        return
    for caminho, conteudo in ARQUIVOS.items():
        Path(caminho).write_text(conteudo, encoding='utf-8')
        print('OK:', caminho, 'atualizado.')
    print()
    print('Agora rode o sistema completo:  py main.py')


if __name__ == '__main__':
    main()
