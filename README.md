# ParcourSup — laboratoire d’amélioration

Ce dépôt est un espace indépendant d’analyse et d’expérimentation autour des algorithmes de Parcoursup. Il part d’une exigence politique et pratique : **les lycéen·nes, premier·es concerné·es, doivent participer à la définition des problèmes, des critères d’évaluation et des changements proposés**. Une modification techniquement élégante n’est pas une amélioration si elle dégrade leur situation ou si elle est conçue sans leurs retours.

> **Statut : prototype de recherche, non destiné à la production.** Le code ici ne remplace pas le moteur de Parcoursup et ne reproduit pas toutes ses règles.

## Première piste étudiée

Le prototype compare deux objets différents :

1. l’ordre d’appel avec quota minimum de boursiers, formalisé pour le cas où le taux de résidents est nul;
2. une fonction de choix expérimentale à réserve de places pour les boursiers, qui sélectionne un ensemble de candidats à l’intérieur d’une capacité donnée.

La fonction de choix renvoie un **ensemble**, pas une liste d’appel. La traiter comme un simple nouvel ordre de classement serait incorrect. L’utiliser dans l’affectation différée suppose de définir le mécanisme complet, les préférences des candidat·es, les capacités, les règles d’acceptabilité et la politique en cas de places vacantes.

## Ce que nous savons — et ce qu’il reste à démontrer

Le code et la documentation officiels décrivent un ordre d’appel calculé une fois à partir du classement pédagogique et des taux applicables. Les propositions sont ensuite envoyées en continu dans cet ordre. Le nombre quotidien dépend aussi des réponses antérieures et de paramètres d’appel fixés par les formations. L’ordre d’appel seul ne suffit donc pas à démontrer une cause de délai ou un gain de vitesse.

Le saut au premier rang d’appel lorsqu’un quota est contraignant est une conséquence possible de la règle de préfixe, pas nécessairement un bug. Le supprimer implique d’évaluer explicitement l’équité, la conformité aux règles, les effets par groupe et la compréhension des candidat·es.

## État d’avancement

- [x] Analyse initiale des affirmations et des sources officielles.
- [x] Prototype du cas « quota boursiers seul » et de la fonction expérimentale à réserve.
- [x] Tests unitaires et vérification exhaustive de la substituabilité sur de petits ensembles.
- [ ] Recueillir et documenter les revendications exprimées directement par les lycéen·nes.
- [ ] Définir des critères de réussite compréhensibles par les candidat·es : lisibilité, rangs vécus, délais mesurés, résultats par groupe.
- [ ] Étendre le modèle aux taux résidents, aux règles de capacité et au calcul quotidien des propositions.
- [ ] Comparer les mécanismes par simulation avec des hypothèses et données publiées, sans confondre simulation et preuve d’impact réel.

## Lancer les tests

Python 3.10 ou plus récent, sans dépendance externe :

```bash
python -m unittest discover -s tests -v
```

Lancer l’exemple comparatif :

```bash
PYTHONPATH=. python examples/compare_policies.py
```

## Sources de référence

- [Dépôt officiel des algorithmes de Parcoursup](https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup) — code Java, tests, documentation et bac à sable.
- [Présentation officielle des algorithmes de Parcoursup, édition 2025](https://services.dgesip.fr/fichiers/presentation_algorithmes_parcoursup_2025_finale.pdf) — notamment §§ 2.4–2.5 et 4.
- [Castéran, *Vérification de l’algorithme de calcul des ordres d’appel…*](https://hal.science/hal-03388671/document) — spécification et travaux de vérification formelle.
- [Hafalir, Yenmez et Yildirim (2013), *Effective Affirmative Action in School Choice*](https://www.econometricsociety.org/publications/theoretical-economics/lookup/paper/8775) — modèle académique de réserves minoritaires et choix substituable dans son cadre.

Voir [l’analyse initiale](docs/analyse-initiale.md) pour le périmètre, les corrections apportées aux hypothèses de départ et les questions ouvertes.
