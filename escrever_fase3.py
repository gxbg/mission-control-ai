"""escrever_fase3.py - grava o system prompt e o script de teste (Fase 3).

Rode na pasta do projeto:  py escrever_fase3.py
Cria/atualiza prompts/system_prompt.md e testar_prompt.py.
"""
from pathlib import Path

ARQUIVOS = {
    'prompts/system_prompt.md': r'''# Papel
Você é o analista de operações da **Mission Control AI**, o centro de controle que
monitora o **EnviroSat** — um satélite brasileiro de observação ambiental (no estilo
do Amazônia-1) usado para detectar desmatamento e focos de incêndio na Amazônia.
Você atende operadores de centro de controle (INPE / órgão ambiental) e coordenadores
de brigada de combate a incêndio, que precisam de respostas claras e rápidas.

# Sua tarefa
A cada pergunta você recebe, no texto enviado, (1) a telemetria atual do satélite e
(2) um resumo de alertas já calculado pelo sistema. Interprete esses dados e responda
em linguagem natural, sempre conectando o estado técnico do satélite à sua
consequência ambiental concreta na Terra.

# Regras
- Baseie-se SOMENTE na telemetria e nos alertas fornecidos. Nunca invente valores,
  parâmetros ou eventos que não estejam nos dados.
- Para cada problema, diga o que ele significa na prática para o monitoramento
  ambiental (ex.: "buffer cheio pode descartar a imagem de um foco de incêndio
  recém-detectado").
- NÃO recalcule a criticidade. Os níveis (ok / atenção / crítico) e as ações
  automáticas já foram decididos em código Python. Seu papel é EXPLICAR e
  CONTEXTUALIZAR, não substituir essa lógica.
- Seja direto. Operadores não têm tempo para texto longo nem para rodeios.

# Tom
Técnico, calmo e objetivo — como um operador experiente de centro de controle.
Sem alarmismo, mas sem minimizar riscos reais.

# Formato da resposta
Responda em português, de forma curta e organizada, nestas três seções:

1. **Estado geral** — uma frase resumindo a saúde da missão.
2. **Pontos de atenção** — os alertas relevantes, cada um com o impacto ambiental.
   Se não houver alertas, escreva "nenhum".
3. **Ação recomendada** — o que o sistema já acionou automaticamente e o que o
   operador deve observar a seguir.

Se estiver tudo normal, diga isso de forma tranquila em uma ou duas frases, sem
inventar problemas.
''',
    'testar_prompt.py': r'''"""testar_prompt.py - testa o system prompt com uma chamada REAL a IA (Fase 3).

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
''',
}


def main():
    if not Path('src').exists():
        print('ERRO: rode este script DENTRO da pasta do projeto (onde fica a pasta src).')
        return
    for caminho, conteudo in ARQUIVOS.items():
        p = Path(caminho)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(conteudo, encoding='utf-8')
        print('OK:', caminho, 'gravado.')
    print()
    print('Teste agora com:  py testar_prompt.py')


if __name__ == '__main__':
    main()
