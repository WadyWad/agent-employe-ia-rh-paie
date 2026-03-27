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
    max-width: 900px;
    padding-top: 1.4rem;
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
}
.hero p {
    margin: 6px 0 0 0;
    opacity: 0.95;
}
.section-card {
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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🤖 Agent Employé IA</h1>
  <p>Assistant RH / Paie guidé par parcours</p>
</div>
""", unsafe_allow_html=True)

# =========================
# ETAT SESSION
# =========================
defaults = {
    "step": 1,
    "theme": None,
    "subtheme": None,
    "q1": None,
    "q2": None,
    "final_answer": None
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def reset_flow():
    st.session_state["step"] = 1
    st.session_state["theme"] = None
    st.session_state["subtheme"] = None
    st.session_state["q1"] = None
    st.session_state["q2"] = None
    st.session_state["final_answer"] = None

# =========================
# LOGIQUE REPONSES
# =========================
def build_answer(theme, subtheme, q1=None, q2=None):
    topic = f"{theme} — {subtheme}"

    # 1) PAIE / BULLETIN
    if theme == "Ma paie / mon bulletin":
        if subtheme == "Mon salaire a baissé":
            if q1 == "Oui, après une absence maladie":
                return topic, """Une baisse de salaire peut s’expliquer par une absence maladie.

En pratique :
- l’absence est déduite du salaire ;
- la Sécurité sociale peut verser des indemnités journalières ;
- il peut y avoir 3 jours de carence, sauf exceptions ;
- selon votre ancienneté, un maintien de salaire ou un complément de prévoyance peut aussi s’appliquer.

Donc, une différence temporaire entre votre paie habituelle et votre paie du mois peut être normale après un arrêt maladie."""
            elif q1 == "Oui, après une autre absence":
                return topic, """Une baisse de salaire peut être liée à une absence non travaillée ou à une absence qui n’est pas intégralement rémunérée.

Le bon réflexe est de vérifier :
- le type d’absence posé ;
- la période concernée ;
- et la présence éventuelle d’une retenue sur le bulletin.

Si vous me décrivez l’absence, je peux vous aider à interpréter la situation."""
            elif q1 == "Non, sans absence":
                return topic, """Si votre salaire a baissé sans absence, les causes possibles sont souvent :
- une prime absente ou différente ;
- un acompte ;
- une régularisation ;
- une évolution de cotisations ;
- ou un élément variable non encore remonté en paie.

Je vous conseille de vérifier en priorité :
- si une prime attendue manque ;
- si vous avez demandé un acompte ;
- ou si un élément a été saisi tardivement."""
            else:
                return topic, """Un salaire en baisse peut venir d’une absence, d’une régularisation, d’un acompte, d’une variation de prime ou d’un élément variable non encore traité. Il faut d’abord vérifier si un événement particulier a eu lieu sur la période."""

        if subtheme == "Il manque des heures":
            if q1 == "Oui, avant le 15":
                if q2 == "Oui":
                    return topic, """Si les heures ont été faites avant le 15 et validées, elles peuvent en principe être intégrées sur la paie du mois, sous réserve que le circuit manager → RH → paie ait bien été respecté.

Si elles n’apparaissent toujours pas, il faut vérifier :
- si la transmission RH a bien été faite ;
- ou si un décalage exceptionnel a eu lieu."""
                elif q2 == "Non":
                    return topic, """Si le manager n’a pas encore validé les heures, elles ne peuvent pas être correctement transmises à la paie.

Le bon réflexe est donc de vérifier d’abord la validation manager."""
                else:
                    return topic, """Si les heures ont été faites avant le 15, elles peuvent être traitées sur la paie du mois, mais seulement si le circuit de validation a bien été respecté."""
            elif q1 == "Oui, après le 15":
                return topic, """Si les heures ont été faites ou transmises après le 15, elles sont généralement payées sur la paie du mois suivant.

Donc, si elles n’apparaissent pas encore sur le bulletin du mois en cours, ce n’est pas forcément un oubli : cela peut être un décalage normal vers M+1."""
            else:
                return topic, """Les heures supplémentaires ou complémentaires suivent un circuit de validation.

En général :
- si elles sont transmises avant le 15, elles peuvent être traitées sur la paie du mois ;
- si elles sont transmises après le 15, elles passent en paie M+1.

L’absence de ligne sur le bulletin ne signifie donc pas forcément un oubli."""
        if subtheme == "Il manque une prime":
            return topic, """Le service paie ne calcule pas lui-même les primes. Le montant est transmis par le service RH en lien avec le manager, puis appliqué tel qu’il est communiqué.

Si vous pensez qu’il y a une erreur, la première vérification doit porter sur le montant validé côté RH / management."""
        if subtheme == "Je pense qu’il y a une erreur":
            return topic, """Si vous pensez qu’il y a une erreur sur votre bulletin, le plus utile est de préciser :
- le mois concerné ;
- la ligne concernée ;
- et la différence constatée.

Cela permettra de distinguer :
- une vraie anomalie ;
- un décalage de traitement ;
- ou une régularisation normale."""
        if subtheme == "Je ne comprends pas une ligne":
            return topic, """Si vous ne comprenez pas une ligne de bulletin, le bon réflexe est d’identifier son type :
- absence / retenue ;
- prime ;
- cotisation ;
- acompte ;
- allocation ou remboursement.

Donnez le libellé exact de la ligne et le mois concerné, et vous pourrez obtenir une explication plus fiable."""

    # 2) ABSENCE
    if theme == "Absence / congé":
        if subtheme == "Arrêt maladie":
            if q1 == "Oui, je veux comprendre la baisse de paie":
                return topic, """En cas d’arrêt maladie, la baisse de paie peut être normale :
- l’absence est déduite ;
- la Sécurité sociale peut verser des IJSS ;
- 3 jours de carence peuvent s’appliquer, sauf exceptions ;
- un maintien de salaire ou un complément de prévoyance peut exister selon l’ancienneté.

Autrement dit, la paie employeur et les versements Sécurité sociale ne se superposent pas toujours de façon simple sur le même mois."""
            elif q1 == "Oui, je veux comprendre la subrogation":
                return topic, """La subrogation signifie que l’employeur continue de verser tout ou partie du salaire, et perçoit directement les indemnités journalières de la Sécurité sociale à votre place.

Concrètement, cela évite que vous ayez à gérer vous-même certains flux pendant l’arrêt."""
            else:
                return topic, """Un arrêt maladie entraîne en principe :
- une déduction d’absence ;
- d’éventuelles IJSS ;
- parfois 3 jours de carence ;
- et, selon l’ancienneté, un maintien ou un complément de rémunération."""
        if subtheme == "Enfant malade":
            return topic, """Les congés enfant malade sont calculés sur l’année civile, du 1er janvier au 31 décembre.

En résumé :
- 3 jours par an pour un enfant de moins de 16 ans ;
- 5 jours par an si l’enfant a moins d’1 an ou si vous avez 3 enfants de moins de 16 ans ;
- moins de 12 mois d’ancienneté : jours non payés ;
- plus de 12 mois d’ancienneté : jours payés."""
        if subtheme == "Décès":
            return topic, """En cas de décès, un justificatif est nécessaire et le livret de famille peut être demandé en plus de l’acte de décès pour prouver le lien de filiation.

Le nombre de jours dépend du lien familial. Ces jours sont à prendre dans un délai raisonnable, en principe dans le mois qui suit."""
        if subtheme == "Mariage / PACS":
            return topic, """Le mariage ou le PACS ouvre droit à une absence exceptionnelle sans condition d’ancienneté.

En pratique :
- salarié : 6 jours ouvrés consécutifs ;
- enfant du salarié : 1 jour ouvré.

Le congé peut être pris le jour de l’événement ou dans un délai raisonnable avant ou après."""
        if subtheme == "Jours de révision":
            return topic, """Pour les jours de révision :
- l’apprenti bénéficie de 5 jours ouvrés rémunérés supplémentaires dans le mois précédant les épreuves ;
- le salarié non apprenti peut bénéficier, sous conditions, de 3 jours ouvrables rémunérés pour un examen universitaire ou professionnel."""
        if subtheme == "Congés payés":
            return topic, """En principe, vous acquérez 25 jours ouvrés de congés légaux par an, auxquels peuvent s’ajouter 5 jours ouvrés mobiles conventionnels.

C’est ce qui explique que le bulletin puisse afficher 30 jours."""
        if subtheme == "Période de gel":
            return topic, """La période de gel correspond à la période pendant laquelle les demandes continuent d’être saisies, mais ne remontent plus immédiatement dans la paie.

Elle a lieu chaque mois entre le 20 et le 7 du mois suivant. Les demandes faites sur cette période sont prises en compte sur la période suivante."""

    # 3) MUTUELLE
    if theme == "Mutuelle":
        if subtheme == "La mutuelle est-elle obligatoire ?":
            return topic, """La mutuelle d’entreprise est en principe obligatoire, sauf cas de dispense prévus.

À l’embauche, l’affiliation est généralement faite par défaut, puis un mail permet de compléter le dossier."""
        if subtheme == "Je n’ai pas répondu au mail":
            return topic, """Vous avez en principe 2 mois pour finaliser votre affiliation. Passé ce délai, il faut vous rapprocher de votre chargé RH pour obtenir un nouveau lien d’affiliation."""
        if subtheme == "Je veux une dispense":
            return topic, """Une dispense de mutuelle peut être possible selon votre situation. La demande doit être faite avec les justificatifs attendus.

Si la demande de dispense est acceptée, elle peut devoir être renouvelée selon le type et la durée du contrat."""
        if subtheme == "Je vois une cotisation mutuelle":
            return topic, """La présence d’une cotisation mutuelle sur le bulletin est normale si vous êtes affilié à la mutuelle d’entreprise et qu’aucune dispense valide n’a été enregistrée.

En cas de transmission tardive d’une dispense, une régularisation peut intervenir, mais elle reste encadrée."""
    
    # 4) TRANSPORT
    if theme == "Transport":
        if subtheme == "Remboursement Navigo":
            return topic, """Le remboursement des frais de transport à hauteur de 50 % se demande sur Mon Portail Paie.

La demande doit comporter, en un seul fichier :
- une attestation sur l’honneur signée ;
- un justificatif de paiement ;
- une copie du pass Navigo."""
        if subtheme == "Quels justificatifs fournir ?":
            return topic, """Les 3 justificatifs attendus sont :
- une attestation sur l’honneur signée ;
- un justificatif de paiement ;
- une copie du pass Navigo.

Ils doivent être regroupés dans un seul fichier pour la demande."""
        if subtheme == "Ce qui n’est pas remboursé":
            return topic, """Ne sont pas pris en charge :
- le pass Navigo Liberté+ ;
- les tickets à l’unité ;
- les carnets.

Seuls les abonnements hebdomadaires, mensuels et annuels sont remboursés."""
    
    # 5) TICKETS RESTAURANT
    if theme == "Tickets restaurant":
        if subtheme == "Combien ai-je de tickets ?":
            return topic, """Vous avez droit à 1 ticket restaurant par journée travaillée, à condition que la journée corresponde à une amplitude minimale de 6 heures avec une pause d’au moins 30 minutes entre 12h00 et 14h00."""
        if subtheme == "Comment les déclarer ?":
            return topic, """La déclaration se fait sur Mon Portail Paie, via Mes demandes puis Mes éléments variables, avant le 20 de chaque mois."""
        if subtheme == "Je n’ai pas reçu ma carte":
            return topic, """Si la carte ticket restaurant n’a pas été reçue, il peut être nécessaire de contacter directement Edenred pour le suivi de la livraison, car certaines informations restent traitées directement avec eux."""
    
    # 6) TELETRAVAIL
    if theme == "Télétravail":
        if subtheme == "Pourquoi je n’ai pas la ligne ?":
            return topic, """Si la ligne d’allocation télétravail n’apparaît pas, c’est souvent qu’un document manque ou n’a pas encore été transmis à la paie.

Les éléments attendus sont en général :
- un avenant signé ;
- une attestation d’assurance habitation en cours de validité."""
        if subtheme == "Quels documents faut-il ?":
            return topic, """Pour bénéficier de l’allocation télétravail, il faut :
- un avenant télétravail signé ;
- une attestation d’assurance habitation valide.

L’assurance doit être fournie chaque année."""
    
    # 7) ARKEVIA
    if theme == "Arkevia / bulletins":
        if subtheme == "Activer mon coffre-fort":
            return topic, """Pour activer Arkevia :
1. accédez au coffre-fort via OneLogin ou myarkevia.com ;
2. cliquez sur “Je m’inscris” ;
3. renseignez votre matricule et votre code secret ;
4. renseignez votre nom, prénom et votre adresse email personnelle ;
5. choisissez votre mot de passe et validez.

L’adresse email personnelle est importante car elle permet de conserver l’accès pendant 50 ans."""
        if subtheme == "Me connecter":
            return topic, """Pour vous connecter à Arkevia :
- utilisez votre adresse email personnelle renseignée lors de l’activation ;
- puis votre mot de passe choisi lors de l’inscription.

En cas d’oubli, utilisez “Mot de passe oublié ?”."""
        if subtheme == "Importer mes anciens bulletins":
            return topic, """Vous pouvez télécharger vos anciens bulletins depuis PeopleDoc puis les déposer dans Arkevia via “Déposer un document”. Vous pouvez aussi créer des dossiers pour mieux les classer."""
    
    # 8) PORTAIL PAIE
    if theme == "Mon Portail Paie":
        if subtheme == "Période de gel":
            return topic, """La période de gel correspond à l’absence d’échange entre le portail et le logiciel de paie.

Elle a lieu chaque mois entre le 20 et le 7 du mois suivant. Les demandes peuvent continuer à être saisies, mais elles ne remontent pas immédiatement en paie."""
        if subtheme == "Acompte via portail":
            return topic, """Les demandes d’acompte doivent être effectuées via Mon Portail Paie. Les modalités et limites apparaissent directement sur le portail."""
        if subtheme == "Prise de contrôle / aide":
            return topic, """Le gestionnaire paie peut prendre le contrôle du portail d’un salarié de son périmètre afin de l’accompagner sur ses démarches si nécessaire."""
        if subtheme == "Demande non remontée":
            return topic, """Une demande peut ne pas remonter pour plusieurs raisons :
- période de gel ;
- validation incomplète ;
- délai de traitement normal ;
- ou demande saisie hors fenêtre attendue selon le type d’élément."""

    return topic, """Je n’ai pas trouvé de réponse assez précise avec ce parcours. Reformulez le besoin ou revenez au menu principal."""

# =========================
# BOUTON RESET
# =========================
col_reset_1, col_reset_2 = st.columns([5, 1])
with col_reset_2:
    if st.button("↺ Recommencer"):
        reset_flow()
        st.rerun()

# =========================
# ETAPE 1 : THEME
# =========================
if st.session_state["step"] == 1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("1. Votre demande concerne quoi ?")

    theme = st.radio(
        "Choisissez le thème principal",
        [
            "Ma paie / mon bulletin",
            "Absence / congé",
            "Mutuelle",
            "Transport",
            "Tickets restaurant",
            "Télétravail",
            "Arkevia / bulletins",
            "Mon Portail Paie",
        ],
        index=None
    )

    if st.button("Continuer", type="primary", use_container_width=True):
        if theme:
            st.session_state["theme"] = theme
            st.session_state["step"] = 2
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ETAPE 2 : SOUS-THEME
# =========================
elif st.session_state["step"] == 2:
    theme = st.session_state["theme"]

    mapping = {
        "Ma paie / mon bulletin": [
            "Mon salaire a baissé",
            "Il manque des heures",
            "Il manque une prime",
            "Je pense qu’il y a une erreur",
            "Je ne comprends pas une ligne",
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
            "Prise de contrôle / aide",
            "Demande non remontée",
        ]
    }

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("2. Quel est votre besoin précis ?")
    st.caption(f"Thème choisi : {theme}")

    subtheme = st.radio(
        "Choisissez le sujet",
        mapping[theme],
        index=None
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            st.session_state["step"] = 1
            st.rerun()
    with col2:
        if st.button("Continuer", type="primary", use_container_width=True):
            if subtheme:
                st.session_state["subtheme"] = subtheme

                if theme == "Ma paie / mon bulletin" and subtheme == "Mon salaire a baissé":
                    st.session_state["step"] = 3
                elif theme == "Ma paie / mon bulletin" and subtheme == "Il manque des heures":
                    st.session_state["step"] = 4
                elif theme == "Absence / congé" and subtheme == "Arrêt maladie":
                    st.session_state["step"] = 5
                else:
                    topic, answer = build_answer(theme, subtheme)
                    st.session_state["final_answer"] = {"topic": topic, "answer": answer}
                    st.session_state["step"] = 99
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ETAPE 3 : QCM salaire en baisse
# =========================
elif st.session_state["step"] == 3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("3. Pour mieux répondre")
    q1 = st.radio(
        "La baisse de salaire fait-elle suite à une absence ?",
        [
            "Oui, après une absence maladie",
            "Oui, après une autre absence",
            "Non, sans absence",
        ],
        index=None
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            st.session_state["step"] = 2
            st.rerun()
    with col2:
        if st.button("Voir la réponse", type="primary", use_container_width=True):
            if q1:
                st.session_state["q1"] = q1
                topic, answer = build_answer(
                    st.session_state["theme"],
                    st.session_state["subtheme"],
                    q1=q1
                )
                st.session_state["final_answer"] = {"topic": topic, "answer": answer}
                st.session_state["step"] = 99
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ETAPE 4 : QCM heures
# =========================
elif st.session_state["step"] == 4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("3. Pour mieux répondre")

    q1 = st.radio(
        "Quand les heures ont-elles été faites ou transmises ?",
        [
            "Oui, avant le 15",
            "Oui, après le 15",
            "Je ne sais pas",
        ],
        index=None
    )

    q2 = None
    if q1 == "Oui, avant le 15":
        q2 = st.radio(
            "Le manager les a-t-il validées ?",
            ["Oui", "Non", "Je ne sais pas"],
            index=None
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            st.session_state["step"] = 2
            st.rerun()
    with col2:
        if st.button("Voir la réponse", type="primary", use_container_width=True):
            if q1:
                st.session_state["q1"] = q1
                st.session_state["q2"] = q2
                topic, answer = build_answer(
                    st.session_state["theme"],
                    st.session_state["subtheme"],
                    q1=q1,
                    q2=q2
                )
                st.session_state["final_answer"] = {"topic": topic, "answer": answer}
                st.session_state["step"] = 99
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ETAPE 5 : QCM arrêt maladie
# =========================
elif st.session_state["step"] == 5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("3. Pour mieux répondre")

    q1 = st.radio(
        "Que souhaitez-vous comprendre ?",
        [
            "Oui, je veux comprendre la baisse de paie",
            "Oui, je veux comprendre la subrogation",
            "Je veux une explication générale",
        ],
        index=None
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retour", use_container_width=True):
            st.session_state["step"] = 2
            st.rerun()
    with col2:
        if st.button("Voir la réponse", type="primary", use_container_width=True):
            if q1:
                st.session_state["q1"] = q1
                topic, answer = build_answer(
                    st.session_state["theme"],
                    st.session_state["subtheme"],
                    q1=q1
                )
                st.session_state["final_answer"] = {"topic": topic, "answer": answer}
                st.session_state["step"] = 99
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ETAPE FINALE
# =========================
elif st.session_state["step"] == 99:
    data = st.session_state["final_answer"]

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Réponse")
    st.markdown(f'<div class="topic-tag">{data["topic"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="answer-card">{data["answer"]}</div>', unsafe_allow_html=True)

    st.markdown("**Vous pouvez maintenant :**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Poser une autre question", use_container_width=True):
            reset_flow()
            st.rerun()
    with col2:
        if st.button("Revenir à l’étape précédente", use_container_width=True):
            theme = st.session_state["theme"]
            subtheme = st.session_state["subtheme"]

            if theme == "Ma paie / mon bulletin" and subtheme == "Mon salaire a baissé":
                st.session_state["step"] = 3
            elif theme == "Ma paie / mon bulletin" and subtheme == "Il manque des heures":
                st.session_state["step"] = 4
            elif theme == "Absence / congé" and subtheme == "Arrêt maladie":
                st.session_state["step"] = 5
            else:
                st.session_state["step"] = 2
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# BAS DE PAGE
# =========================
st.markdown(
    '<p class="small-muted">Astuce : ce parcours est volontairement guidé pour éviter les réponses à côté et mieux orienter la problématique.</p>',
    unsafe_allow_html=True
)