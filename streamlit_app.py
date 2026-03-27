import re
import unicodedata
import streamlit as st

st.set_page_config(
    page_title="Agent Employé IA",
    page_icon="🤖",
    layout="centered"
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 900px;
}
.hero {
    background: linear-gradient(135deg, #0f62fe 0%, #6ea8fe 100%);
    color: white;
    padding: 22px 24px;
    border-radius: 18px;
    margin-bottom: 16px;
}
.hero h1 {
    margin: 0;
    font-size: 2.1rem;
    line-height: 1.1;
}
.hero p {
    margin: 8px 0 0 0;
    opacity: 0.95;
}
.card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.answer-card {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-left: 5px solid #0f62fe;
    border-radius: 16px;
    padding: 16px 18px;
    margin-top: 8px;
    margin-bottom: 16px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}
.topic-tag {
    display: inline-block;
    background: #eef4ff;
    color: #0f62fe;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 8px;
}
.small-muted {
    color: #6c757d;
    font-size: 0.92rem;
}
.suggestions {
    background: #f8f9fa;
    border-radius: 14px;
    padding: 12px;
    border: 1px dashed #d0d7de;
}
div[data-testid="stChatMessage"] {
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🤖 Agent Employé IA</h1>
  <p>Assistant RH / Paie basé sur votre FAQ interne</p>
</div>
""", unsafe_allow_html=True)

# =========================
# FAQ STRUCTURÉE
# =========================
FAQ = [
    {
        "topic": "Maladie",
        "patterns": [
            r"\bmaladie\b", r"\barret\b", r"\barr[eê]t\b", r"\bijss\b",
            r"\bcarence\b", r"\bsubrogation\b", r"\bsalaire.*baisse\b",
            r"\bbaisse.*salaire\b", r"\babsence.*maladie\b", r"\bsecurite sociale\b",
            r"\bs[eé]curit[eé] sociale\b", r"\bmaintien de salaire\b"
        ],
        "examples": [
            "Pourquoi mon salaire a baissé après un arrêt maladie ?",
            "C’est quoi la subrogation ?",
            "Est-ce qu’il y a 3 jours de carence ?"
        ],
        "answer": """En cas d’arrêt maladie, le salaire peut baisser car l’absence est déduite de la paie. La Sécurité sociale peut verser des indemnités journalières, généralement avec 3 jours de carence, sauf exceptions. Selon l’ancienneté, il peut aussi y avoir un maintien de salaire ou un complément de prévoyance.

En clair :
- absence maladie = déduction sur la paie ;
- IJSS = versement par la Sécurité sociale ;
- carence = possible sur les premiers jours ;
- maintien / complément = selon ancienneté et règles applicables.

Si vous voulez, je peux aussi vous répondre plus précisément sur :
- la subrogation ;
- les 3 jours de carence ;
- ou le maintien de salaire."""
    },
    {
        "topic": "Enfant malade",
        "patterns": [
            r"\benfant malade\b", r"\bconge enfant malade\b", r"\bcong[eé] enfant malade\b"
        ],
        "examples": [
            "Combien de jours enfant malade ai-je ?",
            "Les jours enfant malade sont-ils payés ?"
        ],
        "answer": """Les congés enfant malade sont calculés sur l’année civile, du 1er janvier au 31 décembre.

En résumé :
- 3 jours par an pour un enfant de moins de 16 ans ;
- 5 jours par an si l’enfant a moins d’1 an ou si vous avez 3 enfants de moins de 16 ans ;
- moins de 12 mois d’ancienneté : jours non payés ;
- plus de 12 mois d’ancienneté : jours payés.

Si le compteur est épuisé, une journée supplémentaire peut exister sous conditions et avec justificatif."""
    },
    {
        "topic": "Jour décès",
        "patterns": [
            r"\bd[eé]c[eè]s\b", r"\bacte de deces\b", r"\bacte de décès\b",
            r"\blivret de famille\b", r"\bjour deces\b", r"\bconge deces\b", r"\bcong[eé] d[eé]c[eè]s\b"
        ],
        "examples": [
            "Pourquoi faut-il le livret de famille en plus de l’acte de décès ?",
            "Combien de jours ai-je en cas de décès ?"
        ],
        "answer": """En cas de décès, le livret de famille peut être demandé en plus de l’acte de décès pour prouver le lien de filiation. Le nombre de jours dépend du lien familial.

Repères :
- 7 jours : enfant ou personne à charge effective et permanente ;
- 5 jours : père, mère, conjoint, concubin ou partenaire PACS ;
- 3 jours : frère, sœur, beau-père ou belle-mère ;
- 1 jour : autre ascendant que père ou mère.

Ces jours sont à prendre dans un délai raisonnable, en principe dans le mois qui suit."""
    },
    {
        "topic": "Mariage / PACS",
        "patterns": [
            r"\bmariage\b", r"\bpacs\b", r"\bpacser\b", r"\bconge mariage\b", r"\bcong[eé] mariage\b"
        ],
        "examples": [
            "J’ai droit à combien de jours pour mon PACS ?",
            "Quand puis-je prendre mon congé mariage ?"
        ],
        "answer": """Le mariage ou le PACS ouvre droit à une absence exceptionnelle, sans condition d’ancienneté.

En pratique :
- salarié : 6 jours ouvrés consécutifs ;
- enfant du salarié : 1 jour ouvré.

Le congé peut être pris le jour de l’événement ou dans un délai raisonnable avant ou après, en principe dans le mois qui suit."""
    },
    {
        "topic": "Mutuelle",
        "patterns": [
            r"\bmutuelle\b", r"\bcompl[eé]mentaire sant[eé]\b", r"\bdispense\b", r"\baffiliation\b"
        ],
        "examples": [
            "Je n’ai pas répondu au mail de mutuelle, que se passe-t-il ?",
            "La mutuelle est-elle obligatoire ?"
        ],
        "answer": """La mutuelle d’entreprise est en principe obligatoire, sauf cas de dispense prévus.

Fonctionnement :
- à l’embauche, vous êtes inscrit par défaut ;
- environ 15 à 20 jours après votre arrivée, vous recevez un mail pour compléter votre affiliation ;
- vous avez 2 mois pour finaliser l’affiliation ;
- vous pouvez ensuite demander une dispense ou souscrire à des options complémentaires.

Si la mutuelle transmet tardivement une information, une régularisation peut être faite sur la paie."""
    },
    {
        "topic": "Acompte",
        "patterns": [
            r"\bacompte\b", r"\bavance sur salaire\b", r"\bavance\b"
        ],
        "examples": [
            "Puis-je demander un acompte ?",
            "Y a-t-il des avances sur salaire ?"
        ],
        "answer": """Aucune avance sur salaire n’est accordée.

En revanche, un acompte peut être demandé si vous avez déjà effectué les heures correspondant au montant demandé. La demande se fait via Mon Portail Paie."""
    },
    {
        "topic": "Heures supplémentaires / complémentaires",
        "patterns": [
            r"\bheures\b", r"\bheures supplementaires\b", r"\bheures supplémentaires\b",
            r"\bheures complementaires\b", r"\bheures complémentaires\b",
            r"\breleve d heures\b", r"\brelev[eé] d'?heures\b"
        ],
        "examples": [
            "Pourquoi mes heures ne sont pas sur ma paie ?",
            "J’ai envoyé mon relevé d’heures, pourquoi je ne vois rien ?"
        ],
        "answer": """Si vos heures en plus n’apparaissent pas encore sur votre bulletin, cela peut être normal.

Circuit habituel :
- le salarié effectue les heures ;
- le manager les transmet au service RH ;
- le service RH les transmet à la paie ;
- si la transmission est faite avant le 15, elles peuvent être traitées sur la paie du mois ;
- si elle est faite après le 15, elles passent en paie M+1.

Donc, l’absence de ligne sur le bulletin ne signifie pas forcément un oubli."""
    },
    {
        "topic": "Primes",
        "patterns": [
            r"\bprime\b", r"\bprimes\b", r"\bprime objectif\b", r"\bobjectif\b"
        ],
        "examples": [
            "Pourquoi ma prime n’est pas du bon montant ?",
            "La paie calcule-t-elle les primes ?"
        ],
        "answer": """Le service paie ne calcule pas les primes. Le montant est transmis par le service RH, en lien avec le manager, puis appliqué tel qu’il est communiqué.

Si vous pensez qu’il y a une erreur, la première vérification doit se faire sur le montant validé côté RH / management."""
    },
    {
        "topic": "Télétravail",
        "patterns": [
            r"\bt[eé]l[eé]travail\b", r"\ballocation t[eé]l[eé]travail\b",
            r"\b20 euros\b", r"\b20€\b", r"\bavenant\b", r"\bassurance habitation\b"
        ],
        "examples": [
            "Pourquoi je n’ai pas la ligne télétravail ?",
            "Quels documents faut-il pour l’allocation télétravail ?"
        ],
        "answer": """Pour bénéficier de l’allocation forfaitaire télétravail, le dossier doit être complet.

Il faut :
- un avenant télétravail signé ;
- une attestation d’assurance habitation en cours de validité ;
- l’assurance doit être transmise chaque année.

Une fois les éléments transmis par les RH à la paie, l’allocation peut être mise en place."""
    },
    {
        "topic": "Tickets restaurant",
        "patterns": [
            r"\bticket restaurant\b", r"\btickets restaurant\b", r"\btr\b", r"\bedenred\b", r"\bcarte tr\b"
        ],
        "examples": [
            "Combien de tickets restaurant ai-je ?",
            "Pourquoi je n’ai pas reçu ma carte Edenred ?"
        ],
        "answer": """Pour les tickets restaurant :
- vous avez droit à 1 ticket restaurant par journée travaillée ;
- la journée doit être d’au moins 6 heures ;
- elle doit inclure une pause d’au moins 30 minutes entre 12h00 et 14h00 ;
- la déclaration doit être faite via Mon Portail Paie avant le 20 du mois.

Si la carte n’a pas été reçue, il peut être nécessaire de contacter directement Edenred."""
    },
    {
        "topic": "Transport / Navigo",
        "patterns": [
            r"\btransport\b", r"\bnavigo\b", r"\bratp\b", r"\bremboursement transport\b", r"\bpass navigo\b"
        ],
        "examples": [
            "Comment demander le remboursement transport ?",
            "Quels justificatifs faut-il pour le Navigo ?"
        ],
        "answer": """Le remboursement des frais de transport à hauteur de 50 % se demande sur Mon Portail Paie.

La demande doit comporter, en un seul fichier :
- une attestation sur l’honneur signée ;
- un justificatif de paiement ;
- une copie du pass Navigo.

Seuls les abonnements hebdomadaires, mensuels et annuels sont pris en charge. Le Navigo Liberté+ et les tickets à l’unité ne sont pas remboursés."""
    },
    {
        "topic": "Période de gel",
        "patterns": [
            r"\bgel\b", r"\bp[eé]riode de gel\b", r"\b20 au 7\b", r"\bremonte\b", r"\bremont[eé]e\b"
        ],
        "examples": [
            "C’est quoi la période de gel ?",
            "Pourquoi ma demande ne remonte pas sur la paie ?"
        ],
        "answer": """La période de gel signifie qu’il n’y a plus d’échange entre le portail paie et le logiciel de paie.

Elle a lieu chaque mois entre le 20 et le 7 du mois suivant.

Pendant cette période :
- vous pouvez continuer à faire vos demandes ;
- elles ne remontent pas immédiatement en paie ;
- elles sont prises en compte sur la période suivante."""
    },
    {
        "topic": "Arkevia - activation",
        "patterns": [
            r"\barkevia\b", r"\bcoffre fort\b", r"\bcoffre-fort\b", r"\bactivation\b", r"\bactiver\b"
        ],
        "examples": [
            "Comment activer Arkevia ?",
            "Comment accéder à mon coffre-fort ?"
        ],
        "answer": """Pour activer votre coffre-fort Arkevia :
1. Accédez à Arkevia via OneLogin ou myarkevia.com ;
2. cliquez sur “Je m’inscris” ;
3. renseignez votre matricule et votre code secret reçus par mail ;
4. renseignez votre nom, prénom et votre adresse email personnelle ;
5. choisissez votre mot de passe et validez.

L’adresse email personnelle est importante car elle permet de conserver l’accès pendant 50 ans."""
    },
    {
        "topic": "Arkevia - connexion",
        "patterns": [
            r"\bmot de passe oubli[eé]\b", r"\bconnexion arkevia\b", r"\bse connecter arkevia\b"
        ],
        "examples": [
            "J’ai oublié mon mot de passe Arkevia",
            "Comment me connecter à Arkevia ?"
        ],
        "answer": """Pour vous connecter à Arkevia :
- utilisez votre adresse email personnelle renseignée lors de l’activation ;
- puis le mot de passe choisi lors de l’inscription.

Si vous avez oublié votre mot de passe, utilisez le lien “Mot de passe oublié ?”. Un email de réinitialisation sera envoyé sur votre adresse personnelle."""
    },
    {
        "topic": "Portail paie",
        "patterns": [
            r"\bportail paie\b", r"\bmon portail paie\b", r"\bone login\b", r"\bonelogin\b"
        ],
        "examples": [
            "Comment faire une demande sur Mon Portail Paie ?",
            "Je ne vois pas la tuile Mon Portail Paie"
        ],
        "answer": """Mon Portail Paie sert à effectuer plusieurs démarches RH / paie, comme les demandes d’acompte, certaines absences, le transport ou les titres restaurant selon les cas.

Si vous n’avez pas accès à la tuile, il faut généralement vous rapprocher de votre manager et du support informatique."""
    },
]

FALLBACK_QUESTIONS = [
    "Pourquoi mon salaire a baissé après une absence maladie ?",
    "Comment demander un acompte ?",
    "Pourquoi mes heures ne sont pas sur ma paie ?",
    "Comment activer Arkevia ?",
    "Quels justificatifs faut-il pour le remboursement transport ?",
    "Pourquoi ma demande ne remonte pas sur la paie ?",
]

# =========================
# OUTILS
# =========================
def normalize(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def strong_bonus(q: str, patt: str) -> int:
    try:
        if re.search(patt, q):
            return 8
    except re.error:
        pass
    return 0

def word_overlap_score(q: str, topic: str, examples: list[str]) -> int:
    q_words = set(normalize(q).split())
    topic_words = set(normalize(topic).split())
    score = len(q_words.intersection(topic_words))

    for ex in examples:
        ex_words = set(normalize(ex).split())
        score += len(q_words.intersection(ex_words)) // 2

    return score

def classify_question(question: str):
    q = normalize(question)
    scored = []

    for item in FAQ:
        score = 0
        for patt in item["patterns"]:
            score += strong_bonus(q, normalize(patt))
        score += word_overlap_score(q, item["topic"], item["examples"])
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best_item = scored[0]
    return best_score, best_item, scored[:3]

def build_response(question: str):
    score, best, top3 = classify_question(question)

    if score < 4:
        return {
            "found": False,
            "topic": "Question non reconnue clairement",
            "answer": "Je n’ai pas trouvé de réponse suffisamment fiable dans la FAQ. Reformulez votre question avec des mots plus précis, par exemple : maladie, mutuelle, acompte, heures, transport, Arkevia, télétravail.",
            "suggestions": FALLBACK_QUESTIONS
        }

    suggestions = []
    for _, item in top3[1:]:
        if item["examples"]:
            suggestions.append(item["examples"][0])

    return {
        "found": True,
        "topic": best["topic"],
        "answer": best["answer"],
        "suggestions": suggestions[:2]
    }

# =========================
# BARRE DE RACCOURCIS
# =========================
st.markdown('<div class="card"><div class="small-muted">Raccourcis</div></div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("💸 Salaire en baisse", use_container_width=True):
        st.session_state["pending_input"] = "Pourquoi mon salaire a baissé après une absence maladie ?"
with c2:
    if st.button("📁 Arkevia", use_container_width=True):
        st.session_state["pending_input"] = "Comment activer Arkevia ?"
with c3:
    if st.button("⏱️ Heures", use_container_width=True):
        st.session_state["pending_input"] = "Pourquoi mes heures ne sont pas sur ma paie ?"
with c4:
    if st.button("🚆 Transport", use_container_width=True):
        st.session_state["pending_input"] = "Quels justificatifs faut-il pour le remboursement Navigo ?"

# =========================
# ÉTAT
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# AFFICHAGE HISTORIQUE
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and isinstance(msg["content"], dict):
            data = msg["content"]
            st.markdown(f'<div class="topic-tag">{data["topic"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="answer-card">{data["answer"]}</div>', unsafe_allow_html=True)
            if data.get("suggestions"):
                st.markdown('<div class="suggestions"><b>Questions proches :</b></div>', unsafe_allow_html=True)
                for s in data["suggestions"]:
                    st.write(f"• {s}")
        else:
            st.write(msg["content"])

# =========================
# INPUT
# =========================
user_input = st.chat_input("Posez votre question RH / paie...")

if "pending_input" in st.session_state:
    user_input = st.session_state["pending_input"]
    del st.session_state["pending_input"]

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    result = build_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": result})

    st.rerun()
    