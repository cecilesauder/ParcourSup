# Revendications lycéennes et audit du cahier des charges

## Ce que les revendications publiées mettent en avant

Il faut distinguer trois types de sources : une plateforme de revendications portée par des organisations, des témoignages individuels recueillis par des médias, et des enquêtes d’opinion auprès d’une population définie. Aucun de ces matériaux, pris seul, ne représente tous les lycéen·nes.

En octobre 2026, l’Union étudiante et l’Union syndicale lycéenne, avec le soutien annoncé de l’UNEF, de la FAGE et de Solidaires étudiant·es, publient une plateforme commune. Sur Parcoursup, leur revendication est structurelle : **mettre fin à la sélection**, ajouter 250 000 places dans l’enseignement supérieur, et conserver une plateforme nationale d’information et de candidature sans sélection. Elles lient donc directement l’expérience de la procédure au nombre de places disponibles et au principe d’accès aux études. Il s’agit de la position de ces organisations signataires, pas d’un consensus démontré auprès de toute la jeunesse. [1] [2]

Les témoignages recueillis après les premiers résultats 2026 font apparaître des problèmes plus concrets : ne pas comprendre pourquoi un vœu est refusé ou reste très loin sur liste d’attente, vivre l’attente en vérifiant constamment la plateforme, ne pas pouvoir agir sur son dossier une fois les réponses publiées, et devoir gérer cette incertitude pendant les épreuves du bac. Une candidate citée par France 24 dit ne pas comprendre pourquoi un bon dossier n’a débouché sur aucune affectation; d’autres élèves interrogées par le CIDJ décrivent les refus, l’attente et l’impression d’opacité. Ce sont des témoignages éclairants, mais des récits individuels, non une mesure de fréquence. [3] [4]

Les thèmes à intégrer dans notre analyse sont donc :

- **Accès réel aux études souhaitées**, et pas seulement réception d’une proposition quelconque. Le débat porte aussi sur la sélection elle-même et sur le manque de places. Une réforme de fonction de choix qui maintient la sélection ne répond pas, à elle seule, à la demande formulée par les organisations citées.
- **Comprendre une décision et pouvoir y répondre** : critères effectivement utilisés par formation, étapes où ils interviennent, motifs de refus, position d’attente et possibilités de recours ou d’échange humain. La transparence utile n’est pas seulement la publication du code national.
- **Réduire l’incertitude vécue et préserver la capacité d’agir** : savoir ce qui peut encore évoluer, ce qui ne peut plus être modifié, et quand une réponse est attendue; éviter de faire coïncider des démarches importantes avec les examens quand le calendrier le permet.
- **Équité sociale et territoriale**, accompagnement à l’orientation et information accessibles, avec une attention aux parcours scolaires différents et aux élèves qui n’ont pas reçu de proposition adaptée.
- **Participation des lycéen·nes aux décisions**. La plateforme commune comprend aussi une revendication de démocratisation de la représentation lycéenne. Pour ce projet, cela plaide pour des ateliers de co-conception et pour une réponse documentée à leurs retours, plutôt que pour une simple validation finale par des élèves.

Le baromètre CSA 2025 confirme certains ressentis, sans établir à lui seul leurs causes. Il a interrogé en ligne, du 28 août au 4 septembre 2025, 1 005 néo-bachelier·es inscrit·es sur Parcoursup, admis·es ou non, via des adresses fournies par le ministère. À la question sur les adjectifs s’appliquant à la procédure, 83 % répondent « stressante »; 53 % la jugent transparente et 34 % la jugent juste et équitable. Le ministère rapporte aussi 73 % de satisfaction vis-à-vis des réponses obtenues. Ces résultats peuvent coexister : être satisfait·e d’une réponse n’exclut pas le stress ou un doute sur l’équité. L’enquête est un baromètre d’opinion sur une cohorte et une période précises, pas une preuve que l’algorithme cause le stress ni que l’attente est le problème principal de chaque candidat·e. [5] [6]

Les rapports du Comité éthique et scientifique de Parcoursup ajoutent des pistes opérationnelles qui correspondent à la demande de compréhension : publier le code ou une spécification des outils de classement et les facteurs de tri, documenter les règles de départage, et demander aux formations un rapport d’analyse des candidatures de la campagne précédente. Ce sont des recommandations institutionnelles, pas des revendications directement attribuables aux lycéen·nes; elles sont utiles pour convertir la demande de transparence en exigences vérifiables. [7]

## Audit du cahier des charges transmis

### L’objectif politique et l’objet technique ne coïncident pas encore

Le cahier présente une « alternative algorithmique » par réserves. Or la revendication structurante portée par la plateforme commune est de mettre fin à la sélection et d’augmenter le nombre de places. Une fonction à réserves peut modifier qui est retenu parmi des candidatures concurrentes; elle n’ajoute aucune place et ne met pas fin à la sélection. Il faut donc annoncer honnêtement son statut : **une piste limitée pour étudier les règles de priorité sous sélection**, et non une réponse globale aux revendications lycéennes. Il faut aussi prévoir comme scénario de référence la demande d’accès sans sélection, même si elle relève d’une décision de capacité et de droit plutôt que d’un simple changement de code. [1]

### Trois mécanismes distincts sont mélangés

Le cahier juxtapose l’ordre d’appel de Parcoursup, une fonction de choix à réserve, et une procédure d’acceptation différée de type Gale–Shapley. Ce sont des objets différents. L’ordre d’appel actuel produit une séquence d’appel par groupe. Une fonction de choix renvoie, pour un ensemble de candidatures donné, un ensemble retenu. L’acceptation différée combine les préférences des candidat·es, les priorités des formations et ces fonctions de choix. Enfin, la documentation officielle décrit le calcul quotidien des propositions Parcoursup comme un processus distinct qui tient compte des réponses précédentes et de paramètres propres aux formations. Le simulateur peut étudier une affectation différée théorique, mais il ne faut pas la présenter comme une reproduction de la phase réelle sans en avoir spécifié les règles et le temps. [8]

### Le modèle à plusieurs réserves doit être reformulé avant d’être codé

Le cahier écrit `Q_r = floor(Q × (1 − q_h))`, sans définir `q_h`, puis calcule `Q_g = Q − Q_b − Q_r`. Cette partition peut devenir négative; ses arrondis sont incohérents avec le principe d’arrondi supérieur documenté pour les taux; et elle ne dit pas comment traiter les personnes à la fois boursières et résidentes. Des réserves « disjointes » exigent une partition claire des catégories, une règle de priorité entre elles, le traitement des places non pourvues et une règle pour les cas où les objectifs dépassent la capacité. La documentation de Parcoursup précise que, lorsque les taux boursier et résident ne peuvent être respectés simultanément, le taux boursier prime. Il faut traduire cette règle dans le modèle avant de revendiquer une garantie. [8]

L’article de Hafalir, Yenmez et Yildirim porte sur une réserve minoritaire dans un modèle précis de choix scolaire. Son résultat de substituabilité ne constitue pas, sans démonstration supplémentaire, une preuve pour plusieurs réserves qui se chevauchent, les paramètres de Parcoursup ou un mécanisme avec des règles additionnelles. [9]

### Les tests doivent viser les bonnes propriétés

Le test `k = 1` est utile pour reproduire l’effet du quota dans le modèle actuel. Mais l’appeler « bogue » suppose déjà que la règle est erronée. C’est plutôt un **cas limite révélant le compromis de la règle de préfixe**. Pour l’alternative, une fonction de choix ne livre pas un premier rang « général » et un premier rang « réservé » comparables sans définir comment son ensemble choisi serait converti en appels. Le test doit comparer des ensembles retenus ou des affectations complètes, pas inventer un rang d’appel qui n’existe pas dans le modèle.

Pour une fonction de choix `C`, la substituabilité peut se tester ainsi : si une personne `x` est choisie dans un ensemble `S`, retirer de `S` une autre personne ne doit pas faire rejeter `x`. La monotonie des rejets peut être formulée de manière équivalente pour des ensembles emboîtés : une personne rejetée de `S` ne doit pas être choisie quand on passe à un ensemble plus grand `S'`. Le cahier des charges mélange cette propriété avec un test particulier portant sur le retrait d’une personne déjà rejetée; ce dernier ne suffit pas à établir la substituabilité. Nos tests actuels du petit prototype contrôlent la persistance des personnes choisies lors du retrait d’un·e autre candidat·e, par énumération finie seulement; ce n’est pas une preuve générale.

La garantie « au moins `Q_b` boursiers admis » doit être séparée en deux affirmations. Dans un appel statique de la fonction, si au moins `Q_b` candidat·es boursier·es sont présents dans l’ensemble pertinent, la réserve les sélectionne. Cela ne prouve pas automatiquement que l’affectation finale après propositions, préférences, refus et interactions entre formations atteindra ce seuil.

### Les métriques ne doivent pas préjuger du résultat

Le déplacement moyen et le RMSE ne s’appliquent naturellement qu’à des listes ordonnées. La fonction de choix renvoie un ensemble et une affectation finale distribue des vœux préférés; comparer uniquement des « rangs d’appel » pourrait donc favoriser artificiellement un modèle. Il faut mesurer les résultats vécus : accès au vœu préféré ou à une solution acceptable, nombre de personnes sans proposition adaptée, écarts entre groupes, délais observés, nombre et timing des propositions simultanées, compréhension des décisions et perception d’équité.

La « rétention artificielle » et une baisse des délais sont des hypothèses, pas des résultats acquis. Il faut définir le modèle temporel : durée laissée pour répondre, calendrier, taux d’appel de chaque formation, préférences, acceptations provisoires, désistements, surbooking et places effectivement disponibles. Le critère « 95 % des places définitivement attribuées » doit notamment préciser ce que signifie « définitivement » et à quel événement correspond un jour ou un cycle. Une simulation Gale–Shapley calcule un résultat selon ses règles; son nombre d’itérations ne se transforme pas automatiquement en jours d’attente Parcoursup.

Les cohortes artificielles `N=10 000`, `M=50`, la corrélation notes/bourse et la concentration « 80 % des vœux sur 20 % des formations » doivent être présentées comme scénarios de stress, sauf si elles sont calibrées sur des données agrégées et publiées. Les résultats doivent varier avec ces hypothèses; aucun pourcentage d’amélioration ne doit être écrit dans le README avant exécution et publication du code de génération.

## Révisions conseillées avant l’étape de simulation

1. Ajouter une étape de co-conception avec des lycéen·nes de parcours variés, y compris des personnes ayant reçu une réponse satisfaisante, une réponse tardive ou aucune proposition adaptée. Recueillir leurs propres priorités, avec méthode, consentement et limites d’échantillonnage.
2. Garder deux questions distinctes : « Que changer dans l’accès aux formations? » et « Que changer dans la règle algorithmique à places constantes? » Comparer explicitement la réserve à l’option « fin de la sélection et capacité accrue » revendiquée par certaines organisations.
3. Stabiliser le modèle : types de candidatures, priorités, capacités, taux, catégories chevauchantes, arrondis, cas limites, contraintes juridiques, comportement des places vacantes, préférences et temps de réponse.
4. Documenter le modèle actuel à partir du code et des spécifications officiels, avec des tests de non-régression et des cas publiés avant de le qualifier de reproduction fidèle.
5. Annoncer à l’avance les indicateurs et les incertitudes. Publier les scénarios et résultats séparément des promesses d’effet. Ne pas conclure à une accélération sans comparer un simulateur temporel validé à une référence fidèle.
6. Retirer toute biographie ou qualité professionnelle non confirmée du cahier des charges. Vérifier les licences avant de réutiliser du code du dépôt officiel; ne pas supposer qu’un dépôt public est libre de conditions.

## Références

[1]: https://union-etudiante.fr/10mesures/ "Union étudiante, 10 mesures d’urgence pour la jeunesse, mesure 4"

[2]: https://www.letudiant.fr/lycee/mobilisation-lyceenne-la-jeunesse-propose-10-mesures-d-urgence.html "L’Étudiant, les organisations lycéennes et étudiantes proposent 10 mesures d’urgence"

[3]: https://www.cidj.com/s-orienter/avec-parcoursup/parcoursup-2026-c-est-catastrophique-vos-reactions-apres-les-premiers-resultats "CIDJ, témoignages de candidat·es après les premiers résultats Parcoursup 2026"

[4]: https://www.france24.com/fr/france/20261006-france-avenir-de-parcoursup-une-question-au-c%C5%93ur-des-revendications-lyceennes "France 24, l’avenir de Parcoursup au cœur des revendications lycéennes"

[5]: https://csa.eu/wp-content/uploads/2025/10/2500648-Baro-Parcoursup-2025-Resultats_1609_vSITE-CSA.pdf "Institut CSA, Baromètre Parcoursup 2025, vague 6"

[6]: https://www.enseignementsup-recherche.gouv.fr/fr/bilan-parcoursup-2025-un-nombre-record-de-candidats-des-resultats-stables-et-un-accompagnement-100136 "MESR, bilan de la procédure Parcoursup 2025"

[7]: https://www.enseignementsup-recherche.gouv.fr/fr/remise-du-rapport-annuel-2025-du-comite-ethique-et-scientifique-de-parcoursup-et-mon-master-101305 "MESR, recommandations du Comité éthique et scientifique de Parcoursup et Mon Master, 2025"

[8]: https://services.dgesip.fr/fichiers/presentation_algorithmes_parcoursup_2025_finale.pdf "MESR, présentation des algorithmes de Parcoursup, 2025"

[9]: https://www.econometricsociety.org/publications/theoretical-economics/lookup/paper/8775 "Hafalir, Yenmez et Yildirim, Effective Affirmative Action in School Choice, 2013"
