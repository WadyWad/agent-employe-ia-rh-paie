import streamlit as st
from openai import OpenAI

# Configuration page
st.set_page_config(page_title="Agent Employé IA", page_icon="🤖")

# Vérification clé API
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Clé API manquante. Vérifiez la configuration.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Interface
st.title("🤖 Agent Employé IA – Assistant RH / Paie")

st.info(
    "Exemples : 'Pourquoi mon salaire a baissé ?' • "
    "'Je veux une attestation employeur' • "
    "'Je pense qu’il y a une erreur sur mon bulletin'"
)

st.markdown("Posez votre question ou choisissez une action 👇")

# Boutons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Comprendre mon bulletin"):
        st.session_state["pending_input"] = "Pourquoi mon salaire a baissé ce mois-ci ?"

with col2:
    if st.button("📑 Demander une attestation"):
        st.session_state["pending_input"] = "Je veux une attestation employeur"

with col3:
    if st.button("⚠️ Signaler une anomalie"):
        st.session_state["pending_input"] = "Je pense qu’il y a une erreur sur mon bulletin"

# Mémoire
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input utilisateur
user_input = st.chat_input("Posez votre question RH / paie...")

# Gestion boutons
if "pending_input" in st.session_state:
    user_input = st.session_state["pending_input"]
    del st.session_state["pending_input"]

# IA
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):

            try:
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=[
                        {
                            "role": "system",
                            "content": """Tu es un assistant RH / paie expert.

Tu dois :
- répondre en français
- être clair et simple
- vulgariser les termes paie
- proposer des actions concrètes
- ne jamais inventer
- demander des précisions si nécessaire"""
                        },
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                )

                answer = response.output[0].content[0].text

            except Exception:
                answer = (
                    "Le moteur IA est temporairement indisponible. "
                    "Merci de réessayer dans quelques instants."
                )

            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})