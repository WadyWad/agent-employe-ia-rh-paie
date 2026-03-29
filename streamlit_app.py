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
# QUESTIONS DYNAMIQUES
# =========================================================
DYNAMIC_QUESTIONS = {
    ("Ma paie / Mon bulletin", "Mon salaire a baissé / augmenté"): [
        {
            "id": "pay_absence",
            "label": "Avez-vous eu une absence sur la période concernée ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "pay_variables",
            "label": "Aviez-vous des éléments variables attendus ce mois-ci ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "pay_before_15",
            "label": "Ces éléments ont-ils été transmis ou validés avant le 15 ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
            "show_if": lambda a: a.get("pay_variables") == "Oui",
        },
        {
            "id": "pay_acompte",
            "label": "Avez-vous demandé un acompte ce mois-ci ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "pay_prime",
            "label": "Attendiez-vous une prime ou une indemnité habituelle ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
    ],
    ("Ma paie / Mon bulletin", "Il manque des heures (FFP / induites / supplémentaires)"): [
        {
            "id": "hours_type",
            "label": "Quel type d'heures est concerné ?",
            "type": "radio",
            "options": ["FFP", "Heures induites", "Heures supplémentaires", "Autre / Je ne sais pas"],
        },
        {
            "id": "hours_sent",
            "label": "Les heures ont-elles bien été saisies ou transmises ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "hours_validated",
            "label": "Les heures ont-elles été validées par le manager / responsable ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "hours_before_15",
            "label": "La transmission ou la validation a-t-elle eu lieu avant le 15 ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
            "show_if": lambda a: a.get("hours_sent") == "Oui" or a.get("hours_validated") == "Oui",
        },
    ],
    ("Heures / Activité", "Mes heures FFP ne sont pas correctes"): [
        {
            "id": "ffp_validated",
            "label": "Les heures FFP ont-elles été validées ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "ffp_before_15",
            "label": "La validation ou la transmission a-t-elle eu lieu avant le 15 ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "ffp_same_month",
            "label": "Le problème concerne-t-il uniquement le mois en cours ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
    ],
    ("Heures / Activité", "Heures validées mais non payées"): [
        {
            "id": "validated_date",
            "label": "La validation a-t-elle eu lieu avant le 15 ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "bulletin_edited",
            "label": "Le bulletin du mois concerné est-il déjà disponible ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
    ],
    ("Heures / Activité", "Problème de transmission des heures"): [
        {
            "id": "transmission_done",
            "label": "Les heures ont-elles été transmises dans l'outil ou au bon interlocuteur ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "transmission_block",
            "label": "À quelle étape le blocage semble-t-il se situer ?",
            "type": "radio",
            "options": ["Saisie", "Validation", "Remontée paie", "Je ne sais pas"],
        },
    ],
    ("Absences / Arrêts", "Je veux signaler un arrêt de travail"): [
        {
            "id": "stop_medical",
            "label": "S’agit-il bien d’un arrêt de travail médical ?",
            "type": "radio",
            "options": ["Oui", "Non"],
        },
        {
            "id": "stop_sent_rh",
            "label": "Avez-vous déjà transmis l’arrêt au RH de proximité ?",
            "type": "radio",
            "options": ["Oui", "Non"],
        },
        {
            "id": "stop_urgent",
            "label": "L’arrêt commence-t-il aujourd’hui ou est-il déjà en cours ?",
            "type": "radio",
            "options": ["Oui", "Non"],
        },
    ],
    ("Absences / Arrêts", "Je veux comprendre l’impact sur ma paie"): [
        {
            "id": "impact_abs_type",
            "label": "Le sujet concerne-t-il un arrêt maladie ou une autre absence ?",
            "type": "radio",
            "options": ["Arrêt maladie", "Autre absence", "Je ne sais pas"],
        },
        {
            "id": "impact_sent_rh",
            "label": "L’arrêt ou l’information a-t-il été transmis au RH ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "impact_bulletin_done",
            "label": "Le bulletin du mois concerné est-il déjà édité ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
    ],
    ("Télétravail", "Mon manager refuse"): [
        {
            "id": "tt_portal",
            "label": "La demande de télétravail a-t-elle bien été faite via le portail ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "tt_manager_refusal",
            "label": "Le refus vient-il explicitement du manager ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "tt_goal",
            "label": "Souhaitez-vous surtout comprendre la règle ou demander un réexamen ?",
            "type": "radio",
            "options": ["Comprendre la règle", "Demander un réexamen"],
        },
    ],
    ("Acompte sur salaire", "Comment demander un acompte"): [
        {
            "id": "advance_period",
            "label": "Êtes-vous entre le 1er jour du mois et le 11 à minuit ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "advance_portal",
            "label": "Allez-vous faire la demande via Mon Portail Paie ?",
            "type": "radio",
            "options": ["Oui", "Non"],
        },
        {
            "id": "advance_limit",
            "label": "Le montant demandé reste-t-il inférieur ou égal à 50 % du salaire ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
    ],
    ("Acompte sur salaire", "Pourquoi ma demande est refusée"): [
        {
            "id": "advance_after_11",
            "label": "La demande a-t-elle été faite après le 11 ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "advance_over_50",
            "label": "Le montant demandé dépassait-il 50 % du salaire ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
        {
            "id": "advance_done_portal",
            "label": "La demande a-t-elle bien été faite via le portail ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
    ],
    ("Documents RH / Paie", "Attestation employeur"): [
        {
            "id": "doc_urgency",
            "label": "Votre demande est-elle urgente ?",
            "type": "radio",
            "options": ["Oui", "Non"],
        },
        {
            "id": "doc_reason",
            "label": "Souhaitez-vous préciser l’usage du document ?",
            "type": "radio",
            "options": ["Oui", "Non"],
        },
    ],
    ("Documents RH / Paie", "Attestation de salaire"): [
        {
            "id": "doc_urgency",
            "label": "Votre demande est-elle urgente ?",
            "type": "radio",
            "options": ["Oui", "Non"],
        },
    ],
    ("Documents RH / Paie", "Certificat de travail"): [
        {
            "id": "doc_received",
            "label": "Avez-vous déjà reçu ce document ?",
            "type": "radio",
            "options": ["Oui", "Non"],
        },
    ],
    ("Documents RH / Paie", "Solde de tout compte"): [
        {
            "id": "stc_end_date",
            "label": "La date de fin de contrat est-elle déjà passée ?",
            "type": "radio",
            "options": ["Oui", "Non"],
        },
    ],
    ("Tickets restaurant", "Nombre incorrect"): [
        {
            "id": "tr_absence",
            "label": "Avez-vous eu des absences ou un mois incomplet sur la période ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
    ],
    ("Tickets restaurant", "Je ne les ai pas reçus"): [
        {
            "id": "tr_card",
            "label": "Le problème concerne-t-il la carte / le chargement plutôt que le droit lui-même ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
    ],
    ("Transport", "Remboursement Navigo"): [
        {
            "id": "transport_justif",
            "label": "Avez-vous déjà transmis votre justificatif ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
    ],
    ("Transport", "Montant incorrect"): [
        {
            "id": "transport_change",
            "label": "Votre abonnement ou votre situation a-t-il changé récemment ?",
            "type": "radio",
            "options": ["Oui", "Non", "Je ne sais pas"],
        },
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
            {
                "id": "mgr_pay_subject",
                "label": "Le problème du collaborateur concerne-t-il surtout la paie ou les heures ?",
                "type": "radio",
                "options": ["Paie", "Heures", "Les deux"],
            },
            {
                "id": "mgr_pay_validated",
                "label": "Les éléments ont-ils déjà été validés par le manager ?",
                "type": "radio",
                "options": ["Oui", "Non", "Je ne sais pas"],
            },
        ]
    elif role == "Manager" and theme == "Demande manager" and need == "Heures non validées":
        questions = [
            {
                "id": "mgr_hours_stage",
                "label": "Le blocage se situe-t-il au stade de validation manager ?",
                "type": "radio",
                "options": ["Oui", "Non", "Je ne sais pas"],
            },
            {
                "id": "mgr_hours_before_15",
                "label": "Le sujet impacte-t-il la paie du mois en cours avant le 15 ?",
                "type": "radio",
                "options": ["Oui", "Non", "Je ne sais pas"],
            },
        ]

    return questions

def get_visible_questions(questions, answers):
    visible = []
    for q in questions:
        show_if = q.get("show_if")
        if show_if is None or show_if(answers):
            visible.append(q)
    return visible

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
        "summary": "Votre besoin a été qualifié par KAREN. Une orientation fiable peut être proposée sur la base des règles métier connues.",
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
    result = init_result(role, establishment, establishment_data, job_type, contract_type, work_time, theme, need)
    ccn = establishment_data["ccn"]

    # =====================================================
    # DIAGNOSTICS INTELLIGENTS PRIORITAIRES
    # =====================================================
    if theme == "Ma paie / Mon bulletin" and need == "Mon salaire a baissé / augmenté":
        absence = answers.get("pay_absence")
        variables = answers.get("pay_variables")
        before_15 = answers.get("pay_before_15")
        acompte = answers.get("pay_acompte")
        prime = answers.get("pay_prime")

        result["title"] = "Diagnostic intelligent — variation de salaire"

        causes = []
        if absence == "Oui":
            causes.append("une absence ayant pu impacter la paie")
        if variables == "Oui" and before_15 == "Non":
            causes.append("un décalage M+1 lié à des éléments variables transmis ou validés après le 15")
        if acompte == "Oui":
            causes.append("un acompte déduit du net")
        if prime == "Oui":
            causes.append("une prime ou indemnité attendue mais non reprise")

        if causes:
            result["diagnostic"] = "La variation de salaire semble probablement liée à " + ", ".join(causes) + "."
        else:
            result["diagnostic"] = "La variation de salaire ne ressort pas comme anormale à ce stade, mais un contrôle RH / paie reste nécessaire pour confirmer l'origine exacte."

        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Comparer le bulletin du mois avec celui du mois précédent.",
            "Vérifier les absences, primes, acomptes et variables du mois.",
            "Vérifier si des éléments ont été transmis ou validés après le 15.",
        ]
        result["action"] = "Transmettre la demande au RH / Paie avec le mois concerné et la nature de l’écart."
        result["contact"] = "RH / Paie"
        result["channel"] = "Mail RH / Paie"
        result["contact_reason"] = "Variation salariale à confirmer"
        result["message_ready"] = build_rh_message(
            "Je constate une variation sur mon salaire ce mois-ci. Pouvez-vous me préciser si elle est liée à une absence, à un acompte, à une prime ou à un décalage de prise en compte d’éléments variables transmis ou validés après le 15 ?"
        )

    elif theme == "Ma paie / Mon bulletin" and need == "Il manque des heures (FFP / induites / supplémentaires)":
        hours_type = answers.get("hours_type")
        sent = answers.get("hours_sent")
        validated = answers.get("hours_validated")
        before_15 = answers.get("hours_before_15")

        result["title"] = "Diagnostic intelligent — heures manquantes"

        if sent == "Non":
            result["diagnostic"] = "Le problème semble se situer en amont, au niveau de la saisie ou de la transmission des heures."
            result["contact"] = "Manager / Responsable"
            result["channel"] = "Mail manager"
            result["contact_reason"] = "Transmission des heures à sécuriser"
            result["message_manager"] = build_manager_message(
                f"Certaines de mes heures ({hours_type}) ne semblent pas apparaître. Pouvez-vous me confirmer qu’elles ont bien été saisies et transmises dans le bon circuit ?"
            )
        elif validated == "Non":
            result["diagnostic"] = "Le problème semble plutôt lié à une validation manager ou responsable non encore effectuée."
            result["contact"] = "Manager / Responsable"
            result["channel"] = "Mail manager"
            result["contact_reason"] = "Validation manquante"
            result["message_manager"] = build_manager_message(
                f"Certaines de mes heures ({hours_type}) ne figurent pas sur mon bulletin. Pouvez-vous me confirmer si elles ont bien été validées ?"
            )
        elif validated == "Oui" and before_15 == "Non":
            result["diagnostic"] = "Les heures semblent avoir été validées ou transmises après le cut-off du 15. Une prise en compte en M+1 est probable."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Décalage probable M+1"
            result["message_ready"] = build_rh_message(
                f"Certaines de mes heures ({hours_type}) ne figurent pas sur mon bulletin. Pouvez-vous me confirmer si elles ont été validées ou transmises après le 15 et si une régularisation est prévue le mois prochain ?"
            )
        elif validated == "Oui" and before_15 == "Oui":
            result["diagnostic"] = "Les heures semblent avoir été validées dans les délais. Une anomalie de reprise en paie doit être vérifiée."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Anomalie probable de reprise"
            result["message_ready"] = build_rh_message(
                f"Certaines de mes heures ({hours_type}) ont bien été validées avant le 15 mais ne figurent pas sur mon bulletin. Pouvez-vous vérifier leur prise en compte en paie ?"
            )
        else:
            result["diagnostic"] = "Le sujet nécessite un contrôle croisé entre le circuit de transmission, la validation et la reprise en paie."
            result["contact"] = "Manager + RH / Paie"
            result["channel"] = "Mail manager puis RH"
            result["contact_reason"] = "Contrôle croisé nécessaire"
            result["message_manager"] = build_manager_message(
                f"Certaines de mes heures ({hours_type}) ne figurent pas sur mon bulletin. Pouvez-vous me confirmer leur statut de validation et de transmission ?"
            )
            result["message_rh"] = build_rh_message(
                f"Certaines de mes heures ({hours_type}) ne figurent pas sur mon bulletin. Une fois le statut de validation confirmé, pouvez-vous vérifier leur prise en compte en paie ?"
            )

        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Identifier le type d’heures concerné.",
            "Vérifier la saisie, la transmission et la validation.",
            "Vérifier si le traitement a eu lieu avant ou après le 15.",
        ]
        result["action"] = "Suivre le circuit recommandé selon le diagnostic."

    elif theme == "Heures / Activité" and need == "Mes heures FFP ne sont pas correctes":
        validated = answers.get("ffp_validated")
        before_15 = answers.get("ffp_before_15")

        result["title"] = "Diagnostic intelligent — heures FFP"
        if validated == "Non":
            result["diagnostic"] = "Les heures FFP semblent bloquées au stade de la validation."
            result["contact"] = "Manager / Responsable"
            result["channel"] = "Mail manager"
            result["contact_reason"] = "Validation FFP manquante"
            result["message_manager"] = build_manager_message(
                "Mes heures FFP semblent incorrectes. Pouvez-vous me confirmer leur statut de validation et leur remontée ?"
            )
        elif validated == "Oui" and before_15 == "Non":
            result["diagnostic"] = "Les heures FFP ont pu être validées ou remontées après le 15. Un report sur le mois suivant est probable."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Décalage probable M+1 sur FFP"
            result["message_ready"] = build_rh_message(
                "Mes heures FFP semblent incorrectes. Pouvez-vous me confirmer si leur validation ou leur transmission est intervenue après le 15 et si une régularisation est prévue le mois prochain ?"
            )
        elif validated == "Oui" and before_15 == "Oui":
            result["diagnostic"] = "Les heures FFP paraissent validées dans les délais. Une vérification du calcul ou de la reprise en paie est nécessaire."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Contrôle calcul / reprise FFP"
            result["message_ready"] = build_rh_message(
                "Mes heures FFP semblent incorrectes alors qu’elles ont été validées dans les délais. Pouvez-vous vérifier le calcul et leur reprise en paie ?"
            )
        else:
            result["diagnostic"] = "Le sujet FFP nécessite une vérification du circuit complet : remontée, validation et reprise en paie."
            result["contact"] = "Manager + RH / Paie"
            result["channel"] = "Mail manager puis RH"
            result["contact_reason"] = "Circuit FFP à sécuriser"
            result["message_manager"] = build_manager_message(
                "Mes heures FFP semblent incorrectes. Pouvez-vous me confirmer leur volume transmis et leur statut de validation ?"
            )
            result["message_rh"] = build_rh_message(
                "Mes heures FFP semblent incorrectes. Une fois la validation et la transmission confirmées, pouvez-vous vérifier leur reprise en paie ?"
            )

        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Vérifier le volume d’heures FFP attendu.",
            "Vérifier la remontée pédagogique et la validation.",
            "Contrôler la date de validation au regard du cut-off du 15.",
        ]
        result["action"] = "Demander la confirmation du circuit FFP puis la vérification paie si nécessaire."

    elif theme == "Heures / Activité" and need == "Heures validées mais non payées":
        validated_date = answers.get("validated_date")
        bulletin_edited = answers.get("bulletin_edited")

        result["title"] = "Diagnostic intelligent — heures validées non payées"
        if validated_date == "Non":
            result["diagnostic"] = "Les heures validées semblent avoir été reprises après le 15. Un report sur la paie suivante est probable."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Décalage M+1 probable"
            result["message_ready"] = build_rh_message(
                "Mes heures apparaissent comme validées mais ne figurent pas sur mon bulletin. Pouvez-vous me confirmer si la validation est intervenue après le 15 et si une régularisation est prévue sur le mois suivant ?"
            )
        elif validated_date == "Oui" and bulletin_edited == "Oui":
            result["diagnostic"] = "Les heures semblent validées dans les délais et le bulletin est déjà sorti. Une anomalie de reprise est à vérifier."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Anomalie probable de paie"
            result["message_ready"] = build_rh_message(
                "Mes heures apparaissent comme validées avant le 15 mais ne figurent pas sur mon bulletin déjà édité. Pouvez-vous vérifier leur reprise en paie ?"
            )
        else:
            result["diagnostic"] = "Le sujet doit être confirmé en vérifiant la date exacte de validation et le cycle de paie applicable."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Vérification du cycle de paie"
            result["message_ready"] = build_rh_message(
                "Mes heures apparaissent comme validées mais ne figurent pas sur mon bulletin. Pouvez-vous me confirmer leur date de validation et la paie sur laquelle elles doivent être reprises ?"
            )

        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Vérifier la date exacte de validation.",
            "Vérifier le bulletin concerné.",
            "Confirmer le mois de paie attendu.",
        ]
        result["action"] = "Transmettre la preuve de validation avec le mois concerné."

    elif theme == "Absences / Arrêts" and need == "Je veux signaler un arrêt de travail":
        medical = answers.get("stop_medical")
        sent_rh = answers.get("stop_sent_rh")

        result["title"] = "Diagnostic intelligent — arrêt de travail"
        result["contact"] = "RH de proximité"
        result["channel"] = "Transmission directe RH"
        result["contact_reason"] = "Règle interne arrêt de travail"

        if medical == "Oui" and sent_rh == "Non":
            result["diagnostic"] = "L’arrêt de travail doit être transmis directement au RH de proximité. Il ne passe ni par le portail ni par le manager."
            result["action"] = "Envoyer immédiatement l’arrêt au RH de proximité."
            result["message_ready"] = build_rh_message(
                "Je vous informe être en arrêt de travail à compter du [date]. Vous trouverez ci-joint mon arrêt de travail. Merci de bien vouloir en prendre compte."
            )
        elif medical == "Oui" and sent_rh == "Oui":
            result["diagnostic"] = "L’arrêt semble déjà transmis au RH de proximité. Il faut maintenant vérifier sa bonne prise en compte."
            result["action"] = "Demander une confirmation de bonne réception si nécessaire."
            result["message_ready"] = build_rh_message(
                "Je vous confirme avoir transmis mon arrêt de travail. Pouvez-vous me confirmer sa bonne prise en compte ?"
            )
        else:
            result["diagnostic"] = "Le sujet doit être requalifié. S’il s’agit bien d’un arrêt médical, la transmission se fait directement au RH de proximité."
            result["action"] = "Confirmer la nature exacte de l’absence."
            result["message_ready"] = build_rh_message(
                "Je souhaite confirmer la bonne procédure applicable à ma situation. Pouvez-vous m’indiquer si elle doit être traitée comme un arrêt de travail médical ?"
            )

        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Vérifier qu’il s’agit bien d’un arrêt médical.",
            "Vérifier si le document a déjà été transmis.",
            "Ne pas passer par le portail ni par le manager.",
        ]

    elif theme == "Absences / Arrêts" and need == "Je veux comprendre l’impact sur ma paie":
        abs_type = answers.get("impact_abs_type")
        sent_rh = answers.get("impact_sent_rh")
        bulletin_done = answers.get("impact_bulletin_done")

        result["title"] = "Diagnostic intelligent — impact absence sur paie"
        if abs_type == "Arrêt maladie" and sent_rh == "Non":
            result["diagnostic"] = "L’impact paie ne pourra pas être sécurisé tant que l’arrêt n’aura pas été transmis au RH de proximité."
            result["contact"] = "RH de proximité"
            result["channel"] = "Transmission directe RH"
            result["contact_reason"] = "Arrêt non encore transmis"
            result["message_ready"] = build_rh_message(
                "Je souhaite comprendre l’impact de mon arrêt sur ma paie. Pouvez-vous me confirmer la bonne prise en compte de mon arrêt et les éventuelles conséquences sur le bulletin ?"
            )
        elif abs_type == "Arrêt maladie" and bulletin_done == "Oui":
            result["diagnostic"] = "Le bulletin étant déjà édité, une régularisation sur le mois suivant est possible selon le traitement des IJSS et du maintien."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Régularisation possible M+1"
            result["message_ready"] = build_rh_message(
                "Suite à mon arrêt de travail, pouvez-vous me préciser l’impact sur ma paie et m’indiquer si une régularisation est prévue sur le mois suivant ?"
            )
        else:
            result["diagnostic"] = "L’impact sur la paie dépend du motif d’absence, de sa date de traitement et du statut du bulletin."
            result["contact"] = "RH / Paie"
            result["channel"] = "Mail RH / Paie"
            result["contact_reason"] = "Analyse d’impact absence"
            result["message_ready"] = build_rh_message(
                "Pouvez-vous me préciser l’impact de mon absence sur ma paie, ainsi que les éventuelles régularisations à venir ?"
            )

        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Identifier le motif exact de l’absence.",
            "Vérifier si l’information a bien été transmise au RH.",
            "Vérifier si le bulletin est déjà édité.",
        ]
        result["action"] = "Demander une explication ciblée au RH / Paie."

    elif theme == "Télétravail" and need == "Mon manager refuse":
        portal = answers.get("tt_portal")
        refusal = answers.get("tt_manager_refusal")
        goal = answers.get("tt_goal")

        result["title"] = "Diagnostic intelligent — refus télétravail"
        if portal == "Non":
            result["diagnostic"] = "La demande semble ne pas avoir été faite dans le bon circuit. Le télétravail doit d’abord être géré via le portail."
            result["contact"] = "Portail / Manager"
            result["channel"] = "Portail puis validation manager"
            result["contact_reason"] = "Procédure non conforme"
            result["message_ready"] = build_manager_message(
                "Je souhaite régulariser ma demande de télétravail. Pouvez-vous me confirmer le bon circuit une fois ma demande déposée dans le portail ?"
            )
        elif refusal == "Oui":
            if goal == "Comprendre la règle":
                result["diagnostic"] = "Le refus relève vraisemblablement d’une contrainte d’organisation ou d’une règle d’application locale. Le manager est le premier interlocuteur."
            else:
                result["diagnostic"] = "Le refus a bien été exprimé par le manager. Un échange explicatif ou une demande de réexamen doit d’abord être porté au manager."
            result["contact"] = "Manager"
            result["channel"] = "Échange manager"
            result["contact_reason"] = "Refus manager"
            result["message_ready"] = build_manager_message(
                "Suite au refus de ma demande de télétravail, pouvez-vous me préciser les raisons de ce refus et m’indiquer si une adaptation ou un réexamen est possible ?"
            )
        else:
            result["diagnostic"] = "Le sujet nécessite de confirmer si le refus vient réellement du manager ou d’un blocage de procédure."
            result["contact"] = "Manager / RH"
            result["channel"] = "Échange manager puis RH si besoin"
            result["contact_reason"] = "Refus à qualifier"
            result["message_manager"] = build_manager_message(
                "Ma demande de télétravail semble bloquée. Pouvez-vous me confirmer s’il s’agit d’un refus manager ou d’un autre motif ?"
            )

        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Vérifier que la demande a bien été faite dans le portail.",
            "Vérifier la nature exacte du refus.",
            "Échanger avec le manager en premier si le refus est bien managérial.",
        ]
        result["action"] = "Commencer par l’échange manager, puis solliciter le RH en cas de besoin."

    elif theme == "Acompte sur salaire" and need == "Comment demander un acompte":
        period = answers.get("advance_period")
        portal = answers.get("advance_portal")
        limit = answers.get("advance_limit")

        result["title"] = "Diagnostic intelligent — demande d’acompte"
        result["contact"] = "Mon Portail Paie"
        result["channel"] = "Portail"
        result["contact_reason"] = "Acompte géré exclusivement via le portail"

        if portal == "Non":
            result["diagnostic"] = "La demande d’acompte ne doit pas être faite par mail. Elle se fait exclusivement via Mon Portail Paie."
        elif period == "Non":
            result["diagnostic"] = "La période de demande semble dépassée. L’acompte doit être demandé entre le 1er jour du mois et le 11 à minuit."
        elif limit == "Non":
            result["diagnostic"] = "Le montant demandé semble dépasser la limite de 50 % du salaire."
        else:
            result["diagnostic"] = "La demande d’acompte paraît conforme si elle est bien déposée via le portail dans les délais et dans la limite autorisée."

        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Vérifier la date de la demande.",
            "Vérifier que la demande passe bien par le portail.",
            "Vérifier la limite de 50 % du salaire.",
        ]
        result["action"] = "Faire ou suivre la demande directement dans Mon Portail Paie."
        result["message_ready"] = build_rh_message(
            "Je souhaite une confirmation sur ma demande d’acompte. Pouvez-vous me préciser si elle est conforme aux règles applicables et correctement prise en compte ?"
        )

    elif theme == "Acompte sur salaire" and need == "Pourquoi ma demande est refusée":
        after_11 = answers.get("advance_after_11")
        over_50 = answers.get("advance_over_50")
        done_portal = answers.get("advance_done_portal")

        result["title"] = "Diagnostic intelligent — refus d’acompte"
        reasons = []
        if after_11 == "Oui":
            reasons.append("la demande semble avoir été faite après le 11")
        if over_50 == "Oui":
            reasons.append("le montant demandé semble dépasser 50 % du salaire")
        if done_portal == "Non":
            reasons.append("la demande ne semble pas avoir été faite via le portail")

        if reasons:
            result["diagnostic"] = "Le refus de l’acompte peut probablement s’expliquer par " + ", ".join(reasons) + "."
        else:
            result["diagnostic"] = "La cause du refus n’est pas totalement identifiable à ce stade. Une vérification RH / Paie est nécessaire."

        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Vérifier la date exacte de la demande.",
            "Vérifier le montant demandé.",
            "Vérifier le canal utilisé.",
        ]
        result["action"] = "Demander la raison précise du refus au RH / Paie si la demande semble conforme."
        result["contact"] = "RH / Paie"
        result["channel"] = "Mail RH / Paie"
        result["contact_reason"] = "Refus d’acompte à confirmer"
        result["message_ready"] = build_rh_message(
            "Ma demande d’acompte semble avoir été refusée ou non traitée. Pouvez-vous m’indiquer la raison exacte de ce refus ?"
        )

    elif theme == "Documents RH / Paie":
        result["title"] = "Diagnostic intelligent — document RH"
        result["diagnostic"] = "Les documents RH / Paie passent toujours par le service RH."
        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Identifier précisément le document demandé.",
            "Préciser la période concernée si nécessaire.",
            "Préciser le niveau d’urgence le cas échéant.",
        ]
        result["action"] = "Adresser directement la demande au RH."
        result["contact"] = "RH"
        result["channel"] = "Mail RH"
        result["contact_reason"] = "Document RH"
        if need == "Attestation employeur":
            result["message_ready"] = build_rh_message(
                "Je souhaite obtenir une attestation employeur. Pouvez-vous me l’adresser, s’il vous plaît ?"
            )
        elif need == "Attestation de salaire":
            result["message_ready"] = build_rh_message(
                "Je souhaite obtenir une attestation de salaire. Pouvez-vous me l’adresser, s’il vous plaît ?"
            )
        elif need == "Certificat de travail":
            result["message_ready"] = build_rh_message(
                "Je souhaite obtenir mon certificat de travail. Pouvez-vous me l’adresser, s’il vous plaît ?"
            )
        elif need == "Solde de tout compte":
            result["message_ready"] = build_rh_message(
                "Je souhaite obtenir mon solde de tout compte ainsi que les documents associés. Pouvez-vous me les transmettre, s’il vous plaît ?"
            )
        elif need == "Bulletin ancien":
            result["message_ready"] = build_rh_message(
                "Je souhaite récupérer un ancien bulletin de salaire. Pouvez-vous me l’adresser ou m’indiquer où le retrouver ?"
            )
        else:
            result["message_ready"] = build_rh_message(
                "Je souhaite obtenir un document RH / Paie. Pouvez-vous me préciser la marche à suivre ou me le transmettre ?"
            )

    elif theme == "Tickets restaurant" and need == "Nombre incorrect":
        tr_absence = answers.get("tr_absence")
        result["title"] = "Diagnostic intelligent — tickets restaurant"
        if tr_absence == "Oui":
            result["diagnostic"] = "Le nombre de tickets restaurant peut être impacté par les absences ou un mois incomplet."
        else:
            result["diagnostic"] = "Le nombre de tickets restaurant semble nécessiter une vérification du calcul ou des droits sur la période."
        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Vérifier la période concernée.",
            "Vérifier les absences éventuelles.",
            "Vérifier le nombre de jours éligibles.",
        ]
        result["action"] = "Demander une vérification au RH."
        result["contact"] = "RH"
        result["channel"] = "Mail RH"
        result["contact_reason"] = "Contrôle tickets restaurant"
        result["message_ready"] = build_rh_message(
            "Le nombre de tickets restaurant attribué semble incorrect. Pouvez-vous vérifier le calcul en fonction de mes jours de présence et de mes éventuelles absences ?"
        )

    elif theme == "Transport" and need == "Remboursement Navigo":
        justif = answers.get("transport_justif")
        result["title"] = "Diagnostic intelligent — remboursement transport"
        if justif == "Non":
            result["diagnostic"] = "Le remboursement Navigo peut être bloqué en l’absence de justificatif."
        else:
            result["diagnostic"] = "Le remboursement transport nécessite une vérification de la période et du montant pris en compte."
        result["summary"] = result["diagnostic"]
        result["checks"] = [
            "Vérifier le justificatif transmis.",
            "Vérifier la période concernée.",
            "Vérifier le montant repris.",
        ]
        result["action"] = "Régulariser ou relancer la demande auprès du RH."
        result["contact"] = "RH"
        result["channel"] = "Mail RH"
        result["contact_reason"] = "Transport à vérifier"
        result["message_ready"] = build_rh_message(
            "Je souhaite savoir si mon remboursement de transport Navigo a bien été pris en compte. Pouvez-vous vérifier ma situation ?"
        )

    else:
        # -------------------------------------------------
        # FALLBACK : règle métier standard existante
        # -------------------------------------------------
        result["title"] = "Analyse standard de la demande"
        result["summary"] = "KAREN a qualifié votre demande. Le cas ne relève pas d’un diagnostic dynamique spécifique et suit donc la logique standard."
        result["diagnostic"] = result["summary"]
        result["checks"] = [
            "Vérifier le thème, le besoin précis et la période concernée.",
            "Relire les éléments saisis.",
            "Préparer les informations utiles avant transmission.",
        ]
        result["action"] = "Utiliser le message prêt à transmettre."
        result["contact"] = "RH / Paie"
        result["channel"] = "Mail RH / Paie"
        result["contact_reason"] = "Traitement standard"
        result["message_ready"] = build_rh_message(
            f"Je vous contacte au sujet de ma demande « {theme} / {need} ». Pouvez-vous m’indiquer la marche à suivre ou vérifier ma situation ?"
        )

    score = get_complexity_score(theme, need, free_text, job_type, answers)
    result["complexity_score"] = score
    result["complexity_label"] = get_complexity_label(score)

    if answers:
        result["context"].append("Réponses au diagnostic intelligent :")
        for key, value in answers.items():
            result["context"].append(f"- {key} : {value}")

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
            '<div class="small-note">Un assistant RH / Paie conçu comme un véritable outil métier : il qualifie la demande, pose des questions dynamiques, applique une logique de tri, propose une réponse utile et prépare une escalade propre si nécessaire.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<span class="metric-pill">Guidé</span>'
            '<span class="metric-pill">Diagnostic intelligent</span>'
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
    "KAREN ne répond pas au hasard. L’outil qualifie le profil, prend en compte le contexte RH / paie, "
    "pose des questions complémentaires utiles, puis génère un diagnostic, une orientation fiable et un message prêt à transmettre."
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
    "dynamic_answers": {},
    "dynamic_questions_cache": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def reset_karen():
    for key in defaults.keys():
        st.session_state[key] = {} if key == "dynamic_answers" else ([] if key == "dynamic_questions_cache" else ("" if key == "free_text" else None))
    st.session_state.step = 1

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
        st.write("**KAREN :** Pour vous répondre précisément, j’ai besoin de quelques informations complémentaires.")
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
            if st.button("Lancer le diagnostic intelligent", type="primary"):
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
        st.write("Qualification du profil, lecture du besoin, analyse des réponses dynamiques et préparation du diagnostic...")
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
            {result["summary"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result["diagnostic"]:
        st.markdown(
            f'<div class="info-box"><strong>Diagnostic KAREN :</strong> {result["diagnostic"]}</div>',
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
        "Avancez étape par étape dans la conversation avec KAREN pour obtenir une réponse structurée, "
        "des questions de diagnostic, une orientation fiable et un message prêt à transmettre."
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