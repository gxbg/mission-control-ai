"""Motor de análise da Mission Control AI."""
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
