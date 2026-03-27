import re
import unicodedata
import streamlit as st

st.set_page_config(page_title="Agent Employé IA", page_icon="🤖")

st.title("🤖 Agent Employé IA – Assistant RH / Paie")
st.info(
    "Exemples : 'Pourquoi mon salaire a baissé ?' • "
    "'Je veux une attestation employeur' • "
    "'Comment activer Arkevia ?' • "
    "'Pourquoi mes heures ne sont pas sur ma paie ?'"
)

st.markdown("Posez votre question ou choisissez une action 👇")

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

# =========================
# BASE FAQ
# =========================
FAQ_ENTRIES = [
    {
        "title": "Maladie - baisse de salaire / IJSS / carence",
        "keywords": [
            "maladie", "arret", "arrêt", "ijss", "securite sociale", "sécurité sociale",
            "carence", "salaire baisse", "bulletin baisse", "absence maladie", "subrogation"
        ],
        "answer": """Une baisse de salaire peut s’expliquer par une absence maladie.

En pratique :
- l’absence maladie entraîne une déduction du salaire ;
- la Sécurité sociale peut verser des indemnités journalières ;
- les 3 premiers jours de l’arrêt correspondent en principe à des jours de carence, sauf exceptions ;
- selon votre ancienneté, il peut aussi y avoir un maintien de salaire ou un complément via la prévoyance.

Autrement dit, une différence temporaire entre votre salaire habituel et votre paie du mois peut être normale en cas d’arrêt maladie.

Si vous le souhaitez, je peux aussi vous expliquer :
- la subrogation ;
- le maintien de salaire ;
- ou la différence entre salaire brut, IJSS et prévoyance."""
    },
    {
        "title": "Subrogation",
        "keywords": ["subrogation", "ijss employeur", "indemnites journalières employeur", "indemnites journalières"],
        "answer": """La subrogation signifie que l’employeur continue de verser tout ou partie du salaire pendant l’arrêt, puis perçoit directement les indemnités journalières de la Sécurité sociale à votre place.

Concrètement :
- vous n’avez pas nécessairement les IJSS versées directement sur votre compte ;
- elles peuvent être perçues par l’employeur ;
- cela permet de simplifier le maintien de votre rémunération pendant l’arrêt."""
    },
    {
        "title": "Enfant malade",
        "keywords": ["enfant malade", "conge enfant malade", "congé enfant malade", "jour enfant malade"],
        "answer": """Les congés enfant malade sont calculés sur l’année civile, du 1er janvier au 31 décembre.

En résumé :
- 3 jours par an pour un enfant de moins de 16 ans ;
- 5 jours par an si l’enfant a moins d’1 an ou si vous avez 3 enfants de moins de 16 ans ;
- si vous avez moins de 12 mois d’ancienneté, les jours sont non payés ;
- si vous avez plus de 12 mois d’ancienneté, les jours sont payés.

Si votre compteur est épuisé, une journée supplémentaire peut exister sous certaines conditions et avec justificatif."""
    },
    {
        "title": "Jour décès",
        "keywords": ["deces", "décès", "livret de famille", "acte de deces", "conge deces", "congé décès"],
        "answer": """En cas de décès, un justificatif est nécessaire. Le livret de famille peut être demandé en complément de l’acte de décès pour prouver le lien de filiation.

Le nombre de jours dépend du lien familial :
- 7 jours : enfant ou personne à charge effective et permanente ;
- 5 jours : père, mère, conjoint, concubin ou partenaire PACS ;
- 3 jours : frère, sœur, beau-père ou belle-mère ;
- 1 jour : autre ascendant que père ou mère.

Ces jours doivent être pris dans un délai raisonnable, en principe dans le mois qui suit."""
    },
    {
        "title": "Mariage / PACS",
        "keywords": ["mariage", "pacs", "pacser", "conge mariage", "congé mariage", "conge pacs", "congé pacs"],
        "answer": """Le mariage ou le PACS ouvre droit à une absence exceptionnelle, sans condition d’ancienneté.

En pratique :
- salarié : 6 jours ouvrés consécutifs ;
- enfant du salarié : 1 jour ouvré.

Le congé peut être pris le jour de l’événement ou dans un délai raisonnable avant ou après, en principe dans le mois qui suit."""
    },
    {
        "title": "Jours de révision",
        "keywords": ["revision", "révision", "examen", "apprenti", "conge examen", "congé examen"],
        "answer": """Pour les jours de révision :
- un apprenti bénéficie de 5 jours ouvrés rémunérés supplémentaires dans le mois précédant les épreuves ;
- un salarié non apprenti peut bénéficier, sous conditions, de 3 jours ouvrables rémunérés pour un examen universitaire ou professionnel, avec convocation et sous réserve d’une ancienneté minimale de 3 ans."""
    },
    {
        "title": "Congés payés / CP acquis / CP en cours",
        "keywords": ["conges payes", "congés payés", "cp acquis", "cp en cours", "30 jours de cp", "jours exceptionnels"],
        "answer": """En principe :
- vous acquérez 25 jours ouvrés de congés légaux par an ;
- s’y ajoutent 5 jours ouvrés mobiles conventionnels.

C’est pourquoi vous pouvez voir 30 jours sur le bulletin.

Différence importante :
- CP acquis = congés déjà acquis sur la période précédente ;
- CP en cours = congés en cours d’acquisition sur la période actuelle.

Le “jour exceptionnel” correspond à une journée particulière gérée séparément dans le compteur."""
    },
    {
        "title": "Mutuelle",
        "keywords": ["mutuelle", "complementaire sante", "complémentaire santé", "dispense mutuelle", "affiliation mutuelle"],
        "answer": """La mutuelle d’entreprise est en principe obligatoire, sauf cas de dispense prévus.

Fonctionnement :
- à l’embauche, vous êtes inscrit par défaut ;
- environ 15 à 20 jours après votre arrivée, vous recevez un mail pour compléter votre affiliation ;
- vous avez 2 mois pour finaliser votre affiliation ;
- ensuite, vous pouvez demander une dispense ou souscrire à des options complémentaires.

Si la mutuelle transmet tardivement une information, une régularisation positive ou négative peut être faite sur la paie."""
    },
    {
        "title": "Acompte / avance sur salaire",
        "keywords": ["acompte", "avance sur salaire", "avance", "demande acompte"],
        "answer": """Aucune avance sur salaire n’est accordée.

En revanche, un acompte peut être demandé si vous avez déjà réalisé les heures correspondant au montant demandé.

Les demandes d’acompte se font via Mon Portail Paie. Elles doivent être faites dans les délais indiqués sur le portail."""
    },
    {
        "title": "Heures supplémentaires / complémentaires",
        "keywords": ["heures supplementaires", "heures supplémentaires", "heures complementaires", "heures complémentaires", "releve d heures", "relevé d'heures", "heures en plus"],
        "answer": """Si vos heures en plus n’apparaissent pas encore sur votre bulletin, cela peut être normal.

Le circuit est le suivant :
- le salarié effectue les heures ;
- le manager transmet les heures au service RH ;
- le service RH les transmet à la paie ;
- si la transmission est faite avant le 15 du mois, elles peuvent être traitées sur la paie du mois ;
- si la transmission est faite après le 15, elles sont traitées sur la paie du mois suivant.

Autrement dit, une absence de ligne sur le bulletin ne signifie pas forcément un oubli."""
    },
    {
        "title": "Primes",
        "keywords": ["prime", "primes", "prime objectif", "montant prime"],
        "answer": """Le service paie n’effectue pas le calcul des primes.

Le montant est transmis par le service RH, en lien avec le manager, puis appliqué en paie tel qu’il est communiqué.

Si vous pensez que le montant n’est pas correct, il faut donc d’abord vérifier l’information validée côté RH / management."""
    },
    {
        "title": "Télétravail",
        "keywords": ["teletravail", "télétravail", "allocation teletravail", "allocation télétravail", "20 euros", "20€"],
        "answer": """Pour bénéficier de l’allocation forfaitaire télétravail, il faut que le dossier soit complet.

En pratique :
- un avenant télétravail doit être signé ;
- une attestation d’assurance habitation en cours de validité doit être transmise ;
- l’assurance doit être fournie chaque année ;
- une fois les éléments transmis par les RH à la paie, l’allocation peut être mise en place.

Si la ligne n’apparaît pas, cela signifie souvent qu’un document manque ou n’a pas encore été transmis à la paie."""
    },
    {
        "title": "Tickets restaurant",
        "keywords": ["ticket restaurant", "tickets restaurant", "tr", "edenred", "carte ticket resto", "carte edenred"],
        "answer": """Pour les tickets restaurant :
- vous avez droit à 1 ticket restaurant par journée travaillée ;
- une journée travaillée doit correspondre à une amplitude minimale de 6 heures ;
- cette journée doit inclure une pause d’au moins 30 minutes entre 12h00 et 14h00 ;
- la déclaration doit être faite via Mon Portail Paie avant le 20 du mois.

Concernant la carte, si elle n’a pas été reçue, il peut être nécessaire de contacter directement Edenred."""
    },
    {
        "title": "Transport / Navigo",
        "keywords": ["transport", "navigo", "remboursement transport", "ratp", "pass navigo"],
        "answer": """Le remboursement des frais de transport à hauteur de 50 % se demande sur Mon Portail Paie.

La demande doit comporter, en un seul fichier :
- une attestation sur l’honneur signée ;
- un justificatif de paiement ;
- une copie du pass Navigo.

Seuls les abonnements hebdomadaires, mensuels et annuels sont pris en charge.
Le Navigo Liberté+ et les tickets à l’unité ne sont pas remboursés."""
    },
    {
        "title": "Période de gel portail paie",
        "keywords": ["gel", "periode de gel", "période de gel", "20 au 7", "pas remonte", "ne remonte pas", "remontee paie", "remontée paie"],
        "answer": """La période de gel signifie qu’il n’y a plus d’échange entre le portail paie et le logiciel de paie.

Elle a lieu chaque mois entre le 20 et le 7 du mois suivant.

Pendant cette période :
- vous pouvez continuer à faire vos demandes ;
- les managers peuvent continuer à valider ;
- mais les informations ne remontent pas en paie immédiatement ;
- elles seront prises en compte sur la période suivante.

Exemple :
une demande saisie après le 20 février sera traitée sur la paie suivante."""
    },
    {
        "title": "Arkevia - activation",
        "keywords": ["arkevia", "coffre fort", "coffre-fort", "activation arkevia", "activer arkevia", "bulletin coffre fort"],
        "answer": """Pour activer votre coffre-fort Arkevia :

1. Accédez à Arkevia via OneLogin ou directement sur myarkevia.com.
2. Cliquez sur “Je m’inscris”.
3. Renseignez votre matricule et votre code secret reçus par mail.
4. Renseignez votre nom, prénom et votre adresse email personnelle.
5. Choisissez votre mot de passe et validez l’inscription.

Votre adresse email personnelle est importante, car elle permet de conserver l’accès au coffre-fort pendant 50 ans."""
    },
    {
        "title": "Arkevia - connexion",
        "keywords": ["connexion arkevia", "se connecter arkevia", "mot de passe oublie arkevia", "mot de passe oublié arkevia"],
        "answer": """Pour vous connecter à Arkevia :
- utilisez votre adresse email personnelle renseignée lors de l’activation ;
- puis votre mot de passe choisi lors de l’inscription.

Si vous avez oublié votre mot de passe, utilisez le lien “Mot de passe oublié ?”.
Un email de réinitialisation sera envoyé sur votre adresse personnelle."""
    },
    {
        "title": "Arkevia - anciens bulletins",
        "keywords": ["anciens bulletins", "peopledoc", "importer bulletins arkevia", "deposer document arkevia", "déposer document arkevia"],
        "answer": """Vous pouvez regrouper vos anciens bulletins dans Arkevia.

En pratique :
- téléchargez d’abord vos anciens bulletins depuis PeopleDoc ;
- puis, dans Arkevia, cliquez sur “Déposer un document” ;
- vous pouvez aussi créer des dossiers pour classer vos documents."""
    },
    {
        "title": "Portail paie - validation des demandes",
        "keywords": ["mes validations", "valider demande", "validation portail", "titre transport validation", "absence conventionnelle validation"],
        "answer": """Dans Mon Portail Paie, le contact paie peut valider deux grandes catégories de demandes :
- les titres de transport ;
- certaines absences conventionnelles.

Depuis “Responsable” puis “Mes validations”, il est possible :
- d’ouvrir le détail d’une demande ;
- de vérifier la pièce jointe ;
- de valider ;
- ou de refuser la demande."""
    },
    {
        "title": "Portail paie - prise de contrôle",
        "keywords": ["prise de controle", "prise de contrôle", "mon equipe", "mon équipe", "prendre la main portail salarié"],
        "answer": """Le gestionnaire paie peut prendre le contrôle du portail d’un salarié de son périmètre.

Chemin :
- Responsable
- Mon équipe
- Prise de contrôle

Cela permet de visualiser le portail du collaborateur et de l’accompagner sur ses démarches."""
    },
    {
        "title": "Aide générique",
        "keywords": ["contact paie", "adresse generique", "adresse générique", "je ne sais pas", "autre question"],
        "answer": """Je n’ai pas trouvé de réponse suffisamment précise dans la FAQ.

Je vous conseille de contacter le service paie ou votre contact RH en précisant :
- le sujet exact ;
- le mois concerné ;
- la ligne du bulletin si besoin ;
- et tout justificatif utile.

Si vous voulez, reformulez votre question avec plus de détails et je peux essayer de vous orienter."""
    },
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

def score_entry(question: str, entry: dict) -> int:
    q = normalize(question)
    score = 0

    for kw in entry["keywords"]:
        kw_norm = normalize(kw)
        if kw_norm in q:
            score += max(3, len(kw_norm.split()))

    q_words = set(q.split())
    title_words = set(normalize(entry["title"]).split())
    common = q_words.intersection(title_words)
    score += len(common)

    return score

def find_best_answer(question: str):
    best_entry = None
    best_score = -1

    for entry in FAQ_ENTRIES:
        s = score_entry(question, entry)
        if s > best_score:
            best_score = s
            best_entry = entry

    if best_entry is None or best_score <= 0:
        for entry in FAQ_ENTRIES:
            if entry["title"] == "Aide générique":
                return entry

    return best_entry

# =========================
# CHAT
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Posez votre question RH / paie...")

if "pending_input" in st.session_state:
    user_input = st.session_state["pending_input"]
    del st.session_state["pending_input"]

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    result = find_best_answer(user_input)
    answer = f"**Sujet identifié :** {result['title']}\n\n{result['answer']}"

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)
        