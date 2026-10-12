# Analyse initiale : ordre d’appel et réserves

## Périmètre

Le premier prototype isole un seul élément : le taux minimum de boursiers dans un groupe de classement, sans taux de résidents, internat, groupes multiples ni règle particulière de capacité. Ce choix rend les tests lisibles, mais interdit de présenter les résultats comme une simulation complète de Parcoursup.

Le dépôt public du ministère distingue le calcul d’un ordre d’appel de celui des propositions. La classe Java `AlgoOrdreAppel` délègue le calcul à chaque groupe de classement; le dépôt comporte par ailleurs un paquet distinct pour les propositions et des vérifications associées. La documentation ministérielle précise que l’ordre d’appel est calculé une fois, tandis que les propositions sont ensuite envoyées en continu, dans l’ordre d’appel. Le nombre proposé chaque jour dépend aussi des réponses déjà reçues et des paramètres de taux d’appel supplémentaire ou de rang limite définis par la formation. [1] [2]

## Conclusions de départ : examen

### Rang d’appel déplacé par le taux

C’est une conséquence bien identifiée de la règle de préfixe : lorsque le taux minimum est contraignant à un préfixe et qu’il reste des candidat·es boursier·es, un·e boursier·e peut précéder un dossier mieux classé pédagogiquement. Dans le cas « taux boursiers seul », la documentation officielle indique que le taux est arrondi à l’entier supérieur. La spécification de Castéran formalise également les garanties de quota et, pour le cas sans taux résidents, des bornes sur les déplacements. [2] [3]

Dans l’exemple artificiel à quatre personnes avec un taux de 25 %, si la personne classée quatrième est boursière, le modèle de préfixe peut la placer au premier rang d’appel. Cela met en évidence un effet possible, mais ne mesure pas sa fréquence, son impact réel ni son acceptabilité pour les personnes concernées.

### « Engorgement » et ralentissement des listes

Cette chaîne causale n’est pas démontrée par les notes de départ. La proposition « une personne peut recevoir plusieurs propositions de formations différentes » est plausible dans un système de vœux multiples, mais elle ne prouve pas que l’ordre d’appel provoque une rétention artificielle ou retarde mécaniquement la convergence. La documentation officielle décrit un flux continu de propositions et des appels quotidiens tenant compte des réponses précédentes et des paramètres propres aux formations. Pour attribuer une part des délais à l’ordre d’appel, il faudrait un modèle complet et des mesures comparatives qui isolent ces facteurs. [2]

Le chiffre de stress des notes est désormais sourcé, mais le baromètre primaire de l’Institut CSA donne **83 %** (et non 84 %) en 2025. Le questionnaire en ligne a été rempli du 28 août au 4 septembre par 1 005 néo-bachelier·es inscrit·es sur Parcoursup, admis·es ou non, à partir d’adresses fournies par le ministère. À la question sur les adjectifs correspondant à la procédure, 53 % répondent « transparente » et 34 % « juste, qui traite tous les candidats de manière équitable ». Ce sont des opinions déclarées par cette cohorte, pas une preuve que l’algorithme produit le stress ou les délais. [5]

### Réserve à la capacité d’accueil

La proposition est reformulée ici comme une fonction de choix : pour un ensemble de personnes qui postulent à une formation, choisir d’abord jusqu’à `ceil(capacité × taux)` candidat·es boursier·es les mieux classé·es, puis compléter avec les meilleur·es candidat·es restant·es. Si la réserve ne peut pas être remplie, les places restantes sont libérées.

Cette opération renvoie un ensemble de personnes retenues pour un ensemble d’offres donné. Elle ne produit pas automatiquement l’ordre d’appel complet attendu aujourd’hui par Parcoursup. Elle correspond plutôt à une règle de choix qui pourrait entrer dans un mécanisme d’affectation différée à spécifier séparément.

Les travaux de Hafalir, Yenmez et Yildirim étudient des réserves minoritaires dans un modèle de choix scolaire et établissent la substituabilité de la fonction de choix sous leurs hypothèses. C’est une base de comparaison pertinente, mais pas une preuve que la règle proposée est conforme au droit français, compatible avec toutes les règles de Parcoursup, équitable dans chaque sous-groupe ou qu’elle réduirait les délais observés. [4]

### Garantie de résultat

La réserve donne une priorité de choix aux candidat·es boursier·es lorsque l’ensemble examiné contient assez de candidat·es éligibles. Elle ne justifie pas à elle seule l’affirmation « le nombre final d’admis boursiers est toujours au moins le quota », quelles que soient les candidatures, les préférences, les refus et les règles d’acceptabilité. Cette propriété doit être énoncée avec ses hypothèses, puis vérifiée sur le mécanisme complet et sur les données pertinentes.

## Prototype et validations actuelles

`parcoursup_prototype/order_call.py` contient deux fonctions distinctes :

- `prefix_quota_order` : une formalisation exécutable du cas simplifié « taux boursiers seul »;
- `choose_with_scholarship_reserve` : l’alternative expérimentale décrite ci-dessus.

Les tests contrôlent la contrainte de préfixe sur des cas ciblés, l’arrondi supérieur, la capacité, la libération des réserves inutilisées et la substituabilité sur tous les sous-ensembles de quelques instances finies. Cette dernière vérification est un test exhaustif borné, **pas une preuve formelle générale**. Aucun résultat concernant les délais de Parcoursup n’est produit.

## Questions à soumettre en priorité aux lycéen·nes

Avant d’optimiser une métrique technique, le projet doit recueillir leurs revendications dans leurs propres termes. Les premiers ateliers devraient demander : quels moments de la procédure créent le plus d’incertitude? Quelles informations sur le rang et les propositions aideraient réellement à comprendre l’attente? Quels compromis entre priorité sociale, rang pédagogique, délai et prévisibilité sont jugés acceptables? Quels résultats devraient être publiés par groupe, et comment protéger les données personnelles?

Le dépôt devra consigner la méthode de consultation, ses limites et la manière dont les retours modifient les critères d’évaluation. Il ne faut pas présenter une personne ou un petit échantillon comme représentatif de l’ensemble des candidat·es.

## Références

[1] [Code source officiel — calcul de l’ordre d’appel](https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup/-/blob/master/src/main/java/fr/parcoursup/algos/ordreappel/algo/AlgoOrdreAppel.java) — le dépôt officiel comporte aussi les propositions et leurs tests dans des modules distincts.

[2] [MESR, *Présentation des algorithmes de Parcoursup*, 2025, §§ 2.4–2.5, 3 et 4](https://services.dgesip.fr/fichiers/presentation_algorithmes_parcoursup_2025_finale.pdf).

[3] [P. Castéran, *Vérification de l’algorithme de calcul des ordres d’appel…*](https://hal.science/hal-03388671/document) — spécification et vérifications de l’algorithme d’ordre d’appel.

[4] [I. E. Hafalir, M. B. Yenmez et M. A. Yildirim, “Effective Affirmative Action in School Choice”, *Theoretical Economics*, 2013](https://www.econometricsociety.org/publications/theoretical-economics/lookup/paper/8775).

[5] [Institut CSA, *Baromètre Parcoursup 2025, vague 6*](https://csa.eu/wp-content/uploads/2025/10/2500648-Baro-Parcoursup-2025-Resultats_1609_vSITE-CSA.pdf).
