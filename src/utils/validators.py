from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def validate_run_data(run_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Valide les données d'une run
    
    Args:
        run_data: Données de la run à valider
        
    Returns:
        Données validées ou None si invalides
    """
    required_fields = ['id', 'category', 'date', 'times', 'players', 'status', 'system']
    
    try:
        # Vérifie la présence des champs requis
        if not all(field in run_data for field in required_fields):
            missing_fields = [f for f in required_fields if f not in run_data]
            logger.warning(f"Champs manquants dans les données: {missing_fields}")
            return None
            
        # Vérifie la validité des valeurs
        if not run_data['times'].get('primary_t'):
            logger.warning("Temps principal manquant")
            return None
            
        return run_data
        
    except Exception as e:
        logger.error(f"Erreur lors de la validation des données: {e}")
        return None