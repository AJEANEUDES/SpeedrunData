from typing import Dict, List, Optional
import requests
import logging
from config.api_config import API_CONFIG

logger = logging.getLogger(__name__)

class SpeedrunAPI:
    def __init__(self):
        self.base_url = API_CONFIG['base_url']
        self.headers = API_CONFIG['headers']

    def get_game_categories(self, game_id: str) -> List[Dict]:
        """Récupère toutes les catégories d'un jeu"""
        url = f"{self.base_url}/games/{game_id}/categories"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()['data']
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la récupération des catégories: {e}")
            raise

    def get_runs(self, game_id: str, category: Optional[str] = None, offset: int = 0) -> Dict:
        """Récupère les runs avec pagination"""
        params = {
            'game': game_id,
            'status': 'verified',
            'orderby': 'date',
            'max': API_CONFIG['runs_per_page'],
            'offset': offset
        }
        if category:
            params['category'] = category

        url = f"{self.base_url}/runs"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la récupération des runs: {e}")
            raise