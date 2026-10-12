# Intégrer l’IPS au prototype : proposition, garde-fous et choix à trancher

## Recommandation en bref

**Ne pas créer de catégorie « lycée REP » et ne pas attribuer l’IPS du lycée comme si c’était l’IPS personnel d’un·e candidat·e.** Les REP/REP+ sont des réseaux formés d’écoles et d’un collège; ils ne constituent pas une étiquette générale des lycées [1]. L’IPS publié par la DEPP est une moyenne de lycée ou de voie, c’est-à-dire un indicateur de contexte agrégé, pas le profil social de chaque élève [2][3].

La première étape devrait être un **audit descriptif sans effet sur l’ordre d’appel** : charger une version millésimée des données IPS, puis vérifier comment les résultats simulés se répartissent selon le contexte des lycées d’origine. Ensuite seulement, on pourrait comparer des scénarios de priorité contextuelle, avec des paramètres explicites, à la règle de base et aux critères individuels déjà présents.

Cela permet d’étudier la question sociale sans décider à la place des lycéen·nes du poids à accorder à chaque critère. Le prototype n’est pas une règle officielle et cette note ne constitue pas un avis juridique.

## Pourquoi ne pas utiliser « REP/REP+ » comme critère lycée ?

- La politique REP/REP+ décrit des **réseaux collège-écoles**, pas une classification ordinaire des lycées [1].
- Le jeu administratif 2023 consulté distingue les établissements REP/REP+ de ceux seulement situés à proximité d’un quartier prioritaire; son filtre « lycée » n’identifie pas de lycée classé REP/REP+ pour ce millésime [4]. Une proximité QPV, un ancien collège REP ou une autre politique territoriale ne sont pas interchangeables.
- Attribuer un bonus à toutes les personnes d’un lycée donné ferait une **inférence écologique** : la moyenne d’un établissement ne dit pas la situation d’un·e élève. Elle pourrait aussi masquer les élèves défavorisé·es d’un lycée favorisé et l’hétérogénéité interne d’un lycée moins favorisé.
- Un label scolaire est sensible au millésime, au périmètre et aux changements d’établissement. Il ne faut donc pas le convertir automatiquement en droit individuel ou en score secret.

## Ce que mesure l’IPS — et ses limites pratiques

La DEPP calcule l’IPS à partir de la ou des professions et catégories socioprofessionnelles (PCS) déclarées pour les parents; l’indice résume des dimensions sociales et culturelles en moyenne [2]. Pour les lycées, les données ouvertes indiquent notamment un IPS moyen par établissement, et selon le jeu une déclinaison par voie ainsi qu’un écart-type décrivant l’hétérogénéité [3].

Les données récentes sont associées à un UAI et à une rentrée scolaire. Elles couvrent les lycées publics et privés **sous contrat** du champ décrit; les établissements hors champ et certaines valeurs faibles ou masquées nécessitent une règle de traitement explicite [3]. La DEPP signale une rupture méthodologique à partir de la rentrée 2022 et déconseille de surinterpréter des écarts d’IPS moyens de trois points ou moins [3][5].

> Il faut parler de **contexte IPS du lycée / de la voie d’origine**, pas d’« IPS du candidat ».

## Trois options possibles

| Option | Ce qu’elle ferait | Intérêt | Risques / choix non résolus |
|---|---|---|---|
| **A. Audit descriptif seul — recommandé d’abord** | L’IPS est joint aux données synthétiques ou de test; il ne change ni le classement ni l’ordre d’appel. On compare les résultats par groupes de contexte. | Mesure les écarts et valide les données sans créer un avantage d’admission. | Ne corrige pas en soi une éventuelle inégalité; les conclusions dépendent des données d’entrée et des métriques choisies. |
| **B. Scénario de représentation minimale** | Dans une branche expérimentale, un paramètre garantit une proportion minimale de personnes appelées provenant de lycées situés dans une bande IPS pré-définie. | Facile à comparer, en principe lisible; peut être testé en parallèle des taux de bourse et de secteur déjà modélisés. | Il faut décider la bande IPS, le taux, le groupe d’origine, la priorité en cas de conflit, la faisabilité et le traitement des données absentes. C’est un choix politique et potentiellement juridique, pas une conséquence automatique de l’IPS. |
| **C. Bonus de rang lié à l’IPS du lycée** | Le rang pédagogique serait modifié d’après l’IPS moyen du lycée d’origine. | Produit un effet gradué plutôt qu’un groupe binaire. | Plus difficile à expliquer; le poids et la fonction de transformation seraient arbitraires sans co-conception; un petit écart de données pourrait changer l’ordre. **À ne pas coder avant décision explicite.** |

Le critère individuel de bourse actuellement modélisé doit rester distinct de l’IPS d’établissement. Le code de l’éducation décrit, dans les formations concernées, des taux minimaux portant sur des bacheliers boursiers; il ne crée pas une priorité nationale générale nommée « lycée REP » ou « faible IPS » [6]. Il faut aussi garder distincts le classement de la formation, l’ordre d’appel, une proposition, son acceptation et l’inscription finale [6][7].

## Modèle de données proposé pour une première étape

L’indicateur devrait être porté par un objet de **contexte d’établissement**, puis référencé par le dossier synthétique du candidat. Ne pas ajouter un champ appelé `applicant_ips`.

```text
ContexteLycee
- uai_lycee_origine
- annee_scolaire_ips
- ips_etablissement (valeur ou absent)
- ips_voie (valeur ou absent; voie associée au parcours)
- ecart_type_ips (si disponible)
- effectif / état de masquage (si disponible)
- source et version du jeu de données

Candidat·e de simulation
- rang_pedagogique
- statut_boursier (distinct)
- statut_secteur (distinct)
- contexte_lycee (facultatif; référence à ContexteLycee)
```

Règles de traitement à fixer avant le chargement :

- joindre par **UAI + année scolaire + périmètre/voie**; ne pas faire une jointure sur le seul nom du lycée;
- conserver la source, le millésime et la version de la table afin que le calcul soit reproductible;
- si le lycée, l’année, la voie ou l’IPS est inconnu/absent/masqué, le noter comme **non renseigné**; ne jamais traiter une donnée absente comme un IPS élevé ou comme une raison d’exclure;
- ne pas fusionner directement les séries IPS antérieures et postérieures à la rupture de méthode sans la précaution publiée par la DEPP;
- ne pas déduire une catégorie REP/REP+ d’un score IPS ni l’inverse;
- si une simulation utilise une catégorie « IPS bas », définir son seuil, sa population de référence et sa date dans le scénario, et afficher ces paramètres avec le résultat.

## Plan recommandé pour la suite du prototype

### Étape 1 — Importer et documenter, sans effet sur les admissions

Créer un petit adaptateur pour le jeu de données public, ou d’abord une fixture miniature versionnée. Vérifier les colonnes, les UAI, les voies, les millésimes, les valeurs manquantes et les règles de masquage. Ne conserver que les données agrégées nécessaires.

### Étape 2 — Produire un audit de référence

Sur des cas synthétiques ou des données autorisées, calculer les résultats de la règle actuelle et les présenter par contexte IPS, voie, bourse et secteur. Publier les dénominateurs, les groupes absents, les écarts d’ordre et les limites. **Aucun rang ne change à cette étape.**

### Étape 3 — Comparer des scénarios explicitement paramétrés

Si les ateliers/questionnaire concluent qu’une mesure contextuelle mérite un test, ajouter une fonction séparée du calcul officiel, par exemple `simulate_contextual_minimum(...)`. Ne pas modifier silencieusement `order_call_with_quotas`. Comparer au minimum :

- la règle actuelle sans IPS;
- une variante descriptive sans effet sur l’appel;
- un ou plusieurs scénarios B dont les seuils et proportions sont visibles;
- si le groupe n’a pas assez de candidat·es éligibles, le scénario doit signaler que le minimum est impossible, plutôt que cacher une dérogation;
- chaque conflit entre bourse, secteur et contexte IPS doit avoir une règle de priorité approuvée et documentée avant de produire un ordre.

Ne pas adopter de taux ou seuils définitifs avant d’avoir consulté des lycéen·nes aux parcours variés et vérifié le cadre juridique applicable.

## Tests à prévoir

1. **Neutralité de la métadonnée :** ajouter ou retirer l’IPS dans le mode audit ne modifie jamais l’ordre d’appel courant; les exemples officiels A5/A6 continuent de passer.
2. **Provenance :** une jointure UAI/année/voie sélectionne le bon millésime; aucun appariement par nom approximatif.
3. **Donnée absente :** IPS masqué ou inconnu ne pénalise pas le ou la candidat·e; le cas est rapporté séparément.
4. **Pas de confusion individuel/agrégé :** les sorties disent « IPS moyen du lycée/de la voie », jamais « position sociale de la personne ».
5. **Robustesse aux frontières :** tester les valeurs autour du seuil du scénario, les arrondis et des écarts inférieurs ou égaux à trois points; ces petits écarts ne doivent pas être présentés comme des différences sociales certaines.
6. **Effets croisés :** couvrir toutes les intersections bourse × secteur × contexte, y compris des cas où les trois objectifs ne peuvent pas être satisfaits simultanément.
7. **Faisabilité :** aucun taux cible ne dépasse le nombre de personnes admissibles dans le groupe; l’impossibilité est explicite.
8. **Explicabilité :** pour chaque candidat·e déplacé·e dans un scénario, fournir un journal lisible indiquant quel paramètre a changé l’ordre et pourquoi.
9. **Non-régression :** les tests et fixtures de référence officiels déjà existants restent inchangés pour le mode actuel.

## Décision à prendre avant toute modification de l’ordre d’appel

La proposition recommandée est : **commencer par l’Option A**, intégrer l’IPS comme donnée agrégée de contexte uniquement pour auditer les résultats, puis décider avec les lycéen·nes si l’Option B mérite une simulation séparée. L’Option C n’est pas recommandée à ce stade. Le choix entre un indicateur de contexte, un critère individuel et un mécanisme sans bonus d’admission change matériellement la règle : il ne doit pas être décidé par défaut dans le code.

## Sources

1. [Éduscol — Les réseaux d’éducation prioritaire REP et REP+](https://eduscol.education.gouv.fr/4896/la-politique-de-l-education-prioritaire-les-reseaux-d-education-prioritaire-rep-et-rep).
2. [DEPP — Indice de position sociale (IPS) : actualisation 2022](https://www.education.gouv.fr/depp/indice-de-position-sociale-ips-actualisation-2022-452271).
3. [DEPP — Indices de position sociale des lycées (données récentes)](https://data.education.gouv.fr/explore/assets/fr-en-ips-lycees-ap2023/).
4. [Jeu officiel — Établissements de l’éducation prioritaire, requête filtrée sur « lycée »](https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-etablissements-ep/records/?select=uai%2Cep_2022_2023%2Cnom_etablissement%2Ctype_etablissement%2Cuai_tete_de_reseau%2Cqp_a_proximite_o_n&where=type_etablissement%20%3D%20%27Lyc%C3%A9e%27&limit=100&lang=fr).
5. [DEPP — Quel est le profil social des lycées ?](https://www.education.gouv.fr/depp/quel-est-le-profil-social-des-lycees-452742).
6. [Code de l’éducation, article L. 612-3](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053152525/).
7. [Comité éthique et scientifique — 7e rapport sur Parcoursup et Mon Master](https://www.enseignementsup-recherche.gouv.fr/sites/default/files/2025-03/7e-rapport-du-comit-thique-et-scientifique-parcoursup-et-mon-master-36400.pdf).
8. [Rapport de recherche du projet : témoignages, règles et limites de la donnée IPS](retours-lyceen-ips-recherche.md).
