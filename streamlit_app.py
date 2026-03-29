import streamlit as st
from datetime import datetime
import os
import time
import base64

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
LOGO_PATH = "images.png"
AVATAR_GIF_PATH = "giphy.gif"

# =========================================================
# RÉFÉRENTIEL ÉTABLISSEMENTS
# =========================================================
ESTABLISHMENTS = [
    {"pole": "Art & Création", "legal_entity": "ACADEMIE JULIAN RIVE GAUCHE", "name": "ACADEMIE JULIAN RIVE GAUCHE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "ATELIER DE SEVRES", "name": "ATELIER DE SEVRES Etablissement principal", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "BELLECOUR ECOLE ARTS", "name": "BELLECOUR DAUPHIN", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "Etablissement Français Formation et Enseignement", "name": "Etablissement Français Formation et Enseignement", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "Galiléo Institut Culinaire de France", "name": "GICF Paris", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "Institut d'Architecture et de Design", "name": "IDEA RENNES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "Institut de Développement des Arts Appliqués", "name": "IDAA GRAPHISME", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "Institut de Développement des Arts Appliqués", "name": "IDAA ANIMATION", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "Institut de Développement des Arts Appliqués", "name": "IDAA ARCHITECTURE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "Institut de Développement des Arts Appliqués", "name": "IDAA MODE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "Institut de Développement des Arts Appliqués", "name": "IDAA", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "L'Institut Supérieur des Arts Appliqués", "name": "LISAA Strasbourg", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "LISAA NANTES", "name": "ECOLE LISAA NANTES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "LOCOMOTIVE", "name": "Locomotive - Atelier Chardon Savard", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "STRATE COLLEGE", "name": "STRATE COLLEGE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "legal_entity": "STRATE ECOLE DE DESIGN -LYON", "name": "STRATE ECOLE DE DESIGN -LYON", "ccn": "Enseignement privé indépendant"},

    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESGCV PSB PGE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESGCV ESGM", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESGCV ESGCI", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESGCV ESGF", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESGCV ESGFR", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESGCV IICP", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESGCV PSB", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESGRH", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESG LUXE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESG SPORT", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESG ACT", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "ESGCV", "name": "ESGCV ESGRH", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "Galiléo Formation Professionnelle", "name": "Galiléo Formation Professionnelle", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "GALILEO VAE", "name": "GALILEO VAE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "GALILEO VAE", "name": "GALILEO VAE2", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "HETIC", "name": "HETIC", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "Institut de Management Ecole Supérieure de Gestion", "name": "IMESG Paris", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "Institut de Management Ecole Supérieure de Gestion", "name": "ESG LANGUES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "PARIS SCHOOL OF TECHNOLOGY & BUSINESS", "name": "PARIS SCHOOL TECHNOLOY & BUSINESS PARIS", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "legal_entity": "WEB SCHOOL FACTORY", "name": "WEB SCHOOL FACTORY", "ccn": "Enseignement privé indépendant"},

    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV ESARC CEFIRE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV POLE ESG", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV AIX EN PROVENCE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV BORDEAUX", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV TOULOUSE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV MONTPELLIER", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV RENNES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV LYON", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV TOURS", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV STRASBOURG", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV NANTES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV MERKURE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV ELIGE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV ROUEN", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV BIARRITZ", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "legal_entity": "ESGCV", "name": "ESGCV DIJON", "ccn": "Enseignement privé indépendant"},

    {"pole": "Art & Création", "legal_entity": "ATELIER CHARDON SAVARD NANTES", "name": "ACS NANTES", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "legal_entity": "COURS FLORENT JEUNESSE", "name": "COURS FLORENT JEUNESSE PARIS", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "legal_entity": "COURS FLORENT JEUNESSE", "name": "COURS FLORENT JEUNESSE BORDEAUX", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "legal_entity": "COURS FLORENT JEUNESSE", "name": "COURS FLORENT JEUNESSE MONTPELLIER", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "legal_entity": "ECAD CONSULTANTS", "name": "IESA Art & Culture", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "legal_entity": "ECAD CONSULTANTS", "name": "DIGITAL CAMPUS PARIS", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "legal_entity": "ECAD CONSULTANTS", "name": "ECAD CONSULTANTS", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "legal_entity": "FLORENT", "name": "FLORENT", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "legal_entity": "FLORENT", "name": "FLORENT BORDEAUX", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "legal_entity": "FLORENT", "name": "FLORENT MONTPELLIER", "ccn": "Organismes de formation"},

    {"pole": "Holding & Cie", "legal_entity": "EVA SANTE", "name": "EVA SANTE IFAS METZ", "ccn": "Organismes de formation"},
    {"pole": "Holding & Cie", "legal_entity": "EVA SANTE", "name": "EVA SANTE IFAS CHALONS", "ccn": "Organismes de formation"},
    {"pole": "Holding & Cie", "legal_entity": "EVA SANTE", "name": "EVA SANTE IFAS BORDEAUX", "ccn": "Organismes de formation"},
    {"pole": "Holding & Cie", "legal_entity": "EVA SANTE", "name": "EVA SANTE PARIS", "ccn": "Organismes de formation"},
    {"pole": "Holding & Cie", "legal_entity": "GGE Corporate Services", "name": "GGE Corporate Services", "ccn": "SYNTEC"},
    {"pole": "Holding & Cie", "legal_entity": "GGE France", "name": "GGE France", "ccn": "SYNTEC"},
    {"pole": "Holding & Cie", "legal_entity": "GGE Operations", "name": "GGE Operation", "ccn": "SYNTEC"},
    {"pole": "Holding & Cie", "legal_entity": "GGE Strategy", "name": "GGE Strategy", "ccn": "SYNTEC"},
    {"pole": "Autre / non listé", "legal_entity": "À préciser", "name": "Autre entité / Non listée", "ccn": "À préciser"},
]

ESTABLISHMENT_NAMES = [item["name"] for item in ESTABLISHMENTS]

# =========================================================
# DONNÉES DE PARCOURS
# =========================================================
EMPLOYMENT_TYPES = [
    "Administratif - Cadre au forfait jours",
    "Administratif - Cadre en heures",
    "Administratif - Technicien(ne)",
    "Administratif - Employé(e)",
    "Apprenti(e)",
    "Stagiaire",
    "Enseignant(e)",
    "Modèle vivant",
    "Surveillant(e)",
]

CONTRACT_TYPES = ["CDI", "CDD"]
WORK_TIMES = ["Temps plein", "Temps partiel"]
USER_ROLES = ["Salarié(e)", "Manager"]

SPECIAL_PROFILES = {"Enseignant(e)", "Modèle vivant", "Surveillant(e)"}

THEMES = {
    "Ma paie / Mon bulletin": [
        "Je ne comprends pas mon salaire ce mois-ci",
        "Mon salaire a baissé / augmenté",
        "Il manque des heures (FFP / induites / supplémentaires)",
        "Il manque une prime / indemnité",
        "Je ne comprends pas une ligne du bulletin",
        "Je pense qu’il y a une erreur sur mon bulletin",
        "Je veux comprendre mon net à payer",
        "Je veux comprendre le net social",
        "Je veux comprendre mes cotisations",
        "Autre",
    ],
    "Mon Portail Paie": [
        "Je n’arrive pas à me connecter",
        "Je ne vois pas mes bulletins",
        "Je ne vois pas mes tickets restaurant",
        "Je ne vois pas mes jours de télétravail",
        "Je ne comprends pas comment utiliser le portail",
        "Je veux modifier une information",
        "Autre",
    ],
    "Absences / Arrêts": [
        "Je veux déclarer une absence",
        "Quels types d’absence existent ?",
        "Je veux signaler un arrêt de travail",
        "Je veux savoir si mon absence est payée",
        "Je veux comprendre l’impact sur ma paie",
        "Je veux régulariser une absence",
        "Autre",
    ],
    "Congés / RTT / Récup": [
        "Combien de congés il me reste",
        "Comment poser un congé",
        "Délais de validation",
        "Refus de congé",
        "RTT / JRS comment ça marche",
        "Report / perte de congés",
        "Autre",
    ],
    "Télétravail": [
        "Combien de jours j’ai droit",
        "Comment poser un jour",
        "Mon manager refuse",
        "Je veux modifier mes jours",
        "Impact sur paie / indemnité",
        "Problème sur portail",
        "Autre",
    ],
    "Acompte sur salaire": [
        "Comment demander un acompte",
        "Jusqu’à combien je peux demander",
        "Pourquoi ma demande est refusée",
        "Quand est versé l’acompte",
        "Montant incorrect",
        "Autre",
    ],
    "Heures / Activité": [
        "Mes heures FFP ne sont pas correctes",
        "Heures induites manquantes",
        "Heures supplémentaires non payées",
        "Heures validées mais non payées",
        "Problème de transmission des heures",
        "Je veux comprendre le calcul",
        "Autre",
    ],
    "Mutuelle / Prévoyance": [
        "Je veux adhérer",
        "Je veux résilier",
        "Je ne suis pas remboursé",
        "Je veux ajouter un bénéficiaire",
        "Cotisation sur mon bulletin",
        "Autre",
    ],
    "Transport": [
        "Remboursement Navigo",
        "Montant incorrect",
        "Justificatif à fournir",
        "Délai de remboursement",
        "Autre",
    ],
    "Tickets restaurant": [
        "Je ne les ai pas reçus",
        "Montant incorrect",
        "Nombre incorrect",
        "Carte Edenred problème",
        "Autre",
    ],
    "Documents RH / Paie": [
        "Attestation employeur",
        "Attestation de salaire",
        "Certificat de travail",
        "Solde de tout compte",
        "Bulletin ancien",
        "Autre",
    ],
    "Sortie / Fin de contrat": [
        "Je quitte l’entreprise",
        "Je veux comprendre mon solde de tout compte",
        "Je n’ai pas reçu mes documents",
        "Indemnités de fin de contrat",
        "Autre",
    ],
    "Contrat / Statut": [
        "Type de contrat (CDD / CDI)",
        "Temps de travail",
        "Forfait jours / heures",
        "Modification de contrat",
        "Autre",
    ],
    "Demande manager": [
        "Problème paie d’un collaborateur",
        "Heures non validées",
        "Suivi des absences",
        "Recrutement / onboarding",
        "Création de poste",
        "Autre",
    ],
    "Autre demande": [
        "Sujet non trouvé",
    ],
}

# =========================================================
# OUTILS UI
# =========================================================
def safe_display_image(path, width=None):
    if isinstance(path, str) and path.startswith("http"):
        st.image(path, width=width)
    elif os.path.exists(path):
        st.image(path, width=width)

def render_avatar_html(state="idle", width=140):
    labels = {
        "idle": "🟢 KAREN en veille",
        "thinking": "🔵 KAREN analyse",
        "answer": "🔴 KAREN vous répond",
    }
    safe_state = state if state in labels else "idle"

    if os.path.exists(AVATAR_GIF_PATH):
        with open(AVATAR_GIF_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        img_html = f'<img src="data:image/gif;base64,{b64}" width="{width}">'
    else:
        img_html = '<div style="font-size:54px;">🤖</div>'

    st.markdown(
        f"""
        <div style="text-align:center;">
            {img_html}
            <div style="color:#f8fafc; font-size:12px; margin-top:6px; font-weight:600;">{labels[safe_state]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# FONCTIONS MÉTIER
# =========================================================
def get_establishment_data(establishment_name):
    for item in ESTABLISHMENTS:
        if item["name"] == establishment_name:
            return item
    return {
        "pole": "À préciser",
        "legal_entity": "À préciser",
        "name": establishment_name,
        "ccn": "À préciser",
    }

def is_special_population(job_type):
    return job_type in SPECIAL_PROFILES

def get_complexity_score(theme, need, free_text, job_type):
    score = 1
    if need == "Autre" or theme == "Autre demande":
        score += 2
    if theme in [
        "Ma paie / Mon bulletin",
        "Heures / Activité",
        "Sortie / Fin de contrat",
        "Mutuelle / Prévoyance",
        "Demande manager",
    ]:
        score += 1
    if len((free_text or "").strip()) > 80:
        score += 1
    if is_special_population(job_type):
        score += 1
    return min(score, 5)

def get_complexity_label(score):
    if score <= 2:
        return "Simple"
    if score == 3:
        return "Intermédiaire"
    return "Sensible / à vérifier"

def generic_vigilance_from_ccn(ccn):
    if ccn == "Enseignement privé indépendant":
        return "La CCN Enseignement privé indépendant doit être prise en compte pour confirmer les modalités applicables."
    if ccn == "Organismes de formation":
        return "La CCN Organismes de formation peut comporter des modalités spécifiques selon l’activité ou le statut."
    if ccn == "SYNTEC":
        return "La CCN SYNTEC peut prévoir des règles distinctes selon la catégorie et l’organisation du travail."
    return "La convention collective applicable doit être confirmée avant validation définitive."

def build_support_message(role, establishment, establishment_data, job_type, contract_type, work_time, theme, need, free_text=""):
    date_str = datetime.now().strftime("%d/%m/%Y")
    subject = f"[{establishment}] Demande RH / Paie - {theme} - {date_str}"

    body = f"""Bonjour,

Je vous contacte concernant une demande RH / Paie.

Voici les éléments de contexte :
- Profil : {role}
- Pôle : {establishment_data["pole"]}
- Entité juridique : {establishment_data["legal_entity"]}
- Établissement : {establishment}
- CCN : {establishment_data["ccn"]}
- Type d'emploi : {job_type}
- Type de contrat : {contract_type}
- Temps de travail : {work_time}
- Thème : {theme}
- Besoin précis : {need}

Description complémentaire :
{free_text.strip() if free_text and free_text.strip() else "Merci de trouver ci-dessus les éléments nécessaires à l’analyse de ma demande."}

Pouvez-vous m’indiquer la marche à suivre ou procéder à la vérification nécessaire ?

Merci par avance.

Cordialement,
"""
    return subject, body

def init_result(role, establishment, establishment_data, job_type, contract_type, work_time, theme, need):
    return {
        "title": "Analyse de la demande",
        "summary": "Votre besoin a été qualifié par KAREN. Une orientation fiable peut être proposée sur la base des règles métier connues.",
        "checks": [],
        "action": "",
        "contact": "Support RH / Paie",
        "channel": "À confirmer",
        "contact_reason": "",
        "alerts": [],
        "vigilance": [],
        "context": [
            f"Profil déclaré : {role}",
            f"Pôle : {establishment_data['pole']}",
            f"Entité juridique : {establishment_data['legal_entity']}",
            f"Établissement : {establishment}",
            f"CCN : {establishment_data['ccn']}",
            f"Type d'emploi : {job_type}",
            f"Contrat : {contract_type}",
            f"Temps de travail : {work_time}",
            f"Thème : {theme}",
            f"Besoin : {need}",
        ],
    }

def apply_transversal_alerts(result, role, job_type, contract_type, work_time, ccn):
    if is_special_population(job_type):
        result["alerts"].append(
            "Population spécifique détectée : les règles standard ne doivent pas être appliquées automatiquement sans vérification préalable."
        )
        result["vigilance"].append(
            "Le profil Enseignant(e) / Modèle vivant / Surveillant(e) nécessite une validation métier avant conclusion définitive."
        )

    result["vigilance"].append(generic_vigilance_from_ccn(ccn))

    if role == "Manager":
        result["alerts"].append(
            "Profil manager détecté : la demande peut impliquer un rôle de validation, de suivi ou de coordination RH."
        )
    if work_time == "Temps partiel":
        result["alerts"].append(
            "Temps partiel détecté : les droits, montants ou plafonds applicables peuvent nécessiter un contrôle complémentaire."
        )
    if contract_type == "CDD":
        result["alerts"].append(
            "Contrat CDD détecté : certaines règles ou échéances peuvent nécessiter une vérification spécifique."
        )

def build_rule_based_response(theme, need, role, establishment, establishment_data, job_type, contract_type, work_time, free_text):
    result = init_result(role, establishment, establishment_data, job_type, contract_type, work_time, theme, need)
    free_text_lower = (free_text or "").lower()
    ccn = establishment_data["ccn"]

    # =====================================================
    # 1. MA PAIE / MON BULLETIN
    # =====================================================
    if theme == "Ma paie / Mon bulletin":
        if need == "Je ne comprends pas mon salaire ce mois-ci":
            result["title"] = "Comprendre le salaire du mois"
            result["summary"] = "Une variation de salaire doit d’abord être rapprochée des absences, variables, primes, acomptes, régularisations ou changements contractuels du mois."
            result["checks"] = [
                "Comparer avec le bulletin du mois précédent.",
                "Vérifier l’existence d’une absence, d’un acompte ou d’une retenue.",
                "Vérifier si une prime ou un variable habituel manque.",
                "Contrôler s’il existe une régularisation sur le bulletin.",
            ]
            result["action"] = "Comparer le bulletin avec le mois précédent puis, si l’écart persiste, transmettre un message détaillé à la paie."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Analyse d’écart de paie"

        elif need == "Mon salaire a baissé / augmenté":
            result["title"] = "Variation de salaire"
            result["summary"] = "Une baisse ou une hausse de salaire peut résulter d’un variable, d’une absence, d’une prime, d’une régularisation ou d’une évolution de situation."
            result["checks"] = [
                "Vérifier les absences du mois.",
                "Vérifier la présence d’un acompte.",
                "Vérifier les primes, indemnités ou variables saisis.",
                "Contrôler si une régularisation figure sur le bulletin.",
            ]
            result["action"] = "Préparez le mois concerné et l’élément qui vous semble anormal avant transmission au support RH / paie."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Variation salariale"

        elif need == "Il manque des heures (FFP / induites / supplémentaires)":
            result["title"] = "Heures manquantes sur le bulletin"
            result["summary"] = "Les heures absentes du bulletin peuvent provenir d’un retard de transmission, de validation, d’un problème de saisie ou d’un décalage de paie."
            result["checks"] = [
                "Identifier le type d’heures concerné : FFP, induites ou supplémentaires.",
                "Vérifier que les heures ont bien été transmises et validées.",
                "Vérifier la période de réalisation des heures.",
                "Comparer avec les éléments saisis ou remontés.",
            ]
            result["action"] = "Rassemblez les éléments de transmission et de validation puis sollicitez le bon interlocuteur."
            result["contact"] = "Responsable / RH / Paie"
            result["channel"] = "Mail"
            result["contact_reason"] = "Heures non visibles en paie"

        elif need == "Il manque une prime / indemnité":
            result["title"] = "Prime ou indemnité manquante"
            result["summary"] = "Une prime ou une indemnité manquante peut résulter d’un oubli de saisie, d’un décalage de validation ou d’une condition d’attribution non remplie."
            result["checks"] = [
                "Identifier précisément la prime ou l’indemnité attendue.",
                "Vérifier le mois concerné.",
                "Vérifier si la condition d’attribution était bien remplie.",
                "Contrôler si un décalage de versement est possible.",
            ]
            result["action"] = "Adressez une demande ciblée en précisant le type de prime, le mois et le motif attendu."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Prime / indemnité absente"

        elif need == "Je ne comprends pas une ligne du bulletin":
            result["title"] = "Lecture d’une ligne du bulletin"
            result["summary"] = "Pour expliquer correctement une ligne du bulletin, il faut identifier le libellé exact, la base, le taux et la période de calcul."
            result["checks"] = [
                "Relever le libellé exact de la ligne.",
                "Identifier la base et le taux si visibles.",
                "Comparer avec le bulletin précédent.",
                "Vérifier s’il s’agit d’une régularisation ou d’une ligne habituelle.",
            ]
            result["action"] = "Transmettez le libellé exact ou une capture ciblée de la ligne concernée."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Explication d’une ligne de bulletin"

        elif need == "Je pense qu’il y a une erreur sur mon bulletin":
            result["title"] = "Suspicion d’erreur sur le bulletin"
            result["summary"] = "Une erreur de bulletin doit être décrite précisément afin de distinguer un vrai écart d’une ligne normale ou d’une régularisation."
            result["checks"] = [
                "Identifier la rubrique concernée.",
                "Préciser le mois du bulletin.",
                "Comparer avec un mois antérieur si nécessaire.",
                "Préciser l’écart constaté.",
            ]
            result["action"] = "Rédigez un message clair en précisant la rubrique, le mois et l’écart constaté."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Vérification d’erreur de bulletin"

        elif need == "Je veux comprendre mon net à payer":
            result["title"] = "Comprendre le net à payer"
            result["summary"] = "Le net à payer dépend du brut, des cotisations, des retenues, des acomptes éventuels et des éléments variables du mois."
            result["checks"] = [
                "Vérifier le salaire brut du mois.",
                "Vérifier les cotisations et retenues.",
                "Vérifier la présence d’un acompte.",
                "Identifier les primes ou absences influençant le net.",
            ]
            result["action"] = "Si besoin, demandez une explication détaillée du calcul du net à payer."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Explication net à payer"

        elif need == "Je veux comprendre le net social":
            result["title"] = "Comprendre le net social"
            result["summary"] = "Le net social est un indicateur distinct du net à payer. Il peut différer selon les rubriques prises en compte dans le calcul."
            result["checks"] = [
                "Comparer net social et net à payer.",
                "Vérifier la présence de rubriques particulières.",
                "Identifier le mois concerné.",
                "Comparer avec un bulletin précédent si utile.",
            ]
            result["action"] = "Demandez une explication ciblée du net social si l’écart avec le net à payer vous semble incompris."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Explication net social"

        elif need == "Je veux comprendre mes cotisations":
            result["title"] = "Comprendre les cotisations"
            result["summary"] = "Les cotisations peuvent varier selon la situation contractuelle, le statut, la rémunération et certaines régularisations."
            result["checks"] = [
                "Identifier les cotisations concernées.",
                "Comparer avec un bulletin antérieur.",
                "Vérifier si le statut ou la rémunération a évolué.",
                "Contrôler s’il existe une régularisation.",
            ]
            result["action"] = "Adressez une demande en citant les cotisations que vous souhaitez comprendre."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Explication cotisations"

        else:
            result["title"] = "Sujet paie à préciser"
            result["summary"] = "Votre demande paie n’entre pas dans un cas standard clairement identifié."
            result["checks"] = [
                "Préciser la rubrique concernée.",
                "Préciser le mois concerné.",
                "Décrire l’écart constaté.",
            ]
            result["action"] = "Utilisez le message prêt à transmettre pour formuler votre demande au RH / Paie."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Sujet paie hors cas standard"

    # =====================================================
    # 2. MON PORTAIL PAIE
    # =====================================================
    elif theme == "Mon Portail Paie":
        result["title"] = "Assistance Mon Portail Paie"
        result["contact"] = "Support RH / Paie ou support SIRH"
        result["channel"] = "Support"
        result["contact_reason"] = "Blocage ou question d’usage du portail"

        if need == "Je n’arrive pas à me connecter":
            result["summary"] = "Un problème de connexion doit être vérifié avant escalade : bon lien, bon identifiant, navigateur, mot de passe."
            result["checks"] = [
                "Vérifier que vous utilisez le bon portail.",
                "Tester un autre navigateur ou une navigation privée.",
                "Vérifier l’identifiant utilisé.",
                "Tester la fonction mot de passe oublié si disponible.",
            ]
            result["action"] = "Si le blocage persiste, signalez le message d’erreur exact au support."

        elif need == "Je ne vois pas mes bulletins":
            result["summary"] = "L’absence de bulletin dans le portail peut provenir d’un délai de mise à disposition, d’un problème d’accès ou d’un mauvais espace."
            result["checks"] = [
                "Vérifier la période concernée.",
                "Vérifier que vous êtes dans le bon espace.",
                "Vérifier si le bulletin a déjà été publié.",
            ]
            result["action"] = "Signalez le mois concerné si le bulletin reste absent."

        elif need == "Je ne vois pas mes tickets restaurant":
            result["summary"] = "L’absence de visibilité des tickets restaurant dans le portail peut relever soit du portail, soit du circuit de distribution."
            result["checks"] = [
                "Vérifier si le sujet concerne le portail ou la carte Edenred.",
                "Vérifier la période concernée.",
                "Vérifier si un délai de chargement est en cours.",
            ]
            result["action"] = "Précisez s’il s’agit d’un souci d’affichage portail ou d’un problème de droits."

        elif need == "Je ne vois pas mes jours de télétravail":
            result["summary"] = "Les jours de télétravail visibles dans le portail dépendent du module concerné et des validations associées."
            result["checks"] = [
                "Vérifier le module utilisé.",
                "Vérifier si les demandes sont validées.",
                "Vérifier la période affichée.",
            ]
            result["action"] = "Vérifiez le module Mon travail hybride puis signalez le problème si besoin."

        elif need == "Je ne comprends pas comment utiliser le portail":
            result["summary"] = "Le besoin porte sur un accompagnement d’usage du portail."
            result["checks"] = [
                "Identifier le module concerné.",
                "Préciser l’action souhaitée.",
                "Préciser l’étape bloquante.",
            ]
            result["action"] = "Décrivez précisément l’action que vous souhaitez réaliser."

        elif need == "Je veux modifier une information":
            result["summary"] = "Selon l’information à modifier, l’action peut relever du portail, du support SIRH ou du RH."
            result["checks"] = [
                "Identifier l’information à modifier.",
                "Vérifier si le champ est modifiable directement.",
                "Préciser si un message d’erreur apparaît.",
            ]
            result["action"] = "Précisez l’information concernée et l’étape qui bloque."

        else:
            result["summary"] = "Votre besoin portail n’entre pas dans un cas standard totalement qualifié."
            result["checks"] = [
                "Préciser le module concerné.",
                "Préciser l’action attendue.",
                "Décrire le blocage rencontré.",
            ]
            result["action"] = "Utilisez le message prêt à transmettre au support."

    # =====================================================
    # 3. ABSENCES / ARRÊTS
    # =====================================================
    elif theme == "Absences / Arrêts":
        if need == "Je veux signaler un arrêt de travail" or "maladie" in free_text_lower or "maternité" in free_text_lower or "accident du travail" in free_text_lower:
            result["title"] = "Signalement d'arrêt ou d'absence hors portail"
            result["summary"] = "Les absences de type maladie, maternité et accident du travail ne passent pas par le portail et doivent être signalées directement au chargé RH / Paie."
            result["checks"] = [
                "Identifier la nature exacte de l’absence.",
                "Vérifier la date de début.",
                "Préparer le justificatif si disponible.",
                "Confirmer le bon interlocuteur RH / Paie.",
            ]
            result["action"] = "Contactez directement votre chargé RH / Paie."
            result["contact"] = "Chargé RH / Paie"
            result["channel"] = "Signalement direct RH / Paie"
            result["contact_reason"] = "Cas exclu du portail"
        elif need == "Je veux déclarer une absence":
            result["title"] = "Déclaration d’absence"
            result["summary"] = "Par défaut, les absences doivent être déclarées dans Mon Portail Paie, sauf maladie, maternité et accident du travail."
            result["checks"] = [
                "Choisir le bon motif d’absence.",
                "Vérifier la période concernée.",
                "Préparer un justificatif si nécessaire.",
            ]
            result["action"] = "Faites votre demande dans Mon Portail Paie."
            result["contact"] = "Mon Portail Paie"
            result["channel"] = "Portail"
            result["contact_reason"] = "Règle générale absences"
        elif need == "Quels types d’absence existent ?":
            result["title"] = "Typologie des absences"
            result["summary"] = "La plupart des absences courantes se déclarent dans le portail, tandis que certaines situations spécifiques doivent être signalées directement au RH / Paie."
            result["checks"] = [
                "Vérifier si l’absence relève d’un motif standard.",
                "Vérifier si la situation concerne maladie, maternité ou accident du travail.",
            ]
            result["action"] = "Utilisez le portail pour les absences standard. Pour maladie, maternité ou accident du travail, passez directement par le RH / Paie."
            result["contact"] = "Mon Portail Paie / Chargé RH / Paie"
            result["channel"] = "Portail ou RH direct"
            result["contact_reason"] = "Orientation selon motif"
        elif need == "Je veux savoir si mon absence est payée":
            result["title"] = "Absence payée ou non"
            result["summary"] = "Le caractère payé ou non d’une absence dépend du motif, de la situation du salarié et du traitement applicable."
            result["checks"] = [
                "Identifier le motif exact de l’absence.",
                "Vérifier la période concernée.",
                "Préciser le contexte si nécessaire.",
            ]
            result["action"] = "Précisez le motif d’absence pour obtenir une confirmation fiable."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Impact absence"
        elif need == "Je veux comprendre l’impact sur ma paie":
            result["title"] = "Impact d’une absence sur la paie"
            result["summary"] = "Une absence peut modifier le brut, le net, certaines primes ou des droits associés selon son motif et sa durée."
            result["checks"] = [
                "Identifier le motif d’absence.",
                "Vérifier les dates exactes.",
                "Comparer avec le bulletin concerné si déjà édité.",
            ]
            result["action"] = "Précisez le motif et la période de l’absence pour analyse RH / paie."
            result["contact"] = "Support RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Impact paie lié à l’absence"
        elif need == "Je veux régulariser une absence":
            result["title"] = "Régularisation d’absence"
            result["summary"] = "Une régularisation d’absence suppose de vérifier le motif, la période et le canal de correction attendu."
            result["checks"] = [
                "Vérifier le motif initial saisi.",
                "Vérifier la période à corriger.",
                "Identifier si la demande doit être refaite ou signalée.",
            ]
            result["action"] = "Précisez l’absence concernée et la correction attendue."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie ou portail selon cas"
            result["contact_reason"] = "Correction d’une absence"
        else:
            result["title"] = "Demande absence à préciser"
            result["summary"] = "Votre demande sur les absences nécessite une précision complémentaire."
            result["checks"] = [
                "Préciser le motif.",
                "Préciser la période.",
                "Préciser si le portail a déjà été utilisé.",
            ]
            result["action"] = "Utilisez le message prêt à transmettre au RH."

    # =====================================================
    # 4. CONGÉS / RTT / RÉCUP
    # =====================================================
    elif theme == "Congés / RTT / Récup":
        result["title"] = "Congés / RTT / Récupération"
        result["contact"] = "Mon Portail Paie / RH"
        result["channel"] = "Portail puis RH si besoin"
        result["contact_reason"] = "Gestion des droits et demandes"

        if need == "Combien de congés il me reste":
            result["summary"] = "Le solde de congés doit être consulté dans l’outil dédié, sous réserve des mises à jour et validations en cours."
            result["checks"] = [
                "Vérifier le solde affiché dans le portail.",
                "Vérifier si des demandes récentes sont en attente.",
            ]
            result["action"] = "Consultez votre solde dans le portail puis signalez un écart si nécessaire."

        elif need == "Comment poser un congé":
            result["summary"] = "Les congés doivent être demandés via le portail dans le bon module et selon le bon motif."
            result["checks"] = [
                "Choisir le bon type de congé.",
                "Vérifier la période demandée.",
                "Vérifier le niveau de validation attendu.",
            ]
            result["action"] = "Déposez votre demande via le portail."

        elif need == "Délais de validation":
            result["summary"] = "Le délai dépend des circuits internes de validation et des pratiques de l’établissement."
            result["checks"] = [
                "Vérifier si la demande a bien été transmise.",
                "Vérifier le niveau de validation bloquant.",
            ]
            result["action"] = "Relancez si la demande reste en attente de manière inhabituelle."

        elif need == "Refus de congé":
            result["summary"] = "Un refus peut relever d’une contrainte d’organisation, de calendrier ou d’un problème de saisie."
            result["checks"] = [
                "Vérifier le motif du refus.",
                "Vérifier les dates demandées.",
                "Vérifier si un échange manager a déjà eu lieu.",
            ]
            result["action"] = "Demandez le motif précis du refus si nécessaire."

        elif need == "RTT / JRS comment ça marche":
            result["summary"] = "Le fonctionnement des RTT ou JRS dépend du statut, du temps de travail et de l’organisation applicable."
            result["checks"] = [
                "Vérifier le statut du salarié.",
                "Vérifier si le collaborateur est en forfait jours ou en heures.",
                "Vérifier les droits affichés dans le portail.",
            ]
            result["action"] = "Précisez votre statut si vous avez besoin d’une réponse plus ciblée."

        elif need == "Report / perte de congés":
            result["summary"] = "Le report ou la perte de congés dépend des règles internes, des périodes de prise et des situations particulières."
            result["checks"] = [
                "Vérifier la période de référence.",
                "Vérifier si des congés sont en attente.",
                "Vérifier les règles applicables localement.",
            ]
            result["action"] = "Sollicitez une confirmation RH si vous craignez une perte de droits."

        else:
            result["summary"] = "Votre demande congés / RTT / récup nécessite une précision complémentaire."
            result["checks"] = [
                "Préciser le type de droit concerné.",
                "Préciser la période.",
                "Préciser l’action souhaitée.",
            ]
            result["action"] = "Utilisez le message prêt à transmettre."

    # =====================================================
    # 5. TÉLÉTRAVAIL
    # =====================================================
    elif theme == "Télétravail":
        result["title"] = "Télétravail : gestion via Mon Portail Paie"
        result["contact"] = "Mon Portail Paie / Manager / RH"
        result["channel"] = "Portail puis validation manager"
        result["contact_reason"] = "Télétravail géré via portail"

        if need == "Combien de jours j’ai droit":
            result["summary"] = "Le nombre de jours de télétravail dépend du poste, du pôle et de l’accord applicable."
            result["checks"] = [
                "Vérifier si vous êtes en école ou en services support.",
                "Vérifier votre forfait applicable.",
                "Vérifier si une dérogation existe.",
            ]
            result["action"] = "Consultez vos droits dans le portail puis demandez confirmation si besoin."
            result["vigilance"].append("En école : forfait indicatif de 0 à 44 jours. En services support : forfait indicatif de 0 à 60 jours.")
        elif need == "Comment poser un jour":
            result["summary"] = "Les jours de télétravail doivent être saisis dans Mon Portail Paie via le module de travail hybride."
            result["checks"] = [
                "Choisir la bonne date.",
                "Vérifier si la demande est ponctuelle ou récurrente.",
                "Vérifier le circuit de validation manager.",
            ]
            result["action"] = "Passez par Mon Portail Paie > Planning et droits congés > Mon travail hybride."
        elif need == "Mon manager refuse":
            result["summary"] = "Le refus d’un jour de télétravail relève généralement d’une contrainte d’organisation ou d’un cadre non conforme."
            result["checks"] = [
                "Vérifier si le quota est disponible.",
                "Vérifier si la demande respecte le cadre applicable.",
                "Vérifier si un échange explicatif a eu lieu.",
            ]
            result["action"] = "Échangez avec votre manager puis sollicitez le RH si la situation nécessite un arbitrage."
        elif need == "Je veux modifier mes jours":
            result["summary"] = "La modification des jours de télétravail passe par le portail, sous réserve du statut de validation de la demande."
            result["checks"] = [
                "Vérifier si la demande est déjà validée.",
                "Vérifier la date concernée.",
            ]
            result["action"] = "Modifiez la demande dans le portail si possible, sinon sollicitez le bon validateur."
        elif need == "Impact sur paie / indemnité":
            result["summary"] = "Un sujet de télétravail peut avoir un impact indirect selon le cadre applicable, mais il doit d’abord être qualifié précisément."
            result["checks"] = [
                "Préciser l’impact supposé.",
                "Préciser la période concernée.",
                "Préciser s’il s’agit d’un problème de saisie, de validation ou d’indemnité.",
            ]
            result["action"] = "Décrivez le point d’impact exact pour obtenir une réponse ciblée."
        elif need == "Problème sur portail":
            result["summary"] = "Le blocage semble relever soit du module télétravail, soit d’un problème technique d’accès ou d’affichage."
            result["checks"] = [
                "Vérifier le message d’erreur éventuel.",
                "Vérifier le module utilisé.",
                "Tester un autre navigateur si besoin.",
            ]
            result["action"] = "Transmettez le message d’erreur exact si le blocage persiste."
        else:
            result["summary"] = "Votre demande télétravail nécessite une précision complémentaire."
            result["checks"] = [
                "Préciser la date ou la période.",
                "Préciser si le portail a déjà été utilisé.",
                "Préciser l’étape bloquante.",
            ]
            result["action"] = "Utilisez le message prêt à transmettre."

        if "2 heures" in free_text_lower or "2h" in free_text_lower or "temps de trajet" in free_text_lower:
            result["alerts"].append("Dérogation potentielle détectée : temps de trajet domicile ↔ bureau supérieur à 2 heures aller-retour.")
            result["vigilance"].append("Le calcul du temps de trajet est effectué exclusivement par le RRH via Google Maps.")
        if "rqth" in free_text_lower or "handicap" in free_text_lower:
            result["alerts"].append("Dérogation potentielle détectée : situation RQTH.")
            result["vigilance"].append("Une adaptation éventuelle nécessite validation par la médecine du travail, le référent handicap et le RRH.")
        if "province" in free_text_lower or "décision judiciaire" in free_text_lower or "decision judiciaire" in free_text_lower:
            result["alerts"].append("Situation spécifique détectée : une validation DRH peut être nécessaire.")

    # =====================================================
    # 6. ACOMPTE SUR SALAIRE
    # =====================================================
    elif theme == "Acompte sur salaire":
        result["title"] = "Acompte sur salaire"
        result["summary"] = "La demande d’acompte se fait exclusivement via Mon Portail Paie. Elle ne doit pas être adressée par mail ni directement au RH."
        result["checks"] = [
            "Vérifier que la demande est faite entre le 1er jour du mois et le 11 à minuit.",
            "Vérifier que le montant demandé ne dépasse pas 50 % du salaire.",
            "Vérifier si des variables peuvent encore ajuster le salaire entre le 7 et le 11.",
        ]
        result["action"] = "Effectuez ou suivez votre demande dans Mon Portail Paie."
        result["contact"] = "Mon Portail Paie / Paie"
        result["channel"] = "Portail"
        result["contact_reason"] = "Acompte géré exclusivement via portail"
        result["vigilance"].append("Le salaire peut être ajusté entre le 7 et le 11 selon les absences, primes et variables remontées.")

    # =====================================================
    # 7. HEURES / ACTIVITÉ
    # =====================================================
    elif theme == "Heures / Activité":
        result["title"] = "Heures / Activité"
        result["contact"] = "Responsable / RH / Paie"
        result["channel"] = "Mail ou circuit de validation"
        result["contact_reason"] = "Suivi et traitement des heures"

        if need == "Mes heures FFP ne sont pas correctes":
            result["summary"] = "Un écart sur les heures FFP suppose de vérifier la remontée pédagogique, la validation et la période de paie concernée."
            result["checks"] = [
                "Vérifier le volume d’heures FFP attendu.",
                "Vérifier la remontée ou transmission pédagogique.",
                "Vérifier la validation de ces heures.",
                "Vérifier le mois de paie concerné.",
            ]
            result["action"] = "Préparez les éléments de transmission et de validation avant sollicitation."
        elif need == "Heures induites manquantes":
            result["summary"] = "Des heures induites absentes peuvent relever d’une remontée incomplète, d’une règle de calcul ou d’un décalage de traitement."
            result["checks"] = [
                "Vérifier le volume attendu.",
                "Vérifier les éléments transmis.",
                "Vérifier la période concernée.",
            ]
            result["action"] = "Demandez une vérification du calcul et de la remontée associée."
        elif need == "Heures supplémentaires non payées":
            result["summary"] = "Des heures supplémentaires non payées peuvent résulter d’un défaut de saisie, d’un manque de validation ou d’un décalage de paie."
            result["checks"] = [
                "Vérifier la déclaration des heures.",
                "Vérifier la validation manager ou responsable.",
                "Vérifier le mois de paiement attendu.",
            ]
            result["action"] = "Vérifiez le circuit de validation puis sollicitez la paie si l’écart persiste."
        elif need == "Heures validées mais non payées":
            result["summary"] = "Si les heures sont validées mais absentes du bulletin, il faut vérifier le décalage de paie ou une anomalie de reprise."
            result["checks"] = [
                "Vérifier la date de validation.",
                "Vérifier le bulletin concerné.",
                "Vérifier si un décalage de traitement est normal.",
            ]
            result["action"] = "Transmettez la preuve de validation avec le mois de paie concerné."
        elif need == "Problème de transmission des heures":
            result["summary"] = "Le problème peut se situer au niveau de la saisie, de la remontée ou du circuit de validation."
            result["checks"] = [
                "Identifier le canal de transmission utilisé.",
                "Vérifier si la transmission a bien été faite.",
                "Identifier l’étape bloquante.",
            ]
            result["action"] = "Précisez où le circuit semble bloqué."
        elif need == "Je veux comprendre le calcul":
            result["summary"] = "Le calcul des heures doit être rapproché du type d’heures, de la période et des règles applicables."
            result["checks"] = [
                "Identifier le type d’heures concerné.",
                "Identifier la période.",
                "Vérifier les éléments de base utilisés.",
            ]
            result["action"] = "Précisez le type d’heures et la période pour obtenir une réponse plus ciblée."
        else:
            result["summary"] = "Votre demande heures / activité nécessite une précision complémentaire."
            result["checks"] = [
                "Préciser le type d’heures.",
                "Préciser la période.",
                "Préciser le circuit de validation.",
            ]
            result["action"] = "Utilisez le message prêt à transmettre."

    # =====================================================
    # 8. MUTUELLE / PRÉVOYANCE
    # =====================================================
    elif theme == "Mutuelle / Prévoyance":
        result["title"] = "Mutuelle / Prévoyance"
        result["summary"] = "À l’embauche, le salarié est automatiquement inscrit auprès du partenaire mutuelle. L’affiliation ou la dispense doit ensuite être finalisée selon le parcours prévu."
        result["checks"] = [
            "Vérifier l’adresse personnelle renseignée sur Workday.",
            "Vérifier si le délai de 15 à 20 jours après prise de poste est écoulé.",
            "Identifier si le besoin concerne adhésion, dispense, remboursement, bénéficiaire ou cotisation.",
        ]
        result["action"] = "Surveillez l’adresse personnelle utilisée pour l’affiliation. Si le délai est dépassé ou si le blocage persiste, sollicitez le chargé RH."
        result["contact"] = "Partenaire mutuelle / Chargé RH"
        result["channel"] = "Mutuelle puis RH si nécessaire"
        result["contact_reason"] = "Mutuelle gérée avec partenaire, RH en relai"
        result["vigilance"].append("Le salarié dispose de 2 mois pour finaliser son affiliation. Au-delà, un nouveau lien doit être demandé au RH.")
        result["vigilance"].append("Une dispense doit être demandée pour chaque contrat.")
        result["vigilance"].append("Les remboursements liés à une dispense tardive ne peuvent pas excéder 2 mois.")

    # =====================================================
    # 9. TRANSPORT
    # =====================================================
    elif theme == "Transport":
        if need == "Remboursement Navigo" or "ratp" in free_text_lower or "navigo" in free_text_lower:
            result["title"] = "Transport RATP / Navigo"
            result["summary"] = "Les demandes de remboursement transport RATP doivent être faites via Mon Portail Paie."
            result["checks"] = [
                "Vérifier que le titre concerné relève bien de la RATP / Navigo.",
                "Préparer le justificatif si nécessaire.",
                "Vérifier la période concernée.",
            ]
            result["action"] = "Effectuez votre demande via Mon Portail Paie."
            result["contact"] = "Mon Portail Paie"
            result["channel"] = "Portail"
            result["contact_reason"] = "Transport RATP"
        else:
            result["title"] = "Transport hors RATP"
            result["summary"] = "Les autres demandes transport ne passent pas par le portail et doivent être adressées au chargé RH de proximité."
            result["checks"] = [
                "Identifier le type de transport concerné.",
                "Préparer le justificatif adapté.",
                "Préciser la période de remboursement demandée.",
            ]
            result["action"] = "Adressez votre demande par mail au chargé RH de proximité."
            result["contact"] = "Chargé RH de proximité"
            result["channel"] = "Mail"
            result["contact_reason"] = "Transport hors RATP"

    # =====================================================
    # 10. TICKETS RESTAURANT
    # =====================================================
    elif theme == "Tickets restaurant":
        result["title"] = "Tickets restaurant"
        result["contact"] = "RH / Support titres restaurant"
        result["channel"] = "Mail RH ou support selon le cas"
        result["contact_reason"] = "Gestion des droits ou du support carte"

        if need == "Je ne les ai pas reçus":
            result["summary"] = "L’absence de tickets restaurant peut relever d’un délai de distribution, d’un problème de droits ou d’un incident de chargement."
        elif need == "Montant incorrect":
            result["summary"] = "Un montant incorrect suppose de vérifier le nombre de jours éligibles et la période concernée."
        elif need == "Nombre incorrect":
            result["summary"] = "Le nombre de tickets restaurant dépend généralement de la présence et des règles d’éligibilité applicables."
        elif need == "Carte Edenred problème":
            result["summary"] = "Le problème semble relever de la carte ou du service associé."
        else:
            result["summary"] = "Votre demande tickets restaurant nécessite une précision complémentaire."

        result["checks"] = [
            "Vérifier la période concernée.",
            "Vérifier s’il s’agit d’un problème de droits, de nombre, de montant ou de carte.",
            "Vérifier si le blocage est technique ou administratif.",
        ]
        result["action"] = "Précisez la période et la nature du blocage pour orientation correcte."

    # =====================================================
    # 11. DOCUMENTS RH / PAIE
    # =====================================================
    elif theme == "Documents RH / Paie":
        result["title"] = "Documents RH / Paie"
        result["summary"] = "Le traitement dépend du type de document demandé et du canal habituel de mise à disposition."
        result["checks"] = [
            "Identifier le document demandé.",
            "Préciser la période si nécessaire.",
            "Vérifier si le document est déjà disponible dans le portail ou l’espace documentaire.",
        ]
        result["action"] = "Précisez le document demandé et l’urgence éventuelle."
        result["contact"] = "RH / Paie"
        result["channel"] = "Mail RH / Paie"
        result["contact_reason"] = "Émission ou récupération de document"

    # =====================================================
    # 12. SORTIE / FIN DE CONTRAT
    # =====================================================
    elif theme == "Sortie / Fin de contrat":
        result["title"] = "Sortie / Fin de contrat"
        result["summary"] = "Les sujets de sortie nécessitent de vérifier la date de fin, les documents attendus et les éventuelles indemnités de fin de contrat."
        result["checks"] = [
            "Vérifier la date de fin de contrat.",
            "Identifier les documents attendus.",
            "Préciser si le sujet porte sur le solde de tout compte ou une indemnité.",
        ]
        result["action"] = "Précisez la date de fin et le document ou montant concerné."
        result["contact"] = "RH / Paie"
        result["channel"] = "Mail RH / Paie"
        result["contact_reason"] = "Gestion de sortie"
        if contract_type == "CDD":
            result["vigilance"].append("En CDD, la vérification des documents et indemnités de fin de contrat est particulièrement importante.")

    # =====================================================
    # 13. CONTRAT / STATUT
    # =====================================================
    elif theme == "Contrat / Statut":
        result["title"] = "Contrat / Statut"
        result["summary"] = "Le besoin concerne la nature du contrat, le temps de travail, le forfait ou une évolution de statut."
        result["checks"] = [
            "Identifier l’élément contractuel concerné.",
            "Préciser la situation actuelle.",
            "Préciser la modification ou la compréhension attendue.",
        ]
        result["action"] = "Décrivez le point contractuel que vous souhaitez faire vérifier."
        result["contact"] = "RH"
        result["channel"] = "Mail RH"
        result["contact_reason"] = "Sujet contractuel"

    # =====================================================
    # 14. DEMANDE MANAGER
    # =====================================================
    elif theme == "Demande manager":
        result["title"] = "Demande manager"
        result["summary"] = "La demande concerne un besoin de pilotage, de validation ou d’accompagnement RH sur un collaborateur ou une organisation."
        result["checks"] = [
            "Identifier le collaborateur ou le périmètre concerné.",
            "Préciser le blocage ou la demande attendue.",
            "Préciser si le sujet relève de la paie, des absences, des heures ou de l’organisation.",
        ]
        result["action"] = "Décrivez le besoin manager de façon précise pour orienter la demande au bon interlocuteur."
        result["contact"] = "RH / Paie / Support selon le sujet"
        result["channel"] = "Mail RH"
        result["contact_reason"] = "Demande d’encadrement ou de pilotage"

    # =====================================================
    # 15. AUTRE DEMANDE
    # =====================================================
    elif theme == "Autre demande":
        result["title"] = "Sujet non trouvé"
        result["summary"] = "Votre demande n’entre pas encore dans une catégorie standard traitée par KAREN."
        result["checks"] = [
            "Décrire le besoin de façon concrète.",
            "Préciser le contexte, la période et le blocage.",
            "Préciser l’interlocuteur déjà sollicité s’il y en a un.",
        ]
        result["action"] = "KAREN prépare un message RH prêt à transmettre pour sécuriser l’orientation."
        result["contact"] = "RH / Paie"
        result["channel"] = "Mail RH / Paie"
        result["contact_reason"] = "Sujet hors référentiel standard"

    score = get_complexity_score(theme, need, free_text, job_type)
    result["complexity_score"] = score
    result["complexity_label"] = get_complexity_label(score)

    apply_transversal_alerts(result, role, job_type, contract_type, work_time, ccn)

    return result

# =========================================================
# STYLE
# =========================================================
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #0f172a 0%, #172554 45%, #0f172a 100%);
            color: #f8fafc;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111827 0%, #0b1120 100%);
            border-right: 1px solid rgba(255,255,255,0.06);
        }
        .karen-card {
            background: rgba(17,24,39,0.92);
            border-radius: 22px;
            padding: 1.2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.06);
            margin-bottom: 1rem;
            backdrop-filter: blur(4px);
        }
        .hero-card {
            background: linear-gradient(135deg, #1e3a8a 0%, #991b1b 100%);
            border-radius: 24px;
            padding: 1.4rem;
            color: white;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
            margin-bottom: 1rem;
        }
        .karen-title {
            font-size: 2.2rem;
            font-weight: 900;
            letter-spacing: 0.5px;
            color: white;
            margin-bottom: 0.15rem;
        }
        .karen-subtitle {
            font-size: 1rem;
            color: #fee2e2;
            margin-bottom: 0.75rem;
        }
        .section-title {
            font-size: 1.08rem;
            font-weight: 800;
            color: #93c5fd;
            margin-bottom: 0.45rem;
        }
        .small-note {
            font-size: 0.94rem;
            color: #e5e7eb;
        }
        .metric-pill {
            display: inline-block;
            padding: 0.42rem 0.8rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
            color: white;
            font-size: 0.9rem;
            margin-right: 0.45rem;
            margin-bottom: 0.35rem;
        }
        .warning-box {
            background: #450a0a;
            border-left: 5px solid #dc2626;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: white;
        }
        .info-box {
            background: #082f49;
            border-left: 5px solid #38bdf8;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: white;
        }
        .success-box {
            background: #052e16;
            border-left: 5px solid #22c55e;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: white;
        }
        .thinking-ring {
            width: 42px;
            height: 42px;
            border: 4px solid rgba(255,255,255,0.18);
            border-top: 4px solid #60a5fa;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0.2rem auto 0.6rem auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #991b1b 0%, #dc2626 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            padding: 0.7rem 1rem;
        }
        .stButton > button:hover {
            filter: brightness(1.05);
        }
        div[data-baseweb="select"] > div,
        .stTextInput input,
        .stTextArea textarea {
            background-color: #0b1220 !important;
            color: white !important;
            border-radius: 12px !important;
        }
        div[data-baseweb="popover"] * {
            color: #ffffff !important;
            background-color: #0b1220 !important;
        }
        li[role="option"] {
            color: #ffffff !important;
            background-color: #0b1220 !important;
        }
        li[role="option"]:hover {
            background-color: #172554 !important;
        }
        .stSelectbox div[role="combobox"] * {
            color: #ffffff !important;
        }
        .chat-user {
            background: rgba(30,58,138,0.35);
            border: 1px solid rgba(96,165,250,0.35);
            border-radius: 18px 18px 4px 18px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.8rem;
        }
        .chat-karen {
            background: rgba(153,27,27,0.20);
            border: 1px solid rgba(239,68,68,0.25);
            border-radius: 18px 18px 18px 4px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.8rem;
        }
        .chat-label {
            font-size: 0.82rem;
            font-weight: 700;
            color: #93c5fd;
            margin-bottom: 0.35rem;
        }
        .chat-label-user {
            font-size: 0.82rem;
            font-weight: 700;
            color: #fca5a5;
            margin-bottom: 0.35rem;
        }
        .stRadio label,
        .stMarkdown,
        .stCaption,
        .stSelectbox label,
        .stTextArea label,
        .stTextInput label,
        p,
        label,
        span,
        div {
            color: #f8fafc !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## KAREN")
    st.caption("Agent RH / Paie guidé")
    render_avatar_html("idle", width=150)

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
    st.markdown("</div>", unsafe_allow_html=True)

with header_right:
    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    render_avatar_html("idle", width=160)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# INTRO
# =========================================================
st.markdown('<div class="karen-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Parcours intelligent</div>', unsafe_allow_html=True)
st.write(
    "KAREN ne répond pas au hasard. L’outil pose les bonnes questions, qualifie le profil, "
    "prend en compte le contexte RH / paie, puis génère une réponse structurée et actionnable."
)
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "step": 1,
    "role": None,
    "entity": None,
    "job_type": None,
    "contract_type": None,
    "work_time": None,
    "theme": None,
    "need": None,
    "free_text": "",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# PARCOURS
# =========================================================
left, right = st.columns([1.15, 0.85])

with left:
    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Conversation avec KAREN</div>', unsafe_allow_html=True)

    if st.session_state.step == 1:
        st.write("**KAREN :** Bonjour. Votre question vous concerne en tant que ?")
        role = st.radio("Choisissez votre profil", USER_ROLES, key="role_step")
        if st.button("Valider le profil"):
            st.session_state.role = role
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        st.write(f"**KAREN :** Très bien. Profil identifié : **{st.session_state.role}**.")
        entity = st.selectbox("Elle concerne un salarié de quel établissement ?", ESTABLISHMENT_NAMES, key="entity_step")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Retour au profil"):
                st.session_state.step = 1
                st.rerun()
        with c2:
            if st.button("Valider l'établissement"):
                st.session_state.entity = entity
                st.session_state.step = 3
                st.rerun()

    elif st.session_state.step == 3:
        st.write(f"**KAREN :** Établissement enregistré : **{st.session_state.entity}**.")
        job_type = st.selectbox("Quel type d'emploi avez-vous ?", EMPLOYMENT_TYPES, key="job_type_step")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Retour à l'établissement"):
                st.session_state.step = 2
                st.rerun()
        with c2:
            if st.button("Valider le type d'emploi"):
                st.session_state.job_type = job_type
                st.session_state.step = 4
                st.rerun()

    elif st.session_state.step == 4:
        st.write(f"**KAREN :** Type d'emploi retenu : **{st.session_state.job_type}**.")
        contract_type = st.radio("Quel est votre type de contrat ?", CONTRACT_TYPES, key="contract_step", horizontal=True)
        work_time = st.radio("Quel est votre temps de travail ?", WORK_TIMES, key="work_time_step", horizontal=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Retour au type d'emploi"):
                st.session_state.step = 3
                st.rerun()
        with c2:
            if st.button("Valider le contrat et le temps de travail"):
                st.session_state.contract_type = contract_type
                st.session_state.work_time = work_time
                st.session_state.step = 5
                st.rerun()

    elif st.session_state.step == 5:
        st.write("**KAREN :** Nous allons maintenant qualifier votre demande.")
        available_themes = list(THEMES.keys())

        if st.session_state.role == "Manager":
            available_themes = [t for t in available_themes if t != "Demande manager"] + ["Demande manager"]

        theme = st.selectbox("Quel est le thème de votre demande ?", available_themes, key="theme_step")
        need = st.selectbox("Quel est votre besoin précis ?", THEMES[theme], key="need_step")
        free_text = st.text_area(
            "Ajoutez un complément d'information si nécessaire",
            value=st.session_state.free_text,
            placeholder="Exemple : mois concerné, message d’erreur, rubrique du bulletin, RATP, arrêt maladie, délai dépassé, validation manager, FFP, heures induites, Edenred…",
            height=130,
            key="free_text_step",
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Retour"):
                st.session_state.step = 4
                st.rerun()
        with c2:
            if st.button("Réinitialiser"):
                for key in ["role", "entity", "job_type", "contract_type", "work_time", "theme", "need", "free_text"]:
                    st.session_state[key] = None if key != "free_text" else ""
                st.session_state.step = 1
                st.rerun()
        with c3:
            if st.button("Analyser la demande", type="primary"):
                st.session_state.theme = theme
                st.session_state.need = need
                st.session_state.free_text = free_text
                st.session_state.step = 6
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Progression</div>', unsafe_allow_html=True)
    progress_value = (st.session_state.step - 1) / 5 if st.session_state.step <= 6 else 1
    st.progress(progress_value)
    st.caption(f"Étape {min(st.session_state.step, 6)} sur 6")
    if st.session_state.role:
        st.write(f"- Profil : {st.session_state.role}")
    if st.session_state.entity:
        st.write(f"- Établissement : {st.session_state.entity}")
    if st.session_state.job_type:
        st.write(f"- Emploi : {st.session_state.job_type}")
    if st.session_state.contract_type:
        st.write(f"- Contrat : {st.session_state.contract_type}")
    if st.session_state.work_time:
        st.write(f"- Temps : {st.session_state.work_time}")
    if st.session_state.theme and st.session_state.step < 6:
        st.write(f"- Thème : {st.session_state.theme}")
    if st.session_state.need and st.session_state.step < 6:
        st.write(f"- Besoin : {st.session_state.need}")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ANALYSE FINALE
# =========================================================
if st.session_state.step == 6 and st.session_state.theme and st.session_state.need:
    thinking_placeholder = st.empty()
    with thinking_placeholder.container():
        st.markdown('<div class="karen-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">KAREN analyse votre demande</div>', unsafe_allow_html=True)
        render_avatar_html("thinking", width=170)
        st.markdown('<div class="thinking-ring"></div>', unsafe_allow_html=True)
        st.write("Qualification du profil, lecture du besoin, application des règles métier et préparation de la réponse...")
        st.markdown("</div>", unsafe_allow_html=True)

    time.sleep(0.8)

    establishment_data = get_establishment_data(st.session_state.entity)

    result = build_rule_based_response(
        st.session_state.theme,
        st.session_state.need,
        st.session_state.role,
        st.session_state.entity,
        establishment_data,
        st.session_state.job_type,
        st.session_state.contract_type,
        st.session_state.work_time,
        st.session_state.free_text,
    )

    subject, support_message = build_support_message(
        st.session_state.role,
        st.session_state.entity,
        establishment_data,
        st.session_state.job_type,
        st.session_state.contract_type,
        st.session_state.work_time,
        st.session_state.theme,
        st.session_state.need,
        st.session_state.free_text,
    )

    thinking_placeholder.empty()

    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Conversation avec KAREN</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="chat-user">
            <div class="chat-label-user">VOUS</div>
            Bonjour KAREN, je suis <strong>{st.session_state.role}</strong> de l'établissement <strong>{st.session_state.entity}</strong>.
            Mon profil est <strong>{st.session_state.job_type}</strong>, en <strong>{st.session_state.contract_type}</strong>, à <strong>{st.session_state.work_time}</strong>.
            Mon sujet concerne <strong>{st.session_state.theme}</strong> et plus précisément : <strong>{st.session_state.need}</strong>.
            {f'<br><br>Complément transmis : {st.session_state.free_text}' if st.session_state.free_text else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="chat-karen">
            <div class="chat-label">KAREN</div>
            <strong>{result["title"]}</strong><br><br>
            {result["summary"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="karen-card">', unsafe_allow_html=True)
        st.markdown("#### Contexte identifié")
        for line in result["context"]:
            st.write(f"- {line}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="karen-card">', unsafe_allow_html=True)
        st.markdown("#### Vérifications recommandées")
        for item in result["checks"]:
            st.write(f"- {item}")
        st.markdown("</div>", unsafe_allow_html=True)

    if result["alerts"]:
        st.markdown('<div class="info-box"><strong>Diagnostic rapide</strong></div>', unsafe_allow_html=True)
        for alert in result["alerts"]:
            st.write(f"- {alert}")

    if result["vigilance"]:
        st.markdown('<div class="warning-box"><strong>Points de vigilance</strong></div>', unsafe_allow_html=True)
        for item in result["vigilance"]:
            st.write(f"- {item}")

    st.markdown(
        f'<div class="success-box"><strong>Action conseillée :</strong> {result["action"]}</div>',
        unsafe_allow_html=True,
    )
    st.write(f"**Canal recommandé :** {result['channel']}")
    st.write(f"**Interlocuteur recommandé :** {result['contact']}")
    if result["contact_reason"]:
        st.write(f"**Motif d’orientation :** {result['contact_reason']}")

    st.progress(result["complexity_score"] / 5)
    st.caption(f"Score de complexité : {result['complexity_score']} / 5 — {result['complexity_label']}")

    c1, c2 = st.columns([1, 1.3])
    with c1:
        if st.button("Revenir à l'étape précédente"):
            st.session_state.step = 5
            st.rerun()
    with c2:
        if st.button("Nouvelle conversation avec KAREN"):
            for key in ["role", "entity", "job_type", "contract_type", "work_time", "theme", "need", "free_text"]:
                st.session_state[key] = None if key != "free_text" else ""
            st.session_state.step = 1
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown("### Message prêt à transmettre")
    st.text_input("Objet du message", value=subject)
    st.text_area("Contenu du message", value=support_message, height=320)
    st.download_button(
        label="Télécharger le message (.txt)",
        data=f"Objet : {subject}\n\n{support_message}",
        file_name="message_karen.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown("### Réponse KAREN")
    st.write(
        "Avancez étape par étape dans la conversation avec KAREN pour obtenir une réponse structurée, "
        "des vérifications ciblées, des règles métier détectées et un message prêt à transmettre."
    )
    st.markdown("</div>", unsafe_allow_html=True)

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