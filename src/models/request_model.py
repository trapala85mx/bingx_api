from typing import Any, Dict, Optional

from pydantic import BaseModel


class RequestModel(BaseModel):
    """
    Modelo de datos praa una petición.
    """

    method: str
    url: str
    login: bool
    params: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
