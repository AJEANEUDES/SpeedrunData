# Rapport Détaillé du Projet d'Analyse de Speedruns
Date: 2024-12-17

## 1. Vue d'ensemble du projet

Ce projet est une application d'analyse de données de speedruns qui collecte, traite et visualise les performances des joueurs à partir de l'API speedrun.com. L'application est accessible en ligne à l'adresse : https://speedrundata.streamlit.app/

### 1.1 Objectifs du projet
- Collecter des données de speedruns pour différents jeux
- Analyser les performances des joueurs
- Visualiser les statistiques et tendances
- Calculer des métriques de difficulté

### 1.2 Jeux analysés
- Super Mario Bros.
- Super Mario 64
- Mega Man
- Super Meat Boy

## 2. Architecture technique

### 2.1 Structure du projet
```
speedrundata/
├── config/
│   ├── api_config.py      # Configuration de l'API
│   └── settings.py        # Paramètres globaux
├── src/
│   ├── api/
│   │   └── speedrun_api.py    # Interface API
│   ├── data/
│   │   ├── collector.py       # Collecte de données
│   │   └── processor.py       # Traitement des données
│   ├── utils/
│   │   ├── data_loader.py     # Chargement des données
│   │   ├── platform_mapping.py # Mapping des plateformes
│   │   ├── validators.py      # Validation des données
│   │   └── error_handlers.py  # Gestion des erreurs
│   └── visualization/
│       └── dashboard.py       # Interface Streamlit
└── main.py                    # Point d'entrée
```

### 2.2 Technologies utilisées
- Python 3.8+
- Streamlit pour l'interface
- Pandas pour le traitement des données
- Plotly pour les visualisations
- Requests pour les appels API

## 3. Fonctionnalités détaillées

### 3.1 Collecte de données
- Pagination automatique des requêtes API
- Gestion des limites de taux (rate limiting)
- Validation des données entrantes
- Sauvegarde au format CSV

### 3.2 Traitement des données
- Nettoyage des données invalides
- Détection et suppression des valeurs aberrantes
- Normalisation des temps
- Calcul des statistiques agrégées

### 3.3 Interface utilisateur
- Sélecteur de jeu et catégorie
- Métriques clés en temps réel
- Graphiques interactifs
- Mise à jour automatique

## 4. Analyse des données

### 4.1 Métriques principales
Pour Mega Man (catégorie standard) :
- Meilleur temps : 2106.40 secondes
- Nombre de joueurs : 26
- Temps moyen : 2327.15 secondes
- Score de difficulté : 29.9/100

### 4.2 Distribution des plateformes
- Nintendo 64 : ~50 runs (41.7%)
- SNES : ~18 runs (15%)
- Game Boy : ~8 runs (6.7%)

### 4.3 Utilisation des émulateurs
- Hardware original : 85.5%
- Émulateur : 14.5%

## 5. Problèmes rencontrés et solutions

### 5.1 Problèmes API
- Limite de requêtes atteinte
  * Solution : Implémentation d'un délai entre les requêtes
  * Ajout de gestion d'erreurs robuste

### 5.2 Qualité des données
- IDs de plateforme non lisibles
  * Solution : Ajout d'un système de mapping des IDs vers des noms lisibles
- Données manquantes
  * Solution : Validation stricte et logging des erreurs

### 5.3 Performance
- Temps de chargement longs
  * Solution : Mise en cache des données
  * Optimisation des requêtes API

## 6. Améliorations futures

### 6.1 Court terme
1. Correction du score de difficulté (actuellement parfois à 0/100)
2. Amélioration du mapping des plateformes
3. Ajout de filtres temporels

### 6.2 Long terme
1. Ajout d'analyses comparatives entre jeux
2. Implémentation d'un système de prédiction des temps
3. Intégration de plus de jeux et catégories

## 7. Visualisations disponibles

### 7.1 Métriques en temps réel
- Meilleur temps
- Nombre de joueurs uniques
- Durée moyenne
- Score de difficulté

### 7.2 Graphiques
- Distribution des plateformes (graphique à barres)
- Utilisation des émulateurs (graphique circulaire)

## 8. Conclusion

L'application fournit une base solide pour l'analyse des speedruns avec une interface intuitive et des métriques pertinentes. Les améliorations continues et les corrections de bugs permettent une expérience utilisateur de plus en plus raffinée.

## 9. Annexes

### 9.1 Dépendances principales
```
pandas>=1.5.0
streamlit>=1.20.0
plotly>=5.13.0
requests>=2.28.0
```

### 9.2 Configuration requise
- Python 3.8 ou supérieur
- Connexion Internet stable
- Navigateur web moderne
