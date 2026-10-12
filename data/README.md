# Données IPS des lycées

`ips_lycees_2025-2026.csv` est un extrait agrégé du jeu officiel **Indices de position sociale des lycées (à partir de 2023)**, produit par la DEPP. Il contient les 3 662 enregistrements de la rentrée scolaire 2025-2026 et les champs nécessaires à l’audit du projet. Le jeu a été consulté le 12 octobre 2026.

- Page officielle : <https://data.education.gouv.fr/explore/assets/fr-en-ips-lycees-ap2023/>
- API utilisée : <https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-ips-lycees-ap2023/records>
- Filtre appliqué : `rentree_scolaire='2025-2026'`.
- Licence affichée par le portail : Licence Ouverte v2.0 (Etalab).
- Attribution : DEPP — ministère chargé de l’Éducation nationale, *Indices de position sociale des lycées (à partir de 2023)*, rentrée 2025-2026; extrait préparé par le projet ParcourSup.
- SHA-256 du snapshot inclus : `e6776e1f00c7cf16fa42c5e75a612d53a6a338e09df2f271b0c7dc717dc7e496`.
- Le snapshot peut être recréé avec `python scripts/telecharger_ips.py --rentree 2025-2026`.

Le fichier contient une ligne par UAI et rentrée, avec le secteur, le type de lycée, l’IPS moyen de l’établissement, les IPS des voies lorsque disponibles et les écarts-types publiés. Il s’agit d’une sélection de colonnes du jeu officiel, sans modification des valeurs récupérées. Il ne contient pas de dossier individuel de candidature. **L’IPS du lycée est un contexte agrégé, pas l’IPS personnel d’un·e élève.**

Le portail indique que les valeurs d’IPS ne sont pas renseignées lorsqu’elles reposent sur moins de cinq élèves. Une valeur absente ne doit jamais être convertie en zéro, assimilée à un lycée favorisé, ni utilisée pour pénaliser une candidature. Certaines voies n’existent pas dans tous les établissements, ce qui explique aussi l’absence de valeurs par voie.

Pour rafraîchir le snapshot, exécuter le script de téléchargement, puis relancer les tests et l’exemple d’audit. Garder la date et le millésime exacts lorsque les résultats sont cités. La série a une rupture méthodologique à partir de la rentrée 2022; ne pas comparer les millésimes comme s’ils formaient une série parfaitement homogène.
