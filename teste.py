import json
from datetime import datetime

ARQUIVO_PRECO = "preco_anterior.json"

def executar_teste():
    print("A iniciar consulta de teste dos voos LATAM...")
    
    # Aqui simula os valores obtidos na consulta do robô
    preco_total_calculado = 2650.00
    preco_ida_calculado = 1300.00
    preco_volta_calculado = 1350.00
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Lê dados anteriores para preservar histórico se existir
    preco_antigo = 2731.00
    historico = []
    if os.path.exists(ARQUIVO_PRECO):
        try:
            with open(ARQUIVO_PRECO, "r", encoding="utf-8") as f:
                dados_antigos = json.load(f)
                preco_antigo = dados_antigos.get("preco", 2731.00)
                historico = dados_antigos.get("historico", [])
        except:
            pass

    # Adiciona nova entrada ao histórico
    data_curta = datetime.now().strftime("%d/%m")
    historico.append({"data": data_curta, "preco": preco_total_calculado})

    novo_conteudo = {
        "preco": preco_total_calculado,
        "preco_anterior": preco_antigo,
        "preco_ida": preco_ida_calculado,
        "preco_volta": preco_volta_calculado,
        "ultima_consulta": agora,
        "historico": historico
    }

    with open(ARQUIVO_PRECO, "w", encoding="utf-8") as f:
        json.dump(novo_conteudo, f, ensure_ascii=False, indent=4)

    print(f"Consulta concluída com sucesso! Dados atualizados em {agora}")

if name == "main":
    import os
    executar_teste()