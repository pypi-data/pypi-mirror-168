"""TD Ameritrade (non-streaming) API endpoints."""

from collections.abc import Iterable, Mapping
import urllib.parse

Params = Mapping[str, str | Iterable[str]]

BASE_URL = "https://api.tdameritrade.com/"
ENDPOINTS = {
    "Get Option Chain": "v1/marketdata/chains",
    "Get Price History": "v1/marketdata/{symbol}/pricehistory",
    "Get Quote": "v1/marketdata/{symbol}/quotes",
    "Get Quotes": "v1/marketdata/quotes",
    "Get User Principals": "v1/userprincipals",
}


def append_params(url: str, params: Params) -> str:
    """
    Return a URL joined with the encoded params. Any Iterable value is
    joined by commas into a str, then encoded.
    """
    final_params = {
        k: ",".join(v) if isinstance(v, Iterable) and not isinstance(v, str) else v
        for k, v in params.items()
    }
    return f"{url}?{urllib.parse.urlencode(final_params, safe='')}"


def endpoint(name: str, **kwargs: str | Params) -> str:
    """Return an endpoint for a name and any identifiers and params encoded."""
    if "params" in kwargs and isinstance(kwargs["params"], Mapping):
        ids = {k: v for k, v in kwargs.items() if k != "params"}
        return append_params(
            f"{BASE_URL}{ENDPOINTS[name]}".format(**ids), kwargs["params"]
        )
    return f"{BASE_URL}{ENDPOINTS[name]}".format(**kwargs)
