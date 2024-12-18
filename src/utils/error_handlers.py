import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)

def handle_api_errors(func: Callable) -> Callable:
    """
    Décorateur pour gérer les erreurs d'API de manière uniforme
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Erreur API dans {func.__name__}: {str(e)}")
            raise
    return wrapper