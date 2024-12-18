import logging
from pathlib import Path
from src.data.collector import SpeedrunCollector
from src.visualization.dashboard import Dashboard
from config.settings import GAMES
from src.utils.logging_config import setup_logging
import time

def main():
    # Configuration du logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialisation
        data_dir = Path("data")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        collector = SpeedrunCollector(output_dir=str(data_dir))
        dashboard = Dashboard()

        # Collecte des données pour chaque jeu
        for game_id in GAMES.values():
            try:
                categories = collector.api.get_game_categories(game_id)
                for category in categories:
                    try:
                        df = collector.collect_game_data(game_id, category['id'])
                        if not df.empty:
                            collector.save_data(df, f"{game_id}_{category['id']}.csv")
                        # Pause pour respecter les limites de l'API
                        time.sleep(1)
                    except Exception as e:
                        logger.error(f"Erreur lors de la collecte pour la catégorie {category['id']}: {e}")
                        continue
            except Exception as e:
                logger.error(f"Erreur lors de la collecte pour {game_id}: {e}")
                continue

        # Lancement du dashboard avec Streamlit
        st.write("Lancement du dashboard...")
        dashboard.run(data_dir)

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {e}")
        raise

if __name__ == "__main__":
    import streamlit as st
    main()