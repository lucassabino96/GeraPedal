import streamlit as st
import urllib.parse
from datetime import date

st.set_page_config(page_title="Gera Pedal", page_icon="🚴")

st.title("🚴 Gerador de Pedal")

# =========================
# DROPDOWNS
# =========================
grupo = st.selectbox("Grupo", [
    "Gigantes do Pedal",
    "Alto Giro",
    "Tribo da Bike",
    "Pedal dos Amigos",
    "CP MTB"
])

tipo_pedal = st.selectbox("Tipo de pedal", [
    "Giro Leve",
    "Giro Moderado",
    "Giro Forte",
    "Pedal de Sábado",
    "Pedal de Domingo",
    "Pedal do Feriado"
])

destino = st.text_input("Destino / Rota")
local = st.text_input("Local de saída")
horario = st.text_input("Horário", "06:00")

vagas = st.selectbox("Número de vagas", list(range(1, 31)))

data_hoje = date.today().strftime("%d/%m/%Y")

# =========================
# GERAR LISTA DE VAGAS
# =========================
lista_vagas = "\n".join([f"{i+1}️⃣ " for i in range(vagas)])

# =========================
# GERAR TEXTO
# =========================
if st.button("Gerar texto"):

    texto = f"""🚴‍♂️ {grupo} 🚴‍♂️

🔥 {tipo_pedal}

📍 {destino}

📅 {data_hoje}
⏰ {horario}
📌 {local}

Confirmados:
{lista_vagas}
"""

    st.text_area("Texto pronto", texto, height=300)

    # =========================
    # BOTÃO COPIAR
    # =========================
    st.code(texto, language="")

    # =========================
    # BOTÃO WHATSAPP
    # =========================
    mensagem = urllib.parse.quote(texto)
    link_whatsapp = f"https://wa.me/?text={mensagem}"

    st.markdown(f"""
    <a href="{link_whatsapp}" target="_blank">
        <button style="
            background-color:#25D366;
            color:white;
            padding:10px;
            border:none;
            border-radius:8px;
            font-size:16px;
            cursor:pointer;">
            📲 Enviar para WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)
