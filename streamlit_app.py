import streamlit as st
from datetime import datetime
import os

st.set_page_config(
    page_title="KAREN — Agent RH / Paie",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CONFIG UI
# =========================================================
APP_TITLE = "KAREN"
APP_SUBTITLE = "Agent RH / Paie guidé — version premium"
LOGO_PATH = "logo.png"
AVATAR_GIF_PATH = "avatar.gif"
PRIMARY_BLUE = "#0f172a"
SECONDARY_BLUE = "#1e3a8a"
ACCENT_RED = "#991b1b"
BRIGHT_RED = "#dc2626"
CARD_BG = "#111827"
TEXT_MAIN = "#f8fafc"
TEXT_SOFT = "#cbd5e1"

# =========================================================
# DONNÉES MÉTIER
# =========================================================
ENTITIES = [
    "PSB - Paris School of Business",
    "IESA Arts & Culture",
    "Bellecour École",
    "LISAA",
    "Strate School of Design",
    "Atelier de Sèvres",
    "Cours Florent",
    "Penninghen",
    "ESARC",
    "Digital Campus",
    "ECV",
    "Sup de Création",
    "Narratiiv",
    "MBA ESG",
    "ESGCI",
    "ESG Finance",
    "ESG Luxe",
    "ESG Immobilier",
    "ESG Sport",
    "ESG Tourisme",
    "ESG RH",
    "ESG Marketing",
    "ESG Communication",
    "ESG Commerce",
    "PPA Business School",
    "MJM Graphic Design",
    "ICAN",
    "BRASSART",
    "Hetic",
    "Web School Factory",
    "Le Cordon Bleu Paris",
    "Atelier Chardon Savard",
    "EIML Paris",
    "EBS Paris",
    "Sup de Pub",
    "Paris École de Guerre Économique",
    "EGE",
    "IPSSI",
    "EFFICOM",
    "SUPDEWEB",
    "Autre entité / Non listée",
]

EMPLOYMENT_TYPES = [
    "Administrative - Cadre jours",
    "Administrative - Cadre heures",
    "Administrative - Technicien",
    "Administrative - Employé",
    "Apprentie",
    "Stagiaire",
    "Enseignant",
    "Model vivant",
    "Surveillant",
]

CONTRACT_TYPES = ["CDI", "CDD"]
WORK_TIMES = ["Temps plein", "Temps partiel"]
USER_ROLES = ["Salarié", "Manager"]

THEMES = {
    "Ma paie": [
        "Je ne comprends pas une ligne de mon bulletin",
        "Je constate une différence sur mon salaire",
        "Mon variable / mes heures n'apparaissent pas",
        "Mon salaire semble incomplet",
        "Je pense qu'une prime manque",
        "Je veux comprendre un net / brut / imposable",
        "Je veux savoir à qui m'adresser",
        "Autre besoin",
    ],
    "Mon Portail Paie": [
        "Je n'arrive pas à me connecter",
        "J'ai oublié mon mot de passe",
        "Je ne trouve pas un document",
        "Mon accès semble bloqué",
        "Je ne vois pas mes bulletins",
        "Je ne comprends pas où faire ma demande",
        "Autre besoin",
    ],
    "Absence": [
        "Je veux déclarer une absence",
        "Je veux signaler un arrêt de travail",
        "Je veux comprendre l'impact de mon absence en paie",
        "Je veux régulariser une absence passée",
        "Je ne sais pas quel motif choisir",
        "Autre besoin",
    ],
    "Congés": [
        "Je veux poser des congés",
        "Je veux connaître mon solde",
        "Je veux comprendre pourquoi ma demande est bloquée",
        "Je veux modifier / annuler une demande",
        "Je veux comprendre mes droits",
        "Autre besoin",
    ],
    "Mutuelle": [
        "Je veux comprendre ma cotisation",
        "Je veux demander une dispense",
        "Je veux signaler un problème d'affiliation",
        "Je veux ajouter / retirer des ayants droit",
        "Je veux savoir qui contacter",
        "Autre besoin",
    ],
    "Transport": [
        "Je veux demander un remboursement transport",
        "Je veux savoir si je suis éligible",
        "Je veux transmettre un justificatif",
        "Je veux comprendre un refus ou un retard",
        "Autre besoin",
    ],
    "Ticket restaurant": [
        "Je n'ai pas reçu ma carte / mes titres",
        "Ma carte ne fonctionne pas",
        "Je veux comprendre mon solde / mes droits",
        "Je veux signaler une perte ou un vol",
        "Je veux savoir si j'y ai droit",
        "Autre besoin",
    ],
    "Télétravail": [
        "Je veux connaître les règles applicables",
        "Je veux faire une demande",
        "Je veux comprendre un refus",
        "Je veux savoir comment déclarer mes jours",
        "Autre besoin",
    ],
    "Acompte": [
        "Je veux demander un acompte",
        "Je veux savoir si j'y ai droit",
        "Je veux connaître la procédure",
        "Je veux savoir où en est ma demande",
        "Autre besoin",
    ],
    "Bulletins": [
        "Je veux récupérer un bulletin",
        "Je ne vois pas mon bulletin",
        "Je veux un bulletin ancien",
        "Je veux comprendre une date de mise à disposition",
        "Autre besoin",
    ],
    "Documents de sortie": [
        "Je veux savoir quand je recevrai mes documents",
        "Il manque un document de sortie",
        "Je veux comprendre le solde de tout compte",
        "Je veux une attestation spécifique",
        "Autre besoin",
    ],
    "JPO ou SPO": [
        "Je veux déclarer une JPO / SPO",
        "Je veux comprendre pourquoi la récupération est bloquée",
        "Je veux savoir où saisir ma journée",
        "Je veux régulariser une saisie",
        "Autre besoin",
    ],
    "Heures supplémentaires": [
        "Je veux déclarer des heures supplémentaires",
        "Je veux comprendre leur paiement",
        "Je veux comprendre pourquoi elles n'apparaissent pas",
        "Je veux régulariser une période passée",
        "Autre besoin",
    ],
    "Demande de documents": [
        "Je veux une attestation employeur",
        "Je veux une attestation de salaire",
        "Je veux une attestation de présence",
        "Je veux un certificat de travail",
        "Je veux un document pour une administration",
        "Autre besoin",
    ],
}

RESPONSES = {
    ("Ma paie", "Je ne comprends pas une ligne de mon bulletin"): {
        "title": "Comprendre une ligne du bulletin",
        "summary": "Pour analyser correctement une ligne de paie, il faut d'abord identifier la rubrique concernée et vérifier la période, le type de contrat et les éventuels éléments variables du mois.",
        "checks": [
            "Identifier le libellé exact de la ligne concernée sur le bulletin.",
            "Vérifier le mois du bulletin analysé.",
            "Comparer avec le bulletin du mois précédent si nécessaire.",
            "Regarder s'il y a eu une absence, un variable, une prime ou une régularisation.",
        ],
        "action": "Si besoin, transmettez une capture de la ligne concernée ou le libellé exact au support RH / paie pour explication.",
        "contact": "Support RH / Paie",
    },
    ("Ma paie", "Je constate une différence sur mon salaire"): {
        "title": "Écart constaté sur le salaire",
        "summary": "Un écart de salaire peut venir d'une absence, d'un retard de saisie, d'un variable validé trop tard, d'une régularisation ou d'une évolution contractuelle.",
        "checks": [
            "Comparer le net à payer avec le mois précédent.",
            "Vérifier les absences, congés, acomptes ou retenues éventuelles.",
            "Vérifier la présence d'une prime ou d'un variable habituel manquant.",
            "Contrôler si le mois comporte une régularisation.",
        ],
        "action": "Si l'écart persiste après vérification, préparez un message détaillé avec le mois concerné et l'élément qui vous semble incorrect.",
        "contact": "Support RH / Paie",
    },
    ("Mon Portail Paie", "Je n'arrive pas à me connecter"): {
        "title": "Problème de connexion au portail paie",
        "summary": "Avant escalade, il convient de vérifier que le bon lien est utilisé, que les identifiants sont corrects et qu'il ne s'agit pas d'un blocage temporaire.",
        "checks": [
            "Vérifier que vous utilisez le bon portail.",
            "Tester une navigation privée ou un autre navigateur.",
            "Vérifier l'orthographe de votre identifiant.",
            "Tester la fonction mot de passe oublié si disponible.",
        ],
        "action": "Si l'accès reste bloqué, signalez le problème en précisant le message d'erreur affiché.",
        "contact": "Support RH / Paie ou support SIRH",
    },
    ("Absence", "Je veux déclarer une absence"): {
        "title": "Déclarer une absence",
        "summary": "La déclaration dépend du motif d'absence et du circuit interne de validation. Le bon motif doit être sélectionné pour éviter un impact erroné en paie.",
        "checks": [
            "Identifier la nature exacte de l'absence.",
            "Vérifier la période concernée.",
            "Déposer le justificatif si requis.",
            "S'assurer que la demande suit bien le circuit de validation.",
        ],
        "action": "Si vous ne savez pas quel motif choisir, contactez le support avant validation.",
        "contact": "Manager / RH / Paie selon procédure interne",
    },
    ("Congés", "Je veux poser des congés"): {
        "title": "Poser des congés",
        "summary": "Avant dépôt, il faut vérifier le solde disponible, la période demandée et les règles de validation internes.",
        "checks": [
            "Vérifier votre solde de congés.",
            "Contrôler les dates demandées.",
            "S'assurer que la demande est faite dans le bon module.",
            "Informer votre manager si nécessaire.",
        ],
        "action": "En cas de blocage, notez le message affiché et la période concernée.",
        "contact": "Manager / RH / Paie",
    },
    ("Mutuelle", "Je veux demander une dispense"): {
        "title": "Demande de dispense mutuelle",
        "summary": "Une dispense de mutuelle n'est possible que dans certains cas prévus. Un justificatif est généralement nécessaire et doit être transmis selon la procédure prévue.",
        "checks": [
            "Vérifier si votre situation entre dans un cas de dispense.",
            "Préparer le justificatif demandé.",
            "Vérifier si un formulaire spécifique existe.",
            "Respecter le délai de transmission.",
        ],
        "action": "Si vous ne savez pas si vous êtes éligible, demandez une confirmation avant envoi du dossier.",
        "contact": "RH / organisme de gestion mutuelle selon procédure",
    },
    ("Transport", "Je veux demander un remboursement transport"): {
        "title": "Remboursement transport",
        "summary": "La demande nécessite généralement un justificatif valide et dépend de la situation du salarié ainsi que des règles internes applicables.",
        "checks": [
            "Vérifier que votre abonnement / justificatif est valide.",
            "Contrôler la période couverte.",
            "Vérifier le canal de dépôt prévu.",
            "S'assurer que le document est lisible.",
        ],
        "action": "En cas de rejet ou retard, demandez la raison précise et la période traitée.",
        "contact": "RH / Paie",
    },
    ("Ticket restaurant", "Je n'ai pas reçu ma carte / mes titres"): {
        "title": "Carte ou titres non reçus",
        "summary": "Un retard peut venir d'une commande en cours, d'une adresse incorrecte ou d'un problème d'activation / livraison.",
        "checks": [
            "Vérifier l'adresse enregistrée.",
            "Vérifier votre éligibilité et votre date d'entrée.",
            "Contrôler si une commande a bien été lancée.",
            "Préciser s'il s'agit d'une première demande ou d'un renouvellement.",
        ],
        "action": "Si la situation dure, demander une vérification de l'état de commande ou une réédition si nécessaire.",
        "contact": "RH / Paie / gestionnaire titres restaurant",
    },
    ("Télétravail", "Je veux faire une demande"): {
        "title": "Demande de télétravail",
        "summary": "La demande dépend de votre éligibilité, de l'organisation de votre poste et des règles internes de l'entité.",
        "checks": [
            "Vérifier si votre poste est éligible.",
            "Vérifier le nombre de jours autorisés.",
            "Suivre le circuit de validation prévu.",
            "Contrôler si un avenant ou une formalisation est requis.",
        ],
        "action": "Si besoin, rapprochez-vous de votre manager avant dépôt officiel.",
        "contact": "Manager / RH",
    },
    ("Acompte", "Je veux demander un acompte"): {
        "title": "Demander un acompte",
        "summary": "L'acompte suit généralement une procédure précise et peut dépendre de la date de demande et de votre situation contractuelle.",
        "checks": [
            "Vérifier si vous êtes éligible.",
            "Vérifier la date limite de demande.",
            "Préparer le canal de demande prévu.",
            "Préciser le mois concerné.",
        ],
        "action": "Si la procédure n'est pas claire, préparez une demande simple avec votre identité, l'entité et le mois concerné.",
        "contact": "Paie / RH",
    },
    ("Bulletins", "Je veux récupérer un bulletin"): {
        "title": "Récupération d'un bulletin",
        "summary": "Le bulletin est généralement disponible sur le portail dédié. En cas d'absence du document, il faut vérifier la période, l'accès et la mise à disposition.",
        "checks": [
            "Vérifier le bon mois.",
            "Tester un autre navigateur si besoin.",
            "Vérifier si le bulletin a déjà été publié.",
            "Confirmer que vous êtes sur le bon espace documentaire.",
        ],
        "action": "Si le bulletin est introuvable, signalez le mois exact concerné.",
        "contact": "Paie / support portail",
    },
    ("Documents de sortie", "Je veux savoir quand je recevrai mes documents"): {
        "title": "Réception des documents de sortie",
        "summary": "Les documents de sortie sont transmis selon le calendrier de traitement interne après la fin du contrat et la finalisation des éléments nécessaires.",
        "checks": [
            "Vérifier votre date de fin de contrat.",
            "Vérifier si tous les éléments ont bien été remontés.",
            "Identifier les documents attendus.",
            "Vérifier l'adresse ou le canal de transmission prévu.",
        ],
        "action": "Si un document manque, précisez lequel pour accélérer le traitement.",
        "contact": "RH / Paie",
    },
    ("JPO ou SPO", "Je veux comprendre pourquoi la récupération est bloquée"): {
        "title": "Récupération JPO / SPO bloquée",
        "summary": "La récupération peut être bloquée si la journée n'a pas encore été validée complètement, si elle n'est pas sur un mois révolu ou si le mauvais motif a été utilisé.",
        "checks": [
            "Vérifier que la JPO / SPO a bien été saisie.",
            "Vérifier que le processus de validation est terminé.",
            "Vérifier que la journée est sur un mois révolu.",
            "Contrôler le motif d'activité utilisé.",
        ],
        "action": "En cas de doute, transmettre la date exacte et une capture de la saisie effectuée.",
        "contact": "RH / Paie / manager selon circuit",
    },
    ("Heures supplémentaires", "Je veux comprendre leur paiement"): {
        "title": "Comprendre le paiement des heures supplémentaires",
        "summary": "Le paiement dépend de la validation, de la période de paie, du statut du salarié et des règles applicables à l'entité et au contrat.",
        "checks": [
            "Vérifier que les heures ont bien été validées.",
            "Contrôler le mois de réalisation.",
            "Vérifier si une régularisation est en cours.",
            "Préciser la période exacte concernée.",
        ],
        "action": "Si elles n'apparaissent pas, demandez un contrôle en indiquant les dates et le volume concerné.",
        "contact": "Manager / Paie",
    },
    ("Demande de documents", "Je veux une attestation employeur"): {
        "title": "Demande d'attestation employeur",
        "summary": "Pour traiter rapidement la demande, il faut préciser le type exact d'attestation attendu, l'usage prévu et le délai souhaité.",
        "checks": [
            "Préciser le type d'attestation.",
            "Préciser l'organisme destinataire si besoin.",
            "Indiquer l'urgence éventuelle.",
            "Vérifier le format attendu si connu.",
        ],
        "action": "Préparez une demande claire indiquant l'usage du document.",
        "contact": "RH / Administration du personnel",
    },
}

DEFAULT_RESPONSE = {
    "title": "Analyse de la demande",
    "summary": "Votre besoin a bien été identifié. Une vérification ciblée est nécessaire pour confirmer la bonne procédure et éviter une réponse inexacte.",
    "checks": [
        "Vérifier la période concernée.",
        "Vérifier le canal utilisé pour la demande.",
        "Préciser le contexte exact et, si besoin, joindre un justificatif ou une capture.",
    ],
    "action": "Si vous ne trouvez pas la réponse immédiatement, utilisez le message prêt à envoyer ci-dessous.",
    "contact": "Support RH / Paie",
}

# =========================================================
# FONCTIONS
# =========================================================
def safe_display_image(path, width=None):
    if isinstance(path, str) and path.startswith("http"):
        st.image(path, width=width)
    elif os.path.exists(path):
        st.image(path, width=width)


def get_complexity_score(theme, need, free_text):
    score = 1
    if "Autre besoin" in need:
        score += 2
    if theme in ["Ma paie", "Documents de sortie", "Heures supplémentaires", "JPO ou SPO"]:
        score += 2
    if len(free_text.strip()) > 80:
        score += 1
    return min(score, 5)


def get_complexity_label(score):
    if score <= 2:
        return "Simple"
    if score == 3:
        return "Intermédiaire"
    return "Sensibile / à vérifier"


def get_rule_based_alerts(role, job_type, contract_type, work_time, theme):
    alerts = []
    if job_type == "Enseignant" and theme in ["Heures supplémentaires", "JPO ou SPO", "Ma paie"]:
        alerts.append("Pour les enseignants, la vérification des heures, variables et remontées pédagogiques est prioritaire.")
    if job_type == "Stagiaire":
        alerts.append("Pour un stagiaire, certaines rubriques paie ou avantages peuvent suivre des règles spécifiques.")
    if job_type == "Apprentie":
        alerts.append("Pour une apprentie, le contrat, l'âge et le mois d'exécution peuvent influer sur le traitement paie.")
    if work_time == "Temps partiel":
        alerts.append("Le temps partiel peut modifier les droits, soldes, montants et contrôles attendus.")
    if contract_type == "CDD" and theme == "Documents de sortie":
        alerts.append("En CDD, la vérification de la date de fin de contrat et des documents de sortie est essentielle.")
    if role == "Manager":
        alerts.append("En tant que manager, vous pouvez être sollicité sur la validation ou le suivi d'une demande salariée.")
    return alerts


def build_response(theme, need, role, entity, job_type, contract_type, work_time, free_text):
    data = RESPONSES.get((theme, need), DEFAULT_RESPONSE)
    complexity_score = get_complexity_score(theme, need, free_text)
    alerts = get_rule_based_alerts(role, job_type, contract_type, work_time, theme)

    context_lines = [
        f"Profil déclaré : {role}",
        f"Entité : {entity}",
        f"Type d'emploi : {job_type}",
        f"Contrat : {contract_type}",
        f"Temps de travail : {work_time}",
    ]

    return {
        "title": data["title"],
        "summary": data["summary"],
        "checks": data["checks"],
        "action": data["action"],
        "contact": data["contact"],
        "context": context_lines,
        "complexity_score": complexity_score,
        "complexity_label": get_complexity_label(complexity_score),
        "alerts": alerts,
    }


def build_support_message(role, entity, job_type, contract_type, work_time, theme, need, free_text=""):
    date_str = datetime.now().strftime("%d/%m/%Y")
    body = f"""Bonjour,

Je vous contacte concernant une demande RH / Paie.

Voici les éléments de contexte :
- Profil : {role}
- Entité : {entity}
- Type d'emploi : {job_type}
- Type de contrat : {contract_type}
- Temps de travail : {work_time}
- Thème : {theme}
- Besoin précis : {need}

Description complémentaire :
{free_text if free_text else 'Merci de trouver ci-dessus les éléments nécessaires à l’analyse de ma demande.'}

Pouvez-vous m’indiquer la marche à suivre ou procéder à la vérification nécessaire ?

Merci par avance.

Cordialement,
"""
    subject = f"[{entity}] Demande RH / Paie - {theme} - {date_str}"
    return subject, body


# =========================================================
# STYLE
# =========================================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background: linear-gradient(180deg, {PRIMARY_BLUE} 0%, #172554 45%, #0f172a 100%);
            color: {TEXT_MAIN};
        }}
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #111827 0%, #0b1120 100%);
            border-right: 1px solid rgba(255,255,255,0.06);
        }}
        .karen-card {{
            background: rgba(17,24,39,0.92);
            border-radius: 22px;
            padding: 1.2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.06);
            margin-bottom: 1rem;
            backdrop-filter: blur(4px);
        }}
        .hero-card {{
            background: linear-gradient(135deg, {SECONDARY_BLUE} 0%, {ACCENT_RED} 100%);
            border-radius: 24px;
            padding: 1.4rem;
            color: white;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
            margin-bottom: 1rem;
        }}
        .karen-title {{
            font-size: 2.2rem;
            font-weight: 900;
            letter-spacing: 0.5px;
            color: white;
            margin-bottom: 0.15rem;
        }}
        .karen-subtitle {{
            font-size: 1rem;
            color: #fee2e2;
            margin-bottom: 0.75rem;
        }}
        .section-title {{
            font-size: 1.08rem;
            font-weight: 800;
            color: #93c5fd;
            margin-bottom: 0.45rem;
        }}
        .small-note {{
            font-size: 0.94rem;
            color: #e5e7eb;
        }}
        .metric-pill {{
            display:inline-block;
            padding: 0.42rem 0.8rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
            color: white;
            font-size: 0.9rem;
            margin-right: 0.45rem;
            margin-bottom: 0.35rem;
        }}
        .success-box {{
            background: #052e16;
            border-left: 5px solid #22c55e;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: white;
        }}
        .warning-box {{
            background: #450a0a;
            border-left: 5px solid {BRIGHT_RED};
            padding: 0.9rem 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: white;
        }}
        .info-box {{
            background: #082f49;
            border-left: 5px solid #38bdf8;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: white;
        }}
        .avatar-box {{
            position: fixed;
            right: 22px;
            bottom: 18px;
            width: 110px;
            z-index: 999;
            background: rgba(17,24,39,0.88);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 0.55rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.25);
            text-align: center;
        }}
        .avatar-label {{
            color: #cbd5e1;
            font-size: 0.75rem;
            margin-top: 0.35rem;
        }}
        .stButton>button {{
            width: 100%;
            background: linear-gradient(90deg, {ACCENT_RED} 0%, {BRIGHT_RED} 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            padding: 0.7rem 1rem;
        }}
        .stButton>button:hover {{
            filter: brightness(1.05);
        }}
        div[data-baseweb="select"] > div,
        .stTextInput input,
        .stTextArea textarea {{
            background-color: #0b1220 !important;
            color: white !important;
            border-radius: 12px !important;
        }}
        .stRadio label, .stMarkdown, .stCaption, .stSelectbox label, .stTextArea label, .stTextInput label {{
            color: {TEXT_MAIN} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    safe_display_image(LOGO_PATH, width=110)
    st.markdown("## KAREN")
    st.caption("Agent RH / Paie guidé")
    st.markdown("---")
    st.markdown("### Navigation")
    st.markdown("- Qualification")
    st.markdown("- Analyse")
    st.markdown("- Message prêt à transmettre")
    st.markdown("- FAQ métier")
    st.markdown("---")
    st.markdown("### Atouts démo")
    st.markdown("- Sans OpenAI")
    st.markdown("- Parcours guidé")
    st.markdown("- Règles métier")
    st.markdown("- Escalade propre")
    st.markdown("- Compatible Streamlit Cloud")

# =========================================================
# HEADER
# =========================================================
header_left, header_right = st.columns([6, 1.6])

with header_left:
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    top_left, top_right = st.columns([1, 5])
    with top_left:
        safe_display_image(LOGO_PATH, width=95)
    with top_right:
        st.markdown(f'<div class="karen-title">{APP_TITLE}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="karen-subtitle">{APP_SUBTITLE}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="small-note">Un assistant RH / Paie conçu comme un véritable outil métier : il qualifie la demande, applique une logique de tri, propose une réponse utile et prépare une escalade propre si nécessaire.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<span class="metric-pill">Guidé</span>'
            '<span class="metric-pill">Fiable</span>'
            '<span class="metric-pill">Présentable</span>'
            '<span class="metric-pill">Sans IA externe</span>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

with header_right:
    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    safe_display_image(AVATAR_GIF_PATH, width=140)
    st.caption("Avatar KAREN")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# INTRO
# =========================================================
st.markdown('<div class="karen-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Parcours intelligent</div>', unsafe_allow_html=True)
st.write(
    "KAREN ne répond pas au hasard. L’outil pose les bonnes questions, qualifie le profil, "
    "prend en compte le contexte RH / paie, puis génère une réponse structurée et actionnable."
)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FORMULAIRE + PANNEAU D'AIDE
# =========================================================
left, right = st.columns([1.15, 0.85])

with left:
    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Qualification de la demande</div>', unsafe_allow_html=True)

    role = st.radio("1. Votre question vous concerne en tant que :", USER_ROLES, horizontal=True)
    entity = st.selectbox("2. Elle concerne un salarié de quelle entité ?", ENTITIES, index=0)
    job_type = st.selectbox("3. Quel type d'emploi avez-vous ?", EMPLOYMENT_TYPES, index=0)
    contract_type = st.radio("4. Quel est votre type de contrat ?", CONTRACT_TYPES, horizontal=True)
    work_time = st.radio("5. Quel est votre temps de travail ?", WORK_TIMES, horizontal=True)
    theme = st.selectbox("6. Quel est le thème de votre demande ?", list(THEMES.keys()), index=0)
    need = st.selectbox("7. Quel est votre besoin précis ?", THEMES[theme], index=0)
    free_text = st.text_area(
        "8. Complément d'information",
        placeholder="Exemple : mois concerné, message d’erreur, date exacte, rubrique du bulletin, justificatif transmis, niveau d’urgence…",
        height=130,
    )
    generate = st.button("Analyser la demande", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Moteur de décision</div>', unsafe_allow_html=True)
    st.markdown(
        """
- Qualification du rôle
- Identification de l'entité
- Filtrage par emploi, contrat et temps de travail
- Choix du thème puis du besoin précis
- Réponse guidée
- Préparation d'une escalade propre si nécessaire
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Conseil Streamlit Cloud</div>', unsafe_allow_html=True)
    st.write(
        "Pour afficher le logo et l’avatar dans Streamlit Cloud, placez `logo.png` et `avatar.gif` dans le même repo GitHub que `streamlit_app.py`."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ANALYSE
# =========================================================
if generate:
    result = build_response(theme, need, role, entity, job_type, contract_type, work_time, free_text)
    subject, support_message = build_support_message(
        role, entity, job_type, contract_type, work_time, theme, need, free_text
    )

    stat1, stat2, stat3 = st.columns(3)
    stat1.metric("Thème", theme)
    stat2.metric("Besoin", need[:25] + "..." if len(need) > 25 else need)
    stat3.metric("Niveau", result["complexity_label"])

    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown(f"### {result['title']}")
    st.markdown(f'<div class="success-box"><strong>Synthèse :</strong> {result["summary"]}</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("#### Contexte identifié")
        for line in result["context"]:
            st.write(f"- {line}")

    with c2:
        st.markdown("#### Vérifications recommandées")
        for item in result["checks"]:
            st.write(f"- {item}")

    if result["alerts"]:
        st.markdown('<div class="info-box"><strong>Règles métier détectées :</strong></div>', unsafe_allow_html=True)
        for alert in result["alerts"]:
            st.write(f"- {alert}")

    st.markdown(f'<div class="warning-box"><strong>Action conseillée :</strong> {result["action"]}</div>', unsafe_allow_html=True)
    st.write(f"**Interlocuteur recommandé :** {result['contact']}")
    st.progress(result["complexity_score"] / 5)
    st.caption(f"Score de complexité : {result['complexity_score']} / 5")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown("### Message prêt à transmettre")
    st.text_input("Objet du message", value=subject)
    st.text_area("Contenu du message", value=support_message, height=300)
    st.download_button(
        label="Télécharger le message (.txt)",
        data=f"Objet : {subject}\n\n{support_message}",
        file_name="message_karen.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown("### Réponse KAREN")
    st.write(
        "Complétez le parcours puis cliquez sur **Analyser la demande** pour obtenir une réponse structurée, "
        "des vérifications ciblées, des règles métier détectées et un message prêt à transmettre."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FAQ / BLOC DÉMO
# =========================================================
st.markdown('<div class="karen-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">FAQ métier embarquée</div>', unsafe_allow_html=True)
faq_col1, faq_col2 = st.columns(2)
with faq_col1:
    st.write("- Ma paie")
    st.write("- Mon Portail Paie")
    st.write("- Absence")
    st.write("- Congés")
    st.write("- Mutuelle")
    st.write("- Transport")
    st.write("- Ticket restaurant")
with faq_col2:
    st.write("- Télétravail")
    st.write("- Acompte")
    st.write("- Bulletins")
    st.write("- Documents de sortie")
    st.write("- JPO ou SPO")
    st.write("- Heures supplémentaires")
    st.write("- Demande de documents")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div style="text-align:center; color:#cbd5e1; font-size:0.92rem; padding: 1rem 0 2rem 0;">
        KAREN — Agent RH / Paie guidé • Version Premium • Streamlit • Sans IA externe
    </div>
    """,
    unsafe_allow_html=True,
)
