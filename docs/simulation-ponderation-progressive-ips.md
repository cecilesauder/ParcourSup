# Simulation théorique d’une pondération progressive de l’IPS

## Ce que fait le script

Le script `examples/simulate_progressive_ips.py` compare, sur un petit jeu entièrement fictif, l’ordre obtenu avec plusieurs poids attribués au contexte IPS du lycée d’origine. Il s’agit d’un **outil de sensibilité pour discuter de la mécanique**, pas d’une proposition d’admission et pas d’une mesure de l’effet réel de l’IPS.

Le jeu [`examples/fixtures/fictional_candidates.csv`](../examples/fixtures/fictional_candidates.csv) contient 12 identifiants artificiels, quatre lycées explicitement fictifs et des valeurs inventées. Il ne reprend ni les UAI ni les dossiers de personnes réelles, et il n’est pas mélangé au snapshot DEPP.

## Formule de l’illustration

Pour chaque candidat·e, le script calcule deux rangs percentiles dans l’échantillon :

- le **rang de mérite** : meilleur score scolaire dans l’exemple = priorité proche de 1;
- la **priorité de contexte IPS** : IPS moyen plus bas du lycée = priorité proche de 1.

Le score combiné vaut :

```text
score = (1 - poids_IPS) × percentile_mérite
        + poids_IPS × priorité_contexte_IPS
```

Le poids varie par défaut de **0 % à 40 %**, par pas de 10 points. À 0 %, le classement est celui du mérite seul. À 40 %, le contexte IPS compte pour 40 % du score composite de cette illustration. Les égalités sont départagées d’abord par le rang de mérite, puis par l’identifiant fictif. On peut modifier les poids et la capacité avec les options de la commande.

Les percentiles sont calculés à l’intérieur des 12 lignes de l’exemple, avec des rangs moyens pour les égalités. Les priorités sociales dépendent donc de la composition de l’échantillon; elles ne sont pas un barème national. Les valeurs de poids sont des paramètres de démonstration, pas des taux validés par les lycéen·nes.

## Résultat du scénario par défaut

Avec une capacité fictive de six places, le top 6 ne change pas entre un poids de 0 % et un poids de 10 %. À 20 %, F08 sort du top 6 et F02 y entre. Dans le jeu fabriqué, la moyenne des IPS des lycées du top 6 passe alors de **110,00 à 103,33**. Les poids de 30 % et 40 % déplacent aussi des rangs, sans changer davantage les six identifiants retenus par rapport au scénario de 20 %.

Ce résultat illustre uniquement la formule et les données artificielles choisies. Il ne montre pas que la règle serait équitable, souhaitée par les lycéen·nes, légale ou bénéfique dans la réalité.

## Lancer et exporter

Depuis la racine du dépôt :

```bash
PYTHONPATH=. python examples/simulate_progressive_ips.py
```

Pour choisir d’autres poids et exporter le classement détaillé de chaque scénario :

```bash
PYTHONPATH=. python examples/simulate_progressive_ips.py \
  --capacity 6 --weights 0 0.05 0.10 0.20 0.30 \
  --output /tmp/simulation-ips.csv
```

Le résumé affiche les candidat·es dans le top-k fictif, l’IPS moyen des lycées de ce groupe, le nombre de places du top-k remplacées par rapport au poids 0 et les déplacements de rang. Il ne parle pas d’« admis·es » : un top-k simplifié n’est pas une admission Parcoursup.

## Garde-fous et limites

Le simulateur vit dans `parcoursup_prototype/progressive_ips.py`, à part de `order_call.py`. Il ne change pas le classement ou l’ordre d’appel existant. Il ne modélise ni les critères multiples d’une commission, ni les quotas boursier et géographique, ni la liste d’attente, ni les désistements, ni les inscriptions.

La moyenne IPS du lycée est un contexte agrégé. Le script n’invente pas un « IPS personnel » pour chaque candidat·e. Si la valeur IPS était absente dans de futures données, il faudrait décider et publier un traitement distinct; il ne faudrait pas la remplacer silencieusement par zéro.

Enfin, une pondération peut changer les rangs sans garantir une amélioration de l’équité. Ce script sert à voir **qui monte ou descend dans cet exemple précis** lorsque le poids change. Pour évaluer des conséquences réelles, il faudrait des données Parcoursup appropriées, une base juridique et des règles de gouvernance, puis une consultation de lycéen·nes aux parcours variés. Les valeurs par défaut ne préjugent d’aucun choix collectif.

## Tests

Les tests vérifient que le poids nul préserve le classement de mérite, que le top-k a la taille demandée, que des poids plus forts peuvent changer l’ordre sur les données fictives, et que les poids, capacités et identifiants invalides sont rejetés. Ils ne constituent pas une validation empirique ou normative.
