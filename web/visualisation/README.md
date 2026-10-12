# Rang en clair — visualisation IPS

Page statique en français pour explorer des scénarios théoriques de pondération progressive de l’IPS. Les 12 profils du fichier `data/candidates.json` reprennent le jeu fictif du prototype ParcourSup; aucune donnée de personne réelle n’est utilisée.

## Lancer dans l’environnement WebDev

```bash
python3 -m http.server 3000 --bind 0.0.0.0 --directory .
```

Aucune dépendance externe n’est nécessaire. Le manifeste de route se trouve dans `manus-routes.json`.

## Modèle illustratif

La priorité de mérite et la priorité de contexte IPS sont converties en percentiles dans le même échantillon. Le score est `(1 - poids IPS) × percentile de mérite + poids IPS × priorité de contexte`. Un IPS moyen de lycée plus bas reçoit ici une priorité de contexte plus élevée. Cette page ne reproduit pas l’ordre d’appel Parcoursup et ne prédit aucune admission réelle.
