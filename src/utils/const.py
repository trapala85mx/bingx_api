from enum import Enum, StrEnum


class Endpoints(StrEnum):
    """Constantes para las urls / endpoints de Bingx"""

    ACCOUNT = "/openApi/swap/v3/user/balance"
    BASE_URL = "https://open-api.bingx.com"
    CONTRACTS = "/openApi/swap/v2/quote/contracts"
    CHANGE_MARGIN_TYPE = "/openApi/swap/v2/trade/marginType"
    KLINES = "/openApi/swap/v3/quote/klines"
    LISTEN_KEY_DELETE = "/openApi/user/auth/userDataStream"
    LISTEN_KEY_EXTEND = "/openApi/user/auth/userDataStream"
    LISTEN_KEY_POST = "/openApi/user/auth/userDataStream"
    PLACE_ORDER = "/openApi/swap/v2/trade/order"
    QUERY_MARGIN_TYPE = "/openApi/swap/v2/trade/marginType"
    SERVER_TIMESTAMP = "/openApi/swap/v2/server/time"
    WS_URL = "wss://open-api-swap.bingx.com/swap-market"


class HttpMethod(StrEnum):
    """Constantes de métodos HTTP"""

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"


class Intervals(StrEnum):
    """Constantes para los timeframes"""

    KLINE_1_MIN = "1m"
    KLINE_5_MIN = "5m"
    KLINE_15_MIN = "15m"
    KLINE_4_HOUR = "4h"
    KLINE_1_DAY = "1d"
    KLINE_1_MONT = "1M"
    KLINE_1_WEEK = "1w"


class MarginType(StrEnum):
    """Tipo de marge"""

    ISOLATED = "ISOLATED"
    CROSSED = "CROSSED"


class OrderType(StrEnum):
    """Constantes para tipo de órdenes"""

    LIMIT_ORDER = "LIMIT"
    MARKET_ORDER = "MARKET"
    STOP_MARKET_ORDER = "STOP_MARKET"
    TAKE_PROFIT_MARKET_ORDER = "TAKE_PROFIT_MARKET"
    STOP_LIMIT_ORDER = "STOP"
    TAKE_PROFIT_LIMIT_ORDER = "TAKE_PROFIT"
    STOP_LIMIT_ORDER_WITH_TRIGGER = "TRIGGER_LIMIT"
    STOP_MARKET_ORDER_WITH_TRIGGER = "TRIGGER_MARKET"
    TRAILING_STOP_MARKET_ORDER = "TRAILING_STOP_MARKET"
    TRAILING_TAKEPROFIT_OR_STOPLOSS = "TRAILING_TP_SL"


class PositionSide(StrEnum):
    """Constantes para tipo de posición"""

    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"


class BingxLimits(Enum):
    """Límites de la API de Bingx"""

    MAX_WS_PER_IP = 50
    MAX_SUBS_PER_WS = 100
    LISTEN_KEY_RENEWAL_SECS = 1800


class WsStreamTypes(StrEnum):
    KLINES_STREAM = "KLINES"
