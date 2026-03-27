import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Agent Employé IA", page_icon="🤖")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🤖 Agent Employé IA – Assistant RH / Paie")
st.info(
    "Exemples : 'Pourquoi mon salaire a baissé ?' • "
    "'Je veux une attestation employeur' • "
    "'Je pense qu’il y a une erreur sur mon bulletin'"
)

st.markdown("Posez votre question ou choisissez une action 👇")

# Boutons rapides
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

SYSTEM_PROMPT = """
Tu es un assistant RH / paie destiné aux employés.

Règles :
- Réponds en français.
- Sois clair, simple, professionnel et rassurant.
- Vulgarise les termes paie.
- N’invente jamais d’informations internes.
- Si une information manque, dis-le clairement.
- Propose toujours une prochaine étape utile.
- Si la demande concerne une anomalie, demande :
  1. le mois concerné
  2. la ligne concernée
  3. la différence constatée
- Si la demande concerne une attestation, demande le type exact.
- Si la demande concerne une variation de paie, évoque seulement les causes probables :
  absence, prime, régularisation, acompte, cotisations.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Posez votre question RH / paie...")

if "pending_input" in st.session_state:
    user_input = st.session_state["pending_input"]
    del st.session_state["pending_input"]

def build_messages(history, latest_user_message):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": latest_user_message})
    return messages

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=build_messages(st.session_state.messages[:-1], user_input),
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = (
                    "Je n’ai pas pu contacter le moteur IA pour le moment. "
                    f"Erreur : {e}"
                )

            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})