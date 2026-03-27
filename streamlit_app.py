import streamlit as st

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
}
.footer-note {
    color: #6c757d;
    font-size: 0.88rem;
    margin-top: 12px;
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
# SESSION STATE
# =========================================================
DEFAULTS = {
    "step": 1,
    "profile": None,
    "theme": None,
    "subtheme": None,
    "q1": None,
    "q2": None,
    "q3": None,
    "result": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def reset_flow():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v

def go_to(step: int):
    st.session_state["step"] = step
    st.rerun()

# =========================================================
# DONNÉES MÉTIER
# =========================================================
THEMES = {
    "Salarié": [
        "Ma paie / mon bulletin",
        "Absence / congé",
        "Mutuelle",
        "Transport",
        "Tickets restaurant",
        "Télétravail",
        "Arkevia / bulletins",
        "Mon Portail Paie",
    ],
    "Manager": [
        "Paie d’un collaborateur",
        "Absence / congé",
        "Transport",
        "Tickets restaurant",
        "Télétravail",
        "Mon Portail Paie",
    ],
    "Document / accès": [
        "Arkevia / bulletins",
        "Mon Portail Paie",
        "Document RH / paie",
    ]
}

SUBTHEMES = {
    "Ma paie / mon bulletin": [
        "Mon salaire a baissé",
        "Il manque des heures",
        "Il manque une prime",
        "Je pense qu’il y a une erreur",
        "Je ne comprends pas une ligne",
    ],
    "Paie d’un collaborateur": [
        "Salaire en baisse",
        "Heures absentes",
        "Prime absente",
        "Erreur signalée par un salarié",
        "Allocation télétravail absente",
    ],
    "Absence / congé": [
        "Arrêt maladie",
        "Enfant malade",
        "Décès",
        "Mariage / PACS",
        "Jours de révision",
        "Congés payés",
        "Période de gel",
    ],
    "Mutuelle": [
        "La mutuelle est-elle obligatoire ?",
        "Je n’ai pas répondu au mail",
        "Je veux une dispense",
        "Je vois une cotisation mutuelle",
    ],
    "Transport": [
        "Remboursement Navigo",
        "Quels justificatifs fournir ?",
        "Ce qui n’est pas remboursé",
    ],
    "Tickets restaurant": [
        "Combien ai-je de tickets ?",
        "Comment les déclarer ?",
        "Je n’ai pas reçu ma carte",
    ],
    "Télétravail": [
        "Pourquoi je n’ai pas la ligne ?",
        "Quels documents faut-il ?",
    ],
    "Arkevia / bulletins": [
        "Activer mon coffre-fort",
        "Me connecter",
        "Importer mes anciens bulletins",
    ],
    "Mon Portail Paie": [
        "Période de gel",
        "Acompte via portail",
        "Demande non remontée",
        "Je ne vois pas la tuile / pas d’accès",
        "Prise de contrôle / accompagnement",
    ],
    "Document RH / paie": [
        "Attestation employeur",
        "Bulletin de paie",
        "Guide d’accès Arkevia",
    ],
}

# =========================================================
# MOTEUR DE RÉPONSE
# =========================================================
def build_structured_answer(profile, theme, subtheme, q1=None, q2=None, q3=None):
    topic = f"{profile} • {theme} • {subtheme}"

    what_it_means = ""
    why_it_happens = ""
    what_to_do = ""
    who_to_contact = ""
    ready_text = ""

    # -----------------------------------------------------
    # SALARIÉ / PAIE
    # -----------------------------------------------------
    if theme == "Ma paie / mon bulletin" and subtheme == "Mon salaire a baissé":
        if q1 == "Oui, après une absence maladie":
            what_it_means = "La baisse semble cohérente avec une absence maladie."
            why_it_happens = (
                "En arrêt maladie, l’absence est déduite de la paie. "
                "La Sécurité sociale peut verser des indemnités journalières, "
                "avec en principe 3 jours de carence sauf exceptions. "
                "Selon l’ancienneté, il peut aussi y avoir un maintien de salaire ou un complément de prévoyance."
            )
            what_to_do = (
                "Vérifiez le mois concerné, la présence d’une absence maladie sur le bulletin, "
                "et si vous avez perçu ou non des IJSS."
            )
            who_to_contact = "Service paie si l’écart vous semble anormal après vérification."
        elif q1 == "Oui, après une autre absence":
            what_it_means = "La baisse peut être liée à une absence non intégralement rémunérée."
            why_it_happens = (
                "Certaines absences impactent directement la paie. "
                "Le montant final dépend du type d’absence et de sa prise en charge éventuelle."
            )
            what_to_do = "Vérifiez le type d’absence posé et le mois concerné."
            who_to_contact = "Service paie ou RH si le traitement ne vous paraît pas cohérent."
        else:
            what_it_means = "La baisse ne semble pas liée à une absence."
            why_it_happens = (
                "Les causes possibles sont souvent : prime absente ou différente, acompte, régularisation, "
                "cotisation, ou élément variable non encore remonté en paie."
            )
            what_to_do = "Vérifiez s’il manque une prime, s’il y a eu un acompte ou une régularisation."
            who_to_contact = "Service paie après contrôle du bulletin."

    elif theme == "Ma paie / mon bulletin" and subtheme == "Il manque des heures":
        if q1 == "Avant le 15" and q2 == "Oui":
            what_it_means = "Les heures auraient pu être intégrées sur la paie du mois."
            why_it_happens = (
                "Quand les heures sont faites et validées avant le 15, elles peuvent en principe être traitées "
                "sur la paie du mois, à condition que le circuit manager → RH → paie ait bien été respecté."
            )
            what_to_do = "Vérifiez si la transmission RH a bien été faite jusqu’à la paie."
            who_to_contact = "Manager puis RH / paie si besoin."
        elif q1 == "Avant le 15" and q2 == "Non":
            what_it_means = "L’absence de paiement est probablement liée à l’absence de validation."
            why_it_happens = (
                "Sans validation manager, les heures ne peuvent pas être correctement remontées et traitées."
            )
            what_to_do = "Demandez la validation du manager."
            who_to_contact = "Manager."
        elif q1 == "Après le 15":
            what_it_means = "Le décalage vers le mois suivant est probablement normal."
            why_it_happens = (
                "Les heures transmises après le 15 sont généralement traitées sur la paie M+1."
            )
            what_to_do = "Vérifiez le bulletin du mois suivant."
            who_to_contact = "Service paie uniquement si les heures restent absentes ensuite."
        else:
            what_it_means = "Le traitement dépend du moment de transmission et de la validation."
            why_it_happens = (
                "Le circuit des heures suit plusieurs étapes de validation avant la paie."
            )
            what_to_do = "Confirmez la date de transmission et la validation manager."
            who_to_contact = "Manager ou RH."

    elif theme == "Ma paie / mon bulletin" and subtheme == "Il manque une prime":
        what_it_means = "Le service paie n’est pas forcément la source de l’erreur."
        why_it_happens = (
            "Le montant de la prime est transmis par le service RH en lien avec le manager, "
            "puis appliqué en paie tel qu’il est communiqué."
        )
        what_to_do = "Vérifiez d’abord le montant validé côté RH / management."
        who_to_contact = "Manager ou RH en premier."

    elif theme == "Ma paie / mon bulletin" and subtheme == "Je pense qu’il y a une erreur":
        what_it_means = "Il faut qualifier l’écart pour distinguer une vraie anomalie d’un décalage normal."
        why_it_happens = (
            "Une ligne manquante ou un montant différent peut venir d’une régularisation, "
            "d’un décalage de traitement ou d’une erreur réelle."
        )
        what_to_do = (
            "Préparez : le mois concerné, le libellé exact de la ligne, "
            "et la différence constatée."
        )
        who_to_contact = "Service paie."

    elif theme == "Ma paie / mon bulletin" and subtheme == "Je ne comprends pas une ligne":
        what_it_means = "Une ligne de bulletin doit être interprétée par son type."
        why_it_happens = (
            "Une ligne peut correspondre à une absence, une prime, une cotisation, un acompte "
            "ou une allocation."
        )
        what_to_do = "Relevez le libellé exact de la ligne et le mois concerné."
        who_to_contact = "Service paie."

    # -----------------------------------------------------
    # MANAGER / PAIE
    # -----------------------------------------------------
    elif theme == "Paie d’un collaborateur" and subtheme == "Heures absentes":
        what_it_means = "L’absence d’heures sur le bulletin n’est pas forcément une erreur."
        why_it_happens = (
            "Le traitement dépend du circuit manager → RH → paie, ainsi que de la date de transmission. "
            "Après le 15, le paiement bascule souvent sur M+1."
        )
        what_to_do = "Vérifiez la validation manager et la date de transmission au RH."
        who_to_contact = "RH / paie si le circuit a bien été respecté."

    elif theme == "Paie d’un collaborateur" and subtheme == "Allocation télétravail absente":
        what_it_means = "Le dossier télétravail est probablement incomplet."
        why_it_happens = (
            "L’allocation télétravail est mise en place lorsque l’avenant signé et l’attestation "
            "d’assurance habitation valide ont été transmis."
        )
        what_to_do = "Vérifiez la présence de l’avenant signé et de l’assurance en cours de validité."
        who_to_contact = "RH puis paie."

    elif theme == "Paie d’un collaborateur" and subtheme == "Prime absente":
        what_it_means = "La paie applique ce qui lui est transmis."
        why_it_happens = (
            "Le montant de la prime est normalement validé par le manager et/ou RH avant transmission."
        )
        what_to_do = "Vérifiez la validation du montant côté management / RH."
        who_to_contact = "RH."

    elif theme == "Paie d’un collaborateur" and subtheme == "Salaire en baisse":
        what_it_means = "La baisse peut être cohérente avec une absence, une régularisation ou un élément variable."
        why_it_happens = (
            "Une paie varie souvent en fonction des absences, primes, acomptes ou autres éléments variables."
        )
        what_to_do = "Comparer le mois concerné au mois précédent et identifier l’événement déclencheur."
        who_to_contact = "Paie si l’écart reste inexpliqué."

    elif theme == "Paie d’un collaborateur" and subtheme == "Erreur signalée par un salarié":
        what_it_means = "Il faut d’abord qualifier le signalement."
        why_it_happens = (
            "Un signalement peut correspondre à une vraie anomalie ou à un décalage normal de traitement."
        )
        what_to_do = (
            "Demandez au salarié : le mois concerné, la ligne concernée et la différence constatée."
        )
        who_to_contact = "Paie."

    # -----------------------------------------------------
    # ABSENCE / CONGE
    # -----------------------------------------------------
    elif theme == "Absence / congé" and subtheme == "Arrêt maladie":
        if q1 == "Comprendre la baisse de paie":
            what_it_means = "La variation de paie est souvent normale en cas d’arrêt maladie."
            why_it_happens = (
                "L’absence est déduite, la Sécurité sociale peut verser des IJSS, "
                "et 3 jours de carence peuvent s’appliquer sauf exceptions."
            )
            what_to_do = "Vérifiez le bulletin et la période de l’arrêt."
            who_to_contact = "Service paie si besoin."
        elif q1 == "Comprendre la subrogation":
            what_it_means = "La subrogation évite certains flux directs entre salarié et Sécurité sociale."
            why_it_happens = (
                "L’employeur peut verser tout ou partie du salaire puis percevoir directement les IJSS."
            )
            what_to_do = "Vérifiez si l’employeur a mis en place la subrogation."
            who_to_contact = "Service paie."
        else:
            what_it_means = "Un arrêt maladie a un impact paie et potentiellement un flux IJSS."
            why_it_happens = (
                "Il combine souvent déduction d’absence, IJSS, carence et éventuellement maintien."
            )
            what_to_do = "Contrôlez la période et le bulletin concerné."
            who_to_contact = "Service paie."

    elif theme == "Absence / congé" and subtheme == "Enfant malade":
        what_it_means = "Les jours enfant malade obéissent à des règles annuelles spécifiques."
        why_it_happens = (
            "Le nombre de jours dépend de l’âge des enfants, de leur nombre et de l’ancienneté."
        )
        what_to_do = "Vérifiez l’ancienneté et la situation familiale."
        who_to_contact = "RH / paie."

    elif theme == "Absence / congé" and subtheme == "Décès":
        what_it_means = "Le nombre de jours dépend du lien familial."
        why_it_happens = (
            "Le justificatif et parfois le livret de famille servent à établir le lien ouvrant droit au congé."
        )
        what_to_do = "Préparez les justificatifs et identifiez le lien concerné."
        who_to_contact = "RH / paie."

    elif theme == "Absence / congé" and subtheme == "Mariage / PACS":
        what_it_means = "Le mariage ou PACS ouvre droit à une absence exceptionnelle."
        why_it_happens = (
            "Le droit ne dépend pas de l’ancienneté pour ce type d’événement."
        )
        what_to_do = "Préparez le justificatif et positionnez le congé dans un délai raisonnable."
        who_to_contact = "RH / manager."

    elif theme == "Absence / congé" and subtheme == "Jours de révision":
        what_it_means = "Le droit varie selon que vous êtes apprenti ou non."
        why_it_happens = (
            "Les règles diffèrent entre congé apprenti et examen universitaire ou professionnel."
        )
        what_to_do = "Préparez votre convocation et vérifiez votre statut."
        who_to_contact = "RH."

    elif theme == "Absence / congé" and subtheme == "Congés payés":
        what_it_means = "Le compteur CP mélange parfois congés légaux et jours mobiles."
        why_it_happens = (
            "Le bulletin peut afficher 30 jours car il regroupe 25 jours légaux et 5 jours mobiles conventionnels."
        )
        what_to_do = "Distinguez CP acquis et CP en cours."
        who_to_contact = "Paie si besoin d’explication sur le compteur."

    elif theme == "Absence / congé" and subtheme == "Période de gel":
        what_it_means = "Une demande peut être correcte mais non encore remontée."
        why_it_happens = (
            "Entre le 20 et le 7 du mois suivant, les demandes continuent d’être faites, "
            "mais elles ne remontent pas immédiatement en paie."
        )
        what_to_do = "Attendre la prochaine fenêtre de remontée."
        who_to_contact = "Paie si le décalage persiste au-delà."

    # -----------------------------------------------------
    # MUTUELLE
    # -----------------------------------------------------
    elif theme == "Mutuelle":
        if subtheme == "La mutuelle est-elle obligatoire ?":
            what_it_means = "La mutuelle d’entreprise est en principe obligatoire."
            why_it_happens = (
                "L’affiliation est généralement mise en place par défaut, sauf cas de dispense."
            )
            what_to_do = "Vérifiez si vous relevez d’un cas de dispense."
            who_to_contact = "RH / partenaire mutuelle."
        elif subtheme == "Je n’ai pas répondu au mail":
            what_it_means = "Le dossier peut rester incomplet si l’affiliation n’est pas finalisée."
            why_it_happens = (
                "Vous disposez en principe d’un délai de 2 mois pour compléter l’affiliation."
            )
            what_to_do = "Demander un nouveau lien si nécessaire."
            who_to_contact = "Chargé RH."
        elif subtheme == "Je veux une dispense":
            what_it_means = "Une dispense est possible uniquement dans certains cas."
            why_it_happens = (
                "La dispense doit être justifiée et peut devoir être renouvelée selon le contrat."
            )
            what_to_do = "Préparer les justificatifs de dispense."
            who_to_contact = "RH / organisme assureur selon le process interne."
        elif subtheme == "Je vois une cotisation mutuelle":
            what_it_means = "La cotisation est normale si aucune dispense valide n’a été enregistrée."
            why_it_happens = (
                "L’affiliation est active tant qu’aucune dispense reconnue n’est en place."
            )
            what_to_do = "Vérifier si une dispense a été faite et acceptée."
            who_to_contact = "RH."

    # -----------------------------------------------------
    # TRANSPORT
    # -----------------------------------------------------
    elif theme == "Transport":
        if subtheme == "Remboursement Navigo":
            what_it_means = "Le remboursement est conditionné à une demande complète."
            why_it_happens = (
                "Le portail attend une demande avec justificatifs regroupés."
            )
            what_to_do = (
                "Déposer : attestation sur l’honneur signée, justificatif de paiement et copie du pass Navigo."
            )
            who_to_contact = "Paie / RH si la demande complète ne remonte pas."
        elif subtheme == "Quels justificatifs fournir ?":
            what_it_means = "Trois pièces sont attendues."
            why_it_happens = (
                "Le remboursement à 50 % nécessite un dossier complet."
            )
            what_to_do = (
                "Préparer un seul fichier avec attestation sur l’honneur, justificatif de paiement et copie du pass Navigo."
            )
            who_to_contact = "Paie / RH."
        elif subtheme == "Ce qui n’est pas remboursé":
            what_it_means = "Tous les titres de transport ne sont pas éligibles."
            why_it_happens = (
                "Le Navigo Liberté+, les tickets unitaires et carnets ne sont pas remboursés."
            )
            what_to_do = "Vérifier le type d’abonnement utilisé."
            who_to_contact = "Paie / RH."

    # -----------------------------------------------------
    # TR
    # -----------------------------------------------------
    elif theme == "Tickets restaurant":
        if subtheme == "Combien ai-je de tickets ?":
            what_it_means = "Les tickets restaurant dépendent du temps réellement travaillé."
            why_it_happens = (
                "1 ticket est attribué par journée d’au moins 6 heures avec une pause d’au moins 30 minutes entre 12h00 et 14h00."
            )
            what_to_do = "Vérifier les journées réellement éligibles."
            who_to_contact = "Paie si l’écart persiste."
        elif subtheme == "Comment les déclarer ?":
            what_it_means = "La déclaration suit une fenêtre précise."
            why_it_happens = (
                "La saisie doit être faite sur Mon Portail Paie avant le 20 du mois."
            )
            what_to_do = "Déclarer dans Mes demandes / Mes éléments variables."
            who_to_contact = "RH / paie en cas de blocage."
        elif subtheme == "Je n’ai pas reçu ma carte":
            what_it_means = "Le suivi peut dépendre directement du prestataire."
            why_it_happens = (
                "Certaines informations de livraison restent gérées côté Edenred."
            )
            what_to_do = "Contacter Edenred pour le suivi de la carte."
            who_to_contact = "Edenred puis RH si besoin."

    # -----------------------------------------------------
    # TELETRAVAIL
    # -----------------------------------------------------
    elif theme == "Télétravail":
        if subtheme == "Pourquoi je n’ai pas la ligne ?":
            what_it_means = "Le dossier télétravail est probablement incomplet ou non transmis."
            why_it_happens = (
                "L’allocation nécessite un avenant signé et une attestation d’assurance habitation valide."
            )
            what_to_do = "Vérifier ces deux documents."
            who_to_contact = "RH / paie."
        elif subtheme == "Quels documents faut-il ?":
            what_it_means = "Deux documents sont indispensables."
            why_it_happens = (
                "Sans avenant signé ni assurance valide, l’allocation ne peut pas être mise en place."
            )
            what_to_do = "Préparer l’avenant signé et l’assurance habitation."
            who_to_contact = "RH."

    # -----------------------------------------------------
    # ARKEVIA
    # -----------------------------------------------------
    elif theme == "Arkevia / bulletins":
        if subtheme == "Activer mon coffre-fort":
            what_it_means = "L’activation se fait en plusieurs étapes simples."
            why_it_happens = (
                "Le coffre-fort demande matricule, code secret, identité et email personnel."
            )
            what_to_do = (
                "Utiliser OneLogin ou myarkevia.com, cliquer sur “Je m’inscris”, "
                "puis suivre les étapes d’activation."
            )
            who_to_contact = "Paie / RH si vous n’avez plus matricule ou code secret."
        elif subtheme == "Me connecter":
            what_it_means = "La connexion se fait avec l’email personnel déclaré."
            why_it_happens = (
                "L’adresse email personnelle sert d’identifiant principal après activation."
            )
            what_to_do = "Utiliser “Mot de passe oublié ?” si nécessaire."
            who_to_contact = "Support Arkevia / paie si besoin."
        elif subtheme == "Importer mes anciens bulletins":
            what_it_means = "Arkevia peut centraliser vos anciens bulletins."
            why_it_happens = (
                "Les documents peuvent être importés manuellement depuis l’ancien coffre-fort."
            )
            what_to_do = "Télécharger depuis PeopleDoc puis déposer dans Arkevia."
            who_to_contact = "Support si besoin."

    # -----------------------------------------------------
    # PORTAIL PAIE
    # -----------------------------------------------------
    elif theme == "Mon Portail Paie":
        if subtheme == "Période de gel":
            what_it_means = "Une demande peut être bien saisie mais non visible immédiatement en paie."
            why_it_happens = (
                "Entre le 20 et le 7 du mois suivant, les échanges sont gelés entre le portail et la paie."
            )
            what_to_do = "Attendre la prochaine fenêtre de remontée."
            who_to_contact = "Paie si le décalage persiste."
        elif subtheme == "Acompte via portail":
            what_it_means = "Le portail est le canal obligatoire de demande."
            why_it_happens = (
                "Depuis la mise en place du portail, les demandes d’acompte passent exclusivement par cet outil."
            )
            what_to_do = "Faire la demande dans la fenêtre prévue."
            who_to_contact = "Manager / support si la tuile n’est pas visible."
        elif subtheme == "Demande non remontée":
            what_it_means = "La demande peut être bloquée par le workflow ou la période."
            why_it_happens = (
                "Validation incomplète, période de gel ou saisie hors fenêtre peuvent empêcher la remontée."
            )
            what_to_do = "Vérifier le statut de validation et la période de saisie."
            who_to_contact = "Manager, RH ou paie selon le sujet."
        elif subtheme == "Je ne vois pas la tuile / pas d’accès":
            what_it_means = "Le problème est probablement un sujet d’accès et non un sujet paie."
            why_it_happens = (
                "L’accès dépend des habilitations et de l’environnement OneLogin."
            )
            what_to_do = "Signaler l’absence de tuile."
            who_to_contact = "Manager et support informatique."
        elif subtheme == "Prise de contrôle / accompagnement":
            what_it_means = "Le contact paie peut accompagner un collaborateur sur certaines démarches."
            why_it_happens = (
                "Le portail prévoit une fonction de prise de contrôle dans le périmètre du gestionnaire."
            )
            what_to_do = "Demander un accompagnement si besoin."
            who_to_contact = "Contact paie / gestionnaire paie."

    # -----------------------------------------------------
    # DOCUMENT / ACCES
    # -----------------------------------------------------
    elif theme == "Document RH / paie":
        if subtheme == "Attestation employeur":
            what_it_means = "La demande doit être formulée clairement pour être traitée vite."
            why_it_happens = (
                "Le type exact d’attestation change le circuit de traitement."
            )
            what_to_do = "Préciser le type de document demandé."
            who_to_contact = "RH / paie."
        elif subtheme == "Bulletin de paie":
            what_it_means = "Le bulletin est disponible via le coffre-fort électronique."
            why_it_happens = (
                "Le dépôt des bulletins se fait désormais dans Arkevia."
            )
            what_to_do = "Se connecter à Arkevia."
            who_to_contact = "Paie si problème d’accès."
        elif subtheme == "Guide d’accès Arkevia":
            what_it_means = "Le guide sert à accompagner l’activation ou la connexion."
            why_it_happens = (
                "L’accès Arkevia repose sur des identifiants d’activation initiaux."
            )
            what_to_do = "Demander le guide ou le code secret si besoin."
            who_to_contact = "Paie / RH."

    else:
        what_it_means = "Le besoin n’a pas pu être qualifié précisément."
        why_it_happens = "Le parcours manque encore d’informations pour répondre de façon fiable."
        what_to_do = "Revenir en arrière ou recommencer le parcours."
        who_to_contact = "Service paie / RH."

    ready_text = (
        f"Sujet : {topic}\n\n"
        f"Ce que cela signifie :\n{what_it_means}\n\n"
        f"Pourquoi cela arrive :\n{why_it_happens}\n\n"
        f"Ce que vous devez faire :\n{what_to_do}\n\n"
        f"Qui contacter si besoin :\n{who_to_contact}"
    )

    return {
        "topic": topic,
        "what_it_means": what_it_means,
        "why_it_happens": why_it_happens,
        "what_to_do": what_to_do,
        "who_to_contact": who_to_contact,
        "ready_text": ready_text
    }

# =========================================================
# PROGRESSION
# =========================================================
max_steps = 4
current_step = min(st.session_state["step"], 4)
progress_map = {1: 0.25, 2: 0.50, 3: 0.75, 4: 1.0, 99: 1.0}
st.progress(progress_map.get(st.session_state["step"], 0.25))
st.caption(f"Étape {current_step} sur 4")

# =========================================================
# ACTIONS HAUTES
# =========================================================
top1, top2 = st.columns([5, 1])
with top2:
    if st.button("↺ Recommencer", use_container_width=True):
        reset_flow()
        st.rerun()

# =========================================================
# ETAPE 1 : PROFIL
# =========================================================
if st.session_state["step"] == 1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1. Qui êtes-vous ?")

    profile = st.radio(
        "Choisissez votre profil",
        ["Salarié", "Manager", "Document / accès"],
        index=None
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="kpi">👤 Salarié<br><span class="muted">Bulletin, mutuelle, transport, Arkevia…</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="kpi">🧑‍💼 Manager<br><span class="muted">Questions sur un collaborateur ou validation</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="kpi">📁 Accès / document<br><span class="muted">Coffre-fort, bulletins, portail</span></div>', unsafe_allow_html=True)

    if st.button("Continuer", type="primary", use_container_width=True):
        if profile:
            st.session_state["profile"] = profile
            st.session_state["step"] = 2
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ETAPE 2 : THEME
# =========================================================
elif st.session_state["step"] == 2:
    profile = st.session_state["profile"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2. Quel est le thème de votre demande ?")
    st.caption(f"Profil : {profile}")

    theme = st.radio(
        "Choisissez le thème",
        THEMES[profile],
        index=None
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            st.session_state["step"] = 1
            st.rerun()
    with col2:
        if st.button("Continuer", type="primary", use_container_width=True):
            if theme:
                st.session_state["theme"] = theme
                st.session_state["step"] = 3
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ETAPE 3 : SOUS-THEME
# =========================================================
elif st.session_state["step"] == 3:
    theme = st.session_state["theme"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("3. Quel est votre besoin précis ?")
    st.caption(f"Thème choisi : {theme}")

    subtheme = st.radio(
        "Choisissez le sujet",
        SUBTHEMES[theme],
        index=None
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            st.session_state["step"] = 2
            st.rerun()
    with col2:
        if st.button("Continuer", type="primary", use_container_width=True):
            if subtheme:
                st.session_state["subtheme"] = subtheme

                # Cas nécessitant une qualification supplémentaire
                need_qcm = (
                    (theme == "Ma paie / mon bulletin" and subtheme == "Mon salaire a baissé") or
                    (theme == "Ma paie / mon bulletin" and subtheme == "Il manque des heures") or
                    (theme == "Absence / congé" and subtheme == "Arrêt maladie")
                )

                if need_qcm:
                    st.session_state["step"] = 4
                else:
                    st.session_state["result"] = build_structured_answer(
                        st.session_state["profile"],
                        theme,
                        subtheme
                    )
                    st.session_state["step"] = 99
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ETAPE 4 : QUALIFICATION
# =========================================================
elif st.session_state["step"] == 4:
    theme = st.session_state["theme"]
    subtheme = st.session_state["subtheme"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("4. Quelques précisions pour mieux répondre")
    st.caption(f"Sujet : {theme} → {subtheme}")

    q1 = q2 = q3 = None

    if theme == "Ma paie / mon bulletin" and subtheme == "Mon salaire a baissé":
        q1 = st.radio(
            "La baisse de salaire fait-elle suite à une absence ?",
            [
                "Oui, après une absence maladie",
                "Oui, après une autre absence",
                "Non, sans absence",
            ],
            index=None
        )

    elif theme == "Ma paie / mon bulletin" and subtheme == "Il manque des heures":
        q1 = st.radio(
            "Quand les heures ont-elles été faites ou transmises ?",
            ["Avant le 15", "Après le 15", "Je ne sais pas"],
            index=None
        )
        if q1 == "Avant le 15":
            q2 = st.radio(
                "Le manager les a-t-il validées ?",
                ["Oui", "Non", "Je ne sais pas"],
                index=None
            )

    elif theme == "Absence / congé" and subtheme == "Arrêt maladie":
        q1 = st.radio(
            "Que voulez-vous comprendre ?",
            [
                "Comprendre la baisse de paie",
                "Comprendre la subrogation",
                "Avoir une explication générale",
            ],
            index=None
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            st.session_state["step"] = 3
            st.rerun()
    with col2:
        if st.button("Voir la réponse", type="primary", use_container_width=True):
            if q1:
                st.session_state["q1"] = q1
                st.session_state["q2"] = q2
                st.session_state["q3"] = q3
                st.session_state["result"] = build_structured_answer(
                    st.session_state["profile"],
                    theme,
                    subtheme,
                    q1=q1,
                    q2=q2,
                    q3=q3
                )
                st.session_state["step"] = 99
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ETAPE FINALE
# =========================================================
elif st.session_state["step"] == 99:
    result = st.session_state["result"]

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

    st.markdown("**Actions**")
    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("Nouvelle demande", use_container_width=True):
            reset_flow()
            st.rerun()
    with a2:
        if st.button("Revenir à l’étape précédente", use_container_width=True):
            theme = st.session_state["theme"]
            subtheme = st.session_state["subtheme"]

            if (
                (theme == "Ma paie / mon bulletin" and subtheme == "Mon salaire a baissé") or
                (theme == "Ma paie / mon bulletin" and subtheme == "Il manque des heures") or
                (theme == "Absence / congé" and subtheme == "Arrêt maladie")
            ):
                st.session_state["step"] = 4
            else:
                st.session_state["step"] = 3
            st.rerun()
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