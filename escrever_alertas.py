"""escrever_alertas.py - atualiza src/alertas.py (Fase 2, passo 2).

Rode na pasta do projeto:  py escrever_alertas.py
Ele sobrescreve o esqueleto vazio de src/alertas.py pela versao real.
"""
from pathlib import Path

CONTEUDO = r'''"""Regras de alerta e decisão para a telemetria do EnviroSat.

Aqui mora a lógica de decisão EM PYTHON (não no prompt da IA): cada parâmetro
é comparado com seus limites, recebe um nível (ok / atenção / crítico) e, em
situação de crise, dispara uma resposta automatizada. A função avaliar()
devolve um resumo que será injetado no prompt da IA na Fase 4.
"""

# Limites por parâmetro. Para cada um definimos:
#   - "rotulo"        : nome amigável para exibir
#   - "unidade"       : unidade do valor
#   - "direcao"       : "acima"  -> valor alto é ruim
#                       "abaixo" -> valor baixo é ruim
#   - "limite_atencao", "limite_critico"
#   - "impacto"       : a consequência terrestre quando esse parâmetro falha
REGRAS = {
    "temperatura_payload_C": {
        "rotulo": "Temperatura do payload",
        "unidade": "°C",
        "direcao": "acima",
        "limite_atencao": 45,
        "limite_critico": 60,
        "impacto": "Sensor óptico/térmico pode degradar e parar de detectar focos de incêndio.",
    },
    "energia_bateria_pct": {
        "rotulo": "Energia da bateria",
        "unidade": "%",
        "direcao": "abaixo",
        "limite_atencao": 40,
        "limite_critico": 20,
        "impacto": "Sem energia, o satélite corta funções e deixa de imagear áreas monitoradas.",
    },
    "sinal_downlink_pct": {
        "rotulo": "Sinal de downlink",
        "unidade": "%",
        "direcao": "abaixo",
        "limite_atencao": 70,
        "limite_critico": 40,
        "impacto": "Imagens não descem para a Terra; alertas de desmatamento e fogo atrasam.",
    },
    "buffer_imagens_pct": {
        "rotulo": "Buffer de imagens",
        "unidade": "%",
        "direcao": "acima",
        "limite_atencao": 80,
        "limite_critico": 95,
        "impacto": "Buffer cheio descarta imagens novas — pode perder um foco recém-detectado.",
    },
    "erro_geolocalizacao_m": {
        "rotulo": "Erro de geolocalização",
        "unidade": "m",
        "direcao": "acima",
        "limite_atencao": 50,
        "limite_critico": 200,
        "impacto": "Coordenada imprecisa: a brigada de incêndio pode ser enviada ao local errado.",
    },
}


def _classificar(valor, regra):
    """Classifica um valor como 'ok', 'atencao' ou 'critico' conforme a regra."""
    if regra["direcao"] == "acima":
        if valor > regra["limite_critico"]:
            return "critico"
        if valor > regra["limite_atencao"]:
            return "atencao"
        return "ok"
    else:  # "abaixo": valores baixos são ruins
        if valor < regra["limite_critico"]:
            return "critico"
        if valor < regra["limite_atencao"]:
            return "atencao"
        return "ok"


def avaliar(dados):
    """Avalia a telemetria e retorna os alertas e as ações automatizadas.

    Args:
        dados: dicionário vindo de telemetria.coletar().

    Returns:
        dict com:
          - "nivel_geral": "ok" | "atencao" | "critico"
          - "alertas": lista de {parametro, rotulo, valor, unidade, nivel, impacto}
          - "acoes": lista de respostas automatizadas disparadas pela crise
    """
    alertas = []
    acoes = []

    # 1) Classifica cada parâmetro contra seus limites.
    for chave, regra in REGRAS.items():
        if chave not in dados:
            continue
        valor = dados[chave]
        nivel = _classificar(valor, regra)
        if nivel != "ok":
            alertas.append({
                "parametro": chave,
                "rotulo": regra["rotulo"],
                "valor": valor,
                "unidade": regra["unidade"],
                "nivel": nivel,
                "impacto": regra["impacto"],
            })

    # 2) Respostas automatizadas para situações críticas (decisão em Python).
    if dados.get("energia_bateria_pct", 100) < REGRAS["energia_bateria_pct"]["limite_critico"]:
        acoes.append("MODO ECONOMIA ativado: desligar instrumentos não essenciais para preservar a bateria.")
    if dados.get("buffer_imagens_pct", 0) > REGRAS["buffer_imagens_pct"]["limite_critico"]:
        acoes.append("PRIORIZAR DOWNLINK: forçar transmissão imediata para liberar o buffer e não perder imagens.")
    if dados.get("temperatura_payload_C", 0) > REGRAS["temperatura_payload_C"]["limite_critico"]:
        acoes.append("PROTEÇÃO TÉRMICA: reduzir uso do sensor e reorientar o satélite para resfriar o payload.")

    # 3) Nível geral da missão = o pior nível encontrado.
    if any(a["nivel"] == "critico" for a in alertas):
        nivel_geral = "critico"
    elif any(a["nivel"] == "atencao" for a in alertas):
        nivel_geral = "atencao"
    else:
        nivel_geral = "ok"

    return {"nivel_geral": nivel_geral, "alertas": alertas, "acoes": acoes}


# Teste standalone:  py src/alertas.py
if __name__ == "__main__":
    from telemetria import coletar

    for cenario in ["normal", "aleatorio", "critico"]:
        print(f"\n===== Cenário: {cenario.upper()} =====")
        dados = coletar(cenario)
        resultado = avaliar(dados)
        print(f"Nível geral da missão: {resultado['nivel_geral'].upper()}")

        if resultado["alertas"]:
            print("Alertas:")
            for a in resultado["alertas"]:
                print(f"  [{a['nivel'].upper()}] {a['rotulo']}: {a['valor']}{a['unidade']}")
                print(f"        impacto: {a['impacto']}")
        else:
            print("Nenhum alerta — todos os parâmetros dentro do esperado.")

        if resultado["acoes"]:
            print("Ações automatizadas disparadas:")
            for acao in resultado["acoes"]:
                print(f"  -> {acao}")
'''


def main():
    destino = Path('src/alertas.py')
    if not destino.parent.exists():
        print('ERRO: rode este script DENTRO da pasta do projeto (onde fica a pasta src).')
        return
    destino.write_text(CONTEUDO, encoding='utf-8')
    print('OK: src/alertas.py atualizado.')
    print('Teste agora com:  py src/alertas.py')


if __name__ == '__main__':
    main()
