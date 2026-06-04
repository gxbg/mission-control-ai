# 🚀 Mission Control AI — EnviroSat

Sistema de monitoramento e análise de telemetria de satélite por IA generativa.
Recebe dados simulados de um satélite de observação ambiental, detecta anomalias
por lógica em Python e usa o modelo `gpt-oss:120b` (Ollama Cloud) para interpretar
o estado da missão em linguagem natural, sempre traduzindo cada alerta em impacto
terrestre — combate ao desmatamento e resposta a focos de incêndio na Amazônia.

## 👥 Integrantes
- Gabriel de Paula Gil — RM: 567286
- Erik Medveder Nikoluk — RM: 567996
- Diego Leite Asprino — RM: 561662

**Modalidade:** Trio · **Trilha:** EnviroSat (Observação Ambiental)

## 🛰️ O que o projeto faz
A Mission Control AI simula a operação de um satélite ambiental (estilo Amazônia-1)
e funciona como um centro de controle. A cada ciclo ela lê 5 parâmetros de
telemetria, classifica o estado de cada um em Python (ok / atenção / crítico),
dispara respostas automáticas em situações de crise e aciona uma IA generativa que
explica, em linguagem natural, o que está acontecendo e qual a consequência
ambiental na Terra. A interface é uma CLI no estilo Claude Code.

## 🎯 Persona atendida
**Operador de centro de controle ambiental (INPE / órgão estadual), em apoio a
coordenadores de brigada de combate a incêndio.** Esse perfil precisa traduzir
rapidamente a saúde técnica do satélite em decisão operacional — por isso o sistema
entrega diagnóstico, criticidade e ação recomendada em poucos segundos, sem exigir
conhecimento de engenharia espacial.

## 🧰 Tecnologias utilizadas
- Python 3.10+
- Ollama Cloud API — modelo `gpt-oss:120b`
- Bibliotecas: `ollama`, `python-dotenv`, `rich`, `prompt-toolkit`, `pyfiglet`

## ▶️ Como executar
1. Clone o repositório.
2. Crie o ambiente virtual:
   - Windows: `py -m venv .venv` e depois `.venv\Scripts\activate`
   - Linux/Mac: `python -m venv .venv && source .venv/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`
4. Crie um arquivo `.env` na raiz com:
   ```
   OLLAMA_API_KEY=sua_chave_aqui
   ```
5. Execute: `py main.py`

**Comandos da CLI:** `/help`, `/status`, `/ciclo`, `/normal`, `/critico`, `/about`,
`/clear`, `/exit`. Qualquer outra frase é enviada à IA para análise da missão.

## 🖥️ Demonstração
![Status normal da missão](assets/screenshot_normal.png)
![Alerta crítico com análise da IA](assets/screenshot_alerta.png)

## 🧠 System Prompt
O system prompt completo está em [`prompts/system_prompt.md`](prompts/system_prompt.md).
Ele define o papel (analista de centro de controle ambiental), o escopo, as regras
(não inventar dados e não recalcular a criticidade — isso é decidido em Python), o
tom e o formato de saída, e obriga o modelo a amarrar cada análise técnica ao
impacto ambiental.

## 🧪 Cenários de teste demonstrados
1. **Operação normal** (`/normal`) — todos os parâmetros dentro da faixa, sem alertas.
2. **Crise múltipla** (`/critico`) — vários parâmetros em estado crítico, com as três
   respostas automáticas (modo economia, priorizar downlink, proteção térmica) e a
   análise contextualizada da IA.
3. **Leitura aleatória** (`/ciclo`) — telemetria sorteada, usada para verificar a
   consistência da análise. Rodamos o mesmo cenário várias vezes; com
   `temperature=0.3` o diagnóstico se manteve estável entre as execuções.

## ⚠️ Limitações conhecidas
- A telemetria é **simulada** (gerada aleatoriamente), não vem de um satélite real.
- Os limites (thresholds) são plausíveis, mas não calibrados com dados reais de engenharia.
- A IA é não-determinística; respostas podem variar entre execuções (mitigado com
  `temperature=0.3` e teste de consistência).
- Não há persistência de histórico entre sessões — cada execução começa do zero.
- Depende de conexão com a Ollama Cloud; sem internet ou chave válida, a IA não
  responde (o sistema trata o erro sem quebrar).

## 💼 Proposta de valor / modelo de negócio

**1. Qual o problema real terrestre que esta missão resolve?**
A Amazônia precisa de detecção rápida de desmatamento e de focos de incêndio para que
IBAMA, ICMBio e brigadas estaduais ajam antes que um foco vire um grande incêndio. Um
satélite ambiental só gera esse valor se operar bem: sensor térmico frio, imagens
transmitidas a tempo e coordenadas precisas. Quando algo falha em órbita, o impacto é
direto na Terra — os alertas atrasam ou saem com a coordenada errada, e a brigada
chega tarde ou no lugar errado.

**2. Quem paga pela solução?**
Modelo predominantemente **público, com componente híbrido**. O setor público opera e
financia o satélite (INPE) e consome os dados gratuitamente como bem público (IBAMA,
ICMBio, órgãos estaduais de meio ambiente, Defesa Civil). O setor privado entra como
pagante de serviços derivados: seguradoras rurais, certificadoras de cadeia produtiva
e fundos de carbono que precisam de dados auditáveis de compliance ambiental.

**3. Métrica de impacto (se o satélite operar 100% saudável por 1 ano):**
Monitoramento contínuo de cerca de **5 milhões de km²** da Amazônia Legal. Com alerta
de foco em até ~3 horas (em vez de ~24h), estima-se evitar o avanço para grandes
incêndios da ordem de **10 a 15 mil hectares por ano**, o que corresponde a evitar a
emissão de **centenas de milhares de toneladas de CO₂**.

**4. Modelo de negócio:**
**Concessão pública + dado-como-serviço (DaaS).** A operação do satélite é uma
concessão/atribuição pública (recursos do orçamento federal e ambiental), com os dados
ambientais oferecidos gratuitamente aos órgãos de fiscalização. Em paralelo, um braço
de **assinatura/DaaS** comercializa relatórios e APIs de compliance para o setor
privado, criando uma fonte de receita que ajuda a custear a operação.

## 🎬 Vídeo de demonstração
🔗 [Assistir demonstração no YouTube](LINK_DO_YOUTUBE_AQUI)
> Configurado como "Não listado" no YouTube. (Preencher o link na Fase 6.)
