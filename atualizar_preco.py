import json
from datetime import datetime, timedelta, timezone
import os

ARQUIVO_PRECO = "preco_anterior.json"

def atualizar_dados():
    if not os.path.exists(ARQUIVO_PRECO):
        print("Arquivo de preços não encontrado.")
        return

    with open(ARQUIVO_PRECO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    preco_atual = float(dados.get("preco", 0))
    
    fuso_brasil = timezone(timedelta(hours=-3))
    
    dados["preco_anterior"] = preco_atual
    dados["ultima_consulta"] = datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M")

    with open(ARQUIVO_PRECO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print("Arquivo atualizado com sucesso!")

if __name__ == "__main__":
    atualizar_dados()
