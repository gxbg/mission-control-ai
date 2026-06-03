# 🚀 Mission Control AI — EnviroSat

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
