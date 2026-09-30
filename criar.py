import json
import os

ARQUIVO_PRECO = "preco_anterior.json"

dados_iniciais = {
    "preco": 2731.00,
    "preco_anterior": 2900.00,
    "preco_ida": 1350.00,
    "preco_volta": 1381.00,
    "ultima_consulta": "2026-09-30 12:35",
    "historico": [
        {"data": "28/09", "preco": 2900.00},
        {"data": "29/09", "preco": 2850.00},
        {"data": "30/09", "preco": 2731.00}
    ]
}

with open(ARQUIVO_PRECO, "w", encoding="utf-8") as f:
    json.dump(dados_iniciais, f, ensure_ascii=False, indent=4)

print("Ficheiro 'preco_anterior.json' criado/atualizado com sucesso!")