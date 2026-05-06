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
        vagas = st.selectbox("Vagas", list(range(1, 31)))

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
elif pagina == "Ferramenta de Nutrição":
    st.title("🍌 Planejador de Nutrição")
    
    colA, colB = st.columns(2)
    with colA:
        peso = st.number_input("Seu peso (kg):", 40, 150, 75)
        tipo_bike = st.radio("Modalidade:", ["MTB (Mais esforço/Altimetria)", "Road (Ritmo constante)"])
    with colB:
        duracao = st.selectbox("Duração do Pedal (horas):", list(range(1, 11)))
        intensidade = st.select_slider("Intensidade esperada:", ["Leve", "Moderada", "Intensa"])

    # Lógica de Cálculo (Fórmulas fisiológicas)
    # Recomendação base: 30g a 90g de carbo/hora dependendo do peso e intensidade
    carbo_base = 0.8 if tipo_bike == "Road" else 1.0
    if intensidade == "Leve": carbo_base *= 0.6
    elif intensidade == "Intensa": carbo_base *= 1.2
    
    gramas_carbo_total = (peso * carbo_base) * duracao
    agua_ml_total = duracao * 600 if tipo_bike == "Road" else duracao * 800

    st.subheader("📋 Recomendação de Suprimentos")
    
    # Divisão sugerida de alimentos
    # Cada Gel = 20g carbo | 1 Banana = 25g carbo | 5 Balas de Goma = 20g carbo
    qtd_geis = int((gramas_carbo_total * 0.4) / 20)
    qtd_bananas = int((gramas_carbo_total * 0.3) / 25)
    qtd_balas = int((gramas_carbo_total * 0.3) / 4) # 4g por bala

    st.success(f"Para um pedal de {duracao}h, você precisará de aproximadamente **{int(gramas_carbo_total)}g de Carboidratos**.")
    
    c1, c2, c3 = st.columns(3)
    qtd_caramanholas = math.ceil(agua_ml_total / 500)
    c1.metric("Hidratação", f"{qtd_caramanholas} un. (Caramanholas)")
    c2.metric("Géis de Carbo (20G de carboidrato)", f"{max(1, qtd_geis)} un")
    c3.metric("Bananas/Bala de Goma (25G de carboidrato)", f"{max(1, qtd_bananas)} un")
    
    st.warning(f"**Sugestão de Consumo:** Coma algo a cada 40 minutos. Não espere sentir sede ou fome.")
    
    with st.expander("🔬 Detalhes do Cálculo"):
        st.write(f"- **Hidratação:** Baseada em uma perda média de 600-800ml/h.")
        st.write(f"- **Carboidratos:** Calculado em {carbo_base*peso:.1f}g/hora para seu perfil.")
        st.write("- **Dica:** Em pedais de MTB, a altimetria exige mais glicogênio; priorize o Gel em subidas longas.")
