import streamlit as st
import os
import json
from decimal import Decimal
import pandas as pd
import requests

# Configuração da página
st.set_page_config(page_title="Monitor de Voos LATAM", layout="centered", page_icon="🛫")

ARQUIVO_PRECO = "preco_anterior.json"

def carregar_dados_salvos():
    if not os.path.exists(ARQUIVO_PRECO):
        return None
    try:
        with open(ARQUIVO_PRECO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def formatar_dinheiro(valor):
    try:
        val = Decimal(str(valor))
        fmt = "{:,.2f}".format(val)
        return "R$ " + fmt.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(valor)

# Layout do Painel
st.title("🛫 Monitor de Preços - LATAM")
st.markdown("---")

# Botão de Atualização Manual no topo
col_titulo, col_botao = st.columns([3, 1])
with col_titulo:
    st.subheader("Estado Atual")
with col_botao:
    if st.button("🔄 Atualizar", type="primary"):
        try:
            token = st.secrets.get("GITHUB_TOKEN")
            if not token:
                st.error("Erro: GITHUB_TOKEN em falta nos Secrets!")
            else:
                repo = "famousgamerbr-coder/MONITOR-LATAM"
                url = f"https://api.github.com/repos/{repo}/actions/workflows/atualizar.yml/dispatches"
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json"
                }
                data = {"ref": "main"}
                
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 204:
                    # Mensagem flutuante elegante que não estraga o layout
                    st.toast("✅ Ordem enviada! Aguarde 1 a 2 min e recarregue.", icon="🚀")
                else:
                    st.error(f"Erro do GitHub ({response.status_code})")
        except Exception as e:
            st.error(f"Erro: {e}")

# Carregamento dos dados salvos (Garantido após as funções)
dados = carregar_dados_salvos()

# Valores padrão
preco_total = 0.0
preco_anterior_val = 0.0
preco_ida = "Aguardando..."
preco_volta = "Aguardando..."
ultima_atualizacao = "Nunca"
historico = []

if dados:
    if "preco" in dados:
        preco_total = float(dados["preco"])
    if "preco_anterior" in dados:
        preco_anterior_val = float(dados["preco_anterior"])
    if "preco_ida" in dados:
        preco_ida = formatar_dinheiro(dados["preco_ida"])
    if "preco_volta" in dados:
        preco_volta = formatar_dinheiro(dados["preco_volta"])
    if "ultima_consulta" in dados:
        ultima_atualizacao = dados["ultima_consulta"]
    if "historico" in dados:
        historico = dados["historico"]

# Cálculo da variação para as setinhas
delta_str = None
if preco_anterior_val > 0:
    diff = preco_total - preco_anterior_val
    percentual = (diff / preco_anterior_val) * 100
    delta_str = f"{percentual:+.1f}% vs. anterior"

# Alerta Visual de Super Promoção (abaixo de R$ 2.500,00)
META_PROMOCAO = 2500.00
if preco_total > 0 and preco_total <= META_PROMOCAO:
    st.success(f"🔥 SUPER PROMOÇÃO DETECTADA! O preço geral está abaixo de R$ {META_PROMOCAO:,.2f}!".replace(",", "X").replace(".", ",").replace("X", "."))

# Métricas principais na tela
st.metric(
    label="Menor Preço Geral Encontrado", 
    value=formatar_dinheiro(preco_total) if preco_total > 0 else "Aguardando consulta...",
    delta=delta_str,
    delta_color="inverse"
)

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Menor Preço - Ida", value=preco_ida)
with col2:
    st.metric(label="Menor Preço - Volta", value=preco_volta)

# Exibição da Data e Horário da Última Pesquisa logo abaixo dos preços
st.markdown("---")
st.metric(label="🕒 Última Atualização / Consulta", value=ultima_atualizacao)

# Histórico de Preços em Tabela (Mais legível no telemóvel)
if historico and len(historico) > 0:
    st.markdown("---")
    st.subheader("📈 Histórico de Variação de Preços")
    df_hist = pd.DataFrame(historico)
    if "preco" in df_hist.columns and "data" in df_hist.columns:
        df_hist["preco"] = pd.to_numeric(df_hist["preco"])
        df_hist["preco_formatado"] = df_hist["preco"].apply(lambda x: formatar_dinheiro(x))
        
        df_exibir = df_hist[["data", "preco_formatado"]].rename(columns={
            "data": "Data / Hora",
            "preco_formatado": "Preço Registado"
        })
        
        st.dataframe(df_exibir, use_container_width=True, hide_index=True)

# Secção de Detalhes dos Trechos com visual moderno em cartões
st.markdown("---")
st.subheader("🗺️ Itinerário dos Voos Monitorados")

tab_ida, tab_volta = st.tabs(["✈️ Voo de Ida (24/01/2027)", "✈️ Voo de Volta (30/01/2027)"])

with tab_ida:
    st.markdown("**Rota Completa:** Imperatriz ➔ Gramado/POA")
    with st.container(border=True):
        st.markdown("##### 🛫 Trecho 1")
        st.markdown("**Voo:** `LA3435` | LATAM")
        st.markdown("📍 **Origem:** Imperatriz (IMP)")
        st.markdown("🎯 **Destino:** São Paulo (GRU)")
        st.markdown("🕓 **Saída:** 04:10")
    
    with st.container(border=True):
        st.markdown("##### 🛬 Trecho 2")
        st.markdown("**Voo:** `LA3218` | LATAM")
        st.markdown("📍 **Origem:** São Paulo (GRU)")
        st.markdown("🎯 **Destino:** Porto Alegre / Gramado (POA)")
        st.markdown("🕙 **Chegada desejada:** Entre 10:00 e 12:15")

with tab_volta:
    st.markdown("**Rota Completa:** Gramado/POA ➔ Imperatriz")
    with st.container(border=True):
        st.markdown("##### 🛫 Trecho 1")
        st.markdown("**Voo:** `LA4526` | LATAM")
        st.markdown("📍 **Origem:** Porto Alegre / Gramado (POA)")
        st.markdown("🎯 **Destino:** São Paulo (GRU)")
        st.markdown("🕗 **Saída:** 20:05")
    
    with st.container(border=True):
        st.markdown("##### 🛬 Trecho 2")
        st.markdown("**Voo:** `LA3466` | LATAM")
        st.markdown("📍 **Origem:** São Paulo (GRU)")
        st.markdown("🎯 **Destino:** Imperatriz (IMP)")
        st.markdown("🕝 **Chegada:** 02:35 (já no dia 31/01)")
