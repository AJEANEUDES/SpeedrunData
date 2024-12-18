import logging
from typing import Optional

def setup_logging(log_level: int = logging.INFO, 
                 log_file: Optional[str] = None) -> None:
    """
    Configure le logging pour l'application
    
    Args:
        log_level: Niveau de logging (default: logging.INFO)
        log_file: Chemin vers le fichier de log (optional)
    """
    config = {
        'level': log_level,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
    
    if log_file:
        config['filename'] = log_file
        config['filemode'] = 'a'
    
    logging.basicConfig(**config)