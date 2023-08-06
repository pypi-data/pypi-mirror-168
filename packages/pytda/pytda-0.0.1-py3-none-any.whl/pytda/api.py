"""Consume TD Ameritrade (non-streaming) API."""

from collections.abc import Iterable, Mapping, Sequence, MutableMapping
import datetime
from typing import Literal, Optional, TypedDict, cast
from dateutil import parser
import requests

from .auth import Auth
from .endpoint import endpoint

Candles = Sequence[Mapping[str, float]]
Quotes = Mapping[str, Mapping[str, str | float]]

ContractType = Literal["CALL", "PUT", "ALL"]
Strategy = Literal[
    "SINGLE",
    "ANALYTICAL",
    "COVERED",
    "VERTICAL",
    "CALENDAR",
    "STRANGLE",
    "STRADDLE",
    "BUTTERFLY",
    "CONDOR",
    "DIAGONAL",
    "COLLAR",
    "ROLL",
]
Range = Literal["ITM", "NTM", "OTM", "SAK", "SBK", "SNK", "ALL"]
Month = Literal[
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC",
    "ALL",
]
OptionType = Literal["S", "NS", "ALL"]
Period = Literal["day", "month", "year", "ytd"]
Frequency = Literal["minute", "daily", "weekly", "monthly"]

PERIOD_TYPE__PERIOD: Mapping[Period, Sequence[int]] = {
    "day": [10, 1, 2, 3, 4, 5],
    "month": [1, 2, 3, 6],
    "year": [1, 2, 3, 5, 10, 15, 20],
    "ytd": [1],
}
PERIOD_TYPE__FREQ_TYPE: Mapping[Period, Sequence[Frequency]] = {
    "day": ["minute"],
    "month": ["weekly", "daily"],
    "year": ["monthly", "daily", "weekly"],
    "ytd": ["weekly", "daily"],
}
FREQ_TYPE__FREQ: Mapping[Frequency, Sequence[int]] = {
    "minute": [1, 5, 10, 15, 30],
    "daily": [1],
    "weekly": [1],
    "monthly": [1],
}


def dt_to_ms(d_t: datetime.datetime) -> int:
    """Convert a timestamp to milliseconds."""
    return int(round(d_t.timestamp() * 1000))


class CandleList(TypedDict):
    """Price history response type."""

    candles: Candles
    empty: bool
    symbol: str


class Option(TypedDict):
    """Option in a chain."""

    putCall: str
    symbol: str
    description: str
    bid: float
    ask: float
    last: float
    mark: float
    highPrice: float
    lowPrice: float
    openPrice: float
    closePrice: float
    totalVolume: int
    volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float
    openInterest: int
    daysToExpiration: int
    inTheMoney: bool


class Chain(TypedDict):
    """Option chain response type."""

    symbol: str
    status: str
    putExpDateMap: Mapping[str, Mapping[str, Sequence[Option]]]
    callExpDateMap: Mapping[str, Mapping[str, Sequence[Option]]]


class UserPrincipalsAccount(TypedDict):
    """UserPrincipals account field type."""

    accountId: str
    company: str
    segment: str
    accountCdDomainId: str


class UserPrincipalsStreamerInfo(TypedDict):
    """UserPrincipals streamerInfo field type."""

    token: str
    tokenTimestamp: str
    userGroup: str
    accessLevel: str
    appId: str
    acl: str
    streamerSocketUrl: str


class UserPrincipals(TypedDict):
    """User principals response type."""

    accounts: Sequence[UserPrincipalsAccount]
    streamerInfo: UserPrincipalsStreamerInfo


class API:
    """Make API requests."""

    def __init__(self, auth: Auth) -> None:
        self.auth = auth

    @property
    def auth_header(self) -> Mapping[str, str]:
        """The authorization header."""
        return {"Authorization": f"Bearer {self.auth.access_token}"}

    def get(self, url: str) -> requests.Response:
        """Add the auth header and return the results of a get request."""
        res = requests.get(url, headers=self.auth_header)
        if res.status_code == 200:
            return res
        if res.status_code == 401:
            self.auth.request_access_tokens(refresh=True)
            res = requests.get(url, headers=self.auth_header)
            if res.status_code == 200:
                return res
        res.raise_for_status()
        return res

    def get_option_chain(
        self,
        symbol: str,
        contract_type: ContractType = "ALL",
        strike_count: Optional[int] = None,
        include_quotes: bool = False,
        strategy: Strategy = "SINGLE",
        interval: Optional[int] = None,
        strike: Optional[float] = None,
        rng: Range = "ALL",
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        volatility: Optional[float] = None,
        underlying_price: Optional[float] = None,
        interest_rate: Optional[float] = None,
        dte: Optional[int] = None,
        exp_month: Month = "ALL",
        option_type: OptionType = "ALL",
    ) -> Chain:
        """Make a request to the get option chain endpoint."""
        params: MutableMapping[str, str] = {
            "symbol": symbol,
            "contractType": contract_type,
            "strategy": strategy,
            "range": rng,
            "expMonth": exp_month,
            "optionType": option_type,
        }

        if strike_count is not None:
            params["strikeCount"] = str(strike_count)
        if include_quotes is not None:
            params["includeQuotes"] = str(include_quotes).upper()
        if strategy is not None:
            params["strategy"] = strategy
        if interval is not None:
            params["interval"] = str(interval)
        if strike is not None:
            params["strike"] = str(strike)
        if rng is not None:
            params["range"] = rng
        if from_date is not None:
            params["fromDate"] = from_date
        if to_date is not None:
            params["toDate"] = to_date
        if volatility is not None:
            params["volatility"] = str(volatility)
        if underlying_price is not None:
            params["underlyingPrice"] = str(underlying_price)
        if interest_rate is not None:
            params["interestRate"] = str(interest_rate)
        if dte is not None:
            params["daysToExpiration"] = str(dte)
        if exp_month is not None:
            params["expMonth"] = str(exp_month)
        if option_type is not None:
            params["optionType"] = str(option_type)

        res = self.get(endpoint("Get Option Chain", params=params))
        return cast(Chain, res.json())

    def get_price_history(
        self,
        symbol: str,
        period_type: Period = "day",
        period: Optional[int] = None,
        freq_type: Optional[Frequency] = None,
        freq: Optional[int] = None,
        end_date: Optional[str] = None,
        start_date: Optional[str] = None,
        need_ext_hours: Optional[bool] = True,
    ) -> CandleList:
        """Make a request to the get price history endpoint."""
        params: MutableMapping[str, str] = {"periodType": period_type}

        if period:
            params["period"] = str(period)
        else:
            params["period"] = str(PERIOD_TYPE__PERIOD[period_type][0])

        if freq_type:
            final_freq_type = freq_type
        else:
            final_freq_type = PERIOD_TYPE__FREQ_TYPE[period_type][0]
        params["frequencyType"] = final_freq_type

        if freq:
            params["frequency"] = str(freq)
        else:
            params["frequency"] = str(FREQ_TYPE__FREQ[final_freq_type][0])

        if end_date:
            params["endDate"] = str(dt_to_ms(parser.parse(end_date)))
        if start_date:
            params["starDate"] = str(dt_to_ms(parser.parse(start_date)))

        params["needExtendedHours"] = str(need_ext_hours).lower()

        res = self.get(endpoint("Get Price History", symbol=symbol, params=params))
        return cast(CandleList, res.json())

    def get_quote(self, symbol: str) -> Quotes:
        """Make a request to the get quote endpoint."""
        res = self.get(endpoint("Get Quote", symbol=symbol))
        return cast(Quotes, res.json())

    def get_quotes(self, symbols: Iterable[str]) -> Quotes:
        """Make a request to the get quotes endpoint."""
        res = self.get(endpoint("Get Quotes", params={"symbol": symbols}))
        return cast(Quotes, res.json())

    def get_user_principals(
        self,
        fields: Optional[Iterable[str]] = None,
    ) -> UserPrincipals:
        """Make a request to the get user principals endpoint."""
        if not fields:
            fields = ["streamerSubscriptionKeys", "streamerConnectionInfo"]
        res = self.get(endpoint("Get User Principals", params={"fields": fields}))
        return cast(UserPrincipals, res.json())
