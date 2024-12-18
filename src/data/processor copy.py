import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SpeedrunDataProcessor:
    def process_run_data(self, run: Dict) -> Optional[Dict]:
        """Traite les données brutes d'une run"""
        try:
            return {
                'run_id': run['id'],
                'category': run['category'],
                'date': run['date'],
                'time_seconds': run['times']['primary_t'],
                'player': run['players'][0]['id'] if run['players'] else 'unknown',
                'verified': run['status']['status'] == 'verified',
                'platform': run['system']['platform'],
                'emulator': run['system']['emulated']
            }
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la run: {e}")
            return None

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie et prépare les données"""
        df = df.drop_duplicates()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        Q1 = df['time_seconds'].quantile(0.25)
        Q3 = df['time_seconds'].quantile(0.75)
        IQR = Q3 - Q1
        return df[
            (df['time_seconds'] >= Q1 - 1.5 * IQR) & 
            (df['time_seconds'] <= Q3 + 1.5 * IQR)
        ]

    def calculate_metrics(self, df: pd.DataFrame) -> Dict:
        """Calcule les métriques principales"""
        return {
            'total_runs': len(df),
            'unique_players': df['player'].nunique(),
            'avg_time': float(df['time_seconds'].mean()),
            'median_time': float(df['time_seconds'].median()),
            'std_time': float(df['time_seconds'].std()),
            'best_time': float(df['time_seconds'].min()),
            'platform_distribution': df['platform'].value_counts().to_dict(),
            'emulator_percentage': float((df['emulator'].sum() / len(df)) * 100),
            'runs_per_month': float(df.groupby(pd.to_datetime(df['date']).dt.to_period('M')).size().mean())
        }