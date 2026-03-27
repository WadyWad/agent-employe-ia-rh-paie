PAYROLL_AGENT_MASTER_BLOCK = {
    "VERSION": "2026-03-27",
    "DESCRIPTION": "Base métier consolidée pour un agent guide RH/Paie orienté FAQ + conventions collectives + portail paie",

    # =========================================================
    # 1) REGLES GLOBALES DE L'AGENT
    # =========================================================
    "GLOBAL_RULES": {
        "always_ask_first": [
            "Quelle est la convention collective applicable ?",
            "Quel est le statut du salarié ? (cadre / non cadre / ETAM / enseignant / formateur / autre)",
            "Quelle est l’ancienneté ?",
            "Quel est le type de contrat ? (CDI / CDD / alternance / autre)",
            "Quel est le mode d’organisation du temps de travail ? (35h / temps partiel / forfait jours / annualisation / autre)"
        ],
        "safety_rules": [
            "Ne jamais donner un minimum conventionnel chiffré sans vérifier la grille et la catégorie applicables.",
            "Ne jamais trancher une question de maintien de salaire sans vérifier ancienneté, origine de l’arrêt et statut.",
            "Toujours distinguer paie employeur, IJSS, prévoyance et régularisation.",
            "Toujours distinguer temps partiel, heures complémentaires, heures supplémentaires, forfait jours et récupération.",
            "Toujours signaler quand une vérification RH/paie reste nécessaire."
        ],
        "response_format": [
            "Ce que cela signifie",
            "Pourquoi cela arrive",
            "Ce que vous devez faire",
            "Qui contacter si besoin"
        ]
    },

    # =========================================================
    # 2) BASE FAQ / PROCESS INTERNES
    # =========================================================
    "INTERNAL_FAQ": {
        "themes": {
            "MALADIE": {
                "keywords": ["maladie", "arrêt maladie", "ijss", "carence", "subrogation", "maintien", "prévenance"],
                "qualification_questions": [
                    "S’agit-il d’un arrêt maladie simple ou d’un accident du travail / maladie professionnelle ?",
                    "Le salarié a-t-il plus ou moins de 12 mois d’ancienneté ?",
                    "La question porte-t-elle sur la baisse de paie, les IJSS, la subrogation ou le maintien ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Une absence maladie entraîne une déduction de salaire sur la paie employeur.",
                    "pourquoi": "L’absence maladie est décomptée en jours calendaires. La Sécurité sociale peut verser des IJSS, généralement avec 3 jours de carence sauf cas particuliers. Dans ta FAQ interne, la prévoyance complète à hauteur de 80 % du brut une fois les IJSS déduites. La subrogation signifie que l’employeur peut percevoir les IJSS à la place du salarié. L’accident du travail doit être déclaré dans les 48 heures.",
                    "a_faire": [
                        "Vérifier la nature exacte de l’arrêt.",
                        "Vérifier l’ancienneté.",
                        "Vérifier si les IJSS ont été versées au salarié ou à l’employeur.",
                        "Vérifier si la prévoyance est intervenue."
                    ],
                    "contact": "Service paie / RH"
                }
            },

            "ENFANT_MALADE": {
                "keywords": ["enfant malade", "congé enfant malade", "jours enfant malade"],
                "qualification_questions": [
                    "L’enfant a-t-il moins de 16 ans ?",
                    "L’enfant a-t-il moins d’1 an ?",
                    "Le salarié a-t-il plus ou moins de 12 mois d’ancienneté ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Les jours enfant malade suivent l’année civile, pas la logique 1er juin / 31 mai.",
                    "pourquoi": "Dans ta FAQ, le compteur est calculé du 1er janvier au 31 décembre. Il est de 3 jours par an pour un enfant de moins de 16 ans, et 5 jours si l’enfant a moins d’1 an ou si le salarié a 3 enfants de moins de 16 ans. Avec moins de 12 mois d’ancienneté, les jours sont non payés ; avec plus de 12 mois, ils sont payés.",
                    "a_faire": [
                        "Vérifier l’âge de l’enfant.",
                        "Vérifier l’ancienneté.",
                        "Vérifier si le compteur annuel est épuisé."
                    ],
                    "contact": "RH / paie"
                }
            },

            "JOUR_DECES": {
                "keywords": ["décès", "acte de décès", "livret de famille", "jour décès"],
                "qualification_questions": [
                    "Quel est le lien de parenté ?",
                    "Le salarié dispose-t-il des justificatifs ?",
                    "La demande est-elle faite dans un délai raisonnable après l’événement ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Le nombre de jours dépend du lien familial ; le livret de famille peut être demandé en plus de l’acte de décès.",
                    "pourquoi": "La preuve de filiation sert à déterminer le nombre de jours auquel le salarié a droit. Dans ta FAQ, les jours doivent être pris dans un délai raisonnable, en pratique dans le mois qui suit.",
                    "a_faire": [
                        "Identifier le lien de parenté exact.",
                        "Contrôler les justificatifs.",
                        "Vérifier la période de prise."
                    ],
                    "contact": "RH / paie"
                }
            },

            "MARIAGE_PACS": {
                "keywords": ["mariage", "pacs", "congé mariage", "congé pacs"],
                "qualification_questions": [
                    "L’événement concerne-t-il le salarié ou son enfant ?",
                    "Le salarié a-t-il fourni le justificatif ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Le droit existe sans condition d’ancienneté.",
                    "pourquoi": "Dans ta FAQ, le salarié a droit à 6 jours ouvrés consécutifs pour son mariage/PACS, et 1 jour pour celui de son enfant. Le congé peut être pris le jour de l’événement ou dans un délai raisonnable autour de celui-ci.",
                    "a_faire": [
                        "Vérifier le justificatif.",
                        "Vérifier si la demande concerne le salarié ou son enfant."
                    ],
                    "contact": "RH"
                }
            },

            "JOURS_REVISION": {
                "keywords": ["révision", "examen", "apprenti", "congé examen"],
                "qualification_questions": [
                    "Le salarié est-il apprenti ?",
                    "Dispose-t-il d’une convocation ?",
                    "Quelle est son ancienneté ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Les droits diffèrent entre apprenti et salarié hors apprentissage.",
                    "pourquoi": "Dans ta FAQ, l’apprenti bénéficie de 5 jours ouvrés rémunérés supplémentaires. Hors apprentissage, le salarié peut bénéficier de 3 jours ouvrables rémunérés s’il justifie d’une convocation et d’une ancienneté minimale de 3 ans.",
                    "a_faire": [
                        "Vérifier le statut apprentissage.",
                        "Contrôler la convocation.",
                        "Contrôler l’ancienneté."
                    ],
                    "contact": "RH"
                }
            },

            "CP_ET_JOUR_EXCEPTIONNEL": {
                "keywords": ["cp", "congés payés", "cp acquis", "cp en cours", "jour exceptionnel", "31e jour"],
                "qualification_questions": [
                    "La question porte-t-elle sur le compteur CP ou sur le jour exceptionnel ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Le bulletin peut afficher 30 jours car il regroupe 25 jours de congés légaux et 5 jours de congés mobiles.",
                    "pourquoi": "Ta FAQ précise que les CP acquis correspondent aux congés déjà acquis N-1/N et les CP en cours à la période N/N+1. Le jour exceptionnel apparaît comme une ligne distincte et se consomme après épuisement du compteur N-1/N.",
                    "a_faire": [
                        "Vérifier si le compteur N-1/N est épuisé.",
                        "Distinguer CP acquis, CP en cours et jour exceptionnel."
                    ],
                    "contact": "Paie / RH"
                }
            },

            "MUTUELLE": {
                "keywords": ["mutuelle", "dispense", "affiliation", "complémentaire santé"],
                "qualification_questions": [
                    "Le salarié a-t-il reçu le mail d’affiliation ?",
                    "Veut-il s’affilier, changer d’option ou demander une dispense ?",
                    "Est-il dans le délai de 2 mois ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "La mutuelle est en principe obligatoire, sauf cas de dispense.",
                    "pourquoi": "Tes réponses automatiques précisent que le salarié est affilié par défaut à l’embauche, qu’il reçoit un mail environ 15 à 20 jours après sa prise de poste, qu’il dispose de 2 mois pour finaliser son affiliation, et que la dispense peut devoir être renouvelée. Une régularisation positive ou négative est possible si le partenaire transmet tardivement les informations.",
                    "a_faire": [
                        "Vérifier si le salarié est dans le délai.",
                        "Identifier si la demande porte sur l’affiliation ou la dispense.",
                        "Vérifier la présence d’un justificatif de dispense."
                    ],
                    "contact": "Chargé RH / partenaire mutuelle"
                }
            },

            "ACOMPTE_AVANCE": {
                "keywords": ["acompte", "avance", "avance sur salaire"],
                "qualification_questions": [
                    "Le salarié demande-t-il un acompte ou une avance ?",
                    "La demande a-t-elle été faite dans la bonne fenêtre ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Aucune avance sur salaire n’est accordée ; seul l’acompte est possible.",
                    "pourquoi": "Ta FAQ précise qu’un acompte est possible à condition que les heures correspondant au montant demandé aient déjà été réalisées. Le guide portail paie ajoute que la saisie d’une demande d’acompte est possible uniquement sur le mois en cours entre le 1er et le 11.",
                    "a_faire": [
                        "Vérifier que les heures ont bien été réalisées.",
                        "Vérifier la fenêtre de saisie sur le portail."
                    ],
                    "contact": "Paie"
                }
            },

            "HEURES_SUP_ET_COMPLEMENTAIRES": {
                "keywords": ["heures supplémentaires", "heures complémentaires", "relevé d'heures", "heures excédentaires"],
                "qualification_questions": [
                    "Les heures ont-elles été faites avant ou après le 15 ?",
                    "Le manager a-t-il validé ?",
                    "Le service RH les a-t-il bien transmises à la paie ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Des heures absentes du bulletin ne signifient pas forcément un oubli.",
                    "pourquoi": "Dans tes FAQ, les heures remontent via le circuit manager → RH → paie, avec une logique 15/15. Le guide Portail Paie mentionne aussi une fenêtre de saisie des heures excédentaires dans les 8 semaines passées, et indique que les éléments ne remontent que lorsqu’ils ont été entièrement validés.",
                    "a_faire": [
                        "Vérifier la date de réalisation des heures.",
                        "Vérifier la validation manager.",
                        "Vérifier la transmission RH."
                    ],
                    "contact": "Manager / RH / paie"
                }
            },

            "PRIMES": {
                "keywords": ["prime", "primes", "prime objectif", "bonus"],
                "qualification_questions": [
                    "La question porte-t-elle sur le montant ou sur l’absence de la prime ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Le service paie n’effectue pas le calcul métier de la prime.",
                    "pourquoi": "Tes FAQ précisent que le montant est transmis à la paie par le RH en lien avec le manager, puis appliqué tel quel.",
                    "a_faire": [
                        "Vérifier le montant validé côté management / RH.",
                        "Comparer avec l’information transmise à la paie."
                    ],
                    "contact": "Manager / RH"
                }
            },

            "TELETRAVAIL": {
                "keywords": ["télétravail", "allocation télétravail", "20€", "assurance habitation", "avenant"],
                "qualification_questions": [
                    "L’avenant télétravail est-il signé ?",
                    "L’attestation d’assurance habitation a-t-elle été fournie ?",
                    "L’assurance est-elle à jour pour l’année ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "L’allocation télétravail n’est pas automatique.",
                    "pourquoi": "Tes FAQ indiquent qu’il faut un avenant signé et une attestation d’assurance habitation valide, avec renouvellement annuel de l’assurance.",
                    "a_faire": [
                        "Contrôler l’avenant.",
                        "Contrôler l’attestation d’assurance.",
                        "Vérifier la transmission RH → paie."
                    ],
                    "contact": "RH / paie"
                }
            },

            "TRANSPORT": {
                "keywords": ["transport", "navigo", "pass navigo", "remboursement transport", "RATP"],
                "qualification_questions": [
                    "La demande a-t-elle été faite via Mon Portail Paie ?",
                    "Les 3 justificatifs sont-ils réunis en un seul fichier ?",
                    "Le titre est-il éligible ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Le remboursement transport à 50 % suppose un dossier complet.",
                    "pourquoi": "Tes réponses automatiques précisent qu’il faut une attestation sur l’honneur signée, un justificatif de paiement et une copie du pass Navigo, dans un seul fichier. Seuls les abonnements hebdomadaires, mensuels et annuels sont pris en charge ; le Navigo Liberté+ et les tickets unitaires ne le sont pas.",
                    "a_faire": [
                        "Vérifier le type d’abonnement.",
                        "Vérifier les 3 pièces justificatives.",
                        "Vérifier la demande sur le portail."
                    ],
                    "contact": "Paie / contact paie"
                }
            },

            "TICKETS_RESTAURANT": {
                "keywords": ["tickets restaurant", "edenred", "carte tr", "TR", "ticket resto"],
                "qualification_questions": [
                    "La déclaration a-t-elle été faite avant le 20 ?",
                    "Les journées atteignent-elles au moins 6 heures avec pause entre 12h et 14h ?",
                    "La question porte-t-elle sur le nombre de tickets ou sur la carte ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Le droit aux tickets restaurant dépend des journées réellement éligibles et d’une déclaration dans les délais.",
                    "pourquoi": "Tes réponses automatiques indiquent qu’un ticket est dû par journée travaillée d’au moins 6 heures avec une pause d’au moins 30 minutes entre 12h et 14h, à déclarer avant le 20 du mois sur Mon Portail Paie. Pour la carte, le suivi peut relever directement d’Edenred.",
                    "a_faire": [
                        "Vérifier les journées éligibles.",
                        "Vérifier la déclaration.",
                        "Si la carte manque, orienter vers Edenred."
                    ],
                    "contact": "Paie / Edenred"
                }
            },

            "PERIODE_DE_GEL": {
                "keywords": ["gel", "période de gel", "20 au 7", "ne remonte pas", "clôture paie"],
                "qualification_questions": [
                    "La demande a-t-elle été saisie entre le 20 et le 7 ?",
                    "Le workflow est-il totalement validé ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Une demande peut être correctement saisie mais non visible immédiatement en paie.",
                    "pourquoi": "Tes réponses automatiques et le guide gestionnaire paie indiquent qu’entre le 20 et le 7 du mois suivant, les demandes peuvent continuer à être saisies et validées, mais ne remontent pas en paie avant la fin de la période de gel. Elles remonteront ensuite, le guide mentionnant une remontée le 8 du mois suivant dans TeamsRH.",
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
                "qualification_questions": [
                    "La demande porte-t-elle sur l’activation, la connexion ou l’import d’anciens bulletins ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Arkevia est le coffre-fort électronique qui remplace l’ancien système.",
                    "pourquoi": "Ton guide Arkevia indique une activation en 3 étapes via OneLogin ou myarkevia.com, avec matricule, code secret, puis email personnel permettant de conserver l’accès 50 ans. Le mot de passe oublié se réinitialise via l’email personnel. Les anciens bulletins peuvent être importés depuis PeopleDoc.",
                    "a_faire": [
                        "Vérifier si le besoin porte sur activation, connexion ou import.",
                        "Récupérer matricule / code secret si besoin.",
                        "Vérifier l’email personnel utilisé."
                    ],
                    "contact": "Paie / support Arkevia"
                }
            },

            "PORTAIL_PAIE_WORKFLOW": {
                "keywords": ["mon portail paie", "workflow", "validation", "prise de contrôle", "forfait jours", "JPO"],
                "qualification_questions": [
                    "La demande concerne-t-elle une validation, une non-remontée ou un besoin d’accompagnement ?"
                ],
                "answer": {
                    "ce_que_cela_signifie": "Le Portail Paie suit des workflows précis selon le type de demande.",
                    "pourquoi": "Ton guide gestionnaire paie indique que certaines demandes sont validées par le manager, d’autres par le contact paie, et qu’elles ne remontent dans les dossiers que lorsqu’elles sont entièrement validées. Il précise aussi les limites de saisie dans le passé, la prise de contrôle d’un salarié, le caractère déclaratif du forfait jours, et le fonctionnement des JPO payées ou récupérées avec rubriques RECHA / RECJA / JPODH / JPOSH / JPODJ / JPOSJ.",
                    "a_faire": [
                        "Identifier le type de demande.",
                        "Contrôler le statut du workflow.",
                        "Contrôler la fenêtre de saisie.",
                        "Contrôler les règles de remontée."
                    ],
                    "contact": "Contact paie / manager / paie"
                }
            }
        }
    },

    # =========================================================
    # 3) CONVENTIONS COLLECTIVES
    # =========================================================
    "CCN": {
        "IDCC_2691": {
            "nom": "Enseignement privé indépendant",
            "summary": [
                "Convention collective de l’enseignement privé indépendant.",
                "Avenant n°69 du 13 juin 2025 étendu par arrêté du 6 février 2026.",
                "Revalorisation des grilles de rémunération de 1,8 %."
            ],
            "smart_questions": [
                "Le salarié est-il enseignant ou non enseignant ?",
                "Quel est son niveau / annexe / catégorie ?",
                "Quelle est son ancienneté ?",
                "Est-il en temps plein, temps partiel ou forfait ?"
            ],
            "notions": [
                {
                    "theme": "Minima conventionnels",
                    "reponse": "Les minima conventionnels ont été revalorisés via l’avenant n°69. Ne jamais donner un chiffre sans vérifier la grille et l’annexe applicables."
                },
                {
                    "theme": "Prime grands effectifs",
                    "reponse": "Une prime grands effectifs existe pour les enseignants intervenant devant des classes ou groupes de plus de 40 personnes : 10 % du taux horaire minimum conventionnel correspondant."
                },
                {
                    "theme": "Base horaire enseignant",
                    "reponse": "L’avenant rappelle une base de paie calculée sur 151,67 h × 12 mois, soit 1 820 heures annuelles, tout en distinguant le temps plein annuel de travail effectif."
                },
                {
                    "theme": "Maladie",
                    "reponse": "Prévenir sous 24 heures, certificat sous 48 heures, IJSS avec carence de 3 jours sauf cas particuliers, maintien selon ancienneté, prévoyance selon les cas."
                },
                {
                    "theme": "Prévoyance",
                    "reponse": "Pour certains salariés de moins de 12 mois d’ancienneté, la prévoyance complète après 20 jours d’arrêt à partir du 4e jour."
                },
                {
                    "theme": "Licenciement",
                    "reponse": "Indemnité conventionnelle : 1/4 de mois par année jusqu’à 10 ans puis 1/3 au-delà."
                },
                {
                    "theme": "Retraite",
                    "reponse": "Indemnité conventionnelle progressive selon l’ancienneté, jusqu’à 4 mois."
                },
                {
                    "theme": "Grossesse",
                    "reponse": "Réduction quotidienne de 30 minutes à partir du 61e jour de grossesse sans réduction de rémunération."
                },
                {
                    "theme": "Coupures",
                    "reponse": "Dans certains cas, coupure indemnisée à hauteur de 5 % de la rémunération liée au temps travaillé ou repos équivalent."
                }
            ]
        },

        "IDCC_1516": {
            "nom": "Organismes de formation",
            "summary": [
                "Convention collective des organismes de formation.",
                "Avenant salaires du 18 novembre 2024 étendu, fixant les minima annuels bruts 2025.",
                "Avenant frais de santé du 24 octobre 2025 repéré comme non étendu à la date consultée."
            ],
            "smart_questions": [
                "Le salarié est-il employé, technicien / agent de maîtrise ou cadre ?",
                "Est-il à temps plein ou temps partiel ?",
                "Quelle est son ancienneté ?",
                "La question concerne-t-elle une heure complémentaire, une heure supplémentaire ou un congé ?"
            ],
            "notions": [
                {
                    "theme": "Minima conventionnels",
                    "reponse": "Les minima sont fixés par catégorie et classification. Toujours comparer minimum conventionnel et SMIC."
                },
                {
                    "theme": "Temps partiel",
                    "reponse": "Les salariés à temps partiel bénéficient des mêmes droits proratisés."
                },
                {
                    "theme": "Heures complémentaires",
                    "reponse": "Les heures complémentaires concernent le temps partiel au-delà de l’horaire contractuel, avec information préalable et majoration au-delà de certains seuils."
                },
                {
                    "theme": "Heures supplémentaires",
                    "reponse": "Contingent annuel de 145 heures ; possibilité de repos compensateur."
                },
                {
                    "theme": "Temps choisi",
                    "reponse": "Délai de prévenance réciproque de 3 jours ouvrés sauf urgence."
                },
                {
                    "theme": "Formateurs",
                    "reponse": "Le temps de travail des formateurs comprend l’acte de formation, la préparation, la recherche liée à l’acte de formation et des activités connexes."
                },
                {
                    "theme": "Période d’essai",
                    "reponse": "Jusqu’à 4 mois pour les cadres ; règles spécifiques en CDD et CDI."
                },
                {
                    "theme": "Préavis",
                    "reponse": "1 à 3 mois selon statut et ancienneté."
                },
                {
                    "theme": "Licenciement",
                    "reponse": "Indemnité conventionnelle : 1/4 de mois jusqu’à 10 ans puis 1/3 au-delà."
                },
                {
                    "theme": "Retraite",
                    "reponse": "Indemnité conventionnelle de départ à la retraite progressive jusqu’à 3 mois selon ancienneté."
                },
                {
                    "theme": "Maladie / prévoyance",
                    "reponse": "Le maintien de salaire, les IJSS et la prévoyance doivent être distingués dans le traitement paie."
                },
                {
                    "theme": "Jours fériés",
                    "reponse": "Un jour férié chômé ne doit pas réduire la rémunération sous réserve de présence avant/après selon les règles conventionnelles."
                },
                {
                    "theme": "Congés familiaux",
                    "reponse": "Mariage, décès, examens, enfant malade : plusieurs absences rémunérées ou spécifiques sont prévues."
                }
            ]
        },

        "IDCC_1486": {
            "nom": "Syntec / BETIC",
            "summary": [
                "Convention Syntec / bureaux d’études techniques, cabinets d’ingénieurs-conseils et sociétés de conseils.",
                "Convention consolidée sur la base de la version 2021 sur Légifrance.",
                "Accord salaires minimaux 2025 applicable dans la branche."
            ],
            "smart_questions": [
                "Le salarié est-il ETAM ou ingénieur/cadre ?",
                "Quel est son coefficient / sa position ?",
                "Est-il en 35h, RTT, forfait heures ou forfait jours ?",
                "Quelle est son ancienneté ?"
            ],
            "notions": [
                {
                    "theme": "Classification",
                    "reponse": "La paie dépend fortement de la catégorie ETAM ou ingénieurs/cadres, de la position et du coefficient."
                },
                {
                    "theme": "Minima conventionnels",
                    "reponse": "Le salarié doit percevoir au moins le minimum conventionnel ou le SMIC, le plus favorable s’appliquant. Le minimum dépend de la grille, de la position et du coefficient."
                },
                {
                    "theme": "Temps de travail",
                    "reponse": "La paie varie selon le régime : 35h, RTT, forfait heures ou forfait jours."
                },
                {
                    "theme": "Forfait jours",
                    "reponse": "Le forfait jours raisonne en jours et non en heures ; il n’y a pas d’heures supplémentaires dans ce régime."
                },
                {
                    "theme": "Heures supplémentaires",
                    "reponse": "Hors forfait jours, les heures supplémentaires peuvent donner lieu à majoration ou repos."
                },
                {
                    "theme": "Maladie",
                    "reponse": "Il faut distinguer déduction d’absence, IJSS, maintien et prévoyance."
                },
                {
                    "theme": "Prime de vacances",
                    "reponse": "Prime de vacances obligatoire, traditionnellement présentée comme devant représenter au moins 10 % de la masse globale des indemnités de congés payés."
                },
                {
                    "theme": "Préavis",
                    "reponse": "Préavis variables selon la catégorie, avec une logique plus longue pour les cadres."
                },
                {
                    "theme": "Licenciement",
                    "reponse": "Comparer l’indemnité conventionnelle et l’indemnité légale selon ancienneté."
                },
                {
                    "theme": "Période d’essai",
                    "reponse": "La durée dépend de la catégorie ; elle est plus longue pour les cadres."
                }
            ]
        }
    },

    # =========================================================
    # 4) DIAGNOSTIC ORIENTE AGENT
    # =========================================================
    "ROUTING_RULES": [
        {
            "if_contains": ["arkevia", "coffre-fort", "mot de passe oublié", "peopledoc"],
            "route_to": "INTERNAL_FAQ.ARKEVIA"
        },
        {
            "if_contains": ["gel", "20 au 7", "ne remonte pas", "clôture", "workflow"],
            "route_to": "INTERNAL_FAQ.PERIODE_DE_GEL"
        },
        {
            "if_contains": ["acompte", "avance"],
            "route_to": "INTERNAL_FAQ.ACOMPTE_AVANCE"
        },
        {
            "if_contains": ["navigo", "transport", "RATP"],
            "route_to": "INTERNAL_FAQ.TRANSPORT"
        },
        {
            "if_contains": ["ticket restaurant", "edenred", "TR"],
            "route_to": "INTERNAL_FAQ.TICKETS_RESTAURANT"
        },
        {
            "if_contains": ["télétravail", "teletravail", "assurance habitation", "20€"],
            "route_to": "INTERNAL_FAQ.TELETRAVAIL"
        },
        {
            "if_contains": ["mutuelle", "dispense", "affiliation"],
            "route_to": "INTERNAL_FAQ.MUTUELLE"
        },
        {
            "if_contains": ["heures", "relevé d'heures", "heures excédentaires", "JPO", "récupération"],
            "route_to": "INTERNAL_FAQ.HEURES_SUP_ET_COMPLEMENTAIRES"
        },
        {
            "if_contains": ["maladie", "ijss", "subrogation", "carence", "accident du travail"],
            "route_to": "INTERNAL_FAQ.MALADIE"
        },
        {
            "if_contains": ["enfant malade"],
            "route_to": "INTERNAL_FAQ.ENFANT_MALADE"
        },
        {
            "if_contains": ["décès", "livret de famille", "acte de décès"],
            "route_to": "INTERNAL_FAQ.JOUR_DECES"
        },
        {
            "if_contains": ["mariage", "pacs"],
            "route_to": "INTERNAL_FAQ.MARIAGE_PACS"
        },
        {
            "if_contains": ["révision", "examen", "apprenti"],
            "route_to": "INTERNAL_FAQ.JOURS_REVISION"
        }
    ],

    # =========================================================
    # 5) QUESTIONS DE TRI POUR L'AGENT
    # =========================================================
    "GUIDED_TRIAGE": {
        "step_1_profile": [
            "Salarié",
            "Manager",
            "Contact paie",
            "Besoin d’accès / document"
        ],
        "step_2_theme": [
            "Paie / bulletin",
            "Absence / congé",
            "Mutuelle",
            "Transport",
            "Tickets restaurant",
            "Télétravail",
            "Portail paie / workflow",
            "Arkevia / bulletins",
            "Convention collective"
        ],
        "step_3_convention": [
            "Aucune / inconnu",
            "IDCC 2691",
            "IDCC 1516",
            "IDCC 1486"
        ],
        "step_4_precision_examples": {
            "Paie / bulletin": [
                "Mon salaire a baissé",
                "Il manque des heures",
                "Il manque une prime",
                "Je pense qu’il y a une erreur",
                "Je ne comprends pas une ligne"
            ],
            "Absence / congé": [
                "Arrêt maladie",
                "Enfant malade",
                "Décès",
                "Mariage / PACS",
                "Jours de révision",
                "Congés payés / jour exceptionnel"
            ],
            "Portail paie / workflow": [
                "Demande non remontée",
                "Période de gel",
                "Acompte",
                "TR",
                "Heures excédentaires",
                "JPO / récupération",
                "Forfait jours",
                "Prise de contrôle"
            ],
            "Convention collective": [
                "Minima conventionnels",
                "Temps de travail",
                "Maladie / maintien",
                "Heures supplémentaires / complémentaires",
                "Préavis / licenciement / retraite",
                "Congés / événements familiaux"
            ]
        }
    }