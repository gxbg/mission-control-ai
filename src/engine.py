"""Motor de análise da Mission Control AI."""
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
