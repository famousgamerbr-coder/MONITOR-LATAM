import json
from datetime import datetime, timedelta, timezone
import os

ARQUIVO_PRECO = "preco_anterior.json"

def atualizar_dados():
    if not os.path.exists(ARQUIVO_PRECO):
        print("Arquivo de preços não encontrado.")
        return

    # Lê o arquivo atual
    with open(ARQUIVO_PRECO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Aqui você colocaria a lógica que obtém o novo preço
    # (ou pode integrar com alguma API/fonte de dados que utilize)
    preco_atual = float(dados.get("preco", 0))
    
    # Define o fuso horário do Brasil (UTC-3) para a hora ficar correta
    fuso_brasil = timezone(timedelta(hours=-3))
    
    # Atualiza as informações de controle
    dados["preco_anterior"] = preco_atual
    dados["ultima_consulta"] = datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M")

    # Salva de volta no arquivo JSON
    with open(ARQUIVO_PRECO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print("Arquivo atualizado com sucesso!")

if __name__ == "__main__":
    atualizar_dados()
