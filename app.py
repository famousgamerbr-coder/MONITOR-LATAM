import streamlit as st
import os
import json
from decimal import Decimal
import pandas as pd

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

# Gráfico de Histórico de Preços corrigido com Pandas
if historico and len(historico) > 0:
    st.markdown("---")
    st.subheader("📈 Histórico de Variação de Preços")
    df_hist = pd.DataFrame(historico)
    if "preco" in df_hist.columns and "data" in df_hist.columns:
        df_hist["preco"] = pd.to_numeric(df_hist["preco"])
        st.line_chart(df_hist, x="data", y="preco")

st.markdown("---")
st.subheader("Detalhes dos Trechos Monitorados")

st.markdown("Ida (Imperatriz ➔ Gramado/POA):")
st.write("• LA3435 | Imperatriz (IMP) ➔ São Paulo (GRU)")
st.write("• LA3218 | São Paulo (GRU) ➔ Porto Alegre (POA)")

st.markdown("Volta (Gramado/POA ➔ Imperatriz):")
st.write("• LA4526 | Porto Alegre (POA) ➔ São Paulo (GRU)")
st.write("• LA3466 | São Paulo (GRU) ➔ Imperatriz (IMP)")
