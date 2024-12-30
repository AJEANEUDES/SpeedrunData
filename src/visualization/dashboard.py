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

    def display_processed_data(self, processed_data_path: str):
        st.subheader("Données traitées")
        try:
            data = pd.read_csv(processed_data_path)
            st.write("Aperçu des données :")
            st.dataframe(data.head(50))

            st.write("Statistiques générales :")
            st.write(data.describe(include='all'))
        except Exception as e:
            st.error(f"Erreur lors du chargement des données : {e}")

    def create_time_trend(self, data: pd.DataFrame):
        st.subheader("Évolution des performances au fil du temps")
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        trend_data = data.groupby(data['date'].dt.year)['time_seconds'].mean().reset_index()

        fig = px.line(
            trend_data,
            x='date',
            y='time_seconds',
            title="Tendance des temps moyens de speedrun par année",
            labels={"date": "Année", "time_seconds": "Temps moyen (s)"}
        )
        st.plotly_chart(fig, use_container_width=True)

    def create_top_players_chart(self, data: pd.DataFrame, top_n: int = 10):
        st.subheader(f"Top {top_n} joueurs les plus actifs")
        top_players = data['player'].value_counts().head(top_n).reset_index()
        top_players.columns = ['Player', 'Number of Runs']

        fig = px.bar(
            top_players,
            x='Player',
            y='Number of Runs',
            title=f"Top {top_n} joueurs par nombre de runs",
            labels={"Player": "Joueur", "Number of Runs": "Nombre de runs"}
        )
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

        # Nouvelles visualisations
        self.create_time_trend(pd.DataFrame(selected_data['runs']))
        self.create_top_players_chart(pd.DataFrame(selected_data['runs']))

        # Affichage des données traitées
        processed_data_url = "https://raw.githubusercontent.com/AJEANEUDES/SpeedrunData/Main/data/processed_data.csv"
        self.display_processed_data(processed_data_url)

        # Informations supplémentaires
        st.sidebar.write(f"Dernière mise à jour: {selected_data.get('processed_at', 'Non disponible')}")
