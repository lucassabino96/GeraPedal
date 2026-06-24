import streamlit as st
import urllib.parse
from datetime import date
from st_copy_to_clipboard import st_copy_to_clipboard
import math

# Configuração da página (deve ser a primeira instrução)
st.set_page_config(page_title="Portal do Ciclista", page_icon="🚴", layout="wide")

# =========================
# ESTADO E NAVEGAÇÃO
# =========================
st.sidebar.title("🚴 Menu Principal")
pagina = st.sidebar.radio("Selecione a ferramenta:", 
    ["Gerador de Pedal", "Calculadora de Zonas FC", "Ferramenta de Nutrição"])

# =========================
# FUNÇÕES AUXILIARES
# =========================
def is_mobile():
    try:
        user_agent = st.context.headers["user-agent"]
        mobile_keywords = ["Android", "iPhone", "iPad", "Mobile"]
        return any(keyword in user_agent for keyword in mobile_keywords)
    except:
        return False

# =========================
# PÁGINA 1: GERADOR DE PEDAL
# =========================
if pagina == "Gerador de Pedal":
    st.title("🚴 Gerador de Convite para Pedal")
    
    mobile = is_mobile()
    
    numeros_emoji_mobile = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟","1️⃣1️⃣","1️⃣2️⃣","1️⃣3️⃣","1️⃣4️⃣","1️⃣5️⃣","1️⃣6️⃣","1️⃣7️⃣","1️⃣8️⃣","1️⃣9️⃣","2️⃣0️⃣","2️⃣1️⃣","2️⃣2️⃣","2️⃣3️⃣","2️⃣4️⃣","2️⃣5️⃣","2️⃣6️⃣","2️⃣7️⃣","2️⃣8️⃣","2️⃣9️⃣","3️⃣0️⃣"]
    numeros_emoji_desktop = [f"{i+1}." for i in range(30)]

    if mobile:
        bike, fogo, calendario, relogio, local_icon = "🚴‍♂️", "🔥", "📅", "⏰", "📌"
        numeros = numeros_emoji_mobile
    else:
        bike, fogo, calendario, relogio, local_icon = "🚴", "", "Data:", "Hora:", "Local:"
        numeros = numeros_emoji_desktop

    col1, col2 = st.columns(2)
    with col1:
        grupo = st.selectbox("Grupo", ["Gigantes do Pedal", "Alto Giro", "Tribo da Bike", "Pedal dos Amigos", "CP MTB"])
        tipo_pedal = st.selectbox("Tipo", ["Giro Leve", "Giro Moderado", "Giro Forte", "Pedal de Sábado", "Pedal de Domingo"])
        destino = st.text_input("Destino / Rota")
    with col2:
        local = st.text_input("Local de saída")
        horario = st.text_input("Horário", "19:00")
        data = st.date_input("Data", value=date.today())
        vagas = st.selectbox("Vagas", list(range(1, 31)), index=9)

    if st.button("Gerar Texto"):
        data_f = data.strftime("%d/%m/%Y")
        lista_vagas = "\n".join([f"{numeros[i]} " for i in range(vagas)])
        
        texto = f"{bike} {grupo} {bike}\n\n{fogo} {tipo_pedal}\n\n📍 {destino}\n\n{calendario} {data_f}\n{relogio} {horario}\n{local_icon} {local}\n\nConfirmados:\n{lista_vagas}"
        
        st.text_area("Resultado:", texto, height=250)
        st_copy_to_clipboard(texto, "📋 Copiar para WhatsApp")
        
        link_wa = f"https://api.whatsapp.com/send?text={urllib.parse.quote(texto)}"
        st.markdown(f'<a href="{link_wa}" target="_blank"><button style="background-color:#25D366;color:white;padding:10px;border:none;border-radius:8px;cursor:pointer;width:100%">📲 Enviar Direto</button></a>', unsafe_allow_html=True)

# =========================
# PÁGINA 2: CALCULADORA DE ZONAS FC
# =========================
elif pagina == "Calculadora de Zonas FC":
    st.title("💓 Calculadora de Zonas (Joe Friel)")
    st.info("O LTHR (Limiar de Lactato) é a média da frequência cardíaca que você consegue manter em um esforço máximo constante de 30 a 60 minutos.")
    
    lthr = st.number_input("Informe seu LTHR (bpm):", min_value=100, max_value=220, value=160)
    metodo = st.selectbox("Número de Zonas:", [5, 7])
    
    if metodo == 5:
        zonas = {
            "Zona 1 (Recuperação)": (0, 0.81),
            "Zona 2 (Aeróbica)": (0.81, 0.90),
            "Zona 3 (Tempo)": (0.90, 0.94),
            "Zona 4 (Limiar)": (0.94, 1.00),
            "Zona 5 (VO2 Máx)": (1.00, 1.10)
        }
    else:
        zonas = {
            "Zona 1 (Recuperação Active)": (0, 0.81),
            "Zona 2 (Resistência Aeróbica)": (0.81, 0.90),
            "Zona 3 (Tempo)": (0.90, 0.94),
            "Zona 4 (Limiar de Lactato)": (0.94, 1.00),
            "Zona 5a (Super Limiar)": (1.00, 1.02),
            "Zona 5b (Capacidade Aeróbica)": (1.02, 1.06),
            "Zona 5c (Capacidade Anaeróbica)": (1.06, 1.15)
        }

    st.subheader(f"Suas Zonas para LTHR {lthr}")
    for nome, (mini, maxi) in zonas.items():
        st.write(f"**{nome}:** {int(lthr * mini)} - {int(lthr * maxi)} bpm")

    with st.expander("📖 Como configurar no Strava"):
        st.write("""
        1. Abra o app do **Strava** no celular.
        2. Vá em **Você** > **Perfil** > **Editar Perfil** (ou Configurações).
        3. Procure por **Zonas de Desempenho** ou **Minha Frequência Cardíaca**.
        4. Selecione **Frequência Cardíaca Personalizada**.
        5. Insira os valores calculados acima para cada zona.
        """)

# =========================
# PÁGINA 3: FERRAMENTA DE NUTRIÇÃO
# =========================
# --- Nova Lógica de Nutrição Refinada ---

elif pagina == "Ferramenta de Nutrição":
    st.title("🍌 Planejador de Nutrição de Precisão")
    
    colA, colB = st.columns(2)
    with colA:
        peso = st.number_input("Seu peso (kg):", 40, 150, 75)
        tipo_bike = st.radio("Modalidade:", ["Road (Asfalto/Ritmo)", "MTB (Trilha/Altimetria)"])
    with colB:
        duracao = st.selectbox("Duração do Pedal (horas):", list(range(1, 11)))
        # Substituímos a intensidade simples por algo que impacta o metabolismo
        clima = st.select_slider("Temperatura Ambiente:", ["Frio", "Agradável", "Muito Quente"])

    # --- CÁLCULOS TÉCNICOS ---
    
    # 1. Taxa de Oxidação de Carboidratos (g/kg/hora)
    # Road costuma ser mais constante (Z2/Z3), MTB tem picos de potência (Z4/Z5)
    taxa_carbo = 0.7 if "Road" in tipo_bike else 0.9
    
    # 2. Ajuste por Temperatura (Calor aumenta o consumo de glicogênio e água)
    ajuste_clima_agua = 1.0
    if clima == "Frio": ajuste_clima_agua = 0.8
    elif clima == "Muito Quente": ajuste_clima_agua = 1.3
    
    # 3. Resultado Final
    gramas_carbo_total = (peso * taxa_carbo) * duracao
    
    # Hidratação: Road (600ml base) | MTB (850ml base) -> Ajustado pelo clima
    base_hidrica = 600 if "Road" in tipo_bike else 850
    agua_ml_total = (base_hidrica * duracao) * ajuste_clima_agua
    
    # Conversão para Caramanholas (500ml)
    qtd_caramanholas = agua_ml_total / 500

    # --- EXIBIÇÃO ---
    st.subheader("📋 Plano de Suprimentos")
    
    # Itens de consumo
    qtd_geis = int((gramas_carbo_total * 0.5) / 20) # 50% em Gel
    qtd_bananas = int((gramas_carbo_total * 0.5) / 25) # 50% em Alimento Sólido
    
    st.success(f"Estimativa de consumo total: **{int(gramas_carbo_total)}g de Carboidratos**")

    c1, c2, c3 = st.columns(3)
    c1.metric("Hidratação", f"{qtd_caramanholas:.1f} un.", help="Caramanholas de 500ml")
    c2.metric("Géis de Carbo", f"{max(1, qtd_geis)} un.", help="Géis de 20g cada")
    c3.metric("Bananas", f"{max(1, qtd_bananas)} un.", help="Ou 5 balas de goma por cada banana")

    st.info(f"💡 **Dica de Pro:** No **{tipo_bike.split()[0]}**, tente consumir 1/3 da hidratação com eletrólitos (sais) para evitar cãibras, especialmente no clima **{clima.lower()}**.")
