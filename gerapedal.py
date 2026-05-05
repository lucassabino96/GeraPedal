import streamlit as st

st.set_page_config(page_title="Pedal Generator", page_icon="🚴")

st.title("🚴 Gerador de Pedal")

grupo = st.selectbox("Grupo", ["Gigantes do Pedal", "Domingão", "Pelotão Raiz"])
destino = st.text_input("Destino da rota")
horario = st.text_input("Horário de saída", "06:00")
local = st.text_input("Local de saída")
vagas = st.number_input("Número de vagas", min_value=1, max_value=50, value=10)

nomes = st.text_area("Lista de confirmados (um por linha)")

if st.button("Gerar texto"):
    lista = nomes.split("\n")
    lista_formatada = "\n".join([f"{i+1}️⃣ {nome}" for i, nome in enumerate(lista) if nome.strip() != ""])

    texto = f"""🚴‍♂️ {grupo} 🚴‍♂️

📍 {destino}

⏰ {horario}
📌 {local}

Vagas: {vagas}

Confirmados:
{lista_formatada}
"""

    st.text_area("Resultado", texto, height=300)
