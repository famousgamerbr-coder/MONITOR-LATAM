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

def buscar_preco_atual():
    """
    Aqui consulta o preço real dos voos para 24/01/2027 a 30/01/2027 (IMP -> GRU -> POA).
    Pode integrar aqui a sua API de preferência (ex: SerpAPI para Google Flights).
    """
    try:
        # Exemplo de chamada a uma API de voos ou motor de busca
        # (Se estiver a usar uma API externa, insere a chave nos Secrets do GitHub)
        # Por enquanto, colocamos a lógica de requisição real ou simulador de API:
        
        # Exemplo com SerpAPI (Google Flights):
        # api_key = os.environ.get("SERPAPI_KEY")
        # params = {
        #     "engine": "google_flights",
        #     "departure_id": "IMP",
        #     "arrival_id": "POA",
        #     "outbound_date": "2027-01-24",
        #     "return_date": "2027-01-30",
        #     "currency": "BRL",
        #     "api_key": api_key
        # }
        # resp = requests.get("https://serpapi.com/search", params=params)
        # dados_voo = resp.json()
        # preco_total = dados_voo["best_flights"][0]["price"]
        
        # NOTA: Para testes imediatos ou se preferir atualizar via webhook/scraper próprio, 
        # substitua a linha abaixo pela resposta real da sua fonte de dados:
        
        # Vamos manter uma leitura dinâmica ou retornar o valor recolhido:
        return 2532.22, 1200.00, 1332.22 # Exemplo: Total, Ida, Volta
        
    except Exception as e:
        print(f"Erro ao buscar preço real: {e}")
        return None, None, None

def atualizar_dados():
    if not os.path.exists(ARQUIVO_PRECO):
        dados_antigos = {"preco": 0, "historico": []}
    else:
        with open(ARQUIVO_PRECO, "r", encoding="utf-8") as f:
            dados_antigos = json.load(f)

    preco_anterior = float(dados_antigos.get("preco", 0))
    
    # Buscar preço real atualizado
    preco_total, preco_ida, preco_volta = buscar_preco_atual()
    
    if preco_total is None:
        print("❌ Não foi possível obter o preço nesta execução.")
        return

    fuso_brasil = timezone(timedelta(hours=-3))
    agora = datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M")
    
    # Atualiza o histórico
    historico = dados_antigos.get("historico", [])
    historico.insert(0, {"data": agora, "preco": preco_total})
    # Mantém apenas os últimos 50 registos no histórico
    historico = historico[:50]

    novos_dados = {
        "preco": preco_total,
        "preco_anterior": preco_anterior,
        "preco_ida": preco_ida,
        "preco_volta": preco_volta,
        "ultima_consulta": agora,
        "historico": historico
    }

    with open(ARQUIVO_PRECO, "w", encoding="utf-8") as f:
        json.dump(novos_dados, f, ensure_ascii=False, indent=4)

    print("✅ Preços atualizados com sucesso!")

    # Monta a mensagem para o Telegram
    msg = (
        f"🛫 *Monitor LATAM (24/01 a 30/01/2027)*\n\n"
        f"💰 *Preço Atual:* R$ {preco_total:,.2f}\n"
        f"✈️ *Ida:* R$ {preco_ida:,.2f} | *Volta:* R$ {preco_volta:,.2f}\n"
        f"🕒 *Horário:* {agora}"
    )

    # Se o preço estiver abaixo ou igual à meta de R$ 1.750,00, avisa com destaque!
    if 0 < preco_total <= META_PROMOCAO:
        msg = f"🔥 *SUPER PROMOÇÃO ABAIXO DE R$ 1.750,00!*\n\n" + msg

    # Dispara o alerta para o Telegram
    enviar_telegram(msg)

if __name__ == "__main__":
    atualizar_dados()
