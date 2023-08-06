"""API web client."""

import os.path
from flask import Flask, render_template, request

# pytda package must be installed, or PYTHONPATH must include src dir
from pytda.api import API
from pytda.auth import Auth, FileTokenStore
from pytdaclient.console import config

app = Flask(__name__)


@app.template_filter("n_a")
def n_a(value: str) -> str:
    """Render an empty value as N/A."""
    return value if value else "N/A"


@app.template_filter("price")
def price(value: str) -> str:
    """Render a float with commas and 2 decimal places."""
    try:
        float_value = float(value)
    except ValueError:
        return value
    return f"{float_value:,.2f}"


@app.template_filter("mm_dd")
def mm_dd(value: str) -> str:
    """Render a yy[yy]-mm-dd date as mm/dd."""
    if len(value) < 10:
        return value
    return "/".join(value.split("-")[1:3]).split()[0]


@app.route("/")
def quote_cards() -> str:
    """Render quote cards."""
    symbols = request.args.get("symbols", None)
    symbol_list = symbols.split(",") if symbols else []
    if not symbols:
        return render_template("index.html", quotes={})

    api = API(
        Auth(
            config.CLIENT_ID,
            config.REDIRECT_URI,
            token_store=FileTokenStore(
                os.path.join(os.path.dirname(__file__), "token")
            ),
        )
    )
    quotes = api.get_quotes(symbol_list)
    full_quotes = {}

    for symbol, quote in quotes.items():
        quote_extra = {}
        quote_extra["changeType"] = "flat"
        last = quote["lastPrice"]
        opn = quote["openPrice"]
        if isinstance(last, float) and isinstance(opn, float):
            change = last - opn
            if change > 0:
                quote_extra["changeType"] = "up"
            elif change < 0:
                quote_extra["changeType"] = "down"
        full_quotes[symbol] = {**quote, **quote_extra}

    return render_template("index.html", quotes=full_quotes)


if __name__ == "__main__":
    app.run()
