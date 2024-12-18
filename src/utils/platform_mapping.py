import logging

logger = logging.getLogger(__name__)

# Mapping des IDs de plateformes vers leurs noms
PLATFORM_NAMES = {
    'v06dr394': 'NES',
    '7m6ylw9p': 'SNES',
    '83exk6l5': 'Nintendo 64',
    '83exovel': 'Game Boy',
    'nzelkr6q': 'PlayStation',
    'o0e3y2rw': 'PC',
    'mr6k4e7n': 'Wii',
    'w89rwelk': 'Xbox',
    'p86kx6rq': 'PlayStation 2',
    'v06dr3e4': 'GameCube',
    # Ajoutez d'autres mappings selon les  besoins
}

def get_platform_name(platform_id: str) -> str:
    """
    Convertit l'ID de la plateforme en nom lisible
    
    Args:
        platform_id: ID de la plateforme
        
    Returns:
        Nom de la plateforme ou l'ID si non trouvé
    """
    try:
        return PLATFORM_NAMES.get(platform_id, platform_id)
    except Exception as e:
        logger.error(f"Erreur lors de la conversion de l'ID de plateforme {platform_id}: {e}")
        return platform_id