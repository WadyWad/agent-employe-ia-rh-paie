PAYROLL_AGENT_MASTER_BLOCK = {
    "VERSION": "2026-03-27",
    "DESCRIPTION": "Base métier consolidée pour un agent guide RH/Paie",
    "GLOBAL_RULES": {
        "always_ask_first": [
            "Quelle est la convention collective applicable ?",
            "Quel est le statut du salarié ?",
            "Quelle est l’ancienneté ?",
            "Quel est le type de contrat ?",
            "Quel est le mode d’organisation du temps de travail ?"
        ],
        "safety_rules": [
            "Ne jamais donner un minimum conventionnel chiffré sans vérifier la grille applicable.",
            "Toujours distinguer paie employeur, IJSS, prévoyance et régularisation.",
            "Toujours signaler quand une vérification RH/paie reste nécessaire."
        ],
        "response_format": [
            "Ce que cela signifie",
            "Pourquoi cela arrive",
            "Ce que vous devez faire",
            "Qui contacter si besoin"
        ]
    },

    "INTERNAL_FAQ": {
        "MALADIE": {
            "keywords": ["maladie", "arrêt maladie", "ijss", "carence", "subrogation"],
            "answer": {
                "ce_que_cela_signifie": "Une absence maladie entraîne une déduction de salaire sur la paie employeur.",
                "pourquoi": "L’absence maladie est décomptée en jours calendaires. La Sécurité sociale peut verser des IJSS, avec en principe 3 jours de carence sauf exceptions. La subrogation signifie que l’employeur peut percevoir les IJSS à la place du salarié.",
                "a_faire": [
                    "Vérifier la nature exacte de l’arrêt.",
                    "Vérifier l’ancienneté.",
                    "Vérifier si les IJSS ont été versées au salarié ou à l’employeur."
                ],
                "contact": "Service paie / RH"
            }
        },

        "MUTUELLE": {
            "keywords": ["mutuelle", "dispense", "affiliation"],
            "answer": {
                "ce_que_cela_signifie": "La mutuelle est en principe obligatoire, sauf cas de dispense.",
                "pourquoi": "Le salarié est affilié par défaut à l’embauche puis reçoit un mail pour finaliser son affiliation. Une régularisation peut intervenir si les informations arrivent tardivement.",
                "a_faire": [
                    "Vérifier si le salarié est dans le délai.",
                    "Identifier si la demande porte sur l’affiliation ou la dispense.",
                    "Vérifier la présence d’un justificatif de dispense."
                ],
                "contact": "Chargé RH / partenaire mutuelle"
            }
        },

        "ACOMPTE": {
            "keywords": ["acompte", "avance", "avance sur salaire"],
            "answer": {
                "ce_que_cela_signifie": "Aucune avance sur salaire n’est accordée ; seul l’acompte est possible.",
                "pourquoi": "Un acompte est possible à condition que les heures correspondant au montant demandé aient déjà été réalisées.",
                "a_faire": [
                    "Vérifier que les heures ont bien été réalisées.",
                    "Vérifier la fenêtre de saisie sur le portail."
                ],
                "contact": "Paie"
            }
        },

        "HEURES": {
            "keywords": ["heures supplémentaires", "heures complémentaires", "relevé d'heures", "heures excédentaires"],
            "answer": {
                "ce_que_cela_signifie": "Des heures absentes du bulletin ne signifient pas forcément un oubli.",
                "pourquoi": "Les heures remontent via le circuit manager → RH → paie. Si elles sont transmises tardivement, elles peuvent être payées le mois suivant.",
                "a_faire": [
                    "Vérifier la date de réalisation des heures.",
                    "Vérifier la validation manager.",
                    "Vérifier la transmission RH."
                ],
                "contact": "Manager / RH / paie"
            }
        },

        "TRANSPORT": {
            "keywords": ["transport", "navigo", "remboursement transport", "ratp"],
            "answer": {
                "ce_que_cela_signifie": "Le remboursement transport à 50 % suppose un dossier complet.",
                "pourquoi": "Il faut une attestation sur l’honneur signée, un justificatif de paiement et une copie du pass Navigo, dans un seul fichier.",
                "a_faire": [
                    "Vérifier le type d’abonnement.",
                    "Vérifier les 3 pièces justificatives.",
                    "Vérifier la demande sur le portail."
                ],
                "contact": "Paie / contact paie"
            }
        },

        "TICKETS_RESTAURANT": {
            "keywords": ["tickets restaurant", "edenred", "tr", "ticket resto"],
            "answer": {
                "ce_que_cela_signifie": "Le droit aux tickets restaurant dépend des journées réellement éligibles et d’une déclaration dans les délais.",
                "pourquoi": "Un ticket est dû par journée travaillée d’au moins 6 heures avec une pause d’au moins 30 minutes entre 12h00 et 14h00.",
                "a_faire": [
                    "Vérifier les journées éligibles.",
                    "Vérifier la déclaration.",
                    "Si la carte manque, orienter vers Edenred."
                ],
                "contact": "Paie / Edenred"
            }
        },

        "TELETRAVAIL": {
            "keywords": ["télétravail", "teletravail", "allocation télétravail", "assurance habitation"],
            "answer": {
                "ce_que_cela_signifie": "L’allocation télétravail n’est pas automatique.",
                "pourquoi": "Il faut un avenant signé et une attestation d’assurance habitation valide, renouvelée chaque année.",
                "a_faire": [
                    "Contrôler l’avenant.",
                    "Contrôler l’attestation d’assurance.",
                    "Vérifier la transmission RH → paie."
                ],
                "contact": "RH / paie"
            }
        },

        "PERIODE_DE_GEL": {
            "keywords": ["gel", "période de gel", "20 au 7", "clôture paie", "ne remonte pas"],
            "answer": {
                "ce_que_cela_signifie": "Une demande peut être correctement saisie mais non visible immédiatement en paie.",
                "pourquoi": "Entre le 20 et le 7 du mois suivant, les demandes peuvent continuer à être saisies, mais ne remontent pas en paie avant la fin de la période de gel.",
                "a_faire": [
                    "Vérifier la date de saisie.",
                    "Vérifier si la demande est entièrement validée.",
                    "Attendre la prochaine fenêtre de remontée si besoin."
                ],
                "contact": "Paie / manager / contact paie"
            }
        },

        "ARKEVIA": {
            "keywords": ["arkevia", "coffre-fort", "bulletins", "mot de passe oublié", "peopledoc"],
            "answer": {
                "ce_que_cela_signifie": "Arkevia est le coffre-fort électronique qui remplace l’ancien système.",
                "pourquoi": "L’activation se fait via OneLogin ou myarkevia.com avec matricule, code secret et email personnel.",
                "a_faire": [
                    "Vérifier si le besoin porte sur activation, connexion ou import.",
                    "Récupérer matricule / code secret si besoin.",
                    "Vérifier l’email personnel utilisé."
                ],
                "contact": "Paie / support Arkevia"
            }
        }
    },

    "CCN": {
        "IDCC_2691": {
            "nom": "Enseignement privé indépendant",
            "notions": [
                {"theme": "Minima conventionnels", "reponse": "Toujours vérifier la grille et l’annexe applicables."},
                {"theme": "Prime grands effectifs", "reponse": "Prime pour certaines classes/groupes de plus de 40."},
                {"theme": "Maladie", "reponse": "IJSS, carence, maintien selon ancienneté."},
                {"theme": "Licenciement", "reponse": "Indemnité conventionnelle : 1/4 puis 1/3."}
            ]
        },

        "IDCC_1516": {
            "nom": "Organismes de formation",
            "notions": [
                {"theme": "Minima conventionnels", "reponse": "Comparer minimum conventionnel et SMIC."},
                {"theme": "Temps partiel", "reponse": "Droits équivalents proratisés."},
                {"theme": "Heures complémentaires", "reponse": "Au-delà de l’horaire contractuel avec majoration selon seuils."},
                {"theme": "Préavis", "reponse": "1 à 3 mois selon statut et ancienneté."}
            ]
        },

        "IDCC_1486": {
            "nom": "Syntec / BETIC",
            "notions": [
                {"theme": "Classification", "reponse": "ETAM ou ingénieurs/cadres, position et coefficient."},
                {"theme": "Minima conventionnels", "reponse": "Toujours vérifier grille, position et coefficient."},
                {"theme": "Forfait jours", "reponse": "Raisonnement en jours et non en heures."},
                {"theme": "Prime de vacances", "reponse": "Prime conventionnelle obligatoire dans la branche."}
            ]
        }
    },

    "ROUTING_RULES": [
        {"if_contains": ["arkevia", "coffre-fort", "mot de passe oublié"], "route_to": "INTERNAL_FAQ.ARKEVIA"},
        {"if_contains": ["gel", "20 au 7", "ne remonte pas"], "route_to": "INTERNAL_FAQ.PERIODE_DE_GEL"},
        {"if_contains": ["acompte", "avance"], "route_to": "INTERNAL_FAQ.ACOMPTE"},
        {"if_contains": ["navigo", "transport", "ratp"], "route_to": "INTERNAL_FAQ.TRANSPORT"},
        {"if_contains": ["ticket restaurant", "edenred", "tr"], "route_to": "INTERNAL_FAQ.TICKETS_RESTAURANT"},
        {"if_contains": ["télétravail", "teletravail", "assurance habitation"], "route_to": "INTERNAL_FAQ.TELETRAVAIL"},
        {"if_contains": ["mutuelle", "dispense", "affiliation"], "route_to": "INTERNAL_FAQ.MUTUELLE"},
        {"if_contains": ["heures", "relevé d'heures", "heures excédentaires"], "route_to": "INTERNAL_FAQ.HEURES"},
        {"if_contains": ["maladie", "ijss", "subrogation", "carence"], "route_to": "INTERNAL_FAQ.MALADIE"}
    ]
}