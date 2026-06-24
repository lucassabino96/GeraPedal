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
    st.title("🍌 Planejador de Nutrição Prático")
    
    colA, colB = st.columns(2)
    with colA:
        peso = st.number_input("Seu peso (kg):", 40.0, 150.0, 75.0)
        tipo_bike = st.radio("Modalidade:", ["Road (Asfalto/Ritmo)", "MTB (Trilha/Altimetria)"])
    with colB:
        duracao = st.selectbox("Duração do Pedal (horas):", list(range(1, 11)))
        clima = st.select_slider("Temperatura Ambiente:", ["Frio", "Agradável", "Muito Quente"])

    # --- CÁLCULOS CONSERVADORES (Baseados em dados reais do ciclista) ---
    
    # 1. Hidratação (Base 500ml/hora)
    # Frio reduz um pouco a perda, muito quente aumenta a necessidade de água.
    ajuste_clima_agua = 0.8 if clima == "Frio" else (1.2 if clima == "Muito Quente" else 1.0)
    agua_ml_total = (500 * duracao) * ajuste_clima_agua
    
    # 2. Carboidratos (Reposição APENAS após a 1ª hora)
    # Base de ~50g/hora. Ajustamos levemente de acordo com o peso e modalidade para manter a ferramenta dinâmica.
    horas_reposicao_carbo = max(0, duracao - 1)
    fator_esforco = 1.1 if "MTB" in tipo_bike else 1.0 
    
    # Cálculo dinâmico que vai girar em torno de 50g para um ciclista de 75kg
    carbo_por_hora = 50 * (peso / 75.0) * fator_esforco
    gramas_carbo_total = carbo_por_hora * horas_reposicao_carbo
    
    # 3. Sódio (Reposição baseada em todo o tempo de atividade, suando desde o início)
    # Média conservadora de 400mg de sódio por hora de pedal.
    sodio_mg_total = (400 * duracao) * ajuste_clima_agua

    # --- EXIBIÇÃO PRINCIPAL ---
    st.subheader("📋 Necessidades Totais do Pedal")
    
    if horas_reposicao_carbo == 0:
        st.success("Para pedais de até 1 hora, os estoques do próprio corpo dão conta. Foco apenas na hidratação! 💧")
        
    c1, c2, c3 = st.columns(3)
    c1.metric("Água", f"{int(agua_ml_total)} ml")
    c2.metric("Carboidratos", f"{int(gramas_carbo_total)} g")
    c3.metric("Sódio", f"{int(sodio_mg_total)} mg")

    # --- SUGESTÕES DE DISTRIBUIÇÃO ---
    if horas_reposicao_carbo > 0:
        st.subheader("💡 Como distribuir isso na prática?")
        st.markdown(f"Você tem **{horas_reposicao_carbo} hora(s)** de reposição de carboidrato. "
                    f"A meta é consumir aprox. **{int(carbo_por_hora)}g por hora**. Escolha uma das estratégias abaixo para cada hora:")
        
        tab1, tab2, tab3 = st.tabs(["⚡ Géis + Gomets", "🍌 Banana + Gomets", "💰 Kit Low Cost"])
        
        with tab1:
            st.markdown("""
            **Estratégia Mista:**
            * 1 Gel de Carboidrato (aprox. 20g a 25g de carbo)
            * 1 Porção de Gomets/Jujubas (aprox. 25g a 30g de carbo)
            """)
        with tab2:
            st.markdown("""
            **Sólido + Balas:**
            * 1 Banana Média (aprox. 20g a 25g de carbo)
            * 1 Porção de Gomets/Jujubas (aprox. 25g a 30g de carbo)
            """)
        with tab3:
            st.markdown("""
            **Maltodextrina + Mel:**
            * 30g de Maltodextrina (diluída na garrafa de água)
            * 1 sachê ou colher de sopa cheia de Mel (aprox. 20g de carbo)
            """)

    # --- REPOSIÇÃO DE SÓDIO ---
    st.subheader("🧂 Reposição de Sódio")
    
    # Cálculos aproximados para exibição
    capsulas = max(1, int(sodio_mg_total / 150)) # Média de 150mg de sódio por cápsula manipulada
    pitadas = max(1, int(sodio_mg_total / 300))  # Média de 300mg de sódio por pitada/pacotinho de sal
    
    st.info(f"Para atingir a meta de **{int(sodio_mg_total)}mg** de sódio durante o pedal, você pode fracionar e utilizar:\n"
            f"\n💊 **Cápsulas de Farmácia:** ~{capsulas} cápsula(s) ao longo do treino (considerando cápsulas padrão de 150mg).\n"
            f"\n🧂 **Sal de Cozinha:** ~{pitadas} pitada(s) ou sachês pequenos de sal (diluídos na água ou colocados na banana).")
