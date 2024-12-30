import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from ..utils.data_loader import load_processed_data

class Dashboard:
    def __init__(self):
        st.set_page_config(page_title="Speedrun Analytics", layout="wide")

    def create_metrics_cards(self, data: Dict):
        cols = st.columns(4)
        with cols[0]:
            st.metric("Meilleur Temps", f"{data.get('best_time', 0):.2f}s")
        with cols[1]:
            st.metric("Joueurs uniques", data.get('unique_players', 0))
        with cols[2]:
            st.metric("Durée moyenne", f"{data.get('avg_time', 0):.2f}s")
        with cols[3]:
            st.metric("Score de difficulté", f"{data.get('difficulty_score', 0):.1f}/100")

    def create_platform_distribution(self, platform_data: Dict):
        if not platform_data:
            st.warning("Pas de données de plateforme disponibles")
            return
            
        fig = px.bar(
            x=list(platform_data.keys()),
            y=list(platform_data.values()),
            title="Distribution des plateformes",
            labels={'x': 'Plateforme', 'y': "Nombre d'essais"}
        )
        st.plotly_chart(fig, use_container_width=True)

    def create_emulator_pie(self, emulator_percentage: float):
        fig = go.Figure(data=[go.Pie(
            labels=['Émulateur', 'Hardware Original'],
            values=[emulator_percentage, 100 - emulator_percentage],
            hole=.3
        )])
        fig.update_layout(title="Utilisation de l'émulateur vs Hardware Original")
        st.plotly_chart(fig, use_container_width=True)

    def run(self, data_dir: Path):
        st.title("Speedrun Analytics Dashboard")
        st.markdown("Analyse des données et mesure de la difficulté des speedruns")
        
        # Chargement des données
        data_list = load_processed_data(data_dir)
        
        if not data_list:
            st.error("Aucune donnée n'a été trouvée. Veuillez d'abord collecter des données.")
            return
            
        # Création de la liste des jeux et catégories avec leurs noms réels
        game_categories = [(d['game_id'], d['category_id'], d['game_name'], d['category_name']) 
                         for d in data_list]
        
        if not game_categories:
            st.error("Aucune catégorie trouvée dans les données")
            return
            
        # Sélection avec les noms réels
        selected = st.selectbox(
            "Sélectionner le jeu et la catégorie",
            game_categories,
            format_func=lambda x: f"{x[2]} - {x[3]}"  # Affiche game_name - category_name
        )
        
        # Récupération des données sélectionnées
        selected_data = next(
            (d for d in data_list 
             if d['game_id'] == selected[0] and d['category_id'] == selected[1]),
            None
        )
        
        if not selected_data:
            st.error("Données non trouvées pour la sélection")
            return
            
        # Affichage des métriques
        self.create_metrics_cards(selected_data)
        
        # Création des visualisations
        col1, col2 = st.columns(2)
        with col1:
            self.create_platform_distribution(selected_data.get('platform_distribution', {}))
        with col2:
            self.create_emulator_pie(selected_data.get('emulator_percentage', 0))
            
        # Informations supplémentaires
        st.sidebar.write(f"Dernière mise à jour: {selected_data.get('processed_at', 'Non disponible')}")
