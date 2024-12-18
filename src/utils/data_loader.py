import pandas as pd
from pathlib import Path
from typing import List, Dict
import logging
from datetime import datetime
from ..data.processor import SpeedrunDataProcessor
from config.settings import GAME_NAMES
from ..api.speedrun_api import SpeedrunAPI

logger = logging.getLogger(__name__)

def get_category_name(game_id: str, category_id: str) -> str:
    """Récupère le nom de la catégorie à partir de son ID"""
    try:
        api = SpeedrunAPI()
        categories = api.get_game_categories(game_id)
        for category in categories:
            if category['id'] == category_id:
                return category['name']
        return category_id
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du nom de la catégorie: {e}")
        return category_id

def load_processed_data(data_dir: Path) -> List[Dict]:
    """
    Charge et traite les données des fichiers CSV
    """
    processor = SpeedrunDataProcessor()
    processed_data = []
    
    try:
        csv_files = list(data_dir.glob('*.csv'))
        if not csv_files:
            logger.warning(f"Aucun fichier CSV trouvé dans {data_dir}")
            return []
            
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                if df.empty:
                    logger.warning(f"Fichier vide: {csv_file}")
                    continue
                    
                # Extraction des identifiants du nom de fichier
                game_id, category_id = csv_file.stem.split('_')
                
                # Récupération des noms réels
                game_name = GAME_NAMES.get(game_id, game_id)
                category_name = get_category_name(game_id, category_id)
                
                # Nettoyage et calcul des métriques
                df_cleaned = processor.clean_data(df)
                metrics = processor.calculate_metrics(df_cleaned)
                
                processed_data.append({
                    'game_id': game_id,
                    'game_name': game_name,
                    'category_id': category_id,
                    'category_name': category_name,
                    'data': df_cleaned.to_dict('records'),
                    'processed_at': datetime.now().isoformat(),
                    **metrics
                })
                
            except Exception as e:
                logger.error(f"Erreur lors du traitement de {csv_file}: {e}")
                continue
        
        return processed_data
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement des données: {e}")
        return []