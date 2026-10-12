# ParcourSup : comprendre et améliorer l’algorithme

## Pourquoi ce projet ?

Parcoursup influence l’entrée dans les études après le bac. Les lycéen·nes, qui vivent la procédure, doivent participer à la définition des problèmes et des solutions.

Le manque de transparence revient souvent dans les critiques. Dans le baromètre CSA 2025, réalisé auprès de 1 005 jeunes inscrits sur Parcoursup, **83 %** ont jugé la procédure stressante, **53 %** l’ont trouvée transparente et **34 %** juste et équitable. Ce sont des avis recueillis après la campagne : ces chiffres ne prouvent pas, à eux seuls, que l’algorithme est la cause du stress. [Lire l’étude CSA](https://csa.eu/wp-content/uploads/2025/10/2500648-Baro-Parcoursup-2025-Resultats_1609_vSITE-CSA.pdf).

Certaines organisations lycéennes et étudiantes demandent aussi **plus de places et la fin de la sélection**. Une modification de l’algorithme ne peut pas créer de places ni décider, à elle seule, de supprimer la sélection. Ces choix doivent être discutés ouvertement. [Voir leurs revendications](https://union-etudiante.fr/10mesures/).

## En bref : comment fonctionne le système ?

1. **Chaque formation classe les candidatures.** Les équipes de la formation examinent les dossiers et établissent leur classement.
2. **Parcoursup établit un ordre d’appel.** Il part du classement de la formation et applique notamment des règles minimales liées aux élèves boursiers et au secteur géographique.
3. **Les propositions sont envoyées au fil de la campagne.** Le nombre de personnes appelées dépend aussi des places, des réglages de la formation et des réponses déjà reçues.
4. **Les candidat·es répondent.** Une proposition n’est pas la même chose qu’une admission acceptée; les refus et désistements peuvent libérer des places pour d’autres personnes.

**À retenir :** l’ordre d’appel n’est pas à lui seul l’algorithme complet de Parcoursup. Et respecter un quota parmi les personnes appelées ne garantit pas automatiquement le même quota parmi celles qui acceptent une place.

## Quelques mots expliqués simplement

- **Classement de la formation :** l’ordre établi par la formation après l’examen des dossiers.
- **Ordre d’appel :** l’ordre dans lequel Parcoursup propose ensuite des places aux candidat·es en attente. Il peut différer du classement de la formation afin d’appliquer les règles de quota.
- **Quota :** une part minimale de personnes répondant à un critère — par exemple être boursier·e — que la règle cherche à faire apparaître parmi les personnes appelées.
- **Liste d’attente :** les personnes qui n’ont pas encore reçu de proposition pour ce vœu, mais pourraient en recevoir une si des places se libèrent et si leur rang est atteint.
- **Fonction de choix :** une règle qui sélectionne un groupe de personnes à partir des candidatures et des places disponibles. Elle ne produit pas forcément une liste ordonnée.

## Ce que nous testons pour l’instant

Ce dépôt contient un **petit prototype de recherche**, écrit en Python. Il compare :

- une version simplifiée de l’ordre d’appel avec taux boursier et taux lié au secteur géographique;
- une autre règle expérimentale, qui réserve une part des places aux candidat·es boursier·es avant de compléter le groupe selon le classement.

Ces deux règles ne font pas exactement la même chose : la première produit un ordre d’appel; la seconde choisit un groupe de personnes. On ne peut donc pas remplacer l’une par l’autre sans définir le mécanisme complet.

> **Ce prototype ne décide de l’admission de personne et ne reproduit pas toutes les règles de Parcoursup.** Il modélise un groupe de classement strict et les deux taux, mais pas les internats, les groupes multiples ni les échanges quotidiens de propositions et de réponses. Les tests comparent des exemples au code et aux documents officiels; ils ne prouvent pas qu’une règle est juste pour l’ensemble des candidat·es.

## Nos principes

- Expliquer les règles dans des mots compréhensibles, y compris les raisons d’un refus ou d’une attente.
- Distinguer les choix techniques des choix politiques, comme le nombre de places ou le principe de sélection.
- Tester les effets sur des profils différents, pas seulement calculer une moyenne.
- Ne pas promettre des délais plus courts ou une meilleure équité avant de les avoir mesurés.
- Concevoir les critères de réussite avec les lycéen·nes, et pas seulement parler à leur place.

## Où en est le projet ?

- [x] Lire et documenter des sources officielles sur le fonctionnement de Parcoursup.
- [x] Créer un premier prototype et le comparer à des exemples officiels de l’ordre d’appel.
- [x] Examiner les revendications publiques de lycéen·nes et les hypothèses du cahier des charges.
- [x] Analyser le code public de l’ordre d’appel et des propositions quotidiennes.
- [x] Ajouter des tests d’ordre exact pour l’exemple du guide à un taux, l’exemple à deux taux et les démos A1 à A6.
- [ ] Recueillir directement les priorités de lycéen·nes aux parcours variés.
- [x] Étendre le modèle au secteur géographique et comparer A5/A6 au code officiel épinglé.
- [ ] Ajouter un simulateur distinct des propositions quotidiennes.
- [ ] Comparer les règles dans des simulations expliquées et reproductibles.

## Lancer les tests

Il faut Python 3.10 ou une version plus récente. Aucune bibliothèque supplémentaire n’est nécessaire.

```bash
python -m unittest discover -s tests -v
```

Pour voir un exemple de comparaison :

```bash
PYTHONPATH=. python examples/compare_policies.py
```

## Pour aller plus loin

Les documents ci-dessous donnent davantage de détails; il n’est pas nécessaire de les lire pour comprendre l’objectif général du projet.

- [Les revendications lycéennes et l’audit du cahier des charges](docs/revendications-et-audit-cahier-des-charges.md) — ce qui est demandé et les points à clarifier.
- [Analyse du code actuel et pistes d’amélioration](docs/analyse-algorithme-actuel-et-pistes.md) — explication plus technique du calcul de l’ordre d’appel et des propositions.
- [Critères d’optimisation et co-conception](docs/criteres-optimisation-et-co-conception.md) — comment traduire les revendications en critères testables sans cacher les choix politiques.
- [Plan des tests contre les références officielles](docs/plan-tests-validation-officiels.md) — les exemples comparés, la provenance des sorties et les prochaines validations.
- [Analyse initiale](docs/analyse-initiale.md) — premières conclusions, vérifications et questions ouvertes.

### Sources principales

- [Dépôt public du code de Parcoursup](https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup).
- [Présentation officielle des algorithmes de Parcoursup, 2025](https://services.dgesip.fr/fichiers/presentation_algorithmes_parcoursup_2025_finale.pdf).
- [Comité éthique et scientifique : recommandations sur la transparence des classements](https://www.enseignementsup-recherche.gouv.fr/fr/remise-du-rapport-annuel-2025-du-comite-ethique-et-scientifique-de-parcoursup-et-mon-master-101305).
