from typing import Any, Dict

from pydantic import BaseModel


class RequestModel(BaseModel):
    method: str
    url: str
    params: Dict[str, Any]
    data: Dict[str, Any]
    login: bool
