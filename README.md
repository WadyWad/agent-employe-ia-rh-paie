import streamlit as st

st.set_page_config(page_title="Agent Employé IA", page_icon="🤖")

st.title("🤖 Agent Employé IA – Assistant RH / Paie")

st.markdown("Posez votre question ou choisissez une action 👇")

# Boutons (effet WOW)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Comprendre mon bulletin"):
        st.session_state["input"] = "Je ne comprends pas mon bulletin"

with col2:
    if st.button("📑 Demander une attestation"):
        st.session_state["input"] = "Je veux une attestation"

with col3:
    if st.button("⚠️ Signaler une anomalie"):
        st.session_state["input"] = "Je pense qu'il y a une erreur"

# Historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input utilisateur
user_input = st.chat_input("Posez votre question RH / paie...")

if "input" in st.session_state:
    user_input = st.session_state["input"]
    del st.session_state["input"]

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Réponses intelligentes simulées
    if "bulletin" in user_input.lower():
        response = "Votre bulletin de paie peut varier en fonction des absences, primes ou cotisations. Si vous le souhaitez, je peux analyser une ligne précise pour vous."
    
    elif "attestation" in user_input.lower():
        response = "Je peux vous aider à générer votre attestation. Merci de préciser le type de document souhaité (employeur, salaire, etc.)."
    
    elif "erreur" in user_input.lower() or "anomalie" in user_input.lower():
        response = "Je peux vous aider à signaler une anomalie. Pouvez-vous préciser la ligne ou le montant concerné afin que je vérifie ?"
    
    else:
        response = "Je suis votre assistant RH. Je peux vous aider à comprendre votre bulletin, faire une demande ou répondre à vos questions."

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)