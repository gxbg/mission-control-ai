"""escrever_telemetria.py - atualiza src/telemetria.py (Fase 2, passo 1).

Rode na pasta do projeto:  py escrever_telemetria.py
Ele sobrescreve o esqueleto vazio de src/telemetria.py pela versao real.
"""
from pathlib import Path

CONTEUDO = r'''"""Geração da telemetria simulada do satélite EnviroSat.

Simula, a cada ciclo, a leitura dos parâmetros monitorados de um satélite
de observação ambiental (estilo Amazônia-1 / Landsat). Os valores variam
de forma plausível e podem entrar em faixa crítica, o que serve para testar
a lógica de alertas (src/alertas.py) e a análise da IA.

Os 5 parâmetros monitorados:
  - temperatura_payload_C : temperatura do payload óptico/térmico (°C).
  - energia_bateria_pct   : carga restante da bateria (%).
  - sinal_downlink_pct    : qualidade do link para enviar imagens à Terra (%).
  - buffer_imagens_pct    : ocupação do buffer de imagens ainda não transmitidas (%).
  - erro_geolocalizacao_m : erro de posicionamento das imagens (metros).
"""
import random
from datetime import datetime


def coletar(cenario="aleatorio"):
    """Coleta (simula) os parâmetros atuais da telemetria do EnviroSat.

    Args:
        cenario: "aleatorio" (padrão), "normal" ou "critico".
            - "normal"  : força todos os valores dentro da faixa esperada.
            - "critico" : força uma situação de crise (útil para teste e demo).
            - "aleatorio": gera valores variando bastante, podendo cair em alerta.

    Returns:
        dict com os 5 parâmetros monitorados + um timestamp.
    """
    if cenario == "normal":
        dados = {
            "temperatura_payload_C": round(random.uniform(15, 40), 1),
            "energia_bateria_pct": round(random.uniform(55, 95), 1),
            "sinal_downlink_pct": round(random.uniform(75, 99), 1),
            "buffer_imagens_pct": round(random.uniform(10, 60), 1),
            "erro_geolocalizacao_m": round(random.uniform(5, 35), 1),
        }
    elif cenario == "critico":
        dados = {
            "temperatura_payload_C": round(random.uniform(62, 85), 1),
            "energia_bateria_pct": round(random.uniform(8, 18), 1),
            "sinal_downlink_pct": round(random.uniform(15, 38), 1),
            "buffer_imagens_pct": round(random.uniform(92, 100), 1),
            "erro_geolocalizacao_m": round(random.uniform(220, 500), 1),
        }
    else:  # "aleatorio": varia em uma faixa ampla, podendo gerar alertas
        dados = {
            "temperatura_payload_C": round(random.uniform(15, 70), 1),
            "energia_bateria_pct": round(random.uniform(12, 100), 1),
            "sinal_downlink_pct": round(random.uniform(30, 100), 1),
            "buffer_imagens_pct": round(random.uniform(10, 100), 1),
            "erro_geolocalizacao_m": round(random.uniform(5, 300), 1),
        }

    dados["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dados


# Permite testar este módulo sozinho:  py src/telemetria.py
if __name__ == "__main__":
    print("=== Cenário ALEATÓRIO ===")
    for chave, valor in coletar().items():
        print(f"  {chave}: {valor}")

    print("\n=== Cenário CRÍTICO (forçado) ===")
    for chave, valor in coletar("critico").items():
        print(f"  {chave}: {valor}")
'''


def main():
    destino = Path('src/telemetria.py')
    if not destino.parent.exists():
        print('ERRO: rode este script DENTRO da pasta do projeto (onde fica a pasta src).')
        return
    destino.write_text(CONTEUDO, encoding='utf-8')
    print('OK: src/telemetria.py atualizado.')
    print('Teste agora com:  py src/telemetria.py')


if __name__ == '__main__':
    main()
