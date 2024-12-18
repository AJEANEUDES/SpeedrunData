import logging
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List
from ..api.speedrun_api import SpeedrunAPI
from ..data.processor import SpeedrunDataProcessor
from ..utils.validators import validate_run_data
from ..utils.error_handlers import handle_api_errors
from config.settings import GAME_NAMES

logger = logging.getLogger(__name__)

class SpeedrunCollector:
    def __init__(self, output_dir: str = "data"):
        self.api = SpeedrunAPI()
        self.processor = SpeedrunDataProcessor()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @handle_api_errors
    def collect_game_data(self, game_id: str, category: Optional[str] = None, max_runs: int = 1000) -> pd.DataFrame:
        """Collecte les données pour un jeu spécifique"""
        logger.info(f"Collecte des données pour {GAME_NAMES.get(game_id, game_id)}")
        runs_data = []
        offset = 0
        
        while len(runs_data) < max_runs:
            response = self.api.get_runs(game_id, category, offset)
            if not response.get('data'):
                break
            
            for run in response['data']:
                if validated_run := validate_run_data(run):
                    processed_run = self.processor.process_run_data(validated_run)
                    if processed_run:
                        runs_data.append(processed_run)
            
            offset += len(response['data'])
            
        return pd.DataFrame(runs_data) if runs_data else pd.DataFrame()

    def save_data(self, df: pd.DataFrame, filename: str) -> None:
        """Sauvegarde les données dans un fichier CSV"""
        try:
            output_path = self.output_dir / filename
            df.to_csv(output_path, index=False)
            logger.info(f"Données sauvegardées dans {output_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
            raise