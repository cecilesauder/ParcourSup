# Plan de tests comparés aux références officielles

## Ce que les tests officiels vérifient aujourd’hui

Nous avons lu les tests Java et les exemples du dépôt public sur la branche `master`, commit `65273cd09ff12fa719ac3a0c8ca9ecbd8a1797d2`.

- `TestGroupeClassement` vérifie notamment les taux invalides, la sortie vide et le tri des rangs. Son exemple aléatoire ne compare pas un ordre complet attendu.
- `TestAlgoOrdreAppel` construit deux petits groupes sans quota et vérifie que les contrôles de sortie ne lèvent pas d’erreur.
- `TestDemoOrdreAppel` exécute les exemples déterministes A1 à A6, mais ne compare pas explicitement la liste de sortie à une liste attendue.
- Les démonstrations A5/A6 couvrent les taux boursier et du secteur simultanément; notre prototype actuel ne sait pas encore traiter ce second taux.

Il est donc important de ne pas qualifier chaque sortie d’A1 à A6 d’« ordre attendu affirmé par un test officiel ». Le code officiel fournit les entrées des démos; la spécification 2025 fournit une sortie complète pour son propre exemple à 25 %. [1] [2]

## Tests ajoutés maintenant : quota boursier seul

`tests/fixtures/official_order_call_examples.json` conserve les identifiants des cas, leurs entrées, leurs sources et l’origine de la sortie attendue. `tests/test_official_order_call_examples.py` compare ensuite la sortie entière du prototype à la liste fixe du fixture.

- **Exemple explicite du guide, taux de 25 %.** Les vingt personnes sont fournies dans l’ordre pédagogique. Le guide publie l’ordre d’appel exact : `B1, C1, C2, C3, B2, C4, C5, C6, B3, C7, …, C17`. C’est le meilleur test-oracle disponible pour l’instant, car l’entrée et la sortie apparaissent toutes deux dans la spécification officielle.
- **Démonstration A1, taux de 20 %.** Huit personnes, dont deux boursier·es classé·es 6e et 7e. Le fixture compare l’ordre complet, y compris le moment où le deuxième profil boursier doit remonter.
- **Démonstration A2, taux de 2 %.** Une seule personne boursière, classée 6e. Le cas vérifie qu’une faible proportion peut néanmoins imposer le premier appel lorsque le préfixe commence.
- **Démonstration A4, taux de 10 %.** Trois personnes boursières en positions 2, 3 et 8 parmi dix personnes. Le test vérifie que les candidat·es remontent uniquement quand le quota est contraignant, et que le classement pédagogique est autrement conservé.
- **Démonstration A3, 1 000 personnes, taux de 10 %.** Test à grande taille : 900 personnes non boursières précèdent les 100 personnes boursières. La sortie attendue est construite selon le motif annoncé par la règle : une personne boursière, puis neuf personnes dans l’ordre pédagogique, tant qu’il reste des boursier·es. Le test compare l’ordre complet, pas seulement le premier appel.

Les sorties A1/A2/A4/A3 sont figées ici comme sorties de référence **calculées d’après la spécification** et les entrées des démos. Contrairement au cas à 25 %, les tests JUnit de démonstration du dépôt officiel n’assertent pas ces listes exactes. Avant d’appeler ces fixtures « sorties de l’exécutable officiel », il faudra lancer le programme Java officiel sur les entrées et consigner la version et les résultats.

## Propriétés générales à compléter

Au-delà des exemples fixes, chaque ordre calculé doit satisfaire les invariants suivants :

- chaque candidat·e d’entrée apparaît exactement une fois en sortie;
- la liste ne perd ni n’ajoute de personne;
- si le taux est nul, l’ordre d’appel égale le classement pédagogique;
- lorsqu’un taux est contraignant et qu’il reste des candidat·es boursier·es, le prochain appel est boursier·e;
- à chaque préfixe, le minimum boursier annoncé est atteint, sauf si le vivier boursier est épuisé;
- un taux à 100 % appelle d’abord tous les boursier·es disponibles;
- l’ordre d’entrée mélangé ne change pas la sortie, puisque le rang et le statut sont les données déterminantes;
- les taux hors intervalle, rangs non positifs ou dupliqués, et identifiants dupliqués sont rejetés.

Les propriétés dites « de chaque préfixe » doivent être testées pour toute position, y compris la dernière et le cas où il n’y a plus de personne boursière à appeler. Ne pas vérifier uniquement le nombre global de boursier·es dans toute la liste.

## Suite à ajouter après l’extension aux deux taux

Une fois le taux de secteur géographique implémenté, ajouter des fixtures pour les démonstrations officielles A5 et A6. Elles doivent représenter explicitement quatre profils possibles : boursier·e du secteur, boursier·e hors secteur, non-boursier·e du secteur et non-boursier·e hors secteur.

Les tests à prévoir pour A5/A6 sont :

1. comparer l’ordre complet au résultat obtenu en exécutant le code officiel à la révision épinglée;
2. tester les situations où les deux taux sont contraignants et où les objectifs ne peuvent pas être respectés ensemble;
3. vérifier la priorité donnée au critère boursier dans le conflit prévu par la spécification;
4. vérifier la garantie du taux résident tel que précisément formulé dans la spécification — ne pas le remplacer par un simple quota de sièges indépendant;
5. tester les deux catégories qui se chevauchent et des réserves de personnes épuisées;
6. tester l’arrondi aux entiers supérieurs, les taux nuls et 100 %, le vivier vide et les rangs mélangés.

Les attentes complètes A5/A6 devront être générées avec le moteur officiel indépendant, et archivées avec les entrées, l’identifiant du commit, la commande d’exécution et un commentaire lisible. Si la sortie officielle n’est pas explicitement imprimée dans le document, la fixture devra être nommée « sortie de référence du commit … », pas « résultat publié dans le guide ».

## Tests distincts pour les propositions quotidiennes

Le prototype d’ordre d’appel ne simule pas les propositions journalières. Il ne faut donc pas conclure à la conformité du moteur entier après les tests précédents. Quand cette deuxième partie sera créée, ses fixtures devront tester séparément :

- ouverture par rang limite d’appel;
- envoi jusqu’au nombre de recrutements souhaité;
- propositions simultanées et plusieurs formations;
- réponse positive/négative, maintien en attente et libération d’une place;
- démission automatique des vœux moins préférés si le répondeur correspondant est activé;
- début/fin d’application des démissions automatiques selon la date;
- cas avec internat et réduction de barre pour ne pas dépasser la capacité;
- validité de chaque statut avant/après une journée simulée.

Le résultat de ces tests pourrait être comparé aux cas unitaires et exemples du moteur officiel de propositions. Un modèle Gale–Shapley, s’il est étudié, aura ses propres tests et restera un scénario alternatif, pas une comparaison directe du code quotidien actuel.

## Exécution

```bash
python -m unittest discover -s tests -v
```

## Références

[1]: https://services.dgesip.fr/fichiers/presentation_algorithmes_parcoursup_2025_finale.pdf "MESR, présentation des algorithmes de Parcoursup, section 4.1 et exemple à 25 %"

[2]: https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup "Dépôt public des algorithmes de Parcoursup, exemples A1–A6 et tests Java"
