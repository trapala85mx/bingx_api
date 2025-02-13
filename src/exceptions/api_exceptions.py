class ApiException(Exception):
    """Clase General de un error de la API"""


class ApiValidationError(ApiException):
    """Clase que representa un error en la Validación de datos."""
