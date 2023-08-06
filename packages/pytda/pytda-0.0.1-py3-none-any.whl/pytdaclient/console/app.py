"""API and streaming data console client."""

import asyncio
from collections.abc import Mapping
from datetime import datetime, timedelta
import os.path
from typing import Optional

# pytda package must be installed, or PYTHONPATH must include src dir
from pytda.api import API, Candles, CandleList, Chain, Quotes
from pytda.streaming import (
    StreamingData,
    streaming_get_data_responses,
    streaming_get_notify_responses,
    streaming_get_responses,
)
from pytda.auth import Auth, FileTokenStore
from pytdaclient.console import config


def timestamp_to_str(timestamp: float) -> str:
    """Convert a timestamp from the API to a date/time str."""
    return str(datetime.fromtimestamp(timestamp / 1000))


def display_candles(candle_list: CandleList) -> None:
    """Display responses from the get price history API in the terminal."""
    symbol = candle_list.get("symbol", "N/A")
    empty = candle_list.get("empty", "N/A")
    print(f"symbol: {symbol}    empty: {empty}")

    hdr = "when                     open      high       low     close        volume"
    print(hdr)
    print("=" * len(hdr))

    candles: Optional[Candles] = candle_list.get("candles")
    if candles:
        for candle in candles:
            when = timestamp_to_str(candle["datetime"])
            opn = candle.get("open", float("nan"))
            high = candle.get("high", float("nan"))
            low = candle.get("low", float("nan"))
            close = candle.get("close", float("nan"))
            vol = candle.get("volume", float("nan"))
            print(
                f"{when}"
                + f"{opn:>10,.2f}{high:>10,.2f}{low:>10,.2f}{close:>10,.2f}{vol:>14,}"
            )

    print()


def display_chain(chain: Chain) -> None:
    """Display responses from the get option chain API in the terminal."""
    symbol = chain.get("symbol", "N/A")
    status = chain.get("status", "N/A")
    print(f"{symbol:<60}{status:^16}")
    hdr = (
        f"{'open int':>10}{'theta':>10}{'gamma':>10}{'delta':>10}"
        + f"{'bid':>10}{'ask':>10}"
        + f"{'strike':^16}"
        + f"{'bid':>10}{'ask':>10}"
        + f"{'delta':>10}{'gamma':>10}{'theta':>10}{'open int':>10}"
    )
    print(hdr)
    print("=" * len(hdr))

    puts = chain.get("putExpDateMap")
    assert puts is not None
    calls = chain.get("callExpDateMap")
    assert calls is not None
    for exp in puts:
        print(f"{exp[:10]:<10}{'Calls':^50}{exp[11:]:^16}{'Puts':^50}")
        print("-" * len(hdr))
        exp_puts = puts[exp]
        exp_calls = calls[exp]
        for strike in exp_puts:
            put = exp_puts[strike][0]
            call = exp_calls[strike][0]
            print(
                f"{int(call['openInterest']):>10,}{float(call['theta']):>10,.2f}"
                + f"{float(call['gamma']):>10,.2f}{float(call['delta']):>10,.2f}"
                + f"{float(call['bid']):>10,.2f}{float(call['ask']):>10,.2f}"
                + f"{float(strike):^16,.2f}"
                + f"{float(put['bid']):>10,.2f}{float(put['ask']):>10,.2f}"
                + f"{float(put['delta']):>10,.2f}{float(put['gamma']):>10,.2f}"
                + f"{float(put['theta']):>10,.2f}{int(put['openInterest']):>10,}"
            )

    print()


def display_quotes(quotes: Quotes) -> None:
    """Display responses from the get quote or get quotes API in the terminal."""
    for quote in quotes.values():
        symbol = quote.get("symbol", "N/A")
        name = quote.get("description", "N/A")
        last = quote.get("lastPrice", float("nan"))
        bid = quote.get("bidPrice", float("nan"))
        ask = quote.get("askPrice", float("nan"))
        opn = quote.get("openPrice", float("nan"))
        high = quote.get("highPrice", float("nan"))
        low = quote.get("lowPrice", float("nan"))
        close = quote.get("closePrice", float("nan"))
        hdr = (
            f"{symbol:<8}{name}"
            + f"  Last: {last:,.2f}"
            + f"  Bid: {bid:,.2f}"
            + f"  Ask: {ask:,.2f}"
        )
        print(hdr)
        print("=" * len(hdr))
        print(f"{'Open':<8}{opn:>10,.2f}")
        print(f"{'High':<8}{high:>10,.2f}")
        print(f"{'Low':<8}{low:>10,.2f}")
        print(f"{'Close':<8}{close:>10,.2f}")
        print()


def display_streaming_response(
    _: StreamingData, resp_json: Mapping[str, object]
) -> None:
    """Display response messages from the streaming API in the terminal."""
    resps = streaming_get_responses(resp_json)
    for resp in resps:
        when = timestamp_to_str(resp["timestamp"])
        resp_type = "response"
        key1 = "service"
        value1 = resp["service"]
        key2 = "command"
        value2 = resp["command"]
        key3 = "code"
        value3 = resp["content"]["code"]
        key4 = "msg"
        value4 = resp["content"]["msg"]
        print(
            f"{when:<28}"
            + f"{resp_type:<10}"
            + f"{key1:>9}: {value1:<18}"
            + f"{key2:>9}: {value2:<18}"
            + f"{key3:>9}: {value3:<4}"
            + f"{key4:>9}: {value4}"
        )


def display_streaming_data_response(
    _: StreamingData, resp_json: Mapping[str, object]
) -> None:
    """Display data response messages from the streaming API in the terminal."""
    resps = streaming_get_data_responses(resp_json)
    for resp in resps:
        when = timestamp_to_str(resp["timestamp"])
        resp_type = "data"
        key1 = "service"
        value1 = resp["service"]
        key2 = "command"
        value2 = resp["command"]
        key3 = "content"
        value3 = resp["content"]
        print(
            f"{when:<28}"
            + f"{resp_type:<10}"
            + f"{key1:>9}: {value1:<18}"
            + f"{key2:>9}: {value2:<18}"
            + f"{key3:>9}: {value3}"
        )


def display_streaming_notify_response(
    _: StreamingData, resp_json: Mapping[str, object]
) -> None:
    """Display notify response messages from the streaming API in the terminal."""
    resps = streaming_get_notify_responses(resp_json)
    for resp in resps:
        when = timestamp_to_str(int(resp["heartbeat"]))
        resp_type = "notify"
        key1 = "heartbeat"
        value1 = resp["heartbeat"]
        print(f"{when:<28}{resp_type:<10}{key1:>9}: {value1}")


async def main() -> None:
    """Try out the API and the streaming API."""
    api = API(
        Auth(
            config.CLIENT_ID,
            config.REDIRECT_URI,
            token_store=FileTokenStore(
                os.path.join(os.path.dirname(__file__), "token")
            ),
        )
    )
    to_date = datetime.now() + timedelta(days=7)
    to_date_str = to_date.strftime("%Y-%m-%d")
    display_chain(api.get_option_chain("SPY", strike_count=10, to_date=to_date_str))
    display_candles(api.get_price_history("SPY", "month", 1, "daily"))
    display_candles(api.get_price_history("$SPX.X", "day", 1, "minute", 30))
    display_quotes(api.get_quote("SPY"))
    display_quotes(api.get_quotes(["$SPX.X", "GLD"]))

    stream = StreamingData(api.get_user_principals())
    stream.append_recv_processor(display_streaming_response)
    stream.append_recv_processor(display_streaming_data_response)
    stream.append_recv_processor(display_streaming_notify_response)
    async with stream.conn_mgr:
        await asyncio.gather(
            stream.recv_forever(),
            stream.login(),
            stream.subscribe(
                [
                    {
                        "service": "ACTIVES_NASDAQ",
                        "parameters": {
                            "keys": "NASDAQ-60",
                            "fields": "0,1",
                        },
                    },
                    {
                        "service": "LEVELONE_FUTURES",
                        "parameters": {
                            "keys": "/ES",
                            "fields": "0,1,2,3,4",
                        },
                    },
                ],
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
