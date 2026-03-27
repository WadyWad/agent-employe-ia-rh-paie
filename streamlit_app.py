import streamlit as st
from typing import Optional, Dict, List

st.set_page_config(
    page_title="Agent Employé IA",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# STYLE
# =========================================================
st.markdown("""
<style>
.block-container {
    max-width: 980px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
.hero {
    background: linear-gradient(135deg, #0f62fe 0%, #6ea8fe 100%);
    color: white;
    padding: 22px 24px;
    border-radius: 18px;
    margin-bottom: 18px;
}
.hero h1 {
    margin: 0;
    font-size: 2rem;
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
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 1px 5px rgba(0,0,0,0.04);
}
.answer-card {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-left: 5px solid #0f62fe;
    border-radius: 16px;
    padding: 18px;
    margin-top: 10px;
    margin-bottom: 14px;
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
.muted {
    color: #6c757d;
    font-size: 0.92rem;
}
.kpi {
    background: #f8f9fa;
    border-radius: 14px;
    padding: 10px 12px;
    border: 1px dashed #d0d7de;
    font-size: 0.92rem;
    height: 100%;
}
.footer-note {
    color: #6c757d;
    font-size: 0.88rem;
    margin-top: 12px;
}
.context-box {
    background: #f8fbff;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🤖 Agent Employé IA</h1>
  <p>Assistant RH / Paie guidé par parcours métier</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DONNÉES DU PARCOURS
# =========================================================
ROLES = [
    "Salarié",
    "Manager",
]

ENTITIES = [
    "Atelier de Sèvres",
    "CIFACOM, École de graphisme et d’audiovisuel",
    "ESARC Aix-en-Provence",
    "ESARC Bordeaux",
    "ESARC Dijon",
    "ESARC Lyon",
    "ESARC Montpellier",
    "ESARC Nantes",
    "ESARC Rouen",
    "ESARC Strasbourg",
    "ESARC Toulouse",
    "ESARC Tours",
    "ESG Immobilier – Campus de Lyon",
    "HETIC",
    "IESA arts et culture",
    "LISAA Architecture d’intérieur et design Paris",
    "LISAA Bordeaux",
    "LISAA Design graphique et communication Paris",
    "LISAA Nantes",
    "LISAA Paris animation et jeu vidéo",
    "LISAA Rennes",
    "LISAA Strasbourg",
    "LISAA Toulouse",
    "LISAA mode Paris",
    "Narratiiv",
    "Paris School of Business",
    "Strate, école de design",
    "Atelier Chardon-Savard",
    "Atelier Chardon-Savard Nantes",
    "Cours Florent Paris",
    "Digital Campus Aix-en-Provence",
    "Digital Campus Bordeaux",
    "Digital Campus Lyon",
    "Digital Campus Montpellier",
    "Digital Campus Nantes",
    "Digital Campus Paris",
    "Digital Campus Rennes",
    "Digital Campus Strasbourg",
    "Digital Campus Toulouse",
    "e-artsup Aix-en-Provence",
    "e-artsup Lyon",
    "e-artsup Montpellier",
    "Institut Marangoni",
    "Penninghen - école de direction artistique, communication et architecture intérieure",
    "Web School Factory",
]

THEMES = [
    "Ma paie",
    "Mon Portail Paie",
    "Absence",
    "Congés",
    "Mutuelle",
    "Transport",
    "Ticket restaurant",
    "Télétravail",
    "Acompte",
    "Bulletins",
    "Documents de sortie",
    "JPO ou SPO",
    "Heures supplémentaires",
    "Demande de documents",
]

SUBTHEMES = {
    "Ma paie": [
        "Mon salaire a baissé",
        "Je ne comprends pas une ligne de mon bulletin",
        "Il manque une prime",
        "Je pense qu’il y a une erreur sur mon bulletin",
        "Je ne comprends pas mon net à payer",
        "Je ne comprends pas une retenue",
        "Je veux comprendre une régularisation",
        "Mon sujet n’est pas dans la liste",
    ],
    "Mon Portail Paie": [
        "Je ne vois pas la tuile / je n’ai pas accès",
        "Ma demande ne remonte pas",
        "Je ne comprends pas la période de gel",
        "Je ne sais pas où faire ma demande",
        "Je ne comprends pas le circuit de validation",
        "Je souhaite être accompagné sur le portail",
        "Mon sujet n’est pas dans la liste",
    ],
    "Absence": [
        "Arrêt maladie",
        "Enfant malade",
        "Absence injustifiée / justifiée",
        "Je veux comprendre l’impact paie de mon absence",
        "Je veux comprendre la subrogation",
        "Mon sujet n’est pas dans la liste",
    ],
    "Congés": [
        "Congés payés",
        "RTT / récupération",
        "Mariage / PACS",
        "Décès",
        "Jours de révision",
        "Je ne comprends pas mon compteur",
        "Mon sujet n’est pas dans la liste",
    ],
    "Mutuelle": [
        "La mutuelle est-elle obligatoire ?",
        "Je veux une dispense",
        "Je n’ai pas répondu au mail d’affiliation",
        "Je vois une cotisation mutuelle",
        "Je veux comprendre ma situation mutuelle",
        "Mon sujet n’est pas dans la liste",
    ],
    "Transport": [
        "Remboursement Navigo",
        "Quels justificatifs fournir ?",
        "Ce qui n’est pas remboursé",
        "Ma demande transport ne remonte pas",
        "Mon sujet n’est pas dans la liste",
    ],
    "Ticket restaurant": [
        "Combien ai-je de tickets restaurant ?",
        "Comment déclarer mes tickets restaurant ?",
        "Je n’ai pas reçu ma carte",
        "Je ne comprends pas mon nombre de tickets",
        "Mon sujet n’est pas dans la liste",
    ],
    "Télétravail": [
        "Pourquoi je n’ai pas la ligne télétravail ?",
        "Quels documents faut-il ?",
        "Mon avenant / assurance a été transmis",
        "Je veux comprendre l’allocation télétravail",
        "Mon sujet n’est pas dans la liste",
    ],
    "Acompte": [
        "Puis-je demander un acompte ?",
        "Je veux comprendre la différence entre acompte et avance",
        "Je ne vois pas ma demande sur le portail",
        "Je veux connaître la fenêtre de demande",
        "Mon sujet n’est pas dans la liste",
    ],
    "Bulletins": [
        "Je veux accéder à mon bulletin",
        "Je ne retrouve pas mon bulletin",
        "Je veux comprendre comment fonctionne Arkevia",
        "Je veux réinitialiser mon accès",
        "Importer mes anciens bulletins",
        "Mon sujet n’est pas dans la liste",
    ],
    "Documents de sortie": [
        "Solde de tout compte",
        "Certificat de travail",
        "Attestation France Travail",
        "Je n’ai pas reçu mes documents de sortie",
        "Je veux comprendre mes documents de fin de contrat",
        "Mon sujet n’est pas dans la liste",
    ],
    "JPO ou SPO": [
        "Je veux comprendre les JPO / SPO",
        "Je veux comprendre la récupération",
        "Je veux comprendre le paiement",
        "Je ne vois pas ma JPO / SPO",
        "Mon sujet n’est pas dans la liste",
    ],
    "Heures supplémentaires": [
        "Il manque des heures",
        "Mes heures ont été faites avant le 15",
        "Mes heures ont été faites après le 15",
        "Le manager n’a pas validé",
        "Je veux comprendre le décalage de paiement",
        "Mon sujet n’est pas dans la liste",
    ],
    "Demande de documents": [
        "Attestation employeur",
        "Attestation de salaire",
        "Duplicata de bulletin",
        "Guide d’accès Arkevia",
        "Autre document",
        "Mon sujet n’est pas dans la liste",
    ],
}

# =========================================================
# SESSION STATE
# =========================================================
DEFAULTS = {
    "step": 1,
    "role": None,
    "entity": None,
    "theme": None,
    "subtheme": None,
    "q1": None,
    "q2": None,
    "q3": None,
    "result": None,
    "free_message": "",
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_flow() -> None:
    for k, v in DEFAULTS.items():
        st.session_state[k] = v


def set_step(step: int) -> None:
    st.session_state["step"] = step
    st.rerun()


# =========================================================
# MOTEUR DE RÉPONSE
# =========================================================
def _base_result(role: str, entity: str, theme: str, subtheme: str) -> Dict[str, str]:
    topic = f"{role} • {entity} • {theme} • {subtheme}"
    return {
        "topic": topic,
        "what_it_means": "",
        "why_it_happens": "",
        "what_to_do": "",
        "who_to_contact": "",
        "ready_text": "",
    }


def _finalize_result(result: Dict[str, str]) -> Dict[str, str]:
    result["ready_text"] = (
        f"Sujet : {result['topic']}\n\n"
        f"Ce que cela signifie :\n{result['what_it_means']}\n\n"
        f"Pourquoi cela arrive :\n{result['why_it_happens']}\n\n"
        f"Ce que vous devez faire :\n{result['what_to_do']}\n\n"
        f"Qui contacter si besoin :\n{result['who_to_contact']}"
    )
    return result


def build_structured_answer(
    role: str,
    entity: str,
    theme: str,
    subtheme: str,
    q1: Optional[str] = None,
    q2: Optional[str] = None,
    q3: Optional[str] = None,
) -> Dict[str, str]:
    result = _base_result(role, entity, theme, subtheme)

    # -----------------------------------------------------
    # MA PAIE
    # -----------------------------------------------------
    if theme == "Ma paie":
        if subtheme == "Mon salaire a baissé":
            result["what_it_means"] = "Une baisse de salaire n’est pas forcément une anomalie."
            result["why_it_happens"] = (
                "Elle peut venir d’une absence, d’une maladie, d’un acompte, "
                "d’une prime absente, d’une régularisation ou d’un élément variable non encore traité."
            )
            result["what_to_do"] = (
                "Comparez le bulletin du mois concerné avec le mois précédent et vérifiez : "
                "les absences, les primes, les acomptes, les retenues et les régularisations."
            )
            result["who_to_contact"] = "Service paie"

            if q1 == "Oui, après une absence maladie":
                result["why_it_happens"] = (
                    "En arrêt maladie, l’absence est déduite de la paie. "
                    "La Sécurité sociale peut verser des indemnités journalières, "
                    "avec parfois 3 jours de carence. "
                    "Selon l’ancienneté, un maintien de salaire ou un complément de prévoyance peut aussi exister."
                )
                result["what_to_do"] = (
                    "Vérifiez le mois concerné, la présence de l’absence maladie sur le bulletin "
                    "et si des IJSS ont été versées."
                )
            elif q1 == "Oui, après une autre absence":
                result["why_it_happens"] = (
                    "Certaines absences ont un impact direct sur la paie. "
                    "Le montant final dépend du type d’absence et de sa prise en charge éventuelle."
                )
                result["what_to_do"] = "Vérifiez le type d’absence posé et la période concernée."
            elif q1 == "Non, sans absence":
                result["why_it_happens"] = (
                    "Dans ce cas, les causes les plus fréquentes sont : prime absente ou différente, "
                    "acompte, régularisation, retenue ou variation d’éléments variables."
                )
                result["what_to_do"] = "Vérifiez en priorité les primes, acomptes et régularisations."

        elif subtheme == "Je ne comprends pas une ligne de mon bulletin":
            result["what_it_means"] = "Une ligne de bulletin doit être lue selon sa nature."
            result["why_it_happens"] = (
                "Une ligne peut correspondre à une absence, une prime, une cotisation, "
                "un acompte, une régularisation ou une allocation."
            )
            result["what_to_do"] = "Relevez le libellé exact de la ligne et le mois concerné."
            result["who_to_contact"] = "Service paie"

        elif subtheme == "Il manque une prime":
            result["what_it_means"] = "L’absence d’une prime n’est pas toujours une erreur paie."
            result["why_it_happens"] = (
                "Le montant et la validation des primes sont souvent transmis à la paie "
                "par le manager ou le RH."
            )
            result["what_to_do"] = "Vérifiez d’abord si la prime a bien été validée et transmise."
            result["who_to_contact"] = "Manager / RH"

        elif subtheme == "Je pense qu’il y a une erreur sur mon bulletin":
            result["what_it_means"] = "Il faut qualifier précisément l’écart."
            result["why_it_happens"] = (
                "Un montant différent peut provenir d’un décalage de traitement, "
                "d’une régularisation ou d’une anomalie réelle."
            )
            result["what_to_do"] = (
                "Préparez le mois concerné, la ligne concernée et la différence constatée."
            )
            result["who_to_contact"] = "Service paie"

        elif subtheme == "Je ne comprends pas mon net à payer":
            result["what_it_means"] = "Le net à payer varie en fonction de plusieurs éléments."
            result["why_it_happens"] = (
                "Le net dépend du brut, des cotisations, des absences, des acomptes, "
                "des primes et des éventuelles régularisations."
            )
            result["what_to_do"] = (
                "Comparez brut, cotisations, retenues et régularisations avec le mois précédent."
            )
            result["who_to_contact"] = "Service paie"

        elif subtheme == "Je ne comprends pas une retenue":
            result["what_it_means"] = "Une retenue correspond souvent à une absence, un acompte ou une régularisation."
            result["why_it_happens"] = (
                "La retenue peut être normale si une absence, un acompte ou une correction a été enregistré."
            )
            result["what_to_do"] = "Vérifiez la ligne exacte et la période concernée."
            result["who_to_contact"] = "Service paie"

        elif subtheme == "Je veux comprendre une régularisation":
            result["what_it_means"] = "Une régularisation corrige un écart passé."
            result["why_it_happens"] = (
                "Elle peut concerner une prime, une absence, une cotisation, un avantage ou un élément variable."
            )
            result["what_to_do"] = "Comparez avec les bulletins précédents pour repérer l’élément corrigé."
            result["who_to_contact"] = "Service paie"

    # -----------------------------------------------------
    # MON PORTAIL PAIE
    # -----------------------------------------------------
    elif theme == "Mon Portail Paie":
        if subtheme == "Je ne vois pas la tuile / je n’ai pas accès":
            result["what_it_means"] = "Le problème est probablement un sujet d’accès."
            result["why_it_happens"] = "L’accès dépend des habilitations et de l’environnement One Login."
            result["what_to_do"] = "Signalez l’absence de la tuile et vérifiez vos accès."
            result["who_to_contact"] = "Manager et support informatique"

        elif subtheme == "Ma demande ne remonte pas":
            result["what_it_means"] = "Une demande peut être saisie mais non visible immédiatement en paie."
            result["why_it_happens"] = (
                "Cela peut venir d’une validation incomplète, de la période de gel, "
                "ou d’un délai normal de remontée."
            )
            result["what_to_do"] = "Vérifiez le statut de validation et la date de saisie."
            result["who_to_contact"] = "Manager / RH / paie"

        elif subtheme == "Je ne comprends pas la période de gel":
            result["what_it_means"] = "La période de gel suspend temporairement les remontées en paie."
            result["why_it_happens"] = (
                "Entre le 20 et le 7 du mois suivant, les demandes peuvent continuer à être saisies "
                "mais elles ne remontent pas immédiatement dans la paie."
            )
            result["what_to_do"] = "Attendez la prochaine fenêtre de remontée après la période de gel."
            result["who_to_contact"] = "Service paie"

        elif subtheme == "Je ne sais pas où faire ma demande":
            result["what_it_means"] = "Chaque demande suit un chemin spécifique dans le portail."
            result["why_it_happens"] = (
                "Selon le sujet, la demande peut se faire via Mes demandes, Mes validations "
                "ou Mes éléments variables."
            )
            result["what_to_do"] = "Précisez le type de demande pour être orienté vers le bon menu."
            result["who_to_contact"] = "Contact paie / RH"

        elif subtheme == "Je ne comprends pas le circuit de validation":
            result["what_it_means"] = "Certaines demandes nécessitent plusieurs étapes de validation."
            result["why_it_happens"] = (
                "Selon le sujet, la validation peut relever du manager, du contact paie ou des RH."
            )
            result["what_to_do"] = "Vérifiez l’étape actuelle de la demande et le validant attendu."
            result["who_to_contact"] = "Manager / contact paie"

        elif subtheme == "Je souhaite être accompagné sur le portail":
            result["what_it_means"] = "Un accompagnement peut être proposé sur le portail."
            result["why_it_happens"] = (
                "Certaines équipes paie peuvent prendre le contrôle du portail pour accompagner un salarié."
            )
            result["what_to_do"] = "Demandez un accompagnement ciblé sur votre démarche."
            result["who_to_contact"] = "Contact paie / gestionnaire paie"

    # -----------------------------------------------------
    # ABSENCE
    # -----------------------------------------------------
    elif theme == "Absence":
        if subtheme == "Arrêt maladie":
            result["what_it_means"] = "L’arrêt maladie a un impact à la fois sur la paie et sur les flux IJSS."
            result["why_it_happens"] = (
                "L’absence est déduite de la paie, puis la Sécurité sociale peut verser des indemnités journalières. "
                "Il peut aussi exister un maintien de salaire ou une subrogation."
            )
            result["what_to_do"] = "Vérifiez le bulletin, la période d’arrêt et les IJSS éventuelles."
            result["who_to_contact"] = "Service paie"

            if q1 == "Je veux comprendre la subrogation":
                result["what_it_means"] = "La subrogation évite certains flux directs entre salarié et Sécurité sociale."
                result["why_it_happens"] = (
                    "L’employeur peut verser tout ou partie du salaire puis percevoir directement les IJSS."
                )
                result["what_to_do"] = "Vérifiez si l’employeur a mis en place la subrogation."
            elif q1 == "Je veux comprendre l’impact paie":
                result["why_it_happens"] = (
                    "La paie peut varier à cause de la déduction de l’absence, des jours de carence, "
                    "des IJSS et d’un éventuel maintien."
                )

        elif subtheme == "Enfant malade":
            result["what_it_means"] = "Les jours enfant malade suivent des règles annuelles spécifiques."
            result["why_it_happens"] = (
                "Le nombre de jours dépend de l’âge des enfants, de leur nombre et de l’ancienneté."
            )
            result["what_to_do"] = "Vérifiez votre ancienneté et la situation familiale."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Absence injustifiée / justifiée":
            result["what_it_means"] = "L’impact paie dépend de la qualification exacte de l’absence."
            result["why_it_happens"] = (
                "Une absence injustifiée et une absence justifiée n’ont pas le même traitement."
            )
            result["what_to_do"] = "Vérifiez le justificatif et le type d’absence saisi."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Je veux comprendre l’impact paie de mon absence":
            result["what_it_means"] = "Une absence peut modifier le brut, le net et certains droits."
            result["why_it_happens"] = (
                "Selon sa nature, une absence peut entraîner une retenue, un maintien partiel "
                "ou un décalage de traitement."
            )
            result["what_to_do"] = "Identifiez le type exact d’absence et le mois concerné."
            result["who_to_contact"] = "Service paie"

        elif subtheme == "Je veux comprendre la subrogation":
            result["what_it_means"] = "La subrogation concerne les IJSS pendant l’arrêt."
            result["why_it_happens"] = (
                "L’employeur peut recevoir directement les indemnités journalières à la place du salarié."
            )
            result["what_to_do"] = "Vérifiez si la subrogation a été activée."
            result["who_to_contact"] = "Service paie"

    # -----------------------------------------------------
    # CONGÉS
    # -----------------------------------------------------
    elif theme == "Congés":
        if subtheme == "Congés payés":
            result["what_it_means"] = "Le compteur congés peut regrouper plusieurs notions."
            result["why_it_happens"] = (
                "Le bulletin peut distinguer congés acquis, congés en cours, RTT et éventuellement jours spécifiques."
            )
            result["what_to_do"] = "Vérifiez le compteur concerné et la période."
            result["who_to_contact"] = "Service paie / RH"

        elif subtheme == "RTT / récupération":
            result["what_it_means"] = "Les RTT et récupérations suivent des règles de compteur ou de validation."
            result["why_it_happens"] = (
                "Ils peuvent dépendre du temps de travail, d’une JPO/SPO ou d’une organisation spécifique."
            )
            result["what_to_do"] = "Vérifiez le compteur et la validation associée."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Mariage / PACS":
            result["what_it_means"] = "Le mariage ou PACS ouvre droit à une absence exceptionnelle."
            result["why_it_happens"] = "Le droit existe sans condition d’ancienneté dans le cadre du parcours standard."
            result["what_to_do"] = "Préparez le justificatif et positionnez l’absence dans un délai raisonnable."
            result["who_to_contact"] = "RH / manager"

        elif subtheme == "Décès":
            result["what_it_means"] = "Le nombre de jours dépend du lien familial."
            result["why_it_happens"] = (
                "Le justificatif et parfois le livret de famille servent à déterminer le droit."
            )
            result["what_to_do"] = "Préparez les justificatifs et précisez le lien concerné."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Jours de révision":
            result["what_it_means"] = "Le droit dépend du statut et de la situation."
            result["why_it_happens"] = "Les règles diffèrent entre apprenti et salarié hors apprentissage."
            result["what_to_do"] = "Préparez la convocation et vérifiez votre statut."
            result["who_to_contact"] = "RH"

        elif subtheme == "Je ne comprends pas mon compteur":
            result["what_it_means"] = "Le compteur peut regrouper plusieurs catégories de jours."
            result["why_it_happens"] = (
                "Selon les cas, il peut y avoir congés acquis, congés en cours, RTT, récupération ou jours spécifiques."
            )
            result["what_to_do"] = "Identifiez le compteur exact qui pose problème."
            result["who_to_contact"] = "Service paie / RH"

    # -----------------------------------------------------
    # MUTUELLE
    # -----------------------------------------------------
    elif theme == "Mutuelle":
        if subtheme == "La mutuelle est-elle obligatoire ?":
            result["what_it_means"] = "La mutuelle d’entreprise est en principe obligatoire."
            result["why_it_happens"] = "L’affiliation est généralement mise en place par défaut, sauf cas de dispense."
            result["what_to_do"] = "Vérifiez si vous relevez d’un cas de dispense."
            result["who_to_contact"] = "RH / partenaire mutuelle"

        elif subtheme == "Je veux une dispense":
            result["what_it_means"] = "Une dispense est possible dans certains cas uniquement."
            result["why_it_happens"] = "La dispense doit être justifiée et peut devoir être renouvelée."
            result["what_to_do"] = "Préparez les justificatifs correspondant à votre situation."
            result["who_to_contact"] = "RH / organisme assureur"

        elif subtheme == "Je n’ai pas répondu au mail d’affiliation":
            result["what_it_means"] = "Le dossier peut rester incomplet tant que l’affiliation n’est pas finalisée."
            result["why_it_happens"] = "Un délai est généralement prévu pour compléter l’affiliation."
            result["what_to_do"] = "Demandez un nouveau lien si besoin."
            result["who_to_contact"] = "Chargé RH"

        elif subtheme == "Je vois une cotisation mutuelle":
            result["what_it_means"] = "La cotisation est normale si aucune dispense valide n’a été enregistrée."
            result["why_it_happens"] = "L’affiliation est active tant qu’aucune dispense reconnue n’est en place."
            result["what_to_do"] = "Vérifiez si une dispense a été faite et acceptée."
            result["who_to_contact"] = "RH"

        elif subtheme == "Je veux comprendre ma situation mutuelle":
            result["what_it_means"] = "Il faut identifier si le sujet porte sur l’affiliation, la dispense ou la cotisation."
            result["why_it_happens"] = "Chaque sujet mutuelle suit un traitement différent."
            result["what_to_do"] = "Précisez si votre question porte sur l’affiliation, la dispense ou le prélèvement."
            result["who_to_contact"] = "RH / partenaire mutuelle"

    # -----------------------------------------------------
    # TRANSPORT
    # -----------------------------------------------------
    elif theme == "Transport":
        if subtheme == "Remboursement Navigo":
            result["what_it_means"] = "Le remboursement suppose une demande complète."
            result["why_it_happens"] = (
                "Le remboursement à 50 % nécessite une attestation, un justificatif de paiement "
                "et une copie du pass Navigo."
            )
            result["what_to_do"] = "Vérifiez que les 3 justificatifs ont bien été transmis en un seul fichier."
            result["who_to_contact"] = "Paie / RH"

        elif subtheme == "Quels justificatifs fournir ?":
            result["what_it_means"] = "Trois pièces sont attendues."
            result["why_it_happens"] = "Le dossier doit être complet pour être traité."
            result["what_to_do"] = (
                "Préparez : attestation sur l’honneur, justificatif de paiement, copie du pass Navigo."
            )
            result["who_to_contact"] = "Paie / RH"

        elif subtheme == "Ce qui n’est pas remboursé":
            result["what_it_means"] = "Tous les titres ne sont pas éligibles."
            result["why_it_happens"] = "Le Navigo Liberté+ et les tickets unitaires ne sont pas remboursés."
            result["what_to_do"] = "Vérifiez le type exact d’abonnement utilisé."
            result["who_to_contact"] = "Paie / RH"

        elif subtheme == "Ma demande transport ne remonte pas":
            result["what_it_means"] = "La demande peut être bloquée par le workflow ou la période."
            result["why_it_happens"] = "Une validation manquante ou la période de gel peuvent retarder la remontée."
            result["what_to_do"] = "Vérifiez la validation et la date de saisie."
            result["who_to_contact"] = "Paie / contact paie"

    # -----------------------------------------------------
    # TICKET RESTAURANT
    # -----------------------------------------------------
    elif theme == "Ticket restaurant":
        if subtheme == "Combien ai-je de tickets restaurant ?":
            result["what_it_means"] = "Le nombre dépend des journées réellement éligibles."
            result["why_it_happens"] = (
                "Un ticket est attribué par journée travaillée d’au moins 6 heures "
                "avec une pause d’au moins 30 minutes entre 12h00 et 14h00."
            )
            result["what_to_do"] = "Vérifiez les journées réellement éligibles."
            result["who_to_contact"] = "Paie"

        elif subtheme == "Comment déclarer mes tickets restaurant ?":
            result["what_it_means"] = "La déclaration suit une fenêtre précise."
            result["why_it_happens"] = "La saisie doit être faite avant le 20 du mois sur le portail."
            result["what_to_do"] = "Déclarez dans Mon Portail Paie, rubrique appropriée."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Je n’ai pas reçu ma carte":
            result["what_it_means"] = "Le suivi peut dépendre directement du prestataire."
            result["why_it_happens"] = "Certaines informations de livraison sont gérées côté Edenred."
            result["what_to_do"] = "Contactez Edenred pour le suivi de la carte."
            result["who_to_contact"] = "Edenred puis RH si besoin"

        elif subtheme == "Je ne comprends pas mon nombre de tickets":
            result["what_it_means"] = "Le nombre de tickets correspond aux journées éligibles déclarées."
            result["why_it_happens"] = "Une journée non éligible ou non déclarée n’ouvre pas droit à un ticket."
            result["what_to_do"] = "Recomptez les journées de travail répondant aux critères."
            result["who_to_contact"] = "Paie"

    # -----------------------------------------------------
    # TÉLÉTRAVAIL
    # -----------------------------------------------------
    elif theme == "Télétravail":
        if subtheme == "Pourquoi je n’ai pas la ligne télétravail ?":
            result["what_it_means"] = "Le dossier télétravail est probablement incomplet ou non transmis."
            result["why_it_happens"] = (
                "L’allocation nécessite un avenant signé et une assurance habitation valide."
            )
            result["what_to_do"] = "Vérifiez l’avenant et l’attestation d’assurance."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Quels documents faut-il ?":
            result["what_it_means"] = "Deux documents sont indispensables."
            result["why_it_happens"] = (
                "Sans avenant signé ni assurance valide, l’allocation ne peut pas être mise en place."
            )
            result["what_to_do"] = "Préparez l’avenant signé et l’attestation d’assurance."
            result["who_to_contact"] = "RH"

        elif subtheme == "Mon avenant / assurance a été transmis":
            result["what_it_means"] = "Le dossier semble prêt à être traité."
            result["why_it_happens"] = (
                "Une fois les documents transmis, un délai de traitement peut subsister avant apparition en paie."
            )
            result["what_to_do"] = "Vérifiez si le délai de traitement est écoulé."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Je veux comprendre l’allocation télétravail":
            result["what_it_means"] = "L’allocation dépend d’un dossier complet et validé."
            result["why_it_happens"] = "Elle n’est pas automatique sans avenant et assurance valide."
            result["what_to_do"] = "Vérifiez la présence et la validité des documents."
            result["who_to_contact"] = "RH / paie"

    # -----------------------------------------------------
    # ACOMPTE
    # -----------------------------------------------------
    elif theme == "Acompte":
        if subtheme == "Puis-je demander un acompte ?":
            result["what_it_means"] = "Un acompte est possible sous conditions."
            result["why_it_happens"] = (
                "Il porte sur une rémunération déjà gagnée, contrairement à une avance."
            )
            result["what_to_do"] = "Vérifiez que les heures correspondant au montant ont bien été réalisées."
            result["who_to_contact"] = "Service paie"

        elif subtheme == "Je veux comprendre la différence entre acompte et avance":
            result["what_it_means"] = "Acompte et avance ne correspondent pas à la même logique."
            result["why_it_happens"] = (
                "L’acompte porte sur du travail déjà effectué, alors que l’avance correspond à un salaire non encore gagné."
            )
            result["what_to_do"] = "Formulez la demande selon le bon mécanisme."
            result["who_to_contact"] = "Service paie"

        elif subtheme == "Je ne vois pas ma demande sur le portail":
            result["what_it_means"] = "La demande peut ne pas avoir été enregistrée ou visible selon la période."
            result["why_it_happens"] = "La saisie suit une fenêtre spécifique et peut dépendre des accès."
            result["what_to_do"] = "Vérifiez la période de saisie et la présence de la demande."
            result["who_to_contact"] = "Support / paie"

        elif subtheme == "Je veux connaître la fenêtre de demande":
            result["what_it_means"] = "L’acompte suit une période de demande définie."
            result["why_it_happens"] = "La demande s’effectue sur une fenêtre précise via le portail."
            result["what_to_do"] = "Consultez la période active sur Mon Portail Paie."
            result["who_to_contact"] = "Paie"

    # -----------------------------------------------------
    # BULLETINS
    # -----------------------------------------------------
    elif theme == "Bulletins":
        if subtheme == "Je veux accéder à mon bulletin":
            result["what_it_means"] = "Le bulletin est disponible dans le coffre-fort électronique."
            result["why_it_happens"] = "Les bulletins sont déposés dans Arkevia."
            result["what_to_do"] = "Connectez-vous à Arkevia."
            result["who_to_contact"] = "Paie si problème d’accès"

        elif subtheme == "Je ne retrouve pas mon bulletin":
            result["what_it_means"] = "Le bulletin peut être déposé mais non retrouvé dans le coffre."
            result["why_it_happens"] = "Le problème peut venir d’un accès, d’un classement ou d’un compte différent."
            result["what_to_do"] = "Vérifiez l’email utilisé, les dossiers et la période concernée."
            result["who_to_contact"] = "Paie / support Arkevia"

        elif subtheme == "Je veux comprendre comment fonctionne Arkevia":
            result["what_it_means"] = "Arkevia est le coffre-fort électronique pour les bulletins."
            result["why_it_happens"] = "L’accès se fait via activation puis connexion avec email personnel."
            result["what_to_do"] = "Suivez le guide d’activation ou de connexion."
            result["who_to_contact"] = "Paie / support Arkevia"

        elif subtheme == "Je veux réinitialiser mon accès":
            result["what_it_means"] = "L’accès peut être réinitialisé."
            result["why_it_happens"] = "En cas d’oubli du mot de passe, un parcours de réinitialisation est prévu."
            result["what_to_do"] = "Utilisez le lien “Mot de passe oublié ?”."
            result["who_to_contact"] = "Support Arkevia / paie"

        elif subtheme == "Importer mes anciens bulletins":
            result["what_it_means"] = "Les anciens bulletins peuvent être centralisés."
            result["why_it_happens"] = "Ils peuvent être importés depuis l’ancien coffre-fort."
            result["what_to_do"] = "Téléchargez-les puis déposez-les dans Arkevia."
            result["who_to_contact"] = "Support si besoin"

    # -----------------------------------------------------
    # DOCUMENTS DE SORTIE
    # -----------------------------------------------------
    elif theme == "Documents de sortie":
        if subtheme == "Solde de tout compte":
            result["what_it_means"] = "Le solde de tout compte fait partie des documents de fin de contrat."
            result["why_it_happens"] = "Il récapitule les sommes versées à la sortie."
            result["what_to_do"] = "Vérifiez la date de fin de contrat et la remise des documents."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Certificat de travail":
            result["what_it_means"] = "Le certificat de travail fait partie des documents de sortie."
            result["why_it_happens"] = "Il est remis à la fin du contrat."
            result["what_to_do"] = "Vérifiez si la sortie a été finalisée."
            result["who_to_contact"] = "RH"

        elif subtheme == "Attestation France Travail":
            result["what_it_means"] = "L’attestation France Travail est un document de fin de contrat."
            result["why_it_happens"] = "Elle est nécessaire pour les démarches chômage."
            result["what_to_do"] = "Vérifiez si le contrat est bien clôturé."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Je n’ai pas reçu mes documents de sortie":
            result["what_it_means"] = "Les documents peuvent être en cours de préparation ou non encore transmis."
            result["why_it_happens"] = "La finalisation du départ conditionne leur émission."
            result["what_to_do"] = "Vérifiez la date de sortie effective."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Je veux comprendre mes documents de fin de contrat":
            result["what_it_means"] = "Chaque document a une fonction différente."
            result["why_it_happens"] = (
                "Solde de tout compte, certificat de travail et attestation France Travail "
                "ne répondent pas au même besoin."
            )
            result["what_to_do"] = "Précisez le document concerné."
            result["who_to_contact"] = "RH / paie"

    # -----------------------------------------------------
    # JPO / SPO
    # -----------------------------------------------------
    elif theme == "JPO ou SPO":
        if subtheme == "Je veux comprendre les JPO / SPO":
            result["what_it_means"] = "Les JPO / SPO suivent des règles spécifiques de déclaration et de traitement."
            result["why_it_happens"] = (
                "Selon le cas, elles peuvent donner lieu à récupération ou paiement."
            )
            result["what_to_do"] = "Vérifiez si l’événement a bien été déclaré et validé."
            result["who_to_contact"] = "Manager / paie"

        elif subtheme == "Je veux comprendre la récupération":
            result["what_it_means"] = "Certaines JPO / SPO ouvrent droit à récupération."
            result["why_it_happens"] = "Le traitement dépend du type de journée et de la règle appliquée."
            result["what_to_do"] = "Vérifiez la règle de récupération appliquée."
            result["who_to_contact"] = "Paie"

        elif subtheme == "Je veux comprendre le paiement":
            result["what_it_means"] = "Certaines JPO / SPO peuvent être payées."
            result["why_it_happens"] = "Le paiement dépend de la règle déclenchée lors du traitement."
            result["what_to_do"] = "Vérifiez si la JPO / SPO a été traitée en paiement ou en récupération."
            result["who_to_contact"] = "Paie"

        elif subtheme == "Je ne vois pas ma JPO / SPO":
            result["what_it_means"] = "La déclaration peut ne pas encore avoir remonté."
            result["why_it_happens"] = "Cela peut venir d’une validation manquante ou d’un délai de traitement."
            result["what_to_do"] = "Vérifiez la saisie et le statut de validation."
            result["who_to_contact"] = "Manager / paie"

    # -----------------------------------------------------
    # HEURES SUPPLÉMENTAIRES
    # -----------------------------------------------------
    elif theme == "Heures supplémentaires":
        if subtheme == "Il manque des heures":
            result["what_it_means"] = "L’absence des heures sur le bulletin ne signifie pas forcément une erreur."
            result["why_it_happens"] = (
                "Les heures suivent un circuit de validation manager → RH → paie."
            )
            result["what_to_do"] = "Vérifiez la date et la validation."
            result["who_to_contact"] = "Manager / RH / paie"

        elif subtheme == "Mes heures ont été faites avant le 15":
            result["what_it_means"] = "Elles pouvaient potentiellement être intégrées sur la paie du mois."
            result["why_it_happens"] = (
                "Sous réserve de validation et de transmission complète."
            )
            result["what_to_do"] = "Vérifiez la validation manager et la transmission RH."
            result["who_to_contact"] = "Manager / RH / paie"

        elif subtheme == "Mes heures ont été faites après le 15":
            result["what_it_means"] = "Le décalage sur le mois suivant peut être normal."
            result["why_it_happens"] = "Les heures tardives sont souvent payées en M+1."
            result["what_to_do"] = "Vérifiez le bulletin du mois suivant."
            result["who_to_contact"] = "Paie si elles restent absentes ensuite"

        elif subtheme == "Le manager n’a pas validé":
            result["what_it_means"] = "Le circuit est bloqué au stade de validation."
            result["why_it_happens"] = "Sans validation manager, la paie ne peut pas traiter correctement les heures."
            result["what_to_do"] = "Demandez la validation du manager."
            result["who_to_contact"] = "Manager"

        elif subtheme == "Je veux comprendre le décalage de paiement":
            result["what_it_means"] = "Le décalage peut être normal selon le moment de transmission."
            result["why_it_happens"] = "Les heures transmises tardivement basculent souvent sur le mois suivant."
            result["what_to_do"] = "Vérifiez la date de transmission."
            result["who_to_contact"] = "RH / paie"

    # -----------------------------------------------------
    # DEMANDE DE DOCUMENTS
    # -----------------------------------------------------
    elif theme == "Demande de documents":
        if subtheme == "Attestation employeur":
            result["what_it_means"] = "La demande doit être formulée clairement."
            result["why_it_happens"] = "Le type exact d’attestation conditionne le traitement."
            result["what_to_do"] = "Précisez le type d’attestation employeur demandé."
            result["who_to_contact"] = "RH / paie"

        elif subtheme == "Attestation de salaire":
            result["what_it_means"] = "L’attestation de salaire suit un circuit spécifique."
            result["why_it_happens"] = "Elle est souvent liée à une absence ou un arrêt."
            result["what_to_do"] = "Précisez la période et le motif."
            result["who_to_contact"] = "Paie"

        elif subtheme == "Duplicata de bulletin":
            result["what_it_means"] = "Le duplicata peut souvent être récupéré via le coffre-fort."
            result["why_it_happens"] = "Le document existe déjà dans l’espace de stockage électronique."
            result["what_to_do"] = "Vérifiez d’abord Arkevia."
            result["who_to_contact"] = "Paie"

        elif subtheme == "Guide d’accès Arkevia":
            result["what_it_means"] = "Le guide accompagne l’activation ou la connexion."
            result["why_it_happens"] = "L’accès repose sur une procédure d’activation."
            result["what_to_do"] = "Demandez le guide d’accès ou le code si besoin."
            result["who_to_contact"] = "Paie / RH"

        elif subtheme == "Autre document":
            result["what_it_means"] = "Le document demandé n’est pas identifié précisément."
            result["why_it_happens"] = "Le type exact de document change le bon interlocuteur."
            result["what_to_do"] = "Précisez le document souhaité."
            result["who_to_contact"] = "RH / paie"

    else:
        result["what_it_means"] = "Le besoin n’a pas pu être qualifié précisément."
        result["why_it_happens"] = "Le parcours manque encore d’informations pour répondre de façon fiable."
        result["what_to_do"] = "Revenez en arrière ou recommencez le parcours."
        result["who_to_contact"] = "Service paie / RH"

    return _finalize_result(result)


# =========================================================
# OUTILS
# =========================================================
def needs_free_message(subtheme: str) -> bool:
    return subtheme in {"Mon sujet n’est pas dans la liste", "Autre document"}


def render_progress() -> None:
    current_step = min(st.session_state["step"], 5)
    progress_map = {
        1: 0.20,
        2: 0.40,
        3: 0.60,
        4: 0.80,
        5: 1.00,
        99: 1.00,
    }
    st.progress(progress_map.get(st.session_state["step"], 0.20))
    st.caption(f"Étape {current_step} sur 5")


def render_context() -> None:
    if all([
        st.session_state["role"],
        st.session_state["entity"],
        st.session_state["theme"],
    ]):
        st.markdown('<div class="context-box">', unsafe_allow_html=True)
        st.markdown("**Contexte sélectionné**")
        st.write(f"Rôle : {st.session_state['role']}")
        st.write(f"Entité : {st.session_state['entity']}")
        st.write(f"Thème : {st.session_state['theme']}")
        if st.session_state["subtheme"]:
            st.write(f"Besoin : {st.session_state['subtheme']}")
        st.markdown('</div>', unsafe_allow_html=True)


def render_result(result: Dict[str, str]) -> None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Réponse guidée")
    st.markdown(f'<div class="topic-tag">{result["topic"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="answer-card">', unsafe_allow_html=True)
    st.markdown("**Ce que cela signifie**")
    st.write(result["what_it_means"])

    st.markdown("**Pourquoi cela arrive**")
    st.write(result["why_it_happens"])

    st.markdown("**Ce que vous devez faire**")
    st.write(result["what_to_do"])

    st.markdown("**Qui contacter si besoin**")
    st.write(result["who_to_contact"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("**Réponse prête à copier**")
    st.text_area(
        "Vous pouvez copier ce texte",
        value=result["ready_text"],
        height=220,
        key="copy_area"
    )
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# PROGRESSION + ACTIONS
# =========================================================
render_progress()

top1, top2 = st.columns([5, 1])
with top2:
    if st.button("↺ Recommencer", use_container_width=True):
        reset_flow()
        st.rerun()

render_context()

# =========================================================
# ÉTAPE 1 : RÔLE
# =========================================================
if st.session_state["step"] == 1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1. Votre question vous concerne en tant que ?")

    role = st.radio(
        "Choisissez votre rôle",
        ROLES,
        index=None
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="kpi">👤 Salarié<br><span class="muted">Question sur votre propre situation</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="kpi">🧑‍💼 Manager<br><span class="muted">Question sur un salarié ou sur votre rôle de validation</span></div>', unsafe_allow_html=True)

    if st.button("Continuer", type="primary", use_container_width=True):
        if role:
            st.session_state["role"] = role
            set_step(2)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ÉTAPE 2 : ENTITÉ
# =========================================================
elif st.session_state["step"] == 2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2. Elle concerne un salarié de quelle entité ?")

    entity = st.selectbox(
        "Choisissez l’entité",
        [""] + ENTITIES
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            set_step(1)

    with col2:
        if st.button("Continuer", type="primary", use_container_width=True):
            if entity:
                st.session_state["entity"] = entity
                set_step(3)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ÉTAPE 3 : THÈME
# =========================================================
elif st.session_state["step"] == 3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("3. Quel est le thème de votre demande ?")

    theme = st.radio(
        "Choisissez le thème",
        THEMES,
        index=None
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            set_step(2)

    with col2:
        if st.button("Continuer", type="primary", use_container_width=True):
            if theme:
                st.session_state["theme"] = theme
                set_step(4)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ÉTAPE 4 : BESOIN PRÉCIS
# =========================================================
elif st.session_state["step"] == 4:
    theme = st.session_state["theme"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("4. Quel est votre besoin précis ?")

    subtheme = st.radio(
        "Choisissez le besoin",
        SUBTHEMES[theme],
        index=None
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Retour", use_container_width=True):
            set_step(3)

    with col2:
        if st.button("Continuer", type="primary", use_container_width=True):
            if subtheme:
                st.session_state["subtheme"] = subtheme

                if needs_free_message(subtheme):
                    set_step(5)
                else:
                    st.session_state["result"] = build_structured_answer(
                        st.session_state["role"],
                        st.session_state["entity"],
                        st.session_state["theme"],
                        st.session_state["subtheme"],
                    )
                    set_step(99)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ÉTAPE 5 : MESSAGE LIBRE
# =========================================================
elif st.session_state["step"] == 5:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("5. Sujet non traité dans la liste")
    st.caption("Décrivez votre besoin pour préparer un message clair à transmettre.")

    free_message = st.text_area(
        "Décrivez votre demande",
        value=st.session_state.get("free_message", ""),
        height=160
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Retour", use_container_width=True):
            set_step(4)

    with col2:
        if st.button("Préparer le message", type="primary", use_container_width=True):
            if free_message.strip():
                st.session_state["free_message"] = free_message.strip()

                ready_text = f"""Bonjour,

Je vous contacte en tant que {st.session_state['role'].lower()}.

Entité concernée : {st.session_state['entity']}
Thème : {st.session_state['theme']}
Besoin précis : {st.session_state['subtheme']}

Description de la demande :
{st.session_state['free_message']}

Merci par avance pour votre aide.

Cordialement,"""

                st.session_state["result"] = {
                    "topic": f"{st.session_state['role']} • {st.session_state['entity']} • {st.session_state['theme']} • {st.session_state['subtheme']}",
                    "what_it_means": "Le sujet n’est pas couvert directement par l’agent.",
                    "why_it_happens": "La demande nécessite une analyse humaine ou un traitement spécifique.",
                    "what_to_do": "Transmettre le message préparé au bon interlocuteur.",
                    "who_to_contact": "Service paie / RH / manager selon le sujet.",
                    "ready_text": ready_text
                }
                set_step(99)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ÉTAPE FINALE
# =========================================================
elif st.session_state["step"] == 99:
    render_result(st.session_state["result"])

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Actions**")
    a1, a2, a3 = st.columns(3)

    with a1:
        if st.button("Nouvelle demande", use_container_width=True):
            reset_flow()
            st.rerun()

    with a2:
        if st.button("Revenir à l’étape précédente", use_container_width=True):
            if needs_free_message(st.session_state["subtheme"]):
                set_step(5)
            else:
                set_step(4)

    with a3:
        if st.button("Revenir au menu principal", use_container_width=True):
            reset_flow()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# BAS DE PAGE
# =========================================================
st.markdown(
    '<div class="footer-note">Cet agent guide le besoin avant de répondre afin de limiter les réponses hors sujet et d’orienter plus vite vers la bonne information.</div>',
    unsafe_allow_html=True
)