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
# CONFIG
# =========================================================
APP_TITLE = "KAREN"
APP_SUBTITLE = "Agent RH / Paie guidé — version premium"
LOGO_PATH = "images.png"
AVATAR_GIF_PATH = "giphy.gif"

# =========================================================
# ÉTABLISSEMENTS / CCN
# =========================================================
ESTABLISHMENTS = [
    {"pole": "Art & Création", "entite_juridique": "ACADEMIE JULIAN RIVE GAUCHE", "etablissement": "ACADEMIE JULIAN RIVE GAUCHE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "ATELIER DE SEVRES", "etablissement": "ATELIER DE SEVRES Etablissement principal", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "BELLECOUR ECOLE ARTS", "etablissement": "BELLECOUR DAUPHIN", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "Etablissement Français Formation et Enseignement", "etablissement": "Etablissement Français Formation et Enseignement", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "Galiléo Institut Culinaire de France", "etablissement": "GICF Paris", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "Institut d'Architecture et de Design", "etablissement": "IDEA RENNES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "Institut de Développement des Arts Appliqués", "etablissement": "IDAA GRAPHISME", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "Institut de Développement des Arts Appliqués", "etablissement": "IDAA ANIMATION", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "Institut de Développement des Arts Appliqués", "etablissement": "IDAA ARCHITECTURE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "Institut de Développement des Arts Appliqués", "etablissement": "IDAA MODE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "Institut de Développement des Arts Appliqués", "etablissement": "IDAA", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "L'Institut Supérieur des Arts Appliqués", "etablissement": "LISAA Strasbourg", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "LISAA NANTES", "etablissement": "ECOLE LISAA NANTES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "LOCOMOTIVE", "etablissement": "Locomotive - Atelier Chardon Savard", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "STRATE COLLEGE", "etablissement": "STRATE COLLEGE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "STRATE ECOLE DE DESIGN -LYON", "etablissement": "STRATE ECOLE DE DESIGN -LYON", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESGCV PSB PGE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESGCV ESGM", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESGCV ESGCI", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESGCV ESGF", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESGCV ESGFR", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESGCV IICP", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESGCV PSB", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESGRH", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESG LUXE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESG SPORT", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESG ACT", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "ESGCV", "etablissement": "ESGCV ESGRH", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "Galiléo Formation Professionnelle", "etablissement": "Galiléo Formation Professionnelle", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "GALILEO VAE", "etablissement": "GALILEO VAE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "GALILEO VAE", "etablissement": "GALILEO VAE2", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "HETIC", "etablissement": "HETIC", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "Institut de Management Ecole Supérieure de Gestion", "etablissement": "IMESG Paris", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "Institut de Management Ecole Supérieure de Gestion", "etablissement": "ESG LANGUES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "PARIS SCHOOL OF TECHNOLOGY & BUSINESS", "etablissement": "PARIS SCHOOL TECHNOLOY & BUSINESS PARIS", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Paris", "entite_juridique": "WEB SCHOOL FACTORY", "etablissement": "WEB SCHOOL FACTORY", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV ESARC CEFIRE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV POLE ESG", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV AIX EN PROVENCE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV BORDEAUX", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV TOULOUSE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV MONTPELLIER", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV RENNES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV LYON", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV TOURS", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV STRASBOURG", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV NANTES", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV MERKURE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV ELIGE", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV ROUEN", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV BIARRITZ", "ccn": "Enseignement privé indépendant"},
    {"pole": "Business Regions", "entite_juridique": "ESGCV", "etablissement": "ESGCV DIJON", "ccn": "Enseignement privé indépendant"},
    {"pole": "Art & Création", "entite_juridique": "ATELIER CHARDON SAVARD NANTES", "etablissement": "ACS NANTES", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "entite_juridique": "COURS FLORENT JEUNESSE", "etablissement": "COURS FLORENT JEUNESSE PARIS", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "entite_juridique": "COURS FLORENT JEUNESSE", "etablissement": "COURS FLORENT JEUNESSE BORDEAUX", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "entite_juridique": "COURS FLORENT JEUNESSE", "etablissement": "COURS FLORENT JEUNESSE MONTPELLIER", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "entite_juridique": "ECAD CONSULTANTS", "etablissement": "IESA Art & Culture", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "entite_juridique": "ECAD CONSULTANTS", "etablissement": "DIGITAL CAMPUS PARIS", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "entite_juridique": "ECAD CONSULTANTS", "etablissement": "ECAD CONSULTANTS", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "entite_juridique": "FLORENT", "etablissement": "FLORENT", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "entite_juridique": "FLORENT", "etablissement": "FLORENT BORDEAUX", "ccn": "Organismes de formation"},
    {"pole": "Art & Création", "entite_juridique": "FLORENT", "etablissement": "FLORENT MONTPELLIER", "ccn": "Organismes de formation"},
    {"pole": "Holding & Cie", "entite_juridique": "EVA SANTE", "etablissement": "EVA SANTE IFAS METZ", "ccn": "Organismes de formation"},
    {"pole": "Holding & Cie", "entite_juridique": "EVA SANTE", "etablissement": "EVA SANTE IFAS CHALONS", "ccn": "Organismes de formation"},
    {"pole": "Holding & Cie", "entite_juridique": "EVA SANTE", "etablissement": "EVA SANTE IFAS BORDEAUX", "ccn": "Organismes de formation"},
    {"pole": "Holding & Cie", "entite_juridique": "EVA SANTE", "etablissement": "EVA SANTE PARIS", "ccn": "Organismes de formation"},
    {"pole": "Holding & Cie", "entite_juridique": "GGE Corporate Services", "etablissement": "GGE Corporate Services", "ccn": "SYNTEC"},
    {"pole": "Holding & Cie", "entite_juridique": "GGE France", "etablissement": "GGE France", "ccn": "SYNTEC"},
    {"pole": "Holding & Cie", "entite_juridique": "GGE Operations", "etablissement": "GGE Operation", "ccn": "SYNTEC"},
    {"pole": "Holding & Cie", "entite_juridique": "GGE Strategy", "etablissement": "GGE Strategy", "ccn": "SYNTEC"},
]

ENTITY_OPTIONS = [item["etablissement"] for item in ESTABLISHMENTS]

# =========================================================
# PARAMÉTRAGE MÉTIER
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

SPECIAL_EMPLOYMENT_TYPES = ["Enseignant(e)", "Modèle vivant", "Surveillant(e)"]
PORTAL_TOPICS = ["Heures supplémentaires", "Acompte", "Télétravail", "JPO ou SPO"]
PORTAL_ABSENCE_EXCEPTIONS = ["maladie", "maternité", "accident de travail"]

# =========================================================
# THEMES / BESOINS
# =========================================================
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
        "Je veux comprendre le montant de mon acompte",
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

# =========================================================
# RÉPONSES SPÉCIFIQUES
# =========================================================
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
    ("Mutuelle", "Je veux comprendre ma cotisation"): {
        "title": "Fonctionnement de la mutuelle",
        "summary": "En tant que salarié, vous êtes automatiquement affilié à une mutuelle collective proposée par l’employeur. Cette affiliation est obligatoire sauf cas de dispense.",
        "checks": [
            "Vérifier votre date d’embauche.",
            "Vérifier si vous avez reçu l’email d’affiliation entre 15 et 20 jours après votre entrée.",
            "Vérifier que votre affiliation a bien été finalisée.",
            "Identifier si vous êtes dans un cas de dispense.",
        ],
        "action": "Finalisez votre affiliation via le lien reçu par email. En cas de non-réception après 20 jours, contactez le support RH.",
        "contact": "Mutuelle / RH si blocage",
    },
    ("Mutuelle", "Je veux demander une dispense"): {
        "title": "Demande de dispense mutuelle",
        "summary": "Une dispense de mutuelle est possible sous conditions. Elle doit être demandée auprès de la mutuelle, elle est valable 12 mois et doit être renouvelée à chaque contrat.",
        "checks": [
            "Vérifier que votre situation permet une dispense.",
            "Vérifier que vous êtes dans le délai de 2 mois après embauche.",
            "Préparer le justificatif demandé.",
            "Vérifier si une demande de dispense a déjà été faite pour ce contrat.",
        ],
        "action": "Effectuez votre demande auprès de la mutuelle. Si le délai de 2 mois est dépassé, contactez votre chargé RH.",
        "contact": "Mutuelle / RH si délai dépassé",
    },
    ("Mutuelle", "Je veux signaler un problème d'affiliation"): {
        "title": "Problème d'affiliation mutuelle",
        "summary": "L’affiliation est automatique à l’embauche mais doit être finalisée via un email envoyé sur l’adresse personnelle renseignée dans Workday.",
        "checks": [
            "Vérifier la réception de l’email d’affiliation.",
            "Vérifier l’adresse personnelle renseignée dans Workday.",
            "Contrôler le délai depuis votre embauche.",
            "Vérifier si l’affiliation a été finalisée.",
        ],
        "action": "Si vous n’avez rien reçu après 20 jours ou si le lien est expiré, contactez votre chargé RH pour obtenir un nouveau lien.",
        "contact": "RH / Mutuelle",
    },
    ("Mutuelle", "Je veux ajouter / retirer des ayants droit"): {
        "title": "Gestion des ayants droit",
        "summary": "Les ayants droit sont gérés directement auprès de la mutuelle après finalisation de votre affiliation.",
        "checks": [
            "Vérifier que votre affiliation est bien active.",
            "Identifier les ayants droit à ajouter ou retirer.",
            "Préparer les justificatifs nécessaires.",
        ],
        "action": "Effectuez la modification directement auprès de la mutuelle.",
        "contact": "Mutuelle",
    },
    ("Mutuelle", "Je veux savoir qui contacter"): {
        "title": "Interlocuteur mutuelle",
        "summary": "La mutuelle est votre interlocuteur principal pour toute demande liée à votre couverture santé. Le RH intervient en second niveau en cas de blocage ou de lien expiré.",
        "checks": [
            "Identifier la nature exacte de votre demande.",
            "Vérifier si votre affiliation est active.",
            "Vérifier si vous êtes encore dans les délais d’affiliation.",
        ],
        "action": "Contactez d’abord la mutuelle. Si le délai est dépassé ou si aucun lien n’est disponible, contactez votre chargé RH.",
        "contact": "Mutuelle / RH en second niveau",
    },
    ("Transport", "Je veux demander un remboursement transport"): {
        "title": "Remboursement transport",
        "summary": "Le traitement dépend du type de transport concerné : RATP via le portail, tout autre transport par mail auprès du chargé RH de proximité.",
        "checks": [
            "Identifier s’il s’agit d’un abonnement RATP ou d’un autre transport.",
            "Vérifier la période couverte par le justificatif.",
            "Préparer un justificatif lisible.",
        ],
        "action": "Si votre demande concerne la RATP, utilisez le portail. Pour tout autre transport, envoyez votre demande par mail à votre chargé RH de proximité.",
        "contact": "Portail RH / Chargé RH de proximité",
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
        "action": "Si la situation dure, demandez une vérification de l'état de commande ou une réédition si nécessaire.",
        "contact": "RH / Paie / gestionnaire titres restaurant",
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
# FONCTIONS UTILITAIRES
# =========================================================
def safe_display_image(path, width=None):
    if isinstance(path, str) and path.startswith("http"):
        st.image(path, width=width)
    elif os.path.exists(path):
        st.image(path, width=width)


def render_avatar_html(state="idle", width=140):
    labels = {
        "idle": "🟢 KAREN en veille",
        "thinking": "🔵 KAREN réfléchit",
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


def get_selected_establishment(entity_name: str | None):
    if not entity_name:
        return None
    for item in ESTABLISHMENTS:
        if item["etablissement"] == entity_name:
            return item
    return None


def get_complexity_score(theme, need, free_text):
    score = 1
    if "Autre besoin" in need:
        score += 2
    if theme in ["Ma paie", "Documents de sortie", "Heures supplémentaires", "JPO ou SPO", "Absence"]:
        score += 2
    if len(free_text.strip()) > 80:
        score += 1
    return min(score, 5)


def get_complexity_label(score):
    if score <= 2:
        return "Simple"
    if score == 3:
        return "Intermédiaire"
    return "Sensible / à vérifier"


def get_rule_based_alerts(role, job_type, contract_type, work_time, theme, entity_name=None):
    alerts = []
    selected = get_selected_establishment(entity_name)

    if job_type == "Enseignant(e)" and theme in ["Heures supplémentaires", "JPO ou SPO", "Ma paie"]:
        alerts.append("Pour les enseignant(e)s, la vérification des heures, variables et remontées pédagogiques est prioritaire.")

    if job_type in SPECIAL_EMPLOYMENT_TYPES:
        alerts.append("Les règles standard portail ne s'appliquent pas automatiquement aux enseignant(e)s, modèles vivants et surveillant(e)s sans vérification préalable.")

    if job_type == "Stagiaire":
        alerts.append("Pour un(e) stagiaire, certaines rubriques paie ou avantages peuvent suivre des règles spécifiques.")

    if job_type == "Apprenti(e)":
        alerts.append("Pour un(e) apprenti(e), le contrat, l'âge et le mois d'exécution peuvent influer sur le traitement paie.")

    if work_time == "Temps partiel":
        alerts.append("Le temps partiel peut modifier les droits, soldes, montants et contrôles attendus.")

    if contract_type == "CDD" and theme == "Documents de sortie":
        alerts.append("En CDD, la vérification de la date de fin de contrat et des documents de sortie est essentielle.")

    if role == "Manager":
        alerts.append("En tant que manager, vous pouvez être sollicité sur la validation ou le suivi d'une demande salariée.")

    if theme == "Mutuelle":
        alerts.append("L’interlocuteur principal pour la mutuelle est la mutuelle elle-même ; le RH intervient en second niveau.")
        alerts.append("Le délai pour finaliser l’affiliation est de 2 mois après l’embauche.")
        alerts.append("Une dispense acceptée est valable 12 mois et doit être renouvelée à chaque contrat.")

    if theme == "Télétravail":
        alerts.append("Le télétravail se gère via le portail Mon Portail Paie.")
        alerts.append("Le modèle repose sur un forfait annuel de jours, avec accord du salarié, du manager et de la DRH.")
        alerts.append("Des dérogations existent selon le temps de transport, la RQTH ou certaines situations spécifiques.")

    if theme == "Acompte":
        alerts.append("La demande d'acompte se fait uniquement via Mon Portail Paie.")
        alerts.append("La demande est possible du 1er au 11 du mois uniquement.")
        alerts.append("Le montant est limité à 50 % du salaire.")

    if selected:
        alerts.append(f"Établissement sélectionné : {selected['etablissement']} — CCN : {selected['ccn']}.")
        alerts.append(f"Pôle : {selected['pole']} — Entité juridique : {selected['entite_juridique']}.")

        if selected["ccn"] == "Enseignement privé indépendant":
            alerts.append("Cette situation relève de la CCN Enseignement privé indépendant.")
        elif selected["ccn"] == "Organismes de formation":
            alerts.append("Cette situation relève de la CCN Organismes de formation.")
        elif selected["ccn"] == "SYNTEC":
            alerts.append("Cette situation relève de la CCN SYNTEC.")

    return alerts


def get_portal_rule_message(theme, need, job_type, free_text=""):
    combined = f"{need} {free_text}".lower()

    if job_type in SPECIAL_EMPLOYMENT_TYPES and theme in ["Absence", "Heures supplémentaires", "Acompte", "Télétravail", "JPO ou SPO"]:
        return {
            "title": "Vérification spécifique requise",
            "summary": "Votre profil relève d'un circuit particulier. La demande ne doit pas être orientée automatiquement sans vérification préalable.",
            "checks": [
                "Vérifier le profil exact du salarié.",
                "Vérifier les modalités de déclaration applicables à cette population.",
                "Contrôler si le portail est bien le bon canal dans ce cas précis.",
            ],
            "action": "Rapprochez-vous du support RH / Paie avant toute saisie si vous avez un doute sur le circuit applicable.",
            "contact": "Support RH / Paie",
        }

    if theme == "Absence":
        if any(exception in combined for exception in PORTAL_ABSENCE_EXCEPTIONS):
            return {
                "title": "Absence à signaler directement",
                "summary": "Cette situation ne se déclare pas via le portail. Elle doit être signalée directement au chargé RH / Paie avec le justificatif approprié.",
                "checks": [
                    "Identifier précisément la nature de l'arrêt ou de l'absence.",
                    "Transmettre le justificatif requis dès que possible.",
                    "Vérifier que le chargé RH dispose bien des dates exactes de l'absence.",
                ],
                "action": "Signalez directement la situation à votre chargé RH / Paie sans passer par le portail.",
                "contact": "Chargé RH / Paie",
            }
        return {
            "title": "Absence à déclarer via le portail",
            "summary": "Toutes les absences standard doivent être déclarées via le portail. Tant que la saisie n'est pas effectuée correctement et validée, elles ne pourront pas être traitées normalement.",
            "checks": [
                "Choisir le bon motif d'absence dans le portail.",
                "Vérifier les dates saisies.",
                "Joindre le justificatif si nécessaire.",
                "Contrôler le statut de validation de la demande.",
            ],
            "action": "Effectuez la déclaration via le portail puis vérifiez son statut de validation.",
            "contact": "Portail RH / Manager / RH selon circuit",
        }

    if theme == "Transport":
        if "ratp" in combined:
            return {
                "title": "Transport RATP à déclarer via le portail",
                "summary": "La demande de remboursement transport RATP doit être effectuée via le portail.",
                "checks": [
                    "Vérifier que le justificatif correspond bien à un abonnement RATP.",
                    "Contrôler la période concernée.",
                    "Vérifier que la demande a bien été déposée dans le bon module du portail.",
                    "S'assurer que le justificatif transmis est lisible.",
                ],
                "action": "Effectuez votre demande via le portail et vérifiez le statut de validation.",
                "contact": "Portail RH / RH selon circuit",
            }
        return {
            "title": "Autre transport à transmettre par mail",
            "summary": "Pour tout transport autre que la RATP, la demande doit être envoyée par mail au chargé RH de proximité.",
            "checks": [
                "Identifier précisément le type de transport concerné.",
                "Vérifier la période couverte par le justificatif.",
                "Préparer un justificatif lisible.",
                "Vérifier que le mail est adressé au bon chargé RH de proximité.",
            ],
            "action": "Envoyez votre demande par mail à votre chargé RH de proximité avec le justificatif correspondant.",
            "contact": "Chargé RH de proximité",
        }

    if theme == "Télétravail":
        return {
            "title": "Télétravail à gérer via le portail",
            "summary": "Le télétravail fonctionne selon un modèle hybride. La saisie, la planification, la consultation et la modification des jours se font via Mon Portail Paie.",
            "checks": [
                "Vérifier votre forfait annuel de jours de télétravail.",
                "Choisir entre télétravail ponctuel ou régulier.",
                "Vérifier que votre manager valide la demande.",
                "Contrôler votre consommation de jours dans le portail.",
            ],
            "action": "Effectuez votre demande dans le portail : Planning et droits congés > Mon travail hybride.",
            "contact": "Portail / Manager / RH si dérogation",
        }

    if theme == "Acompte":
        return {
            "title": "Acompte à demander via le portail",
            "summary": "La demande d'acompte se fait uniquement via Mon Portail Paie, du 1er au 11 du mois, dans la limite de 50 % du salaire.",
            "checks": [
                "Vérifier que vous êtes entre le 1er et le 11 du mois.",
                "Vérifier le montant demandé.",
                "Prendre en compte les éventuelles absences, primes ou variables du mois.",
                "Contrôler les éléments remontés au service paie.",
            ],
            "action": "Effectuez votre demande via Mon Portail Paie.",
            "contact": "Portail Paie",
        }

    if theme == "Heures supplémentaires":
        return {
            "title": "Heures supplémentaires à déclarer via le portail",
            "summary": "Les heures supplémentaires doivent être déclarées via le portail. Sans saisie correcte et validation, elles ne pourront pas être traitées normalement.",
            "checks": [
                "Vérifier que vous êtes sur le bon module du portail.",
                "Contrôler les dates et le volume d’heures saisis.",
                "Vérifier si une validation manager est attendue.",
                "Suivre le statut de la demande après envoi.",
            ],
            "action": "Passez par le portail pour déclarer vos heures supplémentaires et vérifiez le statut de validation.",
            "contact": "Portail RH / Manager / RH selon circuit",
        }

    if theme == "JPO ou SPO":
        return {
            "title": "JPO / SPO à déclarer via le portail",
            "summary": "La déclaration JPO / SPO doit être effectuée via le portail. Tant que la saisie et la validation ne sont pas complètes, le traitement ne pourra pas être finalisé.",
            "checks": [
                "Vérifier que vous êtes sur le bon module du portail.",
                "Contrôler le motif choisi.",
                "Vérifier les dates saisies.",
                "Suivre le statut de validation.",
            ],
            "action": "Effectuez votre déclaration JPO / SPO via le portail puis vérifiez son statut.",
            "contact": "Portail RH / Manager / RH selon circuit",
        }

    return None


def build_response(theme, need, role, entity, job_type, contract_type, work_time, free_text):
    portal_override = get_portal_rule_message(theme, need, job_type, free_text)
    data = portal_override if portal_override else RESPONSES.get((theme, need), DEFAULT_RESPONSE)

    complexity_score = get_complexity_score(theme, need, free_text)
    alerts = get_rule_based_alerts(role, job_type, contract_type, work_time, theme, entity)
    selected = get_selected_establishment(entity)

    context_lines = [
        f"Profil déclaré : {role}",
        f"Établissement : {entity}",
        f"Type d'emploi : {job_type}",
        f"Contrat : {contract_type}",
        f"Temps de travail : {work_time}",
    ]

    if selected:
        context_lines.append(f"Pôle : {selected['pole']}")
        context_lines.append(f"Entité juridique : {selected['entite_juridique']}")
        context_lines.append(f"CCN applicable : {selected['ccn']}")

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
    selected = get_selected_establishment(entity)
    ccn_line = f"- CCN : {selected['ccn']}\n" if selected else ""

    body = f"""Bonjour,

Je vous contacte concernant une demande RH / Paie.

Voici les éléments de contexte :
- Profil : {role}
- Établissement : {entity}
{ccn_line}- Type d'emploi : {job_type}
- Type de contrat : {contract_type}
- Temps de travail : {work_time}
- Thème : {theme}
- Besoin précis : {need}

Description complémentaire :
{free_text if free_text else "Merci de trouver ci-dessus les éléments nécessaires à l’analyse de ma demande."}

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
        p, label, span, div {
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
    st.markdown("</div>", unsafe_allow_html=True)

with header_right:
    st.empty()

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
for key, default in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

# =========================================================
# FORMULAIRE CONVERSATIONNEL
# =========================================================
left, right = st.columns([1.15, 0.85])

with left:
    if st.session_state.step != 6:
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
            entity = st.selectbox("Elle concerne un salarié de quel établissement ?", ENTITY_OPTIONS, key="entity_step")
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
            theme = st.selectbox("Quel est le thème de votre demande ?", list(THEMES.keys()), key="theme_step")
            need = st.selectbox("Quel est votre besoin précis ?", THEMES[theme], key="need_step")
            free_text = st.text_area(
                "Ajoutez un complément d'information si nécessaire",
                value=st.session_state.free_text,
                placeholder="Exemple : mois concerné, message d’erreur, date exacte, rubrique du bulletin, justificatif transmis, niveau d’urgence…",
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
                    for reset_key, reset_default in defaults.items():
                        st.session_state[reset_key] = reset_default
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
    st.progress((st.session_state.step - 1) / 5 if st.session_state.step <= 6 else 1)
    st.caption(f"Étape {min(st.session_state.step, 6)} sur 6")

    if st.session_state.role:
        st.write(f"- Profil : {st.session_state.role}")
    if st.session_state.entity:
        st.write(f"- Établissement : {st.session_state.entity}")
        selected_progress = get_selected_establishment(st.session_state.entity)
        if selected_progress:
            st.write(f"- CCN : {selected_progress['ccn']}")
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
# ANALYSE
# =========================================================
if st.session_state.step == 6 and st.session_state.theme and st.session_state.need:
    thinking_placeholder = st.empty()
    with thinking_placeholder.container():
        st.markdown('<div class="karen-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">KAREN analyse votre demande</div>', unsafe_allow_html=True)
        render_avatar_html("thinking", width=180)
        st.markdown('<div class="thinking-ring"></div>', unsafe_allow_html=True)
        st.write("Qualification du profil, lecture du besoin, application des règles métier et préparation de la réponse...")
        st.markdown("</div>", unsafe_allow_html=True)

    time.sleep(0.8)

    result = build_response(
        st.session_state.theme,
        st.session_state.need,
        st.session_state.role,
        st.session_state.entity,
        st.session_state.job_type,
        st.session_state.contract_type,
        st.session_state.work_time,
        st.session_state.free_text,
    )
    subject, support_message = build_support_message(
        st.session_state.role,
        st.session_state.entity,
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

    user_extra = ""
    if st.session_state.free_text:
        user_extra = f"<br><br>Complément transmis : {st.session_state.free_text}"

    st.markdown(
        f"""<div class="chat-user">
            <div class="chat-label-user">VOUS</div>
            Bonjour KAREN, je suis <strong>{st.session_state.role}</strong> de l'établissement <strong>{st.session_state.entity}</strong>.
            Mon profil est <strong>{st.session_state.job_type}</strong>, en <strong>{st.session_state.contract_type}</strong>, à <strong>{st.session_state.work_time}</strong>.
            Mon sujet concerne <strong>{st.session_state.theme}</strong> et plus précisément : <strong>{st.session_state.need}</strong>.
            {user_extra}
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<div class="chat-karen">
            <div class="chat-label">KAREN</div>
            <strong>{result["title"]}</strong><br><br>
            {result["summary"]}
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="karen-card">', unsafe_allow_html=True)
    st.markdown("#### Vérifications recommandées")
    for item in result["checks"]:
        st.write(f"- {item}")

    if result["alerts"]:
        st.markdown('<div class="info-box"><strong>Points de vigilance :</strong></div>', unsafe_allow_html=True)
        for alert in result["alerts"]:
            st.write(f"- {alert}")

    st.markdown(
        f'<div class="warning-box"><strong>Action conseillée :</strong> {result["action"]}</div>',
        unsafe_allow_html=True,
    )
    st.write(f"**Interlocuteur recommandé :** {result['contact']}")
    st.progress(result["complexity_score"] / 5)
    st.caption(f"Score de complexité : {result['complexity_score']} / 5")

    c1, c2 = st.columns([1, 1.3])
    with c1:
        if st.button("Revenir à l'étape précédente"):
            st.session_state.step = 5
            st.rerun()
    with c2:
        if st.button("Nouvelle conversation avec KAREN"):
            for reset_key, reset_default in defaults.items():
                st.session_state[reset_key] = reset_default
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

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