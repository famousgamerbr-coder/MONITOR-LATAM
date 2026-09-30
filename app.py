import streamlit as st
import os
import json
from decimal import Decimal
import pandas as pd
import requests

# ... (mantenha as suas funções carregar_dados_salvos e formatar_dinheiro iguais) ...

# Layout do Painel
st.title("🛫 Monitor de Preços - LATAM")
st.markdown("---")

# Botão de Atualização Manual no topo
col_titulo, col_botao = st.columns([3, 1])
with col_titulo:
    st.subheader("Estado Atual")
with col_botao:
    if st.button("🔄 Atualizar Agora", type="primary"):
        # Tenta disparar o GitHub Actions via API
        try:
            token = st.secrets.get("GITHUB_TOKEN")
            repo = "famousgamerbr-coder/MONITOR-LATAM"
            url = f"https://api.github.com/repos/{repo}/actions/workflows/atualizar.yml/dispatches"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json"
            }
            data = {"ref": "main"}
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 204:
                st.success("Solicitação enviada! Os preços vão atualizar em 1-2 minutos.")
                st.rerun()
            else:
                st.error("Erro ao solicitar atualização. Verifique o token.")
        except Exception as e:
            st.error(f"Erro de configuração: {e}")

dados = carregar_dados_salvos()
# ... (restante do código continua igualzinho a partir daqui)
