import json
from datetime import datetime, timedelta, timezone
import os
import requests

ARQUIVO_PRECO = "preco_anterior.json"
META_PROMOCAO = 1750.00  # Meta de preço para alerta especial

def enviar_telegram(mensagem):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("⚠️ Credenciais do Telegram em falta nas variáveis de ambiente.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("📲 Notificação enviada para o Telegram com sucesso!")
        else:
            print(f"❌ Erro ao enviar para o Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão com o Telegram: {e}")

def atualizar_dados():
    if not os.path.exists(ARQUIVO_PRECO):
        print("❌ Arquivo de preços não encontrado.")
        return

    with open(ARQUIVO_PRECO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    preco_atual = float(dados.get("preco", 0))
    
    fuso_brasil = timezone(timedelta(hours=-3))
    agora = datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M")
    
    dados["preco_anterior"] = preco_atual
    dados["ultima_consulta"] = agora

    with open(ARQUIVO_PRECO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print("✅ Arquivo atualizado com sucesso!")

    # Monta a mensagem para o Telegram
    msg = (
        f"🛫 *Monitor LATAM - Atualização*\n\n"
        f"💰 *Preço Atual:* R$ {preco_atual:,.2f}\n"
        f"🕒 *Horário:* {agora}"
    )

    # Se o preço estiver abaixo ou igual à meta de R$ 1.750,00, avisa com destaque!
    if 0 < preco_atual <= META_PROMOCAO:
        msg = f"🔥 *SUPER PROMOÇÃO ABAIXO DE R$ 1.750,00!*\n\n" + msg

    # Dispara o alerta
    enviar_telegram(msg)

if __name__ == "__main__":
    atualizar_dados()
