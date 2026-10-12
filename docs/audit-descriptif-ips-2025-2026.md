# Audit descriptif de l’IPS des lycées — rentrée 2025-2026

## Résultats calculés à partir du jeu DEPP

Le snapshot officiel utilisé est celui des **IPS des lycées pour 2025-2026**, téléchargé le 12 octobre 2026 depuis le jeu de données de la DEPP. Il comprend **3 662 lignes**, chacune associée à un lycée (UAI) pour cette rentrée. L’IPS d’établissement est renseigné dans **3 661 lignes**. Le fichier exact, ses champs, sa licence et son moyen de mise à jour sont documentés dans [`data/README.md`](../data/README.md).

Pour l’IPS de l’établissement, en comptant chaque lycée une fois et sans pondérer par le nombre de ses élèves, la moyenne est de **107,83**, la médiane de **106,60**, le premier quartile de **92,80** et le troisième de **119,90**. Les valeurs observées vont de **60,20 à 161,60**. Les quartiles sont calculés par rang le plus proche; la moyenne est arithmétique, non pondérée.

Les médianes descriptives par secteur sont de **100,30** pour les lycées publics et **119,50** pour les lycées privés sous contrat. Par type de lycée, elles sont de **119,75** pour les LEGT, **90,20** pour les LP et **104,05** pour les LPO. Les valeurs par voie sont également disponibles : la médiane est **116,15** pour la voie générale et technologique, **90,40** pour la voie professionnelle et **102,60** pour le post-bac.

Ces écarts décrivent la distribution des **établissements** du jeu. Ils ne décrivent pas directement les élèves, ne mesurent pas la probabilité d’être admis·e et ne prouvent pas qu’un type de lycée cause une différence de parcours. Les populations, les voies proposées, les territoires et les secteurs diffèrent. La DEPP rappelle que l’IPS est un indicateur synthétique et recommande de ne pas surinterpréter les écarts de trois points ou moins entre IPS moyens d’établissements [1].

## Valeurs absentes et interprétation

Une seule valeur d’IPS d’établissement est absente sur les 3 662 lycées. Les indicateurs par voie sont absents plus souvent : 1 148 IPS de voie générale et technologique, 1 555 de voie professionnelle et 1 620 post-bac ne sont pas renseignés dans ce snapshot. L’absence peut signifier que la voie n’est pas présente ou que la valeur n’est pas publiée, notamment lorsque le calcul porte sur moins de cinq élèves; il ne faut donc jamais remplacer ces valeurs par zéro ni classer automatiquement le lycée comme favorisé ou défavorisé [1].

Le jeu 2025-2026 inclut les territoires indiqués par la DEPP à compter de cette rentrée, notamment les collectivités d’outre-mer listées et la Nouvelle-Calédonie. Le champ de couverture n’est donc pas exactement celui des millésimes précédents [1]. La série a aussi une rupture méthodologique à partir de 2022 et la DEPP signale un changement important de remontée de la seconde PCS dans le privé sous contrat à partir de 2023 [1]. Ces comparaisons temporelles demandent de la prudence.

## Ce que cet audit permet — et ne permet pas

Cet audit confirme qu’un indicateur agrégé par lycée et par voie est disponible et que son niveau varie nettement selon le type d’établissement. Il peut servir à décrire un **contexte scolaire moyen** ou à préparer un futur contrôle d’effets distributifs.

Il ne permet pas de relier une candidature, un rang ou une proposition à l’IPS du lycée d’origine : le jeu ne contient aucune donnée Parcoursup, aucun classement pédagogique, aucune réponse de candidat·e et aucune inscription. Nous n’avons donc pas calculé d’écart de chances d’admission selon l’IPS. Il ne justifie pas non plus d’attribuer à un·e candidat·e la moyenne de son lycée comme si c’était sa situation sociale personnelle.

En conséquence, l’IPS reste **hors du calcul de l’ordre d’appel**. Le nouveau module charge le jeu et en décrit les valeurs séparément; le code `order_call_with_quotas` et les règles boursier·e/secteur ne changent pas. Le test de non-régression vérifie explicitement que l’audit ne modifie pas l’ordre.

## Reproduire l’audit

Depuis la racine du dépôt :

```bash
python -m unittest discover -s tests -v
PYTHONPATH=. python examples/audit_ips.py
```

Pour télécharger à nouveau un snapshot depuis l’API officielle :

```bash
python scripts/telecharger_ips.py --rentree 2025-2026
```

## Sources

[1]: https://data.education.gouv.fr/explore/assets/fr-en-ips-lycees-ap2023/ "DEPP — Indices de position sociale des lycées (à partir de 2023), jeu officiel et documentation"

[2]: https://www.education.gouv.fr/depp/quel-est-le-profil-social-des-lycees-452742 "DEPP — Quel est le profil social des lycées ?, Note d’Information n° 25-21"
