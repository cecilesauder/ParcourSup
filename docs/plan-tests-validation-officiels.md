# Plan de tests comparés aux références officielles

## Ce que vérifient les tests du dépôt officiel

Les tests Java et exemples ont été examinés à la révision `65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2`.

- `TestGroupeClassement` vérifie notamment les taux invalides, la sortie vide et le tri des rangs. Son exemple aléatoire ne compare pas un ordre complet attendu.
- `TestAlgoOrdreAppel` construit deux petits groupes sans quota et vérifie que les contrôles de sortie ne lèvent pas d’erreur.
- `TestDemoOrdreAppel` lance les démonstrations A1 à A6, mais n’affirme pas les ordres complets par des assertions.

Le dépôt officiel fournit donc des entrées très utiles pour des tests de comparaison, mais il faut distinguer ses tests automatisés des sorties de référence que nous avons enregistrées nous-mêmes. [1] [2]

## Références à un taux boursier

Le fichier `tests/fixtures/official_order_call_examples.json` conserve les entrées et sorties, avec la source de chacune. `tests/test_official_order_call_examples.py` compare l’ordre complet.

- **Guide officiel, taux de 25 %.** Le document publie l’entrée et l’ordre d’appel exact : `B1, C1, C2, C3, B2, C4, C5, C6, B3, C7, …, C17`. C’est une sortie officiellement publiée.
- **Démonstrations A1, A2 et A4.** Ces cas testent respectivement des taux de 20 %, 2 % et 10 %. Les sorties exactes sont enregistrées selon la règle du guide; le JUnit officiel ne les affirme pas par une assertion.
- **Démonstration A3.** Le test couvre les 1 000 candidatures du cas public à 10 %. Il vérifie l’ordre complet, pas seulement le nombre de personnes boursières.

## Références à deux taux : bourse et secteur

Le prototype prend maintenant en compte les quatre profils possibles : boursier·e du secteur, boursier·e hors secteur, non-boursier·e du secteur et non-boursier·e hors secteur. La fonction `order_call_with_quotas` sélectionne à chaque étape le meilleur rang parmi les profils admissibles. Si les deux taux sont contraignants et qu’aucun profil ne peut satisfaire les deux, elle applique la priorité boursière prévue par le code public.

`tests/fixtures/official_two_rate_examples.json` et `tests/test_official_two_rate_examples.py` couvrent trois références :

- **Exemple du guide à deux taux.** Le guide publie l’ordre complet pour 20 % de boursier·es et 90 % de candidat·es du secteur. Le cas montre notamment une personne boursière du secteur appelée en premier, puis des profils intercalés, avec la personne non-boursière hors secteur appelée en dernier.
- **Démonstration officielle A5.** La sortie de `GroupeClassement` est le classement d’origine `1, 2, …, 100`. Les profils boursier·e et secteur se recouvrent. Le test s’assure qu’une personne qui satisfait les deux critères apparaît une seule fois.
- **Démonstration officielle A6.** Les personnes du secteur ont les rangs 1 à 100 et les personnes boursières hors secteur les rangs 101 à 111. Avec 10 % de boursier·es et 95 % du secteur, l’ordre de référence commence par la personne 101, puis les personnes 1 à 9, puis 102, puis 10 à 18, et ainsi de suite. Le test vérifie l’ordre complet et le conflit des deux taux dès le premier appel.

Les sorties A5/A6 du fixture ont été obtenues en exécutant la classe Java officielle `GroupeClassement.calculerOrdreAppel` de la révision épinglée, à partir des entrées définies dans les classes de démonstration A5/A6. Les blobs exécutés ont été vérifiés contre le commit indiqué dans le fixture. Elles sont donc des **sorties de référence du code officiel**, et non des sorties explicitement imprimées dans le guide ni des assertions déjà présentes dans le JUnit amont. [2] [3] [4] [5] Le cas du guide à deux taux, lui, a une sortie explicitement publiée et a également été comparé au calcul Java officiel. [1] [3]

## Garanties vérifiées et limites

Les tests comparent les listes entières pour les exemples de référence. Ils vérifient également l’absence de doublons, les taux invalides, le statut de secteur invalide, le recouvrement des critères dans A5 et l’indépendance au désordre des données d’entrée dans A6. Les anciens tests continuent de vérifier le taux boursier seul et la règle expérimentale de réserve.

Cela valide uniquement un groupe de classement à rangs stricts avec les deux taux. Le prototype ne modélise pas encore les internats, les groupes multiples, les places disponibles ni les propositions et réponses quotidiennes. Les résultats de conformité de l’ordre d’appel ne démontrent pas que les résultats seraient équitables pour l’ensemble des candidat·es.

Il reste utile d’ajouter des tests exhaustifs sur des petits ensembles couvrant toutes les combinaisons de profils, et des tests de frontière pour les taux nuls et maximaux, les viviers épuisés et les contraintes qui deviennent inatteignables. Les critères de réussite de ces tests doivent suivre exactement les propriétés de la spécification, surtout pour le taux du secteur; il ne faut pas le traiter automatiquement comme un quota indépendant de sièges.

## Tests distincts à ajouter pour les propositions quotidiennes

Le prototype d’ordre d’appel ne simule pas les propositions journalières. Quand cette deuxième partie sera créée, sa suite devra tester séparément :

- l’ouverture par rang limite d’appel et le nombre de recrutements souhaité;
- plusieurs formations et propositions simultanées;
- les réponses positives ou négatives, les maintiens en attente et les places libérées;
- les démissions automatiques, leur calendrier et les éventuelles règles d’internat;
- la cohérence de chaque statut avant et après une journée simulée.

Il faudra comparer ces sorties aux cas unitaires et exemples du moteur officiel de propositions. Un modèle de Gale–Shapley, s’il est étudié, restera un scénario théorique distinct et ne remplacera pas cette référence sans adaptation.

## Lancer les tests

```bash
python -m unittest discover -s tests -v
```

## Références

[1]: https://services.dgesip.fr/fichiers/presentation_algorithmes_parcoursup_2025_finale.pdf "MESR, présentation des algorithmes de Parcoursup, exemples à un et deux taux"

[2]: https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup/-/blob/65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2/src/test/java/fr/parcoursup/algos/ordreappel/exemples/TestDemoOrdreAppel.java "Test Java officiel qui exécute les démonstrations A1–A6"

[3]: https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup/-/blob/65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2/src/main/java/fr/parcoursup/algos/ordreappel/algo/GroupeClassement.java "Code officiel de calcul de l’ordre d’appel par groupe"

[4]: https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup/-/blob/65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2/src/main/java/fr/parcoursup/algos/bacasable/ordreappel/ExempleA5.java "Entrée de la démonstration officielle A5"

[5]: https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup/-/blob/65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2/src/main/java/fr/parcoursup/algos/bacasable/ordreappel/ExempleA6.java "Entrée de la démonstration officielle A6"
