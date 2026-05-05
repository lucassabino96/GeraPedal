import streamlit as st
import urllib.parse
from datetime import date
import json
from st_copy_to_clipboard import st_copy_to_clipboard

# Detectar se é mobile
def is_mobile():
    try:
        user_agent = st.context.headers["user-agent"]
        mobile_keywords = ["Android", "iPhone", "iPad", "Mobile"]
        return any(keyword in user_agent for keyword in mobile_keywords)
    except:
        return False

mobile = is_mobile()

st.set_page_config(page_title="Gera Pedal", page_icon="🚴")

st.title("🚴 Gerador de Pedal")

# =========================
# LISTA DE EMOJIS (ANTES DE TUDO!)
# =========================
# Emojis completos (mobile)
numeros_emoji_mobile = [
    "1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣",
    "🔟","1️⃣1️⃣","1️⃣2️⃣","1️⃣3️⃣","1️⃣4️⃣","1️⃣5️⃣",
    "1️⃣6️⃣","1️⃣7️⃣","1️⃣8️⃣","1️⃣9️⃣","2️⃣0️⃣",
    "2️⃣1️⃣","2️⃣2️⃣","2️⃣3️⃣","2️⃣4️⃣","2️⃣5️⃣",
    "2️⃣6️⃣","2️⃣7️⃣","2️⃣8️⃣","2️⃣9️⃣","3️⃣0️⃣"
]

# Versão segura (desktop)
numeros_emoji_desktop = [f"{i+1}." for i in range(30)]

if mobile:
    bike = "🚴‍♂️"
    fogo = "🔥"
    calendario = "📅"
    relogio = "⏰"
    local_icon = "📌"
    numeros = numeros_emoji_mobile
else:
    bike = "🚴"
    fogo = ""
    calendario = "Data:"
    relogio = "Hora:"
    local_icon = "Local:"
    numeros = numeros_emoji_desktop
    
# =========================
# INPUTS
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

data = st.date_input("Data do pedal", value=date.today())
data_formatada = data.strftime("%d/%m/%Y")

vagas = st.selectbox("Número de vagas", list(range(1, 31)))

# =========================
# GERAR TEXTO
# =========================
if st.button("Gerar texto"):

    # gera lista de vagas
    lista_vagas = "\n".join([
        f"{numeros[i]} - "
        for i in range(vagas)
    ])

    texto = f"""{bike} {grupo} {bike}

{fogo} {tipo_pedal}

📍 {destino}

{calendario} {data_formatada}
{relogio} {horario}
{local_icon} {local}

Confirmados:
{lista_vagas}
"""

    st.text_area("Texto pronto", texto, height=300)

    st_copy_to_clipboard(texto, "📋 Copiar texto")

    # =========================
    # LINK WHATSAPP
    # =========================
    mensagem = urllib.parse.quote(texto, safe='')
    link_whatsapp = f"https://api.whatsapp.com/send?text={mensagem}"

    if not mobile:
        st.info("💡 No computador, o botão WhatsApp usa uma versão simplificada para evitar erro de emojis. Para versão completa, use 'Copiar texto'.")

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
