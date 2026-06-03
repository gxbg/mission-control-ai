"""testar_prompt.py - testa o system prompt com uma chamada REAL a IA (Fase 3).

Rode na pasta do projeto:  py testar_prompt.py

Ele gera um cenario de telemetria, monta o prompt com os dados + alertas e
chama o gpt-oss:120b via Ollama Cloud para ver a analise em linguagem natural.

Esta e a PRIMEIRA chamada real a IA. Se aparecer erro de chave ou conexao,
e aqui que a gente descobre e ajusta.
"""
from src.engine import llm, load_system_prompt
from src.telemetria import coletar
from src.alertas import avaliar

# Troque por "normal", "aleatorio" ou "critico" para testar cenarios diferentes.
CENARIO = "critico"
PERGUNTA = "Como está a missão agora?"


def montar_prompt(dados, resultado, pergunta):
    """Monta o texto que vai para a IA, injetando dados + alertas + a pergunta."""
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


def main():
    dados = coletar(CENARIO)
    resultado = avaliar(dados)
    prompt = montar_prompt(dados, resultado, PERGUNTA)

    print("=" * 60)
    print(f"PROMPT ENVIADO À IA (cenário: {CENARIO}):")
    print("=" * 60)
    print(prompt)
    print("=" * 60)
    print("RESPOSTA DA IA (pode levar alguns segundos):")
    print("=" * 60)

    system = load_system_prompt()
    resposta = llm(prompt, system=system)
    print(resposta)


if __name__ == "__main__":
    main()
