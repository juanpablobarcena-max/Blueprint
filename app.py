import streamlit as st
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(page_title="MidePlanos PRO", layout="wide", initial_sidebar_state="collapsed")

# Cargar el HTML que contiene toda la lógica
try:
    with open("visor.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Inyectar el visor en la nube ocupando el máximo espacio
    components.html(html_code, height=900, scrolling=True)
    
except FileNotFoundError:
    st.error("No se ha encontrado el archivo visor.html en el repositorio de GitHub.")
