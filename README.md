# ParcourSup : comprendre et améliorer l’algorithme

## Pourquoi ce projet ?

Parcoursup influence l’entrée dans les études après le bac. Les lycéen·nes et étudiant·es qui vivent la procédure doivent pouvoir participer à la définition des problèmes et des solutions.

Des témoignages publiés parlent d’attente, de décisions difficiles à comprendre, de stress, de refus et de contraintes de logement ou de transport. Des organisations lycéennes et étudiantes demandent aussi plus de places et la fin de la sélection via les plateformes. Ce sont des paroles importantes, mais elles ne représentent pas automatiquement l’avis de tout le monde. [Lire notre synthèse des témoignages, enquêtes et revendications](docs/retours-lyceen-ips-recherche.md).

Dans le baromètre CSA 2025, réalisé auprès de **1 005 néo-bacheliers inscrits sur Parcoursup**, **84 %** ont jugé la procédure stressante, **53 %** l’ont trouvée transparente et **34 %** juste et équitable. Ce sont des avis déclarés : ils ne prouvent pas, à eux seuls, que l’algorithme est la cause du stress. [Lire l’étude CSA](https://csa.eu/wp-content/uploads/2025/10/2500648-Baro-Parcoursup-2025-Resultats_1609_vSITE-CSA.pdf).

## En bref : comment fonctionne le système ?

1. **Chaque formation classe les candidatures.** Les équipes de la formation examinent les dossiers et établissent leur classement.
2. **Parcoursup établit un ordre d’appel.** Il part du classement de la formation et applique notamment des règles minimales liées aux élèves boursiers et au secteur géographique.
3. **Les propositions sont envoyées au fil de la campagne.** Le nombre de personnes appelées dépend aussi des places, des réglages de la formation et des réponses déjà reçues.
4. **Les candidat·es répondent.** Une proposition n’est pas la même chose qu’une admission acceptée; les refus et désistements peuvent libérer des places pour d’autres personnes.

**À retenir :** l’ordre d’appel n’est pas à lui seul tout Parcoursup. Et respecter un quota parmi les personnes appelées ne garantit pas automatiquement le même quota parmi celles qui acceptent une place.

## Quelques mots expliqués simplement

- **Classement de la formation :** l’ordre établi par la formation après l’examen des dossiers.
- **Ordre d’appel :** l’ordre dans lequel Parcoursup propose ensuite des places aux candidat·es en attente. Il peut différer du classement de la formation afin d’appliquer certaines règles.
- **Quota :** une part minimale de personnes répondant à un critère — par exemple être boursier·e — que la règle cherche à faire apparaître parmi les personnes appelées.
- **Liste d’attente :** les personnes qui n’ont pas encore reçu de proposition pour ce vœu, mais pourraient en recevoir une si des places se libèrent et si leur rang est atteint.
- **IPS :** un indice qui résume le contexte social moyen des familles d’un établissement. L’IPS d’un lycée n’est pas l’IPS personnel de chaque élève.

## Ce que nous testons pour l’instant

Ce dépôt contient un **petit prototype de recherche**, écrit en Python. Il compare :

- une version simplifiée de l’ordre d’appel avec taux boursier et taux lié au secteur géographique;
- une autre règle expérimentale, qui réserve une part des places aux candidat·es boursier·es avant de compléter le groupe selon le classement.

Ces règles ne font pas exactement la même chose : la première produit un ordre d’appel; la seconde choisit un groupe de personnes. On ne peut donc pas remplacer l’une par l’autre sans définir le mécanisme complet.

> **Ce prototype ne décide de l’admission de personne et ne reproduit pas toutes les règles de Parcoursup.** Il modélise un groupe de classement strict et deux taux, mais pas les internats, les groupes multiples ni les échanges quotidiens de propositions et de réponses. Les tests comparent des exemples au code et aux documents officiels; ils ne prouvent pas qu’une règle est juste pour l’ensemble des candidat·es.

## Audit IPS : descriptif seulement

Nous avons ajouté au dépôt le snapshot officiel de la DEPP pour la rentrée **2025-2026**, portant sur **3 662 lycées**. L’audit calcule des statistiques par établissement, sans pondération par le nombre d’élèves. La médiane de l’IPS d’établissement est de **100,30** dans le public et **119,50** dans le privé sous contrat; par type de lycée, elle est de **119,75** pour les LEGT, **90,20** pour les LP et **104,05** pour les LPO.

Ces chiffres décrivent les établissements, pas leurs élèves ni leurs chances d’admission. Nous n’avons pas de données de candidatures reliées au lycée d’origine; nous ne prétendons donc pas mesurer l’effet de l’IPS sur une admission. **L’IPS n’est pas transmis au calcul de l’ordre d’appel et ne change aucun rang.** [Lire l’audit et ses limites](docs/audit-descriptif-ips-2025-2026.md).

Les données sont agrégées, proviennent du jeu officiel de la DEPP et sont sous Licence Ouverte Etalab 2.0 selon le portail. [Lire les informations sur le snapshot et sa mise à jour](data/README.md).

## Simulation théorique d’une pondération progressive

Un outil séparé compare le classement de mérite à une priorité croissante pour les candidat·es provenant de lycées fictifs à IPS plus bas. Le scénario par défaut utilise **12 candidat·es inventé·es**, quatre lycées imaginaires et des poids de 0 à 40 %. Le score illustratif mélange le percentile de mérite et le rang de priorité IPS selon la formule `(1 - poids) × mérite + poids × contexte IPS`.

Dans cet exemple seulement, le top 6 reste le même à 0 et 10 %. À 20 %, une place du top 6 change : F08 en sort et F02 y entre; l’IPS moyen des lycées du groupe fictif passe de 110 à 103,33. Cela montre l’effet possible de la formule sur **cet échantillon fabriqué**, pas une amélioration réelle de l’équité ou des chances d’admission.

Le simulateur ne touche pas à `order_call.py`, ne calcule pas d’admissions Parcoursup et ne transforme pas l’IPS moyen du lycée en caractéristique individuelle. [Voir la formule, les hypothèses et les limites](docs/simulation-ponderation-progressive-ips.md).

### Page interactive

Une [visualisation web autonome](web/visualisation/README.md) permet de comparer plusieurs poids IPS côte à côte, de régler la taille du groupe fictif et de voir les rangs bouger dans un tableau et deux graphiques. Elle reprend les mêmes 12 profils inventés et la même formule que le simulateur Python. Elle reste séparée de l’ordre d’appel Parcoursup et ne prédit aucune admission.

Pour la lancer depuis la racine du dépôt :

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory web/visualisation
```

Puis ouvrir `http://127.0.0.1:8000/` dans un navigateur.

## Revendications et consultation

Les sources publiques suffisent pour dégager des sujets importants — transparence, attente, accompagnement, capacité d’accueil, contraintes matérielles et équité sociale — mais elles ne suffisent pas pour choisir les poids d’une règle. Les baromètres ne portent que sur une partie des usagers; les reportages racontent des situations particulières; les revendications engagent les organisations qui les portent.

Un [brouillon de questionnaire de consultation](docs/questionnaire-experiences-parcoursup.md) est prêt à être relu avec des jeunes avant diffusion. Il n’est **pas encore diffusé** : l’anonymat dépend aussi des réglages de l’outil, et la consultation devra inclure des parcours variés sans prétendre être un sondage représentatif.

## IPS et critère social : notre prudence

La première étape choisie est de décrire le contexte IPS des lycées, sans modifier les admissions. Une simulation de pondération progressive existe maintenant, mais **uniquement comme outil de sensibilité sur un échantillon fictif**. La moyenne du lycée ne décrit pas la situation de chaque élève. Les REP/REP+ désignent des réseaux d’écoles et de collèges, pas une catégorie générale de lycées : nous ne créons donc pas automatiquement une « priorité lycée REP ».

La [note sur l’IPS et le prototype](docs/prototype-ips-et-critere-social.md) présente les options futures. Tout usage d’un poids dans une règle réelle demanderait des choix explicites, une consultation des lycéen·nes et une vérification du cadre applicable.

## Nos principes

- Expliquer les règles dans des mots compréhensibles, y compris les raisons d’un refus ou d’une attente.
- Distinguer les choix techniques des choix politiques, comme le nombre de places ou le principe de sélection.
- Tester les effets sur des profils différents, pas seulement calculer une moyenne.
- Ne pas promettre des délais plus courts ou une meilleure équité avant de les avoir mesurés.
- Concevoir les critères de réussite avec les lycéen·nes, et pas seulement parler à leur place.
- Ne jamais confondre une moyenne d’établissement avec la situation individuelle d’un·e candidat·e.

## Où en est le projet ?

- [x] Lire et documenter des sources officielles sur le fonctionnement de Parcoursup.
- [x] Créer un premier prototype et le comparer à des exemples officiels de l’ordre d’appel.
- [x] Examiner les revendications publiques de lycéen·nes et les hypothèses du cahier des charges.
- [x] Analyser le code public de l’ordre d’appel et des propositions quotidiennes.
- [x] Ajouter des tests d’ordre exact pour l’exemple du guide à un taux, l’exemple à deux taux et les démos A1 à A6.
- [x] Recueillir des témoignages publiés, vérifier des enquêtes et distinguer les revendications collectives.
- [x] Préparer un questionnaire à relire avec les personnes concernées avant diffusion.
- [x] Étudier les limites d’un critère IPS et expliquer pourquoi REP/REP+ ne désigne pas une catégorie générale de lycées.
- [x] Charger le snapshot DEPP 2025-2026 et créer un audit descriptif de l’IPS sans effet sur l’ordre d’appel.
- [x] Créer une simulation de sensibilité à poids progressif sur un échantillon entièrement fictif, séparée de l’ordre d’appel.
- [x] Créer une visualisation web interactive pour comparer les pondérations, les rangs et les indicateurs du même échantillon fictif.
- [ ] Consulter directement des lycéen·nes aux parcours variés et intégrer leurs priorités choisies.
- [x] Étendre le modèle au secteur géographique et comparer A5/A6 au code officiel épinglé.
- [ ] Relier, sous un cadre autorisé, des données de candidatures aux contextes IPS pour étudier des résultats d’admission.
- [ ] Ajouter un simulateur distinct des propositions quotidiennes.
- [ ] Comparer les règles dans des simulations expliquées et reproductibles.

## Lancer les tests et l’audit

Il faut Python 3.10 ou une version plus récente. Aucune bibliothèque supplémentaire n’est nécessaire.

```bash
python -m unittest discover -s tests -v
PYTHONPATH=. python examples/audit_ips.py
PYTHONPATH=. python examples/simulate_progressive_ips.py
```

Pour voir l’exemple de comparaison des règles actuelles :

```bash
PYTHONPATH=. python examples/compare_policies.py
```

Pour télécharger un snapshot officiel plus récent, en précisant la rentrée :

```bash
python scripts/telecharger_ips.py --rentree 2025-2026
```

## Pour aller plus loin

Les documents ci-dessous donnent davantage de détails; il n’est pas nécessaire de les lire pour comprendre l’objectif général du projet.

- [Témoignages, enquêtes, revendications et sources officielles](docs/retours-lyceen-ips-recherche.md) — ce qui ressort des sources, et ce qu’elles ne permettent pas de conclure.
- [Audit descriptif IPS 2025-2026](docs/audit-descriptif-ips-2025-2026.md) — résultats calculés, méthode et limites.
- [Simulation théorique d’une pondération progressive](docs/simulation-ponderation-progressive-ips.md) — formule, exemple fictif, commandes et garde-fous.
- [Visualisation web interactive](web/visualisation/README.md) — comparaison des scénarios et lancement local de la page.
- [Questionnaire de consultation à relire avant diffusion](docs/questionnaire-experiences-parcoursup.md) — questions, précautions d’anonymat et méthode de restitution.
- [Intégrer l’IPS au prototype](docs/prototype-ips-et-critere-social.md) — options, données, simulations et tests à prévoir.
- [Les revendications lycéennes et l’audit du cahier des charges](docs/revendications-et-audit-cahier-des-charges.md) — demandes publiques et points à clarifier.
- [Analyse du code actuel et pistes d’amélioration](docs/analyse-algorithme-actuel-et-pistes.md) — fonctionnement actuel et améliorations possibles.
- [Critères d’optimisation et co-conception](docs/criteres-optimisation-et-co-conception.md) — critères testables sans cacher les choix politiques.
- [Plan des tests contre les références officielles](docs/plan-tests-validation-officiels.md) — exemples comparés et prochaines validations.
- [Analyse initiale](docs/analyse-initiale.md) — premières conclusions et questions ouvertes.

### Sources principales

- [Dépôt public du code de Parcoursup](https://gitlab.mim-libre.fr/parcoursup/algorithmes-de-parcoursup).
- [Présentation officielle des algorithmes de Parcoursup, 2025](https://services.dgesip.fr/fichiers/presentation_algorithmes_parcoursup_2025_finale.pdf).
- [Comité éthique et scientifique : recommandations sur la transparence des classements](https://www.enseignementsup-recherche.gouv.fr/fr/remise-du-rapport-annuel-2025-du-comite-ethique-et-scientifique-de-parcoursup-et-mon-master-101305).
- [Données IPS des lycées (DEPP)](https://data.education.gouv.fr/explore/assets/fr-en-ips-lycees-ap2023/).
