import pandas as pd
import numpy as np
from typing import Dict, Optional
import logging
from ..utils.platform_mapping import get_platform_name

logger = logging.getLogger(__name__)

class SpeedrunDataProcessor:
    def process_run_data(self, run: Dict) -> Optional[Dict]:
        """Traite les données brutes d'une run"""
        try:
            if not all(key in run for key in ['id', 'category', 'date', 'times', 'players', 'status', 'system']):
                return None
                
            return {
                'run_id': run['id'],
                'category': run['category'],
                'date': run['date'],
                'time_seconds': run['times']['primary_t'],
                'player': run['players'][0]['id'] if run['players'] else 'unknown',
                'verified': run['status']['status'] == 'verified',
                'platform': get_platform_name(run['system']['platform']),
                'emulator': run['system']['emulated']
            }
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la run: {e}")
            return None

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie et prépare les données"""
        df = df.copy()
        df = df.drop_duplicates()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Suppression des valeurs aberrantes
        Q1 = df['time_seconds'].quantile(0.25)
        Q3 = df['time_seconds'].quantile(0.75)
        IQR = Q3 - Q1
        df = df[
            (df['time_seconds'] >= Q1 - 1.5 * IQR) & 
            (df['time_seconds'] <= Q3 + 1.5 * IQR)
        ]
        
        return df

    def calculate_metrics(self, df: pd.DataFrame) -> Dict:
        """Calcule les métriques principales"""
        if df.empty:
            return self._get_empty_metrics()
            
        # Calcul du score de difficulté
        times_normalized = (df['time_seconds'] - df['time_seconds'].min()) / \
                         (df['time_seconds'].max() - df['time_seconds'].min())
        completion_variance = float(times_normalized.std() or 0)
        time_spread = float(
            ((df['time_seconds'].max() - df['time_seconds'].min()) / 
             df['time_seconds'].median()) if not df['time_seconds'].empty else 0
        )
        difficulty_score = float(((completion_variance * 0.6 + time_spread * 0.4) * 100))
        
        return {
            'total_runs': len(df),
            'unique_players': df['player'].nunique(),
            'avg_time': float(df['time_seconds'].mean()),
            'median_time': float(df['time_seconds'].median()),
            'std_time': float(df['time_seconds'].std()),
            'best_time': float(df['time_seconds'].min()),
            'platform_distribution': df['platform'].value_counts().to_dict(),
            'emulator_percentage': float((df['emulator'].sum() / len(df)) * 100),
            'runs_per_month': float(df.groupby(pd.to_datetime(df['date']).dt.to_period('M')).size().mean()),
            'difficulty_score': difficulty_score
        }

    def _get_empty_metrics(self) -> Dict:
        """Retourne des métriques vides"""
        return {
            'total_runs': 0,
            'unique_players': 0,
            'avg_time': 0.0,
            'median_time': 0.0,
            'std_time': 0.0,
            'best_time': 0.0,
            'platform_distribution': {},
            'emulator_percentage': 0.0,
            'runs_per_month': 0.0,
            'difficulty_score': 0.0
        }