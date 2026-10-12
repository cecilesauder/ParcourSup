# Analyse de l’algorithme public de Parcoursup et pistes d’amélioration

## Périmètre vérifié

Cette analyse porte sur le dépôt public du ministère, branche `master`, commit `65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2`, ainsi que sur la présentation officielle 2025. Ce code public permet d’analyser les règles publiées; il ne suffit pas à certifier que chaque version actuellement exécutée en production lui est identique. Le dépôt précise que les commissions d’examen des vœux classent les candidatures et que le code fourni couvre ensuite le calcul des ordres d’appel et l’envoi des propositions. [1] [2]

## Comment fonctionne le système examiné

### 1. Le classement pédagogique est une entrée, pas un résultat de l’algorithme national

La commission de chaque formation examine les dossiers et établit un classement pédagogique, éventuellement par groupes. Le calcul de l’ordre d’appel part de ce classement et des taux réglementaires fournis au groupe. Il ne réévalue pas lui-même la qualité scolaire des dossiers. La distinction est importante : une critique de la sélection pédagogique locale ne doit pas être attribuée automatiquement au seul code national d’ordre d’appel. [2]

### 2. L’ordre d’appel applique les taux au flux des personnes appelées

`GroupeClassement.calculerOrdreAppel` répartit les candidatures en files selon quatre profils : boursier·e/résident·e du secteur, boursier·e hors secteur, non-boursier·e résident·e, et non-boursier·e hors secteur. Les files sont ordonnées selon le rang pédagogique. À chaque étape, le code vérifie si le taux de boursier·es et/ou le taux de résident·es est contraignant, puis prend le meilleur rang parmi les profils qui respectent ces contraintes. Si les deux contraintes sont actives mais ne peuvent être satisfaites ensemble, le code choisit en priorité un·e boursier·e hors secteur. [1] [2]

Dans le cas d’un taux boursier seul, un taux positif implique qu’au premier rang le taux est contraignant. S’il reste au moins un·e candidat·e boursier·e, le code peut donc placer cette personne avant des candidat·es de meilleur rang pédagogique. Ce saut au rang d’appel 1 est un effet mécanique de la contrainte de préfixe. Il respecte la règle publiée; le qualifier de « bogue » est un jugement normatif, pas un constat de défaut logiciel. [1] [2]

La règle garantit un taux minimum dans les personnes **appelées** à chaque préfixe, sauf lorsque le vivier concerné est épuisé. Elle ne garantit pas le même taux dans les admissions finales : les candidat·es restent libres de refuser les propositions. C’est explicitement indiqué dans la présentation ministérielle. [2]

Un résultat souvent omis dans la critique est que, pour le cas **d’un seul taux boursier**, la spécification officielle attribue à l’ordre actuel une minimalité du nombre d’inversions (distance de Kendall) parmi les ordres respectant le taux. Cela ne veut pas dire que l’ordre minimise la distance absolue ou quadratique des rangs, ni que cette propriété s’étend aux deux taux ou au mécanisme d’affectation complet. Mais cela signifie qu’une proposition de simple « baisse des déplacements » doit préciser quelle métrique elle améliore et le compromis qu’elle modifie. [2] [3]

### 3. L’envoi des propositions est un moteur distinct et piloté par les données de formation

`AlgoPropositions` prend l’état des vœux, les propositions déjà présentes, les informations de campagne et des paramètres d’internat. Dans les groupes sans internat, `CalculPropositionsEtDemissions` parcourt les vœux encore en attente dans l’ordre d’appel. Il envoie une proposition lorsque le nombre de recrutements souhaité par la formation n’est pas atteint ou lorsque le rang d’appel du candidat est inclus dans le rang limite d’appel par bloc. Les seuils `nbRecrutementsSouhaite` et `rangLimite` sont des entrées de pilotage du groupe, pas des valeurs calculées uniquement par l’ordre d’appel. [4] [5]

Le moteur boucle ensuite pour intégrer les places libérées par le répondeur automatique et, à la phase prévue, par les démissions automatiques de certains vœux. Pour les vœux avec internat, une autre boucle ajuste les barres d’admission jusqu’à supprimer les surcapacités dans les internats. Le système est donc une procédure séquentielle de propositions et de mise à jour des statuts, avec contraintes de capacité et pilotage; ce n’est pas le simple mécanisme étudiant-proposant de Gale–Shapley décrit dans le cahier des charges. Une simulation Gale–Shapley reste possible comme expérience comparative, mais elle doit être nommée modèle théorique distinct et ne peut servir, sans adaptation, à prédire le nombre de jours de Parcoursup. [4] [6]

## Ce que les données de ressenti disent — et ne disent pas

Le baromètre CSA 2025 interroge 1 005 néo-bachelier·es inscrit·es sur Parcoursup, admis·es ou non, par questionnaire en ligne après la campagne. Il rapporte 83 % jugeant la procédure stressante, 53 % la jugeant transparente et 34 % la jugeant juste et équitable. Parmi les candidat·es admis·es, 72 % se disent satisfait·es du délai de réception des propositions et 73 % des réponses obtenues. Ces mesures ne se contredisent pas : recevoir une proposition dans un délai jugé satisfaisant n’implique pas de trouver la procédure équitable ou non stressante. Elles ne démontrent pas non plus que le calcul de l’ordre d’appel est la cause du stress. [7]

Les revendications organisées recensées dans la plateforme de l’Union étudiante et de l’Union syndicale lycéenne vont plus loin qu’une modification d’ordre d’appel : elles demandent de mettre fin à la sélection et d’augmenter le nombre de places, tout en conservant un portail national d’information et de candidatures. Une réserve sociale à capacité constante doit donc être présentée comme une piste étroite sur la distribution de places rares, non comme une réponse complète à cette revendication. [8]

## Améliorations recommandées

### Priorité 1 — rendre les décisions et l’attente compréhensibles

Avant de modifier la règle d’affectation, ajouter ou améliorer l’explication destinée aux candidat·es : distinguer rang pédagogique et rang d’appel; dire quels taux s’appliquent au groupe et comment ils modifient l’ordre; indiquer les critères locaux effectivement utilisés, les règles de départage et les raisons d’un refus; préciser ce qu’une position d’attente permet ou non de conclure. Toute estimation de chance ou de délai devrait afficher une fourchette, sa date de calcul, les hypothèses et son incertitude, plutôt que promettre une admission.

Cette priorité répond directement au manque de transparence et d’équité perçue. Le Comité éthique et scientifique recommande de publier le code ou une spécification des mécanismes de classement, avec les facteurs, règles de départage et paramètres d’ordre d’affichage, et de rendre systématiques les rapports d’analyse des candidatures par formation. [7] [9]

### Priorité 2 — évaluer les effets de l’ordre d’appel sans préjuger du résultat

Pour le modèle actuel, mesurer par formation et par groupe : nombre d’inversions, déplacement absolu et maximal des rangs, part des premiers appels due à chaque contrainte, taux d’appels et d’offres, délais jusqu’à la première proposition puis jusqu’à une proposition acceptable, et écarts entre profils. Distinguer ces indicateurs entre ordre d’appel, propositions provisoires et admission finale.

Avant tout classement alternatif, fixer avec des lycéen·nes les critères de réussite. Pour un ordre d’appel, comparer les compromis entre respect des taux, rangs déplacés, maximum de déplacement et lisibilité. Pour une fonction de choix, comparer les ensembles retenus et les affectations finales; ne pas lui attribuer artificiellement un « rang d’appel ».

### Priorité 3 — faire un vrai test temporel du mécanisme réel

Si l’objectif reste d’accélérer les propositions, le benchmark de référence doit reproduire les entrées et boucles du moteur public : rang limite d’appel, recrutement souhaité, propositions antérieures, réponses, répondeur automatique, démissions automatiques, règles d’internat et calendrier. Mesurer la latence par candidat·e et par formation, le temps passé sans proposition acceptable et le nombre de places provisoires occupées; faire varier les délais de réponse et les stratégies d’acceptation. Publier des scénarios de sensibilité plutôt qu’un unique chiffre simulé. Aucun gain de vitesse n’est établi par l’analyse du code seul.

### Priorité 4 — garder les réserves comme scénario alternatif, avec ses hypothèses

Le prototype à réserve peut être poursuivi, mais dans un mécanisme complet et explicitement distinct : définir les préférences des candidat·es, la fonction de choix des formations, les priorités pédagogiques, la capacité, les places vacantes, les catégories qui se recouvrent (boursier·e et résident·e), l’arbitrage légal entre les taux, et les règles de sortie. Tester la substituabilité et la stabilité sous ces hypothèses. Le résultat de Hafalir, Yenmez et Yildirim concerne un modèle de réserve minoritaire précis; il ne prouve pas à lui seul la stabilité ou la conformité d’une variante multi-réserves pour Parcoursup. [10]

Comparer au moins trois scénarios distincts : le système publié actuel; une réserve sociale à capacité constante; et une hausse ou redistribution de capacité qui traite directement le manque de places. Les deux derniers portent sur des décisions différentes et des leviers différents.

### Priorité 5 — co-construire les indicateurs avec les personnes concernées

Organiser des ateliers avec des candidat·es aux parcours variés : formations sélectives et non sélectives, bacs général/technologique/professionnel, personnes admises, en attente longue ou sans proposition qui leur convienne. Leur demander de hiérarchiser les problèmes et de tester les explications proposées. Consigner qui a participé, ce qui a changé à la suite des retours et les limites de représentativité; éviter de présenter une seule consultation comme l’opinion de toute une génération.

## Ordre de travail proposé

1. [x] Figer la version du code public et écrire des cas de référence, y compris les quatre profils et le conflit des taux.
2. [x] Reproduire la règle d’ordre d’appel d’un groupe strict à deux taux et la comparer aux exemples officiels disponibles. Cette validation ne couvre pas encore toutes les variantes de production.
3. [ ] Compléter le modèle temporel de propositions et vérifier ses sorties sur des exemples du dépôt officiel.
4. [ ] Tester avec des candidat·es la compréhension des rangs, des refus et des listes d’attente; transformer leurs priorités en critères mesurables.
5. [ ] Seulement ensuite, comparer l’ordre actuel et les politiques alternatives, en publiant les hypothèses, résultats par groupe et incertitudes.

## Références

[1]: https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup/-/blob/65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2/src/main/java/fr/parcoursup/algos/ordreappel/algo/GroupeClassement.java "Code officiel, génération de l’ordre d’appel par groupe"

[2]: https://services.dgesip.fr/fichiers/presentation_algorithmes_parcoursup_2025_finale.pdf "MESR, présentation des algorithmes de Parcoursup, édition 2025"

[3]: https://hal.science/hal-03388671/document "P. Castéran, vérification de l’algorithme de calcul des ordres d’appel"

[4]: https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup/-/blob/65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2/src/main/java/fr/parcoursup/algos/propositions/algo/CalculPropositionsEtDemissions.java "Code officiel, calcul des propositions et libération des places"

[5]: https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup/-/blob/65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2/src/main/java/fr/parcoursup/algos/propositions/algo/GroupeAffectation.java "Code officiel, paramètres de pilotage d’un groupe d’affectation"

[6]: https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup/-/blob/65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2/src/main/java/fr/parcoursup/algos/propositions/algo/AlgoPropositions.java "Code officiel, orchestration des propositions et contraintes d’internat"

[7]: https://csa.eu/wp-content/uploads/2025/10/2500648-Baro-Parcoursup-2025-Resultats_1609_vSITE-CSA.pdf "Institut CSA, Baromètre Parcoursup 2025, vague 6"

[8]: https://union-etudiante.fr/10mesures/ "Union étudiante et organisations signataires, 10 mesures d’urgence pour la jeunesse"

[9]: https://www.enseignementsup-recherche.gouv.fr/fr/remise-du-rapport-annuel-2025-du-comite-ethique-et-scientifique-de-parcoursup-et-mon-master-101305 "MESR, recommandations du Comité éthique et scientifique de Parcoursup et Mon Master, 2025"

[10]: https://www.econometricsociety.org/publications/theoretical-economics/lookup/paper/8775 "Hafalir, Yenmez et Yildirim, Effective Affirmative Action in School Choice, 2013"
