import pandas as pd
import numpy as np
from typing import Dict, Any

class MetricsCalculator:
    @staticmethod
    def calculate_difficulty_score(df: pd.DataFrame) -> float:
        """Calcule le score de difficulté basé sur plusieurs métriques"""
        times_normalized = (df['time_seconds'] - df['time_seconds'].min()) / \
                         (df['time_seconds'].max() - df['time_seconds'].min())
        
        completion_variance = float(times_normalized.std())
        time_spread = float((df['time_seconds'].max() - df['time_seconds'].min()) / 
                          df['time_seconds'].median())
        
        return float(((completion_variance * 0.6 + time_spread * 0.4) * 100))

    @staticmethod
    def calculate_trend_metrics(df: pd.DataFrame) -> Dict[str, Any]:
        """Calcule les métriques de tendance"""
        monthly_runs = df.groupby(pd.to_datetime(df['date']).dt.to_period('M')).size()
        return {
            'trend_coefficient': float(np.polyfit(range(len(monthly_runs)), monthly_runs, 1)[0]),
            'monthly_growth': float(monthly_runs.pct_change().mean() * 100)
        }