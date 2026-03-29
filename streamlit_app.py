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
JPO_EXCLUDED_PROFILES = {"Enseignant(e)", "Modèle vivant", "Surveillant(e)"}
TEACHER_JOB = "Enseignant(e)"

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
    "JPO / SPO": [
        "Je sais pas où saisir",
        "Je peux pas poser ma récup",
        "Ma JPO est validée mais j’ai rien",
        "Je veux comprendre le motif à choisir",
        "Je veux comprendre l’impact paie / récupération",
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
        "Je veux savoir si j’y ai droit",
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
# QUESTIONS DYNAMIQUES
# =========================================================
DYNAMIC_QUESTIONS = {
    ("Ma paie / Mon bulletin", "Mon salaire a baissé / augmenté"): [
        {"id": "pay_absence", "label": "Avez-vous eu une absence sur la période concernée ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "pay_variables", "label": "Aviez-vous des éléments variables attendus ce mois-ci ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {
            "id": "pay_before_15",
            "label": "Ces éléments ont-ils été transmis ou validés avant le 15 ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
            "show_if": lambda a: a.get("pay_variables") == "Oui",
        },
        {"id": "pay_acompte", "label": "Avez-vous demandé un acompte ce mois-ci ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "pay_prime", "label": "Attendiez-vous une prime ou une indemnité habituelle ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Ma paie / Mon bulletin", "Il manque des heures (FFP / induites / supplémentaires)"): [
        {"id": "hours_type", "label": "Quel type d'heures est concerné ?", "type": "radio", "options": ["FFP", "Heures induites", "Heures supplémentaires", "Autre / Je ne sais pas"]},
        {"id": "hours_sent", "label": "Les heures ont-elles bien été saisies ou transmises ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "hours_validated", "label": "Les heures ont-elles été validées par le manager / responsable ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {
            "id": "hours_before_15",
            "label": "La transmission ou la validation a-t-elle eu lieu avant le 15 ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
            "show_if": lambda a: a.get("hours_sent") == "Oui" or a.get("hours_validated") == "Oui",
        },
    ],
    ("Heures / Activité", "Mes heures FFP ne sont pas correctes"): [
        {"id": "ffp_validated", "label": "Les heures FFP ont-elles été validées ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "ffp_before_15", "label": "La validation ou la transmission a-t-elle eu lieu avant le 15 ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "ffp_same_month", "label": "Le problème concerne-t-il uniquement le mois en cours ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Heures / Activité", "Heures validées mais non payées"): [
        {"id": "validated_date", "label": "La validation a-t-elle eu lieu avant le 15 ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "bulletin_edited", "label": "Le bulletin du mois concerné est-il déjà disponible ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Heures / Activité", "Problème de transmission des heures"): [
        {"id": "transmission_done", "label": "Les heures ont-elles été transmises dans l'outil ou au bon interlocuteur ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "transmission_block", "label": "À quelle étape le blocage semble-t-il se situer ?", "type": "radio", "options": ["Saisie", "Validation", "Remontée paie", "Je ne sais pas"]},
    ],
    ("Absences / Arrêts", "Je veux signaler un arrêt de travail"): [
        {"id": "stop_medical", "label": "S’agit-il bien d’un arrêt de travail médical ?", "type": "radio", "options": ["Oui", "Non"]},
        {"id": "stop_sent_rh", "label": "Avez-vous déjà transmis l’arrêt au RH de proximité ?", "type": "radio", "options": ["Oui", "Non"]},
        {"id": "stop_urgent", "label": "L’arrêt commence-t-il aujourd’hui ou est-il déjà en cours ?", "type": "radio", "options": ["Oui", "Non"]},
    ],
    ("Absences / Arrêts", "Je veux comprendre l’impact sur ma paie"): [
        {"id": "impact_abs_type", "label": "Le sujet concerne-t-il un arrêt maladie ou une autre absence ?", "type": "radio", "options": ["Arrêt maladie", "Autre absence", "Je ne sais pas"]},
        {"id": "impact_sent_rh", "label": "L’arrêt ou l’information a-t-il été transmis au RH ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "impact_bulletin_done", "label": "Le bulletin du mois concerné est-il déjà édité ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Télétravail", "Mon manager refuse"): [
        {"id": "tt_portal", "label": "La demande de télétravail a-t-elle bien été faite via le portail ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "tt_manager_refusal", "label": "Le refus vient-il explicitement du manager ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "tt_goal", "label": "Souhaitez-vous surtout comprendre la règle ou demander un réexamen ?", "type": "radio", "options": ["Comprendre la règle", "Demander un réexamen"]},
    ],
    ("Acompte sur salaire", "Comment demander un acompte"): [
        {"id": "advance_period", "label": "Êtes-vous entre le 1er jour du mois et le 11 à minuit ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "advance_portal", "label": "Allez-vous faire la demande via Mon Portail Paie ?", "type": "radio", "options": ["Oui", "Non"]},
        {"id": "advance_limit", "label": "Le montant demandé reste-t-il inférieur ou égal à 50 % du salaire ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Acompte sur salaire", "Pourquoi ma demande est refusée"): [
        {"id": "advance_after_11", "label": "La demande a-t-elle été faite après le 11 ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "advance_over_50", "label": "Le montant demandé dépassait-il 50 % du salaire ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "advance_done_portal", "label": "La demande a-t-elle bien été faite via le portail ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Documents RH / Paie", "Attestation employeur"): [
        {"id": "doc_urgency", "label": "Votre demande est-elle urgente ?", "type": "radio", "options": ["Oui", "Non"]},
        {"id": "doc_reason", "label": "Souhaitez-vous préciser l’usage du document ?", "type": "radio", "options": ["Oui", "Non"]},
    ],
    ("Documents RH / Paie", "Attestation de salaire"): [
        {"id": "doc_urgency", "label": "Votre demande est-elle urgente ?", "type": "radio", "options": ["Oui", "Non"]},
    ],
    ("Documents RH / Paie", "Certificat de travail"): [
        {"id": "doc_received", "label": "Avez-vous déjà reçu ce document ?", "type": "radio", "options": ["Oui", "Non"]},
    ],
    ("Documents RH / Paie", "Solde de tout compte"): [
        {"id": "stc_end_date", "label": "La date de fin de contrat est-elle déjà passée ?", "type": "radio", "options": ["Oui", "Non"]},
    ],
    ("Tickets restaurant", "Je ne les ai pas reçus"): [
        {"id": "tr_card", "label": "Le problème concerne-t-il la carte / le chargement plutôt que le droit lui-même ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "tr_absence", "label": "Avez-vous eu des absences, congés, demi-journées ou journées de moins de 6h sur la période ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Tickets restaurant", "Montant incorrect"): [
        {"id": "tr_absence", "label": "Avez-vous eu des absences, congés, demi-journées ou journées de moins de 6h sur la période ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "tr_regularization", "label": "Pensez-vous qu’une régularisation d’un mois précédent puisse exister ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Tickets restaurant", "Nombre incorrect"): [
        {"id": "tr_absence", "label": "Avez-vous eu des absences, congés, demi-journées ou journées de moins de 6h sur la période ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "tr_regularization", "label": "Pensez-vous qu’une régularisation d’un mois précédent puisse exister ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Tickets restaurant", "Carte Edenred problème"): [
        {"id": "tr_edenred_issue", "label": "Quel est le problème principal ?", "type": "radio", "options": ["Première réception de carte", "Perte / vol", "Activation", "Recharge / chargement", "Blocage général"]},
    ],
    ("Tickets restaurant", "Je veux savoir si j’y ai droit"): [
        {"id": "tr_6h", "label": "Votre journée atteint-elle au moins 6 heures ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "tr_break", "label": "Avez-vous une pause d’au moins 30 minutes entre 12h00 et 14h00 ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Transport", "Remboursement Navigo"): [
        {"id": "transport_justif", "label": "Avez-vous déjà transmis votre justificatif ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("Transport", "Montant incorrect"): [
        {"id": "transport_change", "label": "Votre abonnement ou votre situation a-t-il changé récemment ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("JPO / SPO", "Je sais pas où saisir"): [
        {"id": "jpo_day_type", "label": "L’événement a-t-il eu lieu en semaine ou le week-end ?", "type": "radio", "options": ["En semaine", "Le week-end", "Je ne sais pas"]},
        {"id": "jpo_status", "label": "Êtes-vous salarié en heures ou au forfait jours ?", "type": "radio", "options": ["Salarié en heures", "Forfait jours", "Je ne sais pas"]},
    ],
    ("JPO / SPO", "Je peux pas poser ma récup"): [
        {"id": "jpo_month_elapsed", "label": "La JPO / SPO concerne-t-elle un mois déjà révolu ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "jpo_payroll_validated", "label": "La validation paie est-elle finalisée ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "jpo_correct_entry", "label": "L’événement a-t-il été saisi dans le bon module ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
    ],
    ("JPO / SPO", "Ma JPO est validée mais j’ai rien"): [
        {"id": "jpo_payroll_validated", "label": "La validation paie est-elle bien finalisée ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "jpo_before_20", "label": "La validation est-elle intervenue avant la clôture paie du 20 ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        {"id": "jpo_expected_result", "label": "Attendez-vous surtout du paiement, de la récupération, ou les deux ?", "type": "radio", "options": ["Paiement", "Récupération", "Les deux", "Je ne sais pas"]},
    ],
    ("JPO / SPO", "Je veux comprendre le motif à choisir"): [
        {"id": "jpo_weekend_day", "label": "L’événement a-t-il eu lieu le samedi ou le dimanche ?", "type": "radio", "options": ["Samedi", "Dimanche", "Je ne sais pas"]},
        {"id": "jpo_expected_result", "label": "Cherchez-vous un motif payé, récupéré ou payé et récupéré ?", "type": "radio", "options": ["Payé", "Récupéré", "Payé et récupéré", "Je ne sais pas"]},
    ],
    ("JPO / SPO", "Je veux comprendre l’impact paie / récupération"): [
        {"id": "jpo_weekend_day", "label": "L’événement a-t-il eu lieu le samedi ou le dimanche ?", "type": "radio", "options": ["Samedi", "Dimanche", "Je ne sais pas"]},
        {"id": "jpo_expected_result", "label": "Le motif choisi est-il payé, récupéré, ou payé et récupéré ?", "type": "radio", "options": ["Payé", "Récupéré", "Payé et récupéré", "Je ne sais pas"]},
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

def is_teacher(job_type):
    return job_type == TEACHER_JOB

def is_business_pole(establishment_data):
    return establishment_data["pole"] in {"Business Paris", "Business Regions"}

def is_art_creation_pole(establishment_data):
    return establishment_data["pole"] == "Art & Création"

def get_tickets_context(job_type, establishment_data):
    if is_teacher(job_type):
        if is_business_pole(establishment_data):
            return "teacher_business"
        if is_art_creation_pole(establishment_data):
            return "teacher_art_creation"
        return "teacher_other"
    return "non_teacher"

def build_ready_message_for_tickets(issue_type, context_type):
    if issue_type == "edenred":
        return build_rh_message(
            "Je rencontre un problème concernant mes tickets restaurant. Pouvez-vous me confirmer si mes droits ont bien été ouverts côté RH avant ma prise de contact avec Edenred ?"
        )
    if context_type == "teacher_business":
        return build_rh_message(
            "Je rencontre un problème concernant mes tickets restaurant en tant qu’enseignant du pôle Business. Pouvez-vous vérifier ma déclaration et la prise en compte de mes droits ?"
        )
    if context_type == "teacher_art_creation":
        return build_rh_message(
            "Je rencontre un problème concernant mes tickets restaurant en tant qu’enseignant du pôle Art & Création. Pouvez-vous vérifier ma situation via le circuit école ?"
        )
    return build_rh_message(
        "Je rencontre un problème concernant mes tickets restaurant. Pouvez-vous vérifier mes droits, mon calcul et la prise en compte de ma situation ?"
    )

def get_complexity_score(theme, need, free_text, job_type, answers):
    score = 1
    if need == "Autre" or theme == "Autre demande":
        score += 2
    if theme in [
        "Ma paie / Mon bulletin",
        "Heures / Activité",
        "Sortie / Fin de contrat",
        "Mutuelle / Prévoyance",
        "Demande manager",
        "JPO / SPO",
    ]:
        score += 1
    if len((free_text or "").strip()) > 80:
        score += 1
    if is_special_population(job_type):
        score += 1
    if len(answers) >= 3:
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

def get_dynamic_questions(theme, need, role):
    questions = DYNAMIC_QUESTIONS.get((theme, need), []).copy()

    if role == "Manager" and theme == "Demande manager" and need == "Problème paie d’un collaborateur":
        questions = [
            {"id": "mgr_pay_subject", "label": "Le problème du collaborateur concerne-t-il surtout la paie ou les heures ?", "type": "radio", "options": ["Paie", "Heures", "Les deux"]},
            {"id": "mgr_pay_validated", "label": "Les éléments ont-ils déjà été validés par le manager ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        ]
    elif role == "Manager" and theme == "Demande manager" and need == "Heures non validées":
        questions = [
            {"id": "mgr_hours_stage", "label": "Le blocage se situe-t-il au stade de validation manager ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
            {"id": "mgr_hours_before_15", "label": "Le sujet impacte-t-il la paie du mois en cours avant le 15 ?", "type": "radio", "options": ["Oui", "Non", "Je ne sais pas"]},
        ]

    return questions

def get_visible_questions(questions, answers):
    visible = []
    for q in questions:
        show_if = q.get("show_if")
        if show_if is None or show_if(answers):
            visible.append(q)
    return visible

def build_manager_message(text):
    return f"""Bonjour,

{text}

Merci.

Cordialement,
"""

def build_rh_message(text):
    return f"""Bonjour,

{text}

Merci.

Cordialement,
"""

def build_support_message(
    role,
    establishment,
    establishment_data,
    job_type,
    contract_type,
    work_time,
    theme,
    need,
    free_text="",
    message_override=None,
):
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
{message_override.strip() if message_override and message_override.strip() else (free_text.strip() if free_text and free_text.strip() else "Merci de trouver ci-dessus les éléments nécessaires à l’analyse de ma demande.")}

Pouvez-vous m’indiquer la marche à suivre ou procéder à la vérification nécessaire ?

Merci par avance.

Cordialement,
"""
    return subject, body

def init_result(role, establishment, establishment_data, job_type, contract_type, work_time, theme, need):
    return {
        "title": "Analyse de la demande",
        "answer": "",
        "summary": "",
        "diagnostic": "",
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
        "message_ready": "",
        "message_manager": "",
        "message_rh": "",
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

def build_base_answer(
    theme,
    need,
    role,
    establishment,
    establishment_data,
    job_type,
    contract_type,
    work_time,
    free_text,
):
    result = init_result(role, establishment, establishment_data, job_type, contract_type, work_time, theme, need)
    free_text_lower = (free_text or "").lower()

    if theme == "Ma paie / Mon bulletin":
        if need == "Je ne comprends pas mon salaire ce mois-ci":
            result["title"] = "Comprendre votre salaire"
            result["answer"] = """
Votre salaire peut varier d’un mois à l’autre en fonction :
- des absences
- des heures variables
- des primes ou indemnités
- d’un acompte
- d’une régularisation

👉 La première chose à faire est de comparer votre bulletin avec celui du mois précédent.
"""
            result["summary"] = "Une variation de salaire s’explique généralement par des variables, absences, primes ou régularisations."
            result["checks"] = [
                "Comparer avec le bulletin du mois précédent",
                "Vérifier les absences du mois",
                "Vérifier les variables, primes et éventuel acompte",
            ]
            result["action"] = "Comparer les deux bulletins puis demander une vérification à la paie si l’écart reste incompris."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Analyse du salaire du mois"
            result["message_ready"] = build_rh_message(
                "Je ne comprends pas mon salaire de ce mois-ci. Pouvez-vous me préciser les éléments qui expliquent le montant versé ?"
            )

        elif need == "Mon salaire a baissé / augmenté":
            result["title"] = "Variation de salaire"
            result["answer"] = """
Une baisse ou une hausse de salaire peut venir :
- d’une absence
- d’un acompte
- d’une prime
- d’une régularisation
- d’éléments variables transmis ou validés après le 15

⚠️ Dans votre organisation, le cut-off paie est fixé au 15.
Si des éléments sont transmis ou validés après le 15, ils peuvent être repris le mois suivant.
"""
            result["summary"] = "Une variation de salaire provient souvent d’absences, variables, primes, acompte ou décalage M+1."
            result["checks"] = [
                "Vérifier les absences",
                "Vérifier l’éventuel acompte",
                "Vérifier les primes attendues",
                "Vérifier si les variables ont été validées avant ou après le 15",
            ]
            result["action"] = "Comparer avec le mois précédent puis demander une vérification RH / Paie si nécessaire."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Variation salariale"
            result["message_ready"] = build_rh_message(
                "Je constate une variation sur mon salaire. Pouvez-vous m’indiquer les éléments expliquant cette hausse ou cette baisse ?"
            )

        elif need == "Il manque des heures (FFP / induites / supplémentaires)":
            result["title"] = "Heures manquantes sur le bulletin"
            result["answer"] = """
Si des heures sont absentes de votre bulletin, plusieurs causes sont possibles :
- les heures n’ont pas été transmises
- elles n’ont pas été validées
- elles ont été validées ou transmises après le 15
- elles sont en décalage de paie

⚠️ Pour les heures FFP, votre organisation fonctionne en mix :
- parfois payées en M
- parfois selon validation manager
- parfois en M+1

👉 Il faut donc vérifier à la fois :
- la transmission
- la validation
- la date de validation
"""
            result["summary"] = "Les heures manquantes peuvent relever de la transmission, de la validation ou d’un décalage M+1."
            result["checks"] = [
                "Identifier le type d’heures",
                "Vérifier si elles ont été transmises",
                "Vérifier si elles ont été validées",
                "Vérifier si cela a eu lieu avant ou après le 15",
            ]
            result["action"] = "Commencer par vérifier le circuit de validation, puis solliciter RH / Paie si nécessaire."
            result["contact"] = "Manager + RH / Paie"
            result["channel"] = "Mail manager puis RH / Paie"
            result["contact_reason"] = "Heures absentes du bulletin"
            result["message_manager"] = build_manager_message(
                "Certaines de mes heures ne figurent pas sur mon bulletin. Pouvez-vous me confirmer si elles ont bien été validées et transmises ?"
            )
            result["message_rh"] = build_rh_message(
                "Certaines de mes heures ne figurent pas sur mon bulletin. Pouvez-vous vérifier leur prise en compte en paie ?"
            )

        elif need == "Il manque une prime / indemnité":
            result["title"] = "Prime ou indemnité manquante"
            result["answer"] = """
Si une prime ou une indemnité manque, il faut vérifier :
- si elle était bien due ce mois-ci
- si elle a été transmise
- si elle est versée avec décalage
- si une condition d’attribution manquait
"""
            result["summary"] = "Une prime absente peut venir d’un oubli, d’un décalage ou d’une condition non remplie."
            result["checks"] = [
                "Identifier précisément la prime ou l’indemnité",
                "Vérifier le mois concerné",
                "Vérifier les conditions d’attribution",
            ]
            result["action"] = "Demander une vérification ciblée à la paie."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Prime / indemnité absente"
            result["message_ready"] = build_rh_message(
                "Il semble manquer une prime ou une indemnité sur mon bulletin. Pouvez-vous vérifier sa prise en compte ?"
            )

        elif need == "Je ne comprends pas une ligne du bulletin":
            result["title"] = "Comprendre une ligne du bulletin"
            result["answer"] = """
Pour expliquer une ligne du bulletin, il faut relever :
- son libellé exact
- sa base
- son taux
- le mois concerné

👉 Sans le libellé exact, on ne peut pas sécuriser l’explication.
"""
            result["summary"] = "Une ligne de bulletin doit être analysée à partir de son libellé exact."
            result["checks"] = [
                "Relever le libellé exact",
                "Comparer avec le bulletin précédent",
                "Identifier si la ligne est nouvelle ou habituelle",
            ]
            result["action"] = "Transmettre le libellé exact ou une capture ciblée."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Lecture d’une ligne du bulletin"
            result["message_ready"] = build_rh_message(
                "Je ne comprends pas une ligne de mon bulletin. Pouvez-vous m’expliquer la rubrique concernée ?"
            )

        elif need == "Je pense qu’il y a une erreur sur mon bulletin":
            result["title"] = "Suspicion d’erreur sur le bulletin"
            result["answer"] = """
Si vous pensez qu’il y a une erreur, il faut préciser :
- la ligne concernée
- le mois du bulletin
- l’écart constaté
- ce que vous attendiez à la place

👉 Plus la demande est précise, plus la vérification sera rapide.
"""
            result["summary"] = "Une erreur de bulletin doit être signalée avec une rubrique et un écart précis."
            result["checks"] = [
                "Identifier la rubrique concernée",
                "Préciser le mois du bulletin",
                "Décrire l’écart constaté",
            ]
            result["action"] = "Envoyer une demande claire et ciblée au RH / Paie."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Vérification d’erreur de bulletin"
            result["message_ready"] = build_rh_message(
                "Je pense qu’une erreur figure sur mon bulletin. Pouvez-vous effectuer une vérification sur la rubrique concernée ?"
            )

        elif need == "Je veux comprendre mon net à payer":
            result["title"] = "Comprendre le net à payer"
            result["answer"] = """
Le net à payer dépend :
- du brut
- des cotisations
- des absences
- des primes
- des retenues
- d’un éventuel acompte

👉 Le net à payer n’est donc pas seulement le résultat du brut moins les cotisations.
"""
            result["summary"] = "Le net à payer dépend du brut, des cotisations, des retenues et des variables."
            result["checks"] = [
                "Vérifier le brut",
                "Vérifier les cotisations",
                "Vérifier l’éventuel acompte",
                "Vérifier les absences et primes",
            ]
            result["action"] = "Demander une explication détaillée si le calcul reste incompris."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Explication net à payer"
            result["message_ready"] = build_rh_message(
                "Je souhaite comprendre le calcul de mon net à payer. Pouvez-vous me l’expliquer ?"
            )

        elif need == "Je veux comprendre le net social":
            result["title"] = "Comprendre le net social"
            result["answer"] = """
Le net social est un indicateur distinct du net à payer.
Il peut être différent selon les rubriques prises en compte dans son calcul.

👉 Il est donc normal que le net social et le net à payer ne soient pas toujours identiques.
"""
            result["summary"] = "Le net social et le net à payer sont deux notions différentes."
            result["checks"] = [
                "Comparer le net social et le net à payer",
                "Identifier les rubriques particulières du mois",
            ]
            result["action"] = "Demander une explication ciblée si l’écart vous semble incompris."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Explication net social"
            result["message_ready"] = build_rh_message(
                "Je souhaite comprendre le montant de mon net social. Pouvez-vous me préciser son calcul ?"
            )

        elif need == "Je veux comprendre mes cotisations":
            result["title"] = "Comprendre les cotisations"
            result["answer"] = """
Les cotisations peuvent varier selon :
- le statut
- le niveau de rémunération
- le contrat
- certaines régularisations
- des changements de situation

👉 Une variation n’est donc pas forcément une anomalie.
"""
            result["summary"] = "Les cotisations peuvent évoluer selon la situation du salarié et les régularisations du mois."
            result["checks"] = [
                "Identifier les cotisations concernées",
                "Comparer avec un bulletin précédent",
                "Vérifier s’il y a une régularisation",
            ]
            result["action"] = "Demander une explication détaillée sur les cotisations concernées."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Explication cotisations"
            result["message_ready"] = build_rh_message(
                "Je souhaite comprendre certaines cotisations de mon bulletin. Pouvez-vous me les détailler ?"
            )

        else:
            result["title"] = "Demande paie à préciser"
            result["answer"] = """
Votre demande paie ne correspond pas à un cas standard clairement identifié.
Elle nécessite une reformulation plus précise avec le mois concerné et la rubrique visée.
"""
            result["summary"] = "Le sujet paie doit être précisé pour permettre une réponse fiable."
            result["checks"] = [
                "Préciser le mois concerné",
                "Préciser la rubrique concernée",
                "Décrire le problème constaté",
            ]
            result["action"] = "Utiliser le message prêt à transmettre."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Sujet paie hors cas standard"
            result["message_ready"] = build_rh_message(
                "Je vous contacte au sujet d’un point paie que je n’arrive pas à qualifier précisément. Pouvez-vous m’aider à identifier la bonne lecture de ma situation ?"
            )

    elif theme == "Mon Portail Paie":
        result["title"] = "Assistance Mon Portail Paie"
        result["contact"] = "RH / Paie ou support SIRH"
        result["channel"] = "Support / RH"
        result["contact_reason"] = "Blocage portail"

        if need == "Je n’arrive pas à me connecter":
            result["answer"] = """
Avant d’escalader, il faut vérifier :
- que vous utilisez le bon lien
- le bon identifiant
- le bon mot de passe
- le navigateur utilisé

👉 Si le blocage persiste, il faut transmettre le message d’erreur exact.
"""
            result["summary"] = "Un problème de connexion doit d’abord être vérifié techniquement."
            result["checks"] = [
                "Tester un autre navigateur",
                "Tester en navigation privée",
                "Vérifier le lien utilisé",
                "Noter le message d’erreur exact",
            ]
            result["action"] = "Signaler le message d’erreur exact au support."

        elif need == "Je ne vois pas mes bulletins":
            result["answer"] = """
Si vous ne voyez pas vos bulletins, cela peut venir :
- d’un délai de mise à disposition
- d’un mauvais espace
- d’un problème d’accès
- d’un défaut de publication
"""
            result["summary"] = "L’absence de bulletin peut venir d’un délai ou d’un problème d’accès."
            result["checks"] = [
                "Vérifier le mois concerné",
                "Vérifier le bon espace",
                "Vérifier si le bulletin a déjà été publié",
            ]
            result["action"] = "Signaler le mois concerné si le bulletin reste absent."

        elif need == "Je ne vois pas mes tickets restaurant":
            result["answer"] = """
Le problème peut concerner :
- l’affichage dans le portail
- la carte / le chargement
- le droit lui-même
"""
            result["summary"] = "Le sujet peut relever du portail ou du circuit tickets restaurant."
            result["checks"] = [
                "Vérifier si le problème concerne l’affichage",
                "Vérifier si le problème concerne la carte",
                "Vérifier la période concernée",
            ]
            result["action"] = "Préciser le type exact de blocage."

        elif need == "Je ne vois pas mes jours de télétravail":
            result["answer"] = """
Les jours de télétravail visibles dans le portail dépendent :
- du bon module utilisé
- de la période affichée
- des validations associées
"""
            result["summary"] = "La visibilité des jours dépend du bon module et des validations."
            result["checks"] = [
                "Vérifier la période affichée",
                "Vérifier le module utilisé",
                "Vérifier si les demandes ont été validées",
            ]
            result["action"] = "Contrôler le module puis signaler le blocage si besoin."

        elif need == "Je ne comprends pas comment utiliser le portail":
            result["answer"] = """
Votre besoin relève d’un accompagnement d’usage.
Pour vous aider correctement, il faut préciser :
- le module concerné
- l’action que vous voulez faire
- l’étape où vous bloquez
"""
            result["summary"] = "Le besoin d’aide portail doit être ciblé sur une action précise."
            result["checks"] = [
                "Identifier le module concerné",
                "Identifier l’action souhaitée",
                "Décrire l’étape bloquante",
            ]
            result["action"] = "Décrire précisément ce que vous souhaitez faire."

        elif need == "Je veux modifier une information":
            result["answer"] = """
Selon l’information à modifier :
- cela peut être faisable dans le portail
- ou relever du support / RH
"""
            result["summary"] = "La modification dépend du type d’information concerné."
            result["checks"] = [
                "Identifier l’information à modifier",
                "Vérifier si le champ est modifiable",
                "Signaler le message d’erreur si besoin",
            ]
            result["action"] = "Préciser l’information concernée et l’étape bloquante."

        else:
            result["answer"] = """
Votre demande liée au portail doit être reformulée avec :
- le module concerné
- l’action souhaitée
- le blocage rencontré
"""
            result["summary"] = "Le besoin portail doit être mieux qualifié."
            result["checks"] = [
                "Préciser le module",
                "Préciser l’action",
                "Décrire le blocage",
            ]
            result["action"] = "Utiliser le message prêt à transmettre."

    elif theme == "Absences / Arrêts":
        if need == "Je veux déclarer une absence":
            result["title"] = "Déclaration d’absence"
            result["answer"] = """
Une absence standard doit être déclarée dans Mon Portail Paie.

⚠️ En revanche, les arrêts de travail ne passent pas par le portail.
"""
            result["summary"] = "Les absences standards se gèrent dans le portail."
            result["checks"] = [
                "Choisir le bon motif d’absence",
                "Vérifier la période concernée",
                "Préparer un justificatif si nécessaire",
            ]
            result["action"] = "Faire la demande dans Mon Portail Paie."
            result["contact"] = "Mon Portail Paie"
            result["channel"] = "Portail"
            result["contact_reason"] = "Déclaration d’absence standard"

        elif need == "Quels types d’absence existent ?":
            result["title"] = "Types d’absence"
            result["answer"] = """
La plupart des absences courantes se déclarent dans le portail.

En revanche, les cas comme :
- arrêt maladie
- maternité
- accident du travail

doivent être signalés directement au RH de proximité.
"""
            result["summary"] = "Les absences standards passent par le portail, les arrêts par RH."
            result["checks"] = [
                "Identifier le motif exact",
                "Vérifier si c’est une absence standard ou un arrêt",
            ]
            result["action"] = "Choisir le bon circuit selon le motif."
            result["contact"] = "Portail ou RH de proximité"
            result["channel"] = "Portail ou mail RH"
            result["contact_reason"] = "Orientation selon le motif"

        elif need == "Je veux signaler un arrêt de travail":
            result["title"] = "Signalement d’arrêt de travail"
            result["answer"] = """
Un arrêt de travail ne se déclare pas dans le portail.

👉 Il doit être transmis directement au RH de proximité.

⚠️ Dans votre organisation :
- ce n’est pas le portail
- ce n’est pas le manager
- c’est le RH de proximité
"""
            result["summary"] = "Un arrêt de travail doit être transmis directement au RH de proximité."
            result["checks"] = [
                "Vérifier la date de début d’arrêt",
                "Préparer le justificatif",
                "Transmettre directement au RH",
            ]
            result["action"] = "Envoyer l’arrêt au RH de proximité."
            result["contact"] = "RH de proximité"
            result["channel"] = "Mail RH"
            result["contact_reason"] = "Règle interne arrêt de travail"
            result["message_ready"] = build_rh_message(
                "Je vous informe être en arrêt de travail à compter du [date]. Vous trouverez ci-joint mon arrêt de travail. Merci de bien vouloir en prendre compte."
            )

        elif need == "Je veux savoir si mon absence est payée":
            result["title"] = "Absence payée ou non"
            result["answer"] = """
Le caractère payé ou non d’une absence dépend :
- du motif
- de la durée
- du cadre applicable
- de votre situation
"""
            result["summary"] = "Le paiement d’une absence dépend du motif et de la situation."
            result["checks"] = [
                "Identifier le motif exact",
                "Vérifier les dates",
                "Préciser le contexte si besoin",
            ]
            result["action"] = "Demander confirmation au RH / Paie."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Paiement d’absence"
            result["message_ready"] = build_rh_message(
                "Pouvez-vous me confirmer si mon absence est payée et selon quelles modalités ?"
            )

        elif need == "Je veux comprendre l’impact sur ma paie":
            result["title"] = "Impact d’une absence sur la paie"
            result["answer"] = """
Une absence peut avoir un impact sur :
- le brut
- le net
- certaines primes
- les indemnités
- une éventuelle régularisation
"""
            result["summary"] = "Une absence peut modifier la paie du mois ou entraîner une régularisation."
            result["checks"] = [
                "Identifier le motif de l’absence",
                "Vérifier la période",
                "Vérifier si le bulletin est déjà édité",
            ]
            result["action"] = "Demander une explication ciblée au RH / Paie."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Impact absence sur paie"
            result["message_ready"] = build_rh_message(
                "Pouvez-vous me préciser l’impact de mon absence sur ma paie ainsi que les éventuelles régularisations à venir ?"
            )

        elif need == "Je veux régulariser une absence":
            result["title"] = "Régularisation d’absence"
            result["answer"] = """
Pour régulariser une absence, il faut vérifier :
- le motif saisi
- la période concernée
- si la correction doit être faite dans le portail ou via RH
"""
            result["summary"] = "Une régularisation suppose de requalifier l’absence et la période."
            result["checks"] = [
                "Vérifier le motif initial",
                "Vérifier la période à corriger",
                "Préciser la correction attendue",
            ]
            result["action"] = "Préciser l’absence concernée et la correction souhaitée."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Correction d’absence"
            result["message_ready"] = build_rh_message(
                "Je souhaite régulariser une absence. Pouvez-vous m’indiquer la marche à suivre ou procéder à la correction nécessaire ?"
            )

        else:
            result["title"] = "Demande absence à préciser"
            result["answer"] = """
Votre demande liée aux absences doit être précisée avec :
- le motif exact
- la période concernée
- le circuit déjà utilisé
"""
            result["summary"] = "Le sujet absence doit être mieux qualifié."
            result["checks"] = [
                "Préciser le motif",
                "Préciser la période",
                "Préciser si le portail a déjà été utilisé",
            ]
            result["action"] = "Utiliser le message prêt à transmettre."

    elif theme == "Congés / RTT / Récup":
        result["title"] = "Congés / RTT / Récup"
        result["contact"] = "Portail / RH"
        result["channel"] = "Portail puis RH si besoin"
        result["contact_reason"] = "Gestion des droits"

        if need == "Combien de congés il me reste":
            result["answer"] = """
Le solde de congés doit être consulté dans le portail.

👉 Si vous constatez un écart, il faut vérifier :
- les congés déjà posés
- les demandes en attente
- la mise à jour du solde
"""
            result["summary"] = "Le solde de congés se consulte d’abord dans le portail."
            result["checks"] = [
                "Vérifier le solde affiché",
                "Vérifier les demandes en attente",
            ]
            result["action"] = "Consulter le portail puis signaler tout écart."

        elif need == "Comment poser un congé":
            result["answer"] = """
Un congé doit être posé via le portail avec :
- le bon type de congé
- la bonne période
- le bon circuit de validation
"""
            result["summary"] = "Les congés se posent dans le portail."
            result["checks"] = [
                "Choisir le bon type de congé",
                "Vérifier les dates",
                "Vérifier le circuit de validation",
            ]
            result["action"] = "Déposer la demande via le portail."

        elif need == "Délais de validation":
            result["answer"] = """
Le délai de validation dépend du circuit interne.

👉 Si le délai vous semble anormalement long, il faut vérifier :
- si la demande a bien été transmise
- si elle est bloquée chez un validateur
"""
            result["summary"] = "Le délai dépend du circuit de validation."
            result["checks"] = [
                "Vérifier si la demande a bien été soumise",
                "Vérifier le niveau de validation bloquant",
            ]
            result["action"] = "Relancer si la demande reste en attente."

        elif need == "Refus de congé":
            result["answer"] = """
Un refus de congé peut venir :
- d’une contrainte d’organisation
- du calendrier
- d’une erreur de saisie
- d’un problème de droit
"""
            result["summary"] = "Le refus de congé doit d’abord être expliqué par le manager."
            result["checks"] = [
                "Vérifier les dates demandées",
                "Vérifier le motif du refus",
                "Vérifier si un échange manager a déjà eu lieu",
            ]
            result["action"] = "Commencer par un échange avec le manager."
            result["contact"] = "Manager"
            result["channel"] = "Échange manager"
            result["contact_reason"] = "Refus managérial"
            result["message_ready"] = build_manager_message(
                "Ma demande de congé a été refusée. Pouvez-vous m’indiquer le motif de ce refus ?"
            )

        elif need == "RTT / JRS comment ça marche":
            result["answer"] = """
Le fonctionnement des RTT / JRS dépend :
- du statut
- du temps de travail
- de l’organisation du travail
- d’un éventuel forfait jours
"""
            result["summary"] = "Les RTT / JRS dépendent du statut et du mode d’organisation."
            result["checks"] = [
                "Vérifier votre statut",
                "Vérifier si vous êtes en forfait jours ou en heures",
                "Vérifier vos droits affichés",
            ]
            result["action"] = "Demander une confirmation RH si nécessaire."

        elif need == "Report / perte de congés":
            result["answer"] = """
Le report ou la perte de congés dépend :
- de la période de référence
- des règles internes
- des demandes déjà posées
- de certaines situations particulières
"""
            result["summary"] = "Le report ou la perte de congés doit être vérifié au regard de la période et des règles internes."
            result["checks"] = [
                "Vérifier la période de référence",
                "Vérifier les congés en attente",
                "Vérifier les règles internes applicables",
            ]
            result["action"] = "Solliciter le RH si vous craignez une perte de droits."
            result["contact"] = "RH"
            result["channel"] = "Mail RH"
            result["contact_reason"] = "Report / perte de congés"

        else:
            result["answer"] = """
Votre demande liée aux congés / RTT / récup doit être reformulée avec :
- le type de droit concerné
- la période
- l’action attendue
"""
            result["summary"] = "Le sujet doit être mieux qualifié."
            result["checks"] = [
                "Préciser le type de droit",
                "Préciser la période",
                "Préciser le besoin",
            ]
            result["action"] = "Utiliser le message prêt à transmettre."

    elif theme == "Télétravail":
        result["title"] = "Télétravail"
        result["contact"] = "Manager / RH / Portail"
        result["channel"] = "Portail puis validation manager"
        result["contact_reason"] = "Télétravail"

        if need == "Combien de jours j’ai droit":
            result["answer"] = """
Le nombre de jours de télétravail dépend du poste et du cadre applicable.

Repères internes :
- en école : forfait indicatif de 0 à 44 jours
- en services support : forfait indicatif de 0 à 60 jours

👉 Le droit exact doit être confirmé selon votre situation.
"""
            result["summary"] = "Le nombre de jours dépend du poste et du périmètre."
            result["checks"] = [
                "Vérifier si vous êtes en école ou support",
                "Vérifier le forfait applicable",
            ]
            result["action"] = "Consulter le portail puis demander confirmation si besoin."
            result["vigilance"].append("En école : forfait indicatif de 0 à 44 jours. En services support : forfait indicatif de 0 à 60 jours.")

        elif need == "Comment poser un jour":
            result["answer"] = """
Les jours de télétravail se posent dans Mon Portail Paie, via le module prévu à cet effet.

👉 Il faut ensuite la validation manager.
"""
            result["summary"] = "Le télétravail se pose dans le portail avec validation manager."
            result["checks"] = [
                "Choisir la bonne date",
                "Vérifier le module utilisé",
                "Vérifier le circuit de validation",
            ]
            result["action"] = "Passer par le portail."

        elif need == "Mon manager refuse":
            result["answer"] = """
Si le manager refuse, le premier interlocuteur est le manager lui-même.

Le refus peut être lié :
- à une contrainte d’organisation
- à une règle locale
- à un problème de quota
- à une mauvaise procédure

👉 Il faut donc commencer par demander le motif précis.
"""
            result["summary"] = "Le refus relève d’abord du manager."
            result["checks"] = [
                "Vérifier si la demande a bien été faite dans le portail",
                "Vérifier le quota disponible",
                "Demander le motif du refus",
            ]
            result["action"] = "Échanger d’abord avec le manager."
            result["contact"] = "Manager"
            result["channel"] = "Échange manager"
            result["contact_reason"] = "Refus manager"
            result["message_ready"] = build_manager_message(
                "Ma demande de télétravail a été refusée. Pouvez-vous m’indiquer le motif précis de ce refus ?"
            )

        elif need == "Je veux modifier mes jours":
            result["answer"] = """
La modification des jours de télétravail passe d’abord par le portail, selon le statut de validation de la demande.
"""
            result["summary"] = "La modification dépend du statut de la demande dans le portail."
            result["checks"] = [
                "Vérifier si la demande est déjà validée",
                "Vérifier la date concernée",
            ]
            result["action"] = "Modifier dans le portail ou solliciter le validateur."

        elif need == "Impact sur paie / indemnité":
            result["answer"] = """
Un sujet de télétravail peut avoir un impact indirect selon :
- le cadre applicable
- le type de demande
- l’indemnité concernée
- la période visée
"""
            result["summary"] = "L’impact télétravail doit être qualifié précisément."
            result["checks"] = [
                "Préciser la période",
                "Préciser le type d’impact",
                "Vérifier s’il s’agit d’une saisie, validation ou indemnité",
            ]
            result["action"] = "Décrire précisément l’impact supposé."
            result["contact"] = "RH"
            result["channel"] = "Mail RH"
            result["contact_reason"] = "Impact télétravail"

        elif need == "Problème sur portail":
            result["answer"] = """
Le blocage peut venir :
- du module télétravail
- d’un problème d’accès
- d’un problème d’affichage

👉 Il faut transmettre le message d’erreur exact si le souci persiste.
"""
            result["summary"] = "Le blocage relève d’un problème d’usage ou technique."
            result["checks"] = [
                "Vérifier le module utilisé",
                "Tester un autre navigateur",
                "Noter le message d’erreur",
            ]
            result["action"] = "Transmettre le message d’erreur exact si besoin."

        else:
            result["answer"] = """
Votre demande télétravail doit être précisée avec :
- la période
- l’étape bloquante
- le circuit déjà utilisé
"""
            result["summary"] = "Le besoin télétravail doit être mieux qualifié."
            result["checks"] = [
                "Préciser la période",
                "Préciser l’étape bloquante",
                "Préciser si le portail a déjà été utilisé",
            ]
            result["action"] = "Utiliser le message prêt à transmettre."

        if "2 heures" in free_text_lower or "2h" in free_text_lower or "temps de trajet" in free_text_lower:
            result["alerts"].append("Dérogation potentielle détectée : temps de trajet domicile ↔ bureau supérieur à 2 heures aller-retour.")
            result["vigilance"].append("Le calcul du temps de trajet est effectué exclusivement par le RRH via Google Maps.")
        if "rqth" in free_text_lower or "handicap" in free_text_lower:
            result["alerts"].append("Dérogation potentielle détectée : situation RQTH.")
            result["vigilance"].append("Une adaptation éventuelle nécessite validation par la médecine du travail, le référent handicap et le RRH.")
        if "province" in free_text_lower or "décision judiciaire" in free_text_lower or "decision judiciaire" in free_text_lower:
            result["alerts"].append("Situation spécifique détectée : une validation DRH peut être nécessaire.")

    elif theme == "Acompte sur salaire":
        result["title"] = "Acompte sur salaire"
        result["answer"] = """
La demande d’acompte se fait uniquement via "Mon Portail Paie".

👉 Période de demande :
- à partir du 1er jour du mois
- jusqu’au 11 à minuit

👉 Montant maximum :
- 50 % du salaire

⚠️ Important :
Le salaire peut être ajusté entre le 7 et le 11 selon :
- les absences
- les primes
- les variables
"""
        result["summary"] = "L’acompte se demande exclusivement via le portail entre le 1er et le 11."
        result["checks"] = [
            "Vérifier que la demande est faite entre le 1 et le 11",
            "Vérifier que le montant ne dépasse pas 50 %",
        ]
        result["action"] = "Faire la demande via Mon Portail Paie."
        result["contact"] = "Mon Portail Paie"
        result["channel"] = "Portail"
        result["contact_reason"] = "Acompte géré via portail"
        result["vigilance"].append("Le salaire peut être ajusté entre le 7 et le 11 selon les absences, primes et variables remontées.")
        result["message_ready"] = build_rh_message(
            "Je souhaite une confirmation sur ma demande d’acompte. Pouvez-vous m’indiquer si elle est conforme et correctement prise en compte ?"
        )

    elif theme == "Heures / Activité":
        result["title"] = "Heures / Activité"
        result["contact"] = "Manager / RH / Paie"
        result["channel"] = "Mail manager puis RH / Paie"
        result["contact_reason"] = "Suivi des heures"

        if need == "Mes heures FFP ne sont pas correctes":
            result["answer"] = """
Pour les heures FFP, il faut vérifier :
- la remontée
- la validation
- la date de validation
- la paie concernée

⚠️ Dans votre organisation, les FFP fonctionnent en mix :
- parfois payées en M
- parfois selon validation manager
- parfois en M+1
"""
            result["summary"] = "Les heures FFP doivent être rapprochées de leur validation et du cut-off du 15."
            result["checks"] = [
                "Vérifier le volume attendu",
                "Vérifier la remontée",
                "Vérifier la validation",
                "Vérifier la date de validation",
            ]
            result["action"] = "Vérifier le circuit FFP puis demander un contrôle RH / Paie si besoin."
            result["message_manager"] = build_manager_message(
                "Mes heures FFP semblent incorrectes. Pouvez-vous me confirmer leur statut de validation et de transmission ?"
            )
            result["message_rh"] = build_rh_message(
                "Mes heures FFP semblent incorrectes. Pouvez-vous vérifier leur reprise en paie ?"
            )

        elif need == "Heures induites manquantes":
            result["answer"] = """
Des heures induites manquantes peuvent venir :
- d’une remontée incomplète
- d’une règle de calcul
- d’un décalage de traitement
"""
            result["summary"] = "Les heures induites absentes nécessitent une vérification de remontée et de calcul."
            result["checks"] = [
                "Vérifier le volume attendu",
                "Vérifier les éléments transmis",
                "Vérifier la période concernée",
            ]
            result["action"] = "Demander une vérification du calcul et de la remontée."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Heures induites"

        elif need == "Heures supplémentaires non payées":
            result["answer"] = """
Des heures supplémentaires non payées peuvent venir :
- d’un défaut de saisie
- d’un manque de validation
- d’un décalage de paie
"""
            result["summary"] = "Les heures supplémentaires absentes doivent être vérifiées dans le circuit de validation."
            result["checks"] = [
                "Vérifier la déclaration",
                "Vérifier la validation manager",
                "Vérifier le mois attendu",
            ]
            result["action"] = "Vérifier le circuit manager puis solliciter la paie."
            result["message_manager"] = build_manager_message(
                "Mes heures supplémentaires ne semblent pas avoir été payées. Pouvez-vous me confirmer leur validation ?"
            )
            result["message_rh"] = build_rh_message(
                "Mes heures supplémentaires ne semblent pas avoir été payées. Pouvez-vous vérifier leur reprise en paie ?"
            )

        elif need == "Heures validées mais non payées":
            result["answer"] = """
Si les heures sont validées mais non payées, deux cas principaux existent :
- validation après le 15 → reprise possible en M+1
- anomalie de reprise en paie

👉 Il faut donc vérifier la date exacte de validation.
"""
            result["summary"] = "Des heures validées mais absentes du bulletin relèvent soit d’un décalage M+1, soit d’une anomalie de reprise."
            result["checks"] = [
                "Vérifier la date de validation",
                "Vérifier le bulletin concerné",
                "Vérifier le mois attendu",
            ]
            result["action"] = "Transmettre la preuve de validation avec le mois concerné."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Heures validées non payées"
            result["message_ready"] = build_rh_message(
                "Mes heures apparaissent comme validées mais ne figurent pas sur mon bulletin. Pouvez-vous vérifier leur prise en compte en paie ?"
            )

        elif need == "Problème de transmission des heures":
            result["answer"] = """
Le problème peut se situer :
- à la saisie
- à la transmission
- à la validation
- à la reprise paie
"""
            result["summary"] = "Le circuit de transmission doit être contrôlé étape par étape."
            result["checks"] = [
                "Identifier le canal utilisé",
                "Vérifier si la transmission a bien été faite",
                "Identifier l’étape bloquante",
            ]
            result["action"] = "Préciser l’étape de blocage puis solliciter le bon interlocuteur."

        elif need == "Je veux comprendre le calcul":
            result["answer"] = """
Pour expliquer le calcul des heures, il faut identifier :
- le type d’heures
- la période
- les éléments de base
- la règle de calcul appliquée
"""
            result["summary"] = "Le calcul doit être rapproché du type d’heures et de la période."
            result["checks"] = [
                "Identifier le type d’heures",
                "Identifier la période",
                "Vérifier les éléments de base",
            ]
            result["action"] = "Demander une explication ciblée avec le type d’heures et la période."

        else:
            result["answer"] = """
Votre demande liée aux heures doit être reformulée avec :
- le type d’heures
- la période
- l’étape du circuit concernée
"""
            result["summary"] = "Le sujet heures / activité doit être mieux qualifié."
            result["checks"] = [
                "Préciser le type d’heures",
                "Préciser la période",
                "Préciser le circuit concerné",
            ]
            result["action"] = "Utiliser le message prêt à transmettre."

    elif theme == "JPO / SPO":
        result["title"] = "JPO / SPO"
        result["contact"] = "RH / Paie"
        result["channel"] = "Portail ou RH / Paie selon le cas"
        result["contact_reason"] = "JPO / SPO"

        if job_type in JPO_EXCLUDED_PROFILES:
            result["answer"] = """
Pour votre profil, la logique standard JPO / SPO ne doit pas être appliquée automatiquement.

👉 Une vérification métier préalable est nécessaire.
"""
            result["summary"] = "Le profil sélectionné ne relève pas de la logique standard JPO / SPO."
            result["checks"] = [
                "Vérifier la population concernée",
                "Demander confirmation au RH / Paie",
            ]
            result["action"] = "Solliciter le RH / Paie pour confirmer le circuit applicable."
            result["message_ready"] = build_rh_message(
                "Je souhaite vérifier la procédure applicable à ma situation concernant une JPO / SPO. Pouvez-vous me confirmer le bon traitement pour mon profil ?"
            )

        elif need == "Je sais pas où saisir":
            result["answer"] = """
La règle interne est la suivante :

✅ JPO / SPO le week-end :
- saisie dans la section **JPO** du portail

✅ JPO / SPO en semaine :
- pour les salariés en heures → logique des heures supplémentaires / éléments variables
- pour les forfait jours → contrôle spécifique à vérifier selon le cas

👉 La bonne orientation dépend donc :
- du jour de l’événement
- du statut heures / forfait jours
"""
            result["summary"] = "Le bon module dépend du jour de l’événement et du statut heures / forfait jours."
            result["checks"] = [
                "Vérifier si l’événement a eu lieu en semaine ou le week-end",
                "Vérifier si vous êtes en heures ou au forfait jours",
                "Week-end = section JPO / semaine en heures = éléments variables",
            ]
            result["action"] = "Utiliser le bon module selon le jour et le statut."
            result["message_ready"] = build_rh_message(
                "Je souhaite confirmer le bon circuit de saisie pour une JPO / SPO. Pouvez-vous me préciser si je dois utiliser la section JPO ou les éléments variables ?"
            )

        elif need == "Je peux pas poser ma récup":
            result["answer"] = """
Pour pouvoir poser la récupération correspondante :
- la JPO / SPO doit avoir été saisie
- la validation paie doit être finalisée
- l’événement doit porter sur un mois révolu
- l’événement doit avoir été saisi dans le bon module

👉 Ensuite, la récupération se pose dans la section congés avec le motif :
**Récupération**

⚠️ La validation de cette récupération se fait par le manager.
"""
            result["summary"] = "La récupération est bloquée si le mois n’est pas révolu, si la validation paie n’est pas finalisée ou si le mauvais module a été utilisé."
            result["checks"] = [
                "Vérifier que la JPO / SPO a été saisie",
                "Vérifier que la validation paie est finalisée",
                "Vérifier que l’événement porte sur un mois révolu",
                "Poser ensuite la récup dans Congés > Récupération",
            ]
            result["action"] = "Corriger le point bloquant puis poser la récupération dans les congés."
            result["message_ready"] = build_rh_message(
                "Je ne peux pas poser ma récupération suite à une JPO / SPO. Pouvez-vous me confirmer si la validation paie est finalisée et si la récupération est bien disponible ?"
            )

        elif need == "Ma JPO est validée mais j’ai rien":
            result["answer"] = """
Si votre JPO semble validée mais que vous n’avez rien :
- il faut distinguer validation manager et validation paie
- il faut vérifier si la validation est intervenue avant ou après la clôture du 20
- il faut vérifier si vous attendez du paiement, de la récupération, ou les deux

⚠️ Une validation après la clôture du 20 peut décaler la disponibilité au cycle suivant.
"""
            result["summary"] = "Une JPO validée mais non visible peut relever d’un décalage lié à la validation paie ou à la clôture du 20."
            result["checks"] = [
                "Vérifier si la validation paie est bien finalisée",
                "Vérifier si la validation est intervenue avant ou après le 20",
                "Vérifier si vous attendez du paiement, de la récupération ou les deux",
            ]
            result["action"] = "Demander une vérification du cycle de paie et du statut de récupération."
            result["message_ready"] = build_rh_message(
                "Ma JPO semble validée, mais je ne vois ni le paiement ni la récupération attendue. Pouvez-vous vérifier son statut de prise en compte ?"
            )

        elif need == "Je veux comprendre le motif à choisir":
            result["answer"] = """
Les motifs JPO / SPO réellement utilisés sont :

- Samedi récupéré
- Samedi payé
- Dimanche payé
- Dimanche récupéré
- Dimanche payé et récupéré

👉 Le bon motif dépend :
- du jour concerné
- de ce que vous attendez : paiement, récupération, ou les deux
"""
            result["summary"] = "Le motif dépend du jour concerné et du résultat attendu."
            result["checks"] = [
                "Vérifier si l’événement a eu lieu le samedi ou le dimanche",
                "Vérifier si vous attendez paiement, récupération ou les deux",
            ]
            result["action"] = "Choisir le motif correspondant exactement à votre situation."
            result["message_ready"] = build_rh_message(
                "Je souhaite confirmer le bon motif à utiliser pour ma JPO / SPO. Pouvez-vous me préciser celui qui correspond à ma situation ?"
            )

        elif need == "Je veux comprendre l’impact paie / récupération":
            result["answer"] = """
Une JPO / SPO peut :
- alimenter un compteur de récupération
- générer du paiement direct
- ou les deux

👉 Cela dépend du motif choisi :
- samedi = majoration 25 %
- dimanche = majoration 100 %
- payé / récupéré / payé et récupéré selon le motif

⚠️ Le résultat dépend aussi de la validation manager et de la validation paie.
"""
            result["summary"] = "L’impact paie / récupération dépend du motif choisi, du jour et des validations."
            result["checks"] = [
                "Vérifier le jour concerné",
                "Vérifier le motif choisi",
                "Vérifier la validation manager et la validation paie",
            ]
            result["action"] = "Demander confirmation du motif et du résultat attendu si besoin."
            result["message_ready"] = build_rh_message(
                "Je souhaite comprendre l’impact paie / récupération de ma JPO / SPO. Pouvez-vous me confirmer le traitement attendu selon le motif choisi ?"
            )

        else:
            result["answer"] = """
Votre demande JPO / SPO doit être reformulée avec :
- le jour concerné
- le statut heures / forfait jours
- le résultat attendu
"""
            result["summary"] = "Le sujet JPO / SPO doit être mieux qualifié."
            result["checks"] = [
                "Préciser le jour concerné",
                "Préciser le statut",
                "Préciser si vous attendez paiement, récupération ou les deux",
            ]
            result["action"] = "Utiliser le message prêt à transmettre."
            result["message_ready"] = build_rh_message(
                "Je vous contacte concernant une JPO / SPO. Pouvez-vous me confirmer la règle applicable à ma situation ?"
            )

    elif theme == "Mutuelle / Prévoyance":
        result["title"] = "Mutuelle / Prévoyance"
        result["answer"] = """
La mutuelle suit un parcours encadré :
- inscription automatique à l’embauche
- affiliation ou dispense à finaliser ensuite
- gestion avec le partenaire mutuelle, avec RH en relai si besoin
"""
        result["summary"] = "Le sujet mutuelle dépend du parcours d’affiliation ou de dispense."
        result["checks"] = [
            "Vérifier l’adresse personnelle renseignée",
            "Vérifier le délai depuis la prise de poste",
            "Identifier si le besoin concerne adhésion, dispense, remboursement ou cotisation",
        ]
        result["action"] = "Surveiller l’affiliation puis solliciter le RH si le délai est dépassé."
        result["contact"] = "Partenaire mutuelle / RH"
        result["channel"] = "Mutuelle puis RH"
        result["contact_reason"] = "Mutuelle / prévoyance"
        result["vigilance"].append("Le salarié dispose de 2 mois pour finaliser son affiliation. Au-delà, un nouveau lien doit être demandé au RH.")
        result["vigilance"].append("Une dispense doit être demandée pour chaque contrat.")
        result["vigilance"].append("Les remboursements liés à une dispense tardive ne peuvent pas excéder 2 mois.")
        result["message_ready"] = build_rh_message(
            "Je rencontre une difficulté liée à ma mutuelle / prévoyance. Pouvez-vous m’indiquer la marche à suivre ou vérifier ma situation ?"
        )

    elif theme == "Transport":
        if need == "Remboursement Navigo" or "navigo" in free_text_lower or "ratp" in free_text_lower:
            result["title"] = "Remboursement Navigo"
            result["answer"] = """
Les demandes de remboursement Navigo / RATP passent par Mon Portail Paie.
"""
            result["summary"] = "Le remboursement Navigo relève du portail."
            result["checks"] = [
                "Vérifier le justificatif",
                "Vérifier la période",
                "Vérifier le montant repris",
            ]
            result["action"] = "Faire ou suivre la demande dans le portail."
            result["contact"] = "Mon Portail Paie"
            result["channel"] = "Portail"
            result["contact_reason"] = "Transport RATP / Navigo"
        else:
            result["title"] = "Transport hors Navigo"
            result["answer"] = """
Les autres demandes transport ne passent pas par le portail.
Elles doivent être adressées au RH de proximité.
"""
            result["summary"] = "Le transport hors RATP / Navigo relève du RH."
            result["checks"] = [
                "Identifier le type de transport",
                "Préparer le justificatif",
                "Préciser la période",
            ]
            result["action"] = "Adresser la demande au RH de proximité."
            result["contact"] = "RH de proximité"
            result["channel"] = "Mail RH"
            result["contact_reason"] = "Transport hors Navigo"
            result["message_ready"] = build_rh_message(
                "Je souhaite faire une demande liée à mon remboursement transport. Pouvez-vous m’indiquer la marche à suivre ou vérifier ma situation ?"
            )

    elif theme == "Tickets restaurant":
        tickets_context = get_tickets_context(job_type, establishment_data)
        result["title"] = "Tickets restaurant"

        if need == "Je ne les ai pas reçus":
            if tickets_context == "teacher_business":
                result["answer"] = """
En tant qu’enseignant du pôle Business, vous devez déclarer le nombre de tickets restaurant éligibles dans :

Mon Portail Paie > Mes demandes > Mes éléments variables

👉 avant le 20 de chaque mois.

Si les tickets ne sont pas reçus, il faut vérifier :
- la déclaration avant le 20
- les jours réellement éligibles
- le chargement éventuel
"""
                result["contact"] = "RH de proximité"
                result["channel"] = "Mail RH"
                result["contact_reason"] = "Tickets restaurant enseignant Business"
                result["action"] = "Vérifier la déclaration et demander confirmation au RH de proximité."
            elif tickets_context == "teacher_art_creation":
                result["answer"] = """
En tant qu’enseignant du pôle Art & Création, la déclaration des tickets restaurant passe par l’école et non par Mon Portail Paie.
"""
                result["contact"] = "École / RH de proximité"
                result["channel"] = "Circuit école"
                result["contact_reason"] = "Tickets restaurant enseignant Art & Création"
                result["action"] = "Vérifier la situation via le circuit école."
            else:
                result["answer"] = """
Pour les salariés non enseignants, le calcul des tickets restaurant est automatique.

Un problème peut venir :
- d’un droit non ouvert
- d’une période non éligible
- d’un chargement non encore visible
- d’un problème Edenred
"""
                result["contact"] = "RH de proximité"
                result["channel"] = "Mail RH"
                result["contact_reason"] = "Tickets restaurant non enseignant"
                result["action"] = "Vérifier les jours éligibles puis demander confirmation au RH."

            result["summary"] = "Le circuit tickets restaurant dépend du profil et du pôle."
            result["checks"] = [
                "Vérifier le profil : enseignant ou non enseignant",
                "Vérifier le pôle si vous êtes enseignant",
                "Vérifier les jours réellement éligibles",
            ]
            result["message_ready"] = build_ready_message_for_tickets("standard", tickets_context)

        elif need == "Montant incorrect":
            result["answer"] = """
Le montant ou le calcul des tickets restaurant dépend :
- du nombre de journées réellement éligibles
- des absences
- des congés
- des demi-journées
- des journées de moins de 6h
- de l’absence de pause méridienne conforme
- d’une éventuelle régularisation d’un mois précédent

⚠️ Le calcul est mensuel, au réel.
"""
            result["summary"] = "Le montant dépend des jours éligibles et d’éventuelles régularisations."
            result["checks"] = [
                "Vérifier les absences",
                "Vérifier les congés ou demi-journées",
                "Vérifier les journées de moins de 6h",
                "Vérifier les éventuelles régularisations",
            ]
            result["action"] = "Demander une vérification au RH de proximité."
            result["contact"] = "RH de proximité"
            result["channel"] = "Mail RH"
            result["contact_reason"] = "Montant tickets restaurant"
            result["message_ready"] = build_ready_message_for_tickets("standard", tickets_context)

        elif need == "Nombre incorrect":
            result["answer"] = """
Le nombre de tickets restaurant est recalculé mensuellement, au réel.

Il peut donc varier selon :
- les absences
- les congés
- les demi-journées
- les journées de moins de 6h
- l’absence de pause méridienne conforme
- une régularisation liée à un mois précédent
"""
            result["summary"] = "Le nombre de tickets dépend des jours réellement éligibles et des régularisations."
            result["checks"] = [
                "Vérifier les jours travaillés réellement éligibles",
                "Vérifier les absences ou congés",
                "Vérifier les éventuelles régularisations",
            ]
            result["action"] = "Demander une vérification au RH de proximité."
            result["contact"] = "RH de proximité"
            result["channel"] = "Mail RH"
            result["contact_reason"] = "Nombre tickets restaurant"
            result["message_ready"] = build_ready_message_for_tickets("standard", tickets_context)

        elif need == "Carte Edenred problème":
            result["answer"] = """
Pour les sujets liés à la carte Edenred :

- première réception : J+5 après virement fin de mois, directement à domicile
- perte / vol : voir avec Edenred
- activation : voir avec Edenred
- recharge : J+2 après virement
- délai de chargement : 48h après virement
- blocage : voir avec Edenred
"""
            result["summary"] = "Les sujets carte relèvent principalement d’Edenred."
            result["checks"] = [
                "Vérifier la date du dernier virement fin de mois",
                "Tenir compte de J+2 pour la recharge",
                "Tenir compte de 48h de délai de chargement",
                "Contacter Edenred pour activation, perte, vol ou blocage",
            ]
            result["action"] = "Contacter directement Edenred."
            result["contact"] = "Prestataire Edenred"
            result["channel"] = "Support Edenred"
            result["contact_reason"] = "Carte Edenred"
            result["message_ready"] = build_ready_message_for_tickets("edenred", tickets_context)

        elif need == "Je veux savoir si j’y ai droit":
            result["answer"] = """
La règle générale est la suivante :

✅ 1 ticket restaurant par journée travaillée

Une journée éligible doit respecter :
- une amplitude minimale de 6 heures
- une pause d’au moins 30 minutes entre 12h00 et 14h00

❌ Pas de ticket restaurant en cas de :
- absence
- congé
- demi-journée
- journée de moins de 6h
- pause méridienne non conforme

⚠️ Cas particuliers :
- enseignant Business : déclaration dans Mon Portail Paie avant le 20
- enseignant Art & Création : déclaration via école
- non enseignant : calcul automatique
"""
            result["summary"] = "L’éligibilité dépend de la durée de journée, de la pause et du profil."
            result["checks"] = [
                "Vérifier que la journée atteint 6h",
                "Vérifier la pause entre 12h et 14h",
                "Vérifier l’absence d’exclusion",
                "Vérifier le circuit selon le profil",
            ]
            result["action"] = "Comparer votre situation à la règle d’éligibilité puis demander confirmation au RH si besoin."
            result["contact"] = "RH de proximité"
            result["channel"] = "Mail RH"
            result["contact_reason"] = "Éligibilité tickets restaurant"
            result["message_ready"] = build_ready_message_for_tickets("standard", tickets_context)

        else:
            result["answer"] = """
Votre demande tickets restaurant doit être précisée avec :
- la période
- la nature exacte du problème
- votre profil (enseignant ou non)
- le pôle si vous êtes enseignant
"""
            result["summary"] = "Le sujet tickets restaurant doit être mieux qualifié."
            result["checks"] = [
                "Préciser la période",
                "Préciser le problème exact",
                "Préciser votre profil et votre pôle",
            ]
            result["action"] = "Utiliser le message prêt à transmettre."
            result["contact"] = "RH de proximité"
            result["channel"] = "Mail RH"
            result["contact_reason"] = "Sujet tickets restaurant à préciser"
            result["message_ready"] = build_ready_message_for_tickets("standard", tickets_context)

    elif theme == "Documents RH / Paie":
        result["title"] = "Documents RH / Paie"
        result["answer"] = """
Dans votre organisation, les documents RH / Paie passent toujours par le RH.

👉 Cela concerne notamment :
- attestation employeur
- attestation de salaire
- certificat de travail
- solde de tout compte
- ancien bulletin si besoin
"""
        result["summary"] = "Les documents RH passent toujours par le RH."
        result["checks"] = [
            "Identifier le document demandé",
            "Préciser la période si nécessaire",
            "Préciser l’urgence si besoin",
        ]
        result["action"] = "Adresser directement la demande au RH."
        result["contact"] = "RH"
        result["channel"] = "Mail RH"
        result["contact_reason"] = "Document RH / Paie"
        result["message_ready"] = build_rh_message(
            f"Je souhaite obtenir le document suivant : {need}. Pouvez-vous me le transmettre, s’il vous plaît ?"
        )

    elif theme == "Sortie / Fin de contrat":
        result["title"] = "Sortie / Fin de contrat"
        result["answer"] = """
Les sujets de fin de contrat nécessitent de vérifier :
- la date de fin
- les documents attendus
- les éventuelles indemnités
- le solde de tout compte
"""
        result["summary"] = "Les sujets de sortie doivent être rapprochés de la date de fin et des documents attendus."
        result["checks"] = [
            "Vérifier la date de fin",
            "Identifier le document ou montant concerné",
            "Préciser le besoin exact",
        ]
        result["action"] = "Demander une vérification RH / Paie."
        result["contact"] = "RH / Paie"
        result["channel"] = "Mail RH / Paie"
        result["contact_reason"] = "Gestion de sortie"
        if contract_type == "CDD":
            result["vigilance"].append("En CDD, la vérification des documents et indemnités de fin de contrat est particulièrement importante.")
        result["message_ready"] = build_rh_message(
            "Je vous contacte concernant ma fin de contrat. Pouvez-vous m’indiquer la marche à suivre ou vérifier ma situation ?"
        )

    elif theme == "Contrat / Statut":
        result["title"] = "Contrat / Statut"
        result["answer"] = """
Votre demande concerne un élément contractuel :
- type de contrat
- temps de travail
- forfait jours / heures
- modification de contrat

👉 Ce type de sujet relève du RH.
"""
        result["summary"] = "Les sujets contractuels doivent être traités par le RH."
        result["checks"] = [
            "Identifier le point contractuel concerné",
            "Préciser la situation actuelle",
            "Préciser la modification ou l’explication attendue",
        ]
        result["action"] = "Décrire précisément le point contractuel à vérifier."
        result["contact"] = "RH"
        result["channel"] = "Mail RH"
        result["contact_reason"] = "Sujet contractuel"
        result["message_ready"] = build_rh_message(
            f"Je souhaite obtenir des précisions sur le point contractuel suivant : {need}. Pouvez-vous m’aider, s’il vous plaît ?"
        )

    elif theme == "Demande manager":
        result["title"] = "Demande manager"
        result["answer"] = """
Votre demande relève d’un besoin manager :
- suivi d’un collaborateur
- validation
- paie
- absences
- création / onboarding

👉 Il faut d’abord identifier si le sujet relève du manager seul, du RH ou des deux.
"""
        result["summary"] = "Le besoin manager doit être orienté selon la nature du sujet."
        result["checks"] = [
            "Identifier le collaborateur ou le périmètre concerné",
            "Préciser le blocage",
            "Préciser si le sujet porte sur paie, heures, absences ou organisation",
        ]
        result["action"] = "Décrire précisément le besoin pour orienter vers le bon interlocuteur."
        result["contact"] = "Manager / RH / Paie"
        result["channel"] = "Mail RH / coordination"
        result["contact_reason"] = "Sujet manager"
        result["message_ready"] = build_rh_message(
            f"En tant que manager, je vous contacte concernant le sujet suivant : {need}. Pouvez-vous m’indiquer la marche à suivre ou vérifier la situation ?"
        )

    else:
        result["title"] = "Sujet non trouvé"
        result["answer"] = """
Votre demande n’entre pas encore dans une catégorie standard de KAREN.

👉 Cela ne veut pas dire qu’elle ne peut pas être traitée :
il faut simplement la reformuler avec plus de précision.
"""
        result["summary"] = "Le sujet doit être reformulé pour permettre une orientation fiable."
        result["checks"] = [
            "Décrire le besoin concret",
            "Préciser le contexte",
            "Préciser la période et le blocage",
        ]
        result["action"] = "KAREN prépare un message RH prêt à transmettre."
        result["contact"] = "RH / Paie"
        result["channel"] = "Mail RH / Paie"
        result["contact_reason"] = "Sujet hors référentiel standard"
        result["message_ready"] = build_rh_message(
            "Je vous contacte concernant une demande RH / Paie que je n’arrive pas à rattacher à une catégorie standard. Pouvez-vous m’indiquer la marche à suivre ?"
        )

    apply_transversal_alerts(result, role, job_type, contract_type, work_time, establishment_data["ccn"])
    return result

def run_intelligent_diagnosis(
    theme,
    need,
    role,
    establishment,
    establishment_data,
    job_type,
    contract_type,
    work_time,
    free_text,
    answers,
):
    result = build_base_answer(
        theme,
        need,
        role,
        establishment,
        establishment_data,
        job_type,
        contract_type,
        work_time,
        free_text,
    )

    if theme == "Ma paie / Mon bulletin" and need == "Mon salaire a baissé / augmenté":
        absence = answers.get("pay_absence")
        variables = answers.get("pay_variables")
        before_15 = answers.get("pay_before_15")
        acompte = answers.get("pay_acompte")
        prime = answers.get("pay_prime")

        causes = []
        if absence == "Oui":
            causes.append("une absence")
        if variables == "Oui" and before_15 == "Non":
            causes.append("un décalage M+1 lié à des éléments variables transmis ou validés après le 15")
        if acompte == "Oui":
            causes.append("un acompte déduit")
        if prime == "Oui":
            causes.append("une prime ou indemnité attendue mais non reprise")

        if causes:
            result["diagnostic"] = "Diagnostic KAREN : la variation de salaire semble probablement liée à " + ", ".join(causes) + "."
            result["summary"] = result["diagnostic"]

    elif theme == "Ma paie / Mon bulletin" and need == "Il manque des heures (FFP / induites / supplémentaires)":
        hours_type = answers.get("hours_type")
        sent = answers.get("hours_sent")
        validated = answers.get("hours_validated")
        before_15 = answers.get("hours_before_15")

        if sent == "Non":
            result["diagnostic"] = "Diagnostic KAREN : le problème semble se situer au niveau de la saisie ou de la transmission des heures."
        elif validated == "Non":
            result["diagnostic"] = "Diagnostic KAREN : le problème semble plutôt lié à une validation manager ou responsable non encore effectuée."
        elif validated == "Oui" and before_15 == "Non":
            result["diagnostic"] = "Diagnostic KAREN : les heures semblent avoir été validées ou transmises après le 15. Une prise en compte en M+1 est probable."
        elif validated == "Oui" and before_15 == "Oui":
            result["diagnostic"] = "Diagnostic KAREN : les heures semblent validées dans les délais. Une anomalie de reprise en paie doit être vérifiée."

        if result["diagnostic"]:
            result["summary"] = result["diagnostic"]

        if hours_type and hours_type != "Autre / Je ne sais pas":
            result["context"].append(f"Type d’heures identifié : {hours_type}")

    elif theme == "Heures / Activité" and need == "Mes heures FFP ne sont pas correctes":
        validated = answers.get("ffp_validated")
        before_15 = answers.get("ffp_before_15")

        if validated == "Non":
            result["diagnostic"] = "Diagnostic KAREN : les heures FFP semblent bloquées au stade de la validation."
        elif validated == "Oui" and before_15 == "Non":
            result["diagnostic"] = "Diagnostic KAREN : les heures FFP ont pu être validées ou remontées après le 15. Un report sur le mois suivant est probable."
        elif validated == "Oui" and before_15 == "Oui":
            result["diagnostic"] = "Diagnostic KAREN : les heures FFP paraissent validées dans les délais. Une vérification du calcul ou de la reprise en paie est nécessaire."

        if result["diagnostic"]:
            result["summary"] = result["diagnostic"]

    elif theme == "Heures / Activité" and need == "Heures validées mais non payées":
        validated_date = answers.get("validated_date")
        bulletin_edited = answers.get("bulletin_edited")

        if validated_date == "Non":
            result["diagnostic"] = "Diagnostic KAREN : les heures validées semblent avoir été reprises après le 15. Un report sur la paie suivante est probable."
        elif validated_date == "Oui" and bulletin_edited == "Oui":
            result["diagnostic"] = "Diagnostic KAREN : les heures semblent validées dans les délais et le bulletin est déjà sorti. Une anomalie de reprise est à vérifier."
        else:
            result["diagnostic"] = "Diagnostic KAREN : le sujet doit être confirmé en vérifiant la date exacte de validation et le cycle de paie applicable."

        if result["diagnostic"]:
            result["summary"] = result["diagnostic"]

    elif theme == "Absences / Arrêts" and need == "Je veux signaler un arrêt de travail":
        medical = answers.get("stop_medical")
        sent_rh = answers.get("stop_sent_rh")

        if medical == "Oui" and sent_rh == "Non":
            result["diagnostic"] = "Diagnostic KAREN : l’arrêt doit être transmis directement au RH de proximité."
        elif medical == "Oui" and sent_rh == "Oui":
            result["diagnostic"] = "Diagnostic KAREN : l’arrêt semble déjà transmis, il reste à confirmer sa bonne prise en compte."

        if result["diagnostic"]:
            result["summary"] = result["diagnostic"]

    elif theme == "Absences / Arrêts" and need == "Je veux comprendre l’impact sur ma paie":
        abs_type = answers.get("impact_abs_type")
        sent_rh = answers.get("impact_sent_rh")
        bulletin_done = answers.get("impact_bulletin_done")

        if abs_type == "Arrêt maladie" and sent_rh == "Non":
            result["diagnostic"] = "Diagnostic KAREN : l’impact paie ne pourra pas être sécurisé tant que l’arrêt n’aura pas été transmis au RH."
        elif abs_type == "Arrêt maladie" and bulletin_done == "Oui":
            result["diagnostic"] = "Diagnostic KAREN : le bulletin étant déjà édité, une régularisation sur le mois suivant est possible."
        else:
            result["diagnostic"] = "Diagnostic KAREN : l’impact sur la paie dépend du motif d’absence, de sa date de traitement et du statut du bulletin."

        if result["diagnostic"]:
            result["summary"] = result["diagnostic"]

    elif theme == "Télétravail" and need == "Mon manager refuse":
        portal = answers.get("tt_portal")
        refusal = answers.get("tt_manager_refusal")
        goal = answers.get("tt_goal")

        if portal == "Non":
            result["diagnostic"] = "Diagnostic KAREN : la demande ne semble pas avoir été faite dans le bon circuit."
        elif refusal == "Oui" and goal == "Comprendre la règle":
            result["diagnostic"] = "Diagnostic KAREN : le refus semble relever d’une contrainte d’organisation ou d’une règle locale."
        elif refusal == "Oui":
            result["diagnostic"] = "Diagnostic KAREN : le refus a bien été exprimé par le manager. Un échange explicatif doit d’abord être mené avec lui."
        else:
            result["diagnostic"] = "Diagnostic KAREN : le sujet nécessite de confirmer si le refus vient réellement du manager ou d’un blocage de procédure."

        if result["diagnostic"]:
            result["summary"] = result["diagnostic"]

    elif theme == "Acompte sur salaire" and need == "Comment demander un acompte":
        period = answers.get("advance_period")
        portal = answers.get("advance_portal")
        limit = answers.get("advance_limit")

        if portal == "Non":
            result["diagnostic"] = "Diagnostic KAREN : la demande d’acompte ne doit pas être faite par mail, uniquement via Mon Portail Paie."
        elif period == "Non":
            result["diagnostic"] = "Diagnostic KAREN : la période de demande semble dépassée."
        elif limit == "Non":
            result["diagnostic"] = "Diagnostic KAREN : le montant demandé semble dépasser la limite autorisée de 50 %."
        else:
            result["diagnostic"] = "Diagnostic KAREN : la demande paraît conforme si elle est bien déposée via le portail dans les délais."

        if result["diagnostic"]:
            result["summary"] = result["diagnostic"]

    elif theme == "Acompte sur salaire" and need == "Pourquoi ma demande est refusée":
        after_11 = answers.get("advance_after_11")
        over_50 = answers.get("advance_over_50")
        done_portal = answers.get("advance_done_portal")

        reasons = []
        if after_11 == "Oui":
            reasons.append("la demande semble avoir été faite après le 11")
        if over_50 == "Oui":
            reasons.append("le montant demandé semble dépasser 50 % du salaire")
        if done_portal == "Non":
            reasons.append("la demande ne semble pas avoir été faite via le portail")

        if reasons:
            result["diagnostic"] = "Diagnostic KAREN : le refus peut probablement s’expliquer par " + ", ".join(reasons) + "."
            result["summary"] = result["diagnostic"]

    elif theme == "Tickets restaurant" and need == "Nombre incorrect":
        tr_absence = answers.get("tr_absence")
        tr_regularization = answers.get("tr_regularization")

        causes = []
        if tr_absence == "Oui":
            causes.append("des jours non éligibles sur la période")
        if tr_regularization == "Oui":
            causes.append("une régularisation d’un mois précédent")

        if causes:
            result["diagnostic"] = "Diagnostic KAREN : le nombre de tickets restaurant peut probablement s’expliquer par " + " et ".join(causes) + "."
        else:
            result["diagnostic"] = "Diagnostic KAREN : le nombre de tickets semble nécessiter une vérification RH du calcul mensuel."
        result["summary"] = result["diagnostic"]

    elif theme == "Tickets restaurant" and need == "Montant incorrect":
        tr_absence = answers.get("tr_absence")
        tr_regularization = answers.get("tr_regularization")

        causes = []
        if tr_absence == "Oui":
            causes.append("des jours non éligibles")
        if tr_regularization == "Oui":
            causes.append("une régularisation d’un mois précédent")

        if causes:
            result["diagnostic"] = "Diagnostic KAREN : le montant ou le calcul des tickets restaurant peut probablement s’expliquer par " + " et ".join(causes) + "."
        else:
            result["diagnostic"] = "Diagnostic KAREN : le montant semble nécessiter une vérification RH du calcul mensuel."
        result["summary"] = result["diagnostic"]

    elif theme == "Tickets restaurant" and need == "Je ne les ai pas reçus":
        tr_card = answers.get("tr_card")
        tr_absence = answers.get("tr_absence")
        context_type = get_tickets_context(job_type, establishment_data)

        if tr_card == "Oui":
            result["diagnostic"] = "Diagnostic KAREN : le problème semble relever de la carte ou du chargement Edenred."
            result["contact"] = "Prestataire Edenred"
            result["channel"] = "Support Edenred"
            result["contact_reason"] = "Carte / chargement Edenred"
        elif context_type == "teacher_business":
            result["diagnostic"] = "Diagnostic KAREN : pour un enseignant Business, il faut d’abord vérifier la déclaration dans Mon Portail Paie avant le 20."
        elif context_type == "teacher_art_creation":
            result["diagnostic"] = "Diagnostic KAREN : pour un enseignant Art & Création, il faut vérifier le circuit école."
        elif tr_absence == "Oui":
            result["diagnostic"] = "Diagnostic KAREN : l’absence de tickets peut venir de jours non éligibles sur la période."
        else:
            result["diagnostic"] = "Diagnostic KAREN : l’absence de tickets semble nécessiter une vérification des droits et du chargement."
        result["summary"] = result["diagnostic"]

    elif theme == "Tickets restaurant" and need == "Carte Edenred problème":
        issue = answers.get("tr_edenred_issue")

        if issue == "Première réception de carte":
            result["diagnostic"] = "Diagnostic KAREN : la première réception intervient à J+5 après le virement de fin de mois, directement à domicile."
        elif issue == "Perte / vol":
            result["diagnostic"] = "Diagnostic KAREN : la perte ou le vol de la carte relève directement d’Edenred."
        elif issue == "Activation":
            result["diagnostic"] = "Diagnostic KAREN : l’activation de la carte relève directement d’Edenred."
        elif issue == "Recharge / chargement":
            result["diagnostic"] = "Diagnostic KAREN : la recharge intervient à J+2 après virement, avec un délai de chargement de 48h."
        else:
            result["diagnostic"] = "Diagnostic KAREN : le blocage de carte doit être traité directement avec Edenred."

        result["summary"] = result["diagnostic"]

    elif theme == "Tickets restaurant" and need == "Je veux savoir si j’y ai droit":
        tr_6h = answers.get("tr_6h")
        tr_break = answers.get("tr_break")
        context_type = get_tickets_context(job_type, establishment_data)

        if tr_6h == "Oui" and tr_break == "Oui":
            if context_type == "teacher_business":
                result["diagnostic"] = "Diagnostic KAREN : vous semblez potentiellement éligible, sous réserve de déclaration enseignant Business dans Mon Portail Paie avant le 20."
            elif context_type == "teacher_art_creation":
                result["diagnostic"] = "Diagnostic KAREN : vous semblez potentiellement éligible, sous réserve du circuit école applicable à votre établissement."
            else:
                result["diagnostic"] = "Diagnostic KAREN : vous semblez potentiellement éligible à un ticket restaurant par journée travaillée."
        else:
            result["diagnostic"] = "Diagnostic KAREN : vous ne semblez pas réunir à ce stade tous les critères d’éligibilité."
        result["summary"] = result["diagnostic"]

    elif theme == "Transport" and need == "Remboursement Navigo":
        justif = answers.get("transport_justif")
        if justif == "Non":
            result["diagnostic"] = "Diagnostic KAREN : le remboursement peut être bloqué en l’absence de justificatif."
        else:
            result["diagnostic"] = "Diagnostic KAREN : le remboursement nécessite une vérification de la période et du montant."
        result["summary"] = result["diagnostic"]

    elif theme == "JPO / SPO":
        if job_type in JPO_EXCLUDED_PROFILES:
            result["diagnostic"] = "Diagnostic KAREN : votre profil nécessite une vérification préalable, la logique standard JPO / SPO ne s’applique pas automatiquement."
            result["summary"] = result["diagnostic"]

        elif need == "Je sais pas où saisir":
            day_type = answers.get("jpo_day_type")
            jpo_status = answers.get("jpo_status")

            if day_type == "Le week-end":
                result["diagnostic"] = "Diagnostic KAREN : un événement JPO / SPO du week-end doit être saisi dans la section JPO du portail."
            elif day_type == "En semaine" and jpo_status == "Salarié en heures":
                result["diagnostic"] = "Diagnostic KAREN : un événement JPO / SPO en semaine pour un salarié en heures suit la logique des heures supplémentaires / éléments variables."
            elif day_type == "En semaine" and jpo_status == "Forfait jours":
                result["diagnostic"] = "Diagnostic KAREN : pour un forfait jours, l’événement en semaine ne suit pas la logique standard du salarié en heures et nécessite un contrôle spécifique."
            else:
                result["diagnostic"] = "Diagnostic KAREN : le bon module dépend du jour de l’événement et du statut heures / forfait jours."

            result["summary"] = result["diagnostic"]

        elif need == "Je peux pas poser ma récup":
            month_elapsed = answers.get("jpo_month_elapsed")
            payroll_validated = answers.get("jpo_payroll_validated")
            correct_entry = answers.get("jpo_correct_entry")

            causes = []
            if month_elapsed == "Non":
                causes.append("la JPO / SPO ne semble pas encore porter sur un mois révolu")
            if payroll_validated == "Non":
                causes.append("la validation paie ne semble pas encore finalisée")
            if correct_entry == "Non":
                causes.append("la saisie ne semble pas avoir été faite dans le bon module")

            if causes:
                result["diagnostic"] = "Diagnostic KAREN : la récupération est probablement bloquée car " + ", ".join(causes) + "."
            else:
                result["diagnostic"] = "Diagnostic KAREN : la récupération devrait être disponible si la JPO / SPO est bien validée et porte sur un mois révolu."

            result["summary"] = result["diagnostic"]

        elif need == "Ma JPO est validée mais j’ai rien":
            payroll_validated = answers.get("jpo_payroll_validated")
            before_20 = answers.get("jpo_before_20")
            expected = answers.get("jpo_expected_result")

            if payroll_validated == "Non":
                result["diagnostic"] = "Diagnostic KAREN : la validation paie ne semble pas finalisée, même si une validation partielle peut apparaître."
            elif before_20 == "Non":
                result["diagnostic"] = "Diagnostic KAREN : la validation semble être intervenue après la clôture du 20, ce qui peut décaler le résultat au cycle suivant."
            elif expected == "Récupération":
                result["diagnostic"] = "Diagnostic KAREN : la récupération peut ne pas encore être disponible si le cycle paie n’est pas totalement clôturé."
            elif expected == "Paiement":
                result["diagnostic"] = "Diagnostic KAREN : le paiement peut être décalé selon le cycle de reprise paie."
            else:
                result["diagnostic"] = "Diagnostic KAREN : le sujet nécessite de vérifier séparément la récupération et le paiement."

            result["summary"] = result["diagnostic"]

        elif need == "Je veux comprendre le motif à choisir":
            day = answers.get("jpo_weekend_day")
            expected = answers.get("jpo_expected_result")

            if day == "Samedi" and expected == "Récupéré":
                result["diagnostic"] = "Diagnostic KAREN : le motif attendu semble être Samedi récupéré."
            elif day == "Samedi" and expected == "Payé":
                result["diagnostic"] = "Diagnostic KAREN : le motif attendu semble être Samedi payé."
            elif day == "Dimanche" and expected == "Récupéré":
                result["diagnostic"] = "Diagnostic KAREN : le motif attendu semble être Dimanche récupéré."
            elif day == "Dimanche" and expected == "Payé":
                result["diagnostic"] = "Diagnostic KAREN : le motif attendu semble être Dimanche payé."
            elif day == "Dimanche" and expected == "Payé et récupéré":
                result["diagnostic"] = "Diagnostic KAREN : le motif attendu semble être Dimanche payé et récupéré."
            else:
                result["diagnostic"] = "Diagnostic KAREN : le bon motif dépend du jour concerné et du résultat attendu."

            result["summary"] = result["diagnostic"]

        elif need == "Je veux comprendre l’impact paie / récupération":
            day = answers.get("jpo_weekend_day")
            expected = answers.get("jpo_expected_result")

            if day == "Samedi":
                result["diagnostic"] = "Diagnostic KAREN : pour le samedi, la majoration de référence est de 25 %."
            elif day == "Dimanche":
                result["diagnostic"] = "Diagnostic KAREN : pour le dimanche, la majoration de référence est de 100 %."
            else:
                result["diagnostic"] = "Diagnostic KAREN : l’impact dépend du jour concerné, du motif choisi et des validations."

            if expected in {"Payé", "Récupéré", "Payé et récupéré"}:
                result["context"].append(f"Résultat attendu indiqué : {expected}")

            result["summary"] = result["diagnostic"]

    score = get_complexity_score(theme, need, free_text, job_type, answers)
    result["complexity_score"] = score
    result["complexity_label"] = get_complexity_label(score)

    if answers:
        result["context"].append("Réponses au diagnostic intelligent :")
        for key, value in answers.items():
            result["context"].append(f"- {key} : {value}")

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
    "dynamic_answers": {},
    "dynamic_questions_cache": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def reset_karen():
    st.session_state.step = 1
    st.session_state.role = None
    st.session_state.entity = None
    st.session_state.job_type = None
    st.session_state.contract_type = None
    st.session_state.work_time = None
    st.session_state.theme = None
    st.session_state.need = None
    st.session_state.free_text = ""
    st.session_state.dynamic_answers = {}
    st.session_state.dynamic_questions_cache = []

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## KAREN")
    st.caption("Agent RH / Paie guidé")
    avatar_state = "thinking" if st.session_state.get("step", 1) in [6, 7] else "idle"
    render_avatar_html(avatar_state, width=150)

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
            '<div class="small-note">Un assistant RH / Paie conçu comme un véritable outil métier : il qualifie la demande, pose des questions dynamiques, répond concrètement, puis affine le diagnostic et prépare une escalade propre si nécessaire.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<span class="metric-pill">Guidé</span>'
            '<span class="metric-pill">Réponse métier</span>'
            '<span class="metric-pill">Diagnostic intelligent</span>'
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
    "KAREN ne répond pas au hasard. L’outil qualifie le profil, prend en compte le contexte RH / paie, "
    "pose des questions utiles si besoin, puis génère une vraie réponse métier, un diagnostic complémentaire et un message prêt à transmettre."
)
st.markdown("</div>", unsafe_allow_html=True)

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
            placeholder="Exemple : mois concerné, message d’erreur, rubrique du bulletin, arrêt maladie, délai dépassé, validation manager, FFP, heures induites, Edenred…",
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
                reset_karen()
                st.rerun()
        with c3:
            if st.button("Continuer", type="primary"):
                st.session_state.theme = theme
                st.session_state.need = need
                st.session_state.free_text = free_text
                st.session_state.dynamic_answers = {}
                st.session_state.dynamic_questions_cache = get_dynamic_questions(theme, need, st.session_state.role)
                if st.session_state.dynamic_questions_cache:
                    st.session_state.step = 6
                else:
                    st.session_state.step = 7
                st.rerun()

    elif st.session_state.step == 6:
        st.write("**KAREN :** Pour affiner ma réponse, j’ai besoin de quelques informations complémentaires.")
        questions = get_visible_questions(st.session_state.dynamic_questions_cache, st.session_state.dynamic_answers)

        if not questions:
            st.session_state.step = 7
            st.rerun()

        for idx, question in enumerate(questions, start=1):
            st.markdown(f"**Question {idx}**")
            key = f"dyn_{question['id']}"
            current_value = st.session_state.dynamic_answers.get(question["id"])

            if question["type"] == "radio":
                options = question["options"]
                if current_value not in options:
                    current_value = options[0]
                value = st.radio(question["label"], options, index=options.index(current_value), key=key)
                st.session_state.dynamic_answers[question["id"]] = value

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Retour au besoin"):
                st.session_state.step = 5
                st.rerun()
        with c2:
            if st.button("Réinitialiser le diagnostic"):
                st.session_state.dynamic_answers = {}
                st.rerun()
        with c3:
            if st.button("Lancer l’analyse finale", type="primary"):
                st.session_state.step = 7
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Progression</div>', unsafe_allow_html=True)
    total_steps = 7
    progress_value = (st.session_state.step - 1) / (total_steps - 1) if st.session_state.step <= total_steps else 1
    st.progress(progress_value)
    st.caption(f"Étape {min(st.session_state.step, total_steps)} sur {total_steps}")
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
    if st.session_state.theme:
        st.write(f"- Thème : {st.session_state.theme}")
    if st.session_state.need:
        st.write(f"- Besoin : {st.session_state.need}")
    if st.session_state.dynamic_answers and st.session_state.step >= 6:
        st.write(f"- Questions dynamiques répondues : {len(st.session_state.dynamic_answers)}")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ANALYSE FINALE
# =========================================================
if st.session_state.step == 7 and st.session_state.theme and st.session_state.need:
    thinking_placeholder = st.empty()
    with thinking_placeholder.container():
        st.markdown('<div class="karen-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">KAREN analyse votre demande</div>', unsafe_allow_html=True)
        render_avatar_html("thinking", width=170)
        st.markdown('<div class="thinking-ring"></div>', unsafe_allow_html=True)
        st.write("Qualification du profil, lecture du besoin, réponse métier, analyse des réponses dynamiques et préparation du message...")
        st.markdown("</div>", unsafe_allow_html=True)

    time.sleep(0.8)

    establishment_data = get_establishment_data(st.session_state.entity)

    result = run_intelligent_diagnosis(
        st.session_state.theme,
        st.session_state.need,
        st.session_state.role,
        st.session_state.entity,
        establishment_data,
        st.session_state.job_type,
        st.session_state.contract_type,
        st.session_state.work_time,
        st.session_state.free_text,
        st.session_state.dynamic_answers,
    )

    message_for_export = result["message_ready"] or result["message_rh"] or result["message_manager"] or st.session_state.free_text
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
        message_override=message_for_export,
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
            {result["answer"] if result["answer"] else ""}
            {"<br><br>" + result["summary"] if result["summary"] else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result["diagnostic"]:
        st.markdown(
            f'<div class="info-box"><strong>{result["diagnostic"]}</strong></div>',
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
        st.markdown('<div class="info-box"><strong>Alertes contextuelles</strong></div>', unsafe_allow_html=True)
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

    if result["message_manager"]:
        st.markdown('<div class="karen-card">', unsafe_allow_html=True)
        st.markdown("### Message prêt à transmettre au manager")
        st.text_area("Message manager", value=result["message_manager"], height=180, key="manager_msg")
        st.markdown("</div>", unsafe_allow_html=True)

    if result["message_rh"]:
        st.markdown('<div class="karen-card">', unsafe_allow_html=True)
        st.markdown("### Message prêt à transmettre au RH")
        st.text_area("Message RH", value=result["message_rh"], height=180, key="rh_msg")
        st.markdown("</div>", unsafe_allow_html=True)

    if result["message_ready"]:
        st.markdown('<div class="karen-card">', unsafe_allow_html=True)
        st.markdown("### Message prêt à transmettre")
        st.text_area("Message", value=result["message_ready"], height=220, key="ready_msg")
        st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.3])
    with c1:
        if st.button("Revenir aux questions dynamiques"):
            if st.session_state.dynamic_questions_cache:
                st.session_state.step = 6
            else:
                st.session_state.step = 5
            st.rerun()
    with c2:
        if st.button("Nouvelle conversation avec KAREN"):
            reset_karen()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown("### Export du message")
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
        "Avancez étape par étape dans la conversation avec KAREN pour obtenir une vraie réponse métier, "
        "des questions de diagnostic si nécessaire, une orientation fiable et un message prêt à transmettre."
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