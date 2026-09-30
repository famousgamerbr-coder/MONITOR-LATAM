import os
import sys

print("--- DIAGNÓSTICO DO PROJETO LATAM ---")
print(f"Versão do Python: {sys.version}")

ficheiros_necessarios = ["app.py", "preco_anterior.json", "teste.py"]
for f in ficheiros_necessarios:
    existe = os.path.exists(f)
    status = "OK [Encontrado]" if existe else "FALTA [Não encontrado]"
    print(f"Ficheiro '{f}': {status}")

try:
    import streamlit
    print("Biblioteca Streamlit: Instalada OK")
except ImportError:
    print("Biblioteca Streamlit: FALTA (instalar com 'pip install streamlit')")

print("-----------------------------------")