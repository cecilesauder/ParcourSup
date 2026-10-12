# Quels critères coder pour une affectation plus juste et compréhensible ?

## Notre principe de départ

Nous ne devrions pas cacher plusieurs choix politiques dans un unique « score d’équité ». Le programme doit d’abord respecter des règles annoncées, puis montrer clairement les compromis entre les résultats possibles. Les critères doivent être discutés avec les lycéen·nes avant de décider lequel prévaut lorsqu’ils entrent en conflit.

Les revendications actuellement documentées portent à la fois sur l’accès aux études souhaitées, le nombre de places, la fin de la sélection, la transparence, l’équité ressentie et le poids de l’attente. Certaines organisations demandent la fin de la sélection et 250 000 places supplémentaires; il s’agit de leur revendication publiée, pas d’une préférence universellement mesurée. [1] Le baromètre CSA 2025 montre un écart entre les ressentis : 83 % des jeunes interrogé·es disent la procédure stressante, contre 53 % qui la jugent transparente et 34 % juste et équitable. Parmi les candidat·es admis·es, 72 % sont satisfait·es des délais. Ces indicateurs portent sur des questions et des populations de réponse différentes; aucun ne suffit, seul, à dire quelle modification d’algorithme est juste. [2]

## Traduire les revendications en exigences testables

### 1. Accéder à une formation qui convient au candidat ou à la candidate

**Critère à étudier :** mesurer la part des candidat·es qui reçoivent une offre acceptable, et pas seulement le nombre d’offres produites ou le nombre de places qui finissent occupées.

**Point à décider avec les élèves :** comment le modèle saura-t-il qu’une formation « convient » ? L’acceptation effective d’une proposition donne une information après coup; elle ne dit pas forcément ce qui aurait été acceptable au début. Demander aux candidat·es de classer leurs vœux ou de signaler les formations acceptables constituerait une nouvelle donnée et pourrait changer leur comportement. Ne l’ajoutons pas en supposant que tout le monde souhaite classer ses vœux de la même manière.

### 2. Évaluer l’équité des résultats, pas seulement une règle de quota

**Critères à mesurer séparément :**

- chances de recevoir au moins une offre acceptable;
- accès au vœu préféré, ou au groupe de vœux défini comme acceptable si les élèves choisissent de le déclarer;
- temps passé sans offre acceptable;
- résultats selon des groupes pertinents, dans les limites des données disponibles et légalement utilisables;
- nombre d’appels, d’offres provisoires et d’admissions effectivement acceptées.

Un quota dans les **personnes appelées** ne garantit pas la même proportion dans les personnes qui acceptent une place. Il faudra donc présenter ces deux résultats à part. [3]

**À ne pas coder sans accord :** un coefficient de « mérite social » qui réordonnerait secrètement les personnes, une pondération arbitraire des groupes, ou une égalité de résultats imposée comme si elle était la seule définition possible de l’équité. Nous pourrons comparer plusieurs politiques et leurs écarts, mais il faudra rendre visible qui a choisi les groupes et les objectifs.

### 3. Rendre chaque décision explicable et vérifiable

La transparence n’est pas simplement une note ajoutée au classement. Pour chaque décision simulée, le code devrait pouvoir expliquer, dans un langage simple :

- quel classement de départ a été utilisé;
- quelles règles de priorité ou quels quotas s’appliquaient;
- si un quota était contraignant à cette étape;
- pourquoi une personne a été appelée avant une autre, ou pourquoi une offre n’a pas été produite;
- quelles données et quels réglages de la formation ont influencé l’étape.

On peut aussi produire une trace technique lisible par les équipes d’audit, et sa traduction courte pour les candidat·es. Cela rejoint la recommandation du Comité éthique et scientifique de publier le code ou une spécification des classements, les facteurs, les départages et les paramètres qui modifient l’ordre d’affichage. [4]

### 4. Réduire l’incertitude sans promettre une place

**Mesures à tester :** jour de la première offre; jour de la première offre acceptable; nombre de jours sans offre acceptable; délai auquel 50 %, 90 % ou 95 % des places sont stabilisées; écarts entre candidat·es et formations; nombre de propositions annulées ou libérées.

Le délai moyen seul peut masquer les personnes qui attendent le plus longtemps. Il faut donc publier une médiane et des percentiles élevés, ainsi que les hypothèses de simulation. Un ordre d’appel plus rapide à calculer ne prouve pas que les candidat·es attendront moins longtemps : dans le code public, les propositions quotidiennes dépendent aussi des réponses, des seuils de formation, des places libérées et, parfois, des internats. [3]

La clarté de l’interface et les alertes pourraient être améliorées sans changer la règle de sélection. Ces changements doivent être testés avec des élèves : comprennent-ils ce qui peut encore bouger, et ce qui n’est qu’une estimation ?

### 5. Reconnaître ce que le code ne peut pas décider

Si le nombre de places est inférieur au nombre de demandes, un mécanisme de priorité répartit la rareté; il ne la supprime pas. Le dépôt devra donc comparer les règles à capacité constante avec des scénarios où le nombre de places augmente. Le scénario « accès sans sélection » demandé par certaines organisations doit rester visible comme option politique distincte, même s’il ne se réduit pas à une fonction de classement. [1]

## Les algorithmes à comparer dans le code

### Modèle A — reproduire l’ordre d’appel public

C’est notre référence : coder en Python, indépendamment, les règles publiées pour les taux boursier et du secteur géographique, les personnes qui relèvent des deux catégories, l’arrondi, les cas où un vivier est épuisé et la priorité applicable lorsque les objectifs se contredisent. Comparer les sorties à des exemples officiels et aux tests du dépôt public.

Cette étape ne vise pas à optimiser la politique. Elle nous assure que nous comparons une variante à une représentation compréhensible du système de référence, et non à un prototype trop simplifié. La minimalité des inversions donnée par la spécification dans le seul cas d’un quota boursier doit être conservée comme propriété de référence à vérifier, sans la généraliser aux autres cas. [3]

### Modèle B — simuler les propositions quotidiennes du système actuel

Une deuxième brique reprendra, dans un périmètre annoncé, les règles publiques d’appel au fil des jours : ordre d’appel, seuil de rang, nombre de recrutements visé, places disponibles, réponses des candidat·es et libérations de places. Les internats pourront être ajoutés ensuite. Le but est de mesurer les délais et les situations d’attente dans un modèle défini; ce ne sera pas une prévision garantie des résultats nationaux. [3]

### Modèle C — tester une réserve de places comme alternative, pas comme correction évidente

La règle expérimentale devra être une fonction de choix : pour une formation et un groupe de candidatures, elle renvoie les personnes retenues, pas une nouvelle liste d’appel. Elle peut être intégrée à une simulation d’acceptation différée où les candidat·es proposent leurs vœux par ordre de préférence, puis où les formations gardent les personnes retenues par leur fonction de choix.

Avant de produire des résultats, nous devrons publier les règles de la variante :

- capacité de chaque formation;
- définition du classement pédagogique;
- objectifs boursier et géographique;
- traitement des personnes qui appartiennent aux deux catégories, sans compter une personne deux fois;
- arbitrage explicite si les contraintes ne peuvent être respectées ensemble;
- libération des places réservées mais inutilisées;
- façon de représenter les préférences et les vœux acceptables des candidat·es.

Nous ne supposerons pas que plusieurs réserves qui se recouvrent sont automatiquement stables ou équitables. La substituabilité devra être testée sur des cas exhaustifs de petite taille; si elle échoue, il faudra revoir la fonction de choix ou reconnaître que certaines garanties ne sont pas établies. Le résultat théorique publié sur une réserve minoritaire ne prouve pas une variante à plusieurs réserves pour Parcoursup. [5]

## Règle de décision recommandée pour comparer les politiques

Au lieu d’additionner tous les objectifs dans une formule opaque, nous proposons trois niveaux :

1. **Contraintes annoncées :** capacité, règles juridiques retenues, absence de double attribution d’une même place, choix exprimés par les candidat·es et données autorisées.
2. **Critères de comparaison publiés séparément :** offres acceptables, résultats par groupe, déplacements dans l’ordre d’appel, délais, stabilité et compréhension des décisions.
3. **Décision collective sur les compromis :** présenter les politiques qui font mieux sur certains critères et moins bien sur d’autres. Ne pas attribuer des poids cachés qui prétendraient produire une réponse « mathématiquement neutre » à un désaccord politique.

## Tests que nous voulons avoir avant de conclure

- **Conformité :** exemples officiels, arrondis, quota nul ou maximal, catégorie absente, chevauchement boursier/secteur, capacité nulle et égalités de rang.
- **Propriétés de la règle :** respect des contraintes annoncées; pas de double attribution; places restantes remises en jeu selon la règle publiée; substituabilité et stabilité lorsqu’elles sont revendiquées.
- **Comparaison :** sorties du modèle A contre le modèle B, puis contre le modèle C, avec cohortes synthétiques et hypothèses publiques.
- **Équité :** métriques par groupe, avec résultats d’appel séparés des résultats d’admission acceptée.
- **Compréhension :** faire lire des explications à des lycéen·nes et vérifier qu’elles comprennent pourquoi le résultat apparaît et ce qui peut encore changer.
- **Robustesse :** faire varier les capacités, préférences, réponses et hypothèses de participation; rapporter les cas défavorables, pas uniquement la moyenne.

## Points à trancher avec les lycéen·nes avant de figer les critères

- Qu’est-ce qui constitue une issue acceptable : toute place, une formation choisie par la personne, ou un sous-ensemble de ses vœux ?
- Quelles dimensions d’équité veulent-elles prioriser et comment les mesurer ?
- Quelle part de déplacement du classement scolaire leur paraît justifiée pour réduire les écarts sociaux ou territoriaux ?
- Veulent-elles déclarer un ordre de préférence entre formations, et avec quelles garanties contre la pression ou la stratégie ?
- Quel type d’attente est le plus pénible : délai avant toute proposition, absence de place souhaitée, ou manque d’information sur l’évolution ?
- Quels profils de candidat·es doivent participer à la conception et à la validation des explications ?

Ces questions sont des décisions de projet à documenter, pas des paramètres techniques à choisir en secret. Elles guideront les prochains critères et les tests avant tout changement de la règle d’admission.

## Références

[1]: https://union-etudiante.fr/10mesures/ "Union étudiante et organisations signataires, revendications pour la jeunesse"

[2]: https://csa.eu/wp-content/uploads/2025/10/2500648-Baro-Parcoursup-2025-Resultats_1609_vSITE-CSA.pdf "Institut CSA, Baromètre Parcoursup 2025"

[3]: https://services.dgesip.fr/fichiers/presentation_algorithmes_parcoursup_2025_finale.pdf "MESR, présentation des algorithmes de Parcoursup, édition 2025"

[4]: https://www.enseignementsup-recherche.gouv.fr/fr/remise-du-rapport-annuel-2025-du-comite-ethique-et-scientifique-de-parcoursup-et-mon-master-101305 "MESR, recommandations du Comité éthique et scientifique de Parcoursup et Mon Master, 2025"

[5]: https://www.econometricsociety.org/publications/theoretical-economics/lookup/paper/8775 "Hafalir, Yenmez et Yildirim, Effective Affirmative Action in School Choice, 2013"
