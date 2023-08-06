"""Consume TD Ameritrade streaming data."""

from __future__ import annotations
import asyncio
from collections.abc import Mapping, MutableSequence, Sequence
from datetime import datetime, timezone
import json
import urllib.parse
from types import TracebackType
from typing import (
    Any,
    Callable,
    Generator,
    Optional,
    Tuple,
    Type,
    TypeGuard,
    TypeVar,
    cast,
)
from typing_extensions import NotRequired, TypedDict

from websockets.client import connect as ws_connect, WebSocketClientProtocol

from .api import UserPrincipals

# https://docs.python.org/3/library/typing.html#typing.Callable
F = TypeVar("F", bound=Callable[..., Any])
Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]


class StreamingRequestPartial(TypedDict):
    """Type of a partial basic request that clients should provide."""

    service: str
    parameters: NotRequired[Mapping[str, str]]


StreamingRequestsPartial = Sequence[StreamingRequestPartial]


class StreamingRequest(TypedDict):
    """Basic request type that the StreamingAPI will create."""

    service: str
    requestid: NotRequired[str]
    command: NotRequired[str]
    account: NotRequired[str]
    source: NotRequired[str]
    parameters: NotRequired[Mapping[str, str]]


class StreamingRequests(TypedDict):
    """Sequence of basic requests type that the StreamingAPI will create."""

    requests: MutableSequence[StreamingRequest]


class StreamingResponseCont(TypedDict):
    """Basic response content field type."""

    code: int
    msg: str


class StreamingResponse(TypedDict):
    """Basic response type."""

    service: str
    requestid: str
    command: str
    timestamp: int
    content: StreamingResponseCont


class StreamingDataResponse(TypedDict):
    """Basic data response type."""

    service: str
    timestamp: int
    command: str
    content: Sequence[Mapping[str, str | int | float | bool]]


class StreamingNotifyResponse(TypedDict):
    """Basic notify response type."""

    heartbeat: str


StreamingResponses = MutableSequence[StreamingResponse]
StreamingDataResponses = MutableSequence[StreamingDataResponse]
StreamingNotifyResponses = MutableSequence[StreamingNotifyResponse]
StreamingRecvProc = Callable[["StreamingData", Mapping[str, object]], None]


def get_deep_attr(obj: object, attrs: Sequence[str]) -> object:
    """Traverse objects to get nested attrs."""
    value = getattr(obj, attrs[0])
    return value if len(attrs) == 1 else get_deep_attr(value, attrs[1:])


def attrs_set(*attrs: str) -> Decorator:
    """
    Decorate API endpoint methods to check that certain instance attrs are
    not None.
    """

    def decorator(method: F) -> F:
        def wrapper(*args: object, **kwargs: object) -> F:
            self = args[0]
            for attr in attrs:
                try:
                    if get_deep_attr(self, attr.split(".")) is None:
                        raise RuntimeError(
                            f"'{self.__class__.__name__}' object "
                            + f"attrbute '{attr}' is None",
                        )
                except AttributeError as exc:
                    raise RuntimeError(
                        f"'{self.__class__.__name__}' object "
                        + f"attrbute '{attr}' not found",
                    ) from exc

            return cast(F, method(*args, **kwargs))

        return cast(F, wrapper)

    return decorator


def id_gen(initial_id: int = 0) -> Generator[int, None, None]:
    """Generate sequential ints, which can used as unique request IDs."""
    cur_id = initial_id
    while True:
        yield cur_id
        cur_id += 1


def has_keys(
    typed_dict: Mapping[str, object], spec: Sequence[Tuple[str, type]]
) -> bool:
    """Check that a mapping has keys of the correct type."""
    return all(
        key in typed_dict and isinstance(typed_dict[key], key_type)
        for key, key_type in spec
    )


def is_streaming_response(
    resp_json: Mapping[str, object],
) -> TypeGuard[StreamingResponse]:
    """StreamingResponse TypeGuard."""
    if not has_keys(
        resp_json,
        [
            ("service", str),
            ("requestid", str),
            ("command", str),
            ("timestamp", int),
            ("content", Mapping),
        ],
    ):
        return False
    assert isinstance(resp_json["content"], Mapping)
    return has_keys(resp_json["content"], [("code", int), ("msg", str)])


def is_streaming_data_response(
    resp_json: Mapping[str, object],
) -> TypeGuard[StreamingDataResponse]:
    """StreamingDataResponse TypeGuard."""
    return has_keys(
        resp_json,
        [
            ("service", str),
            ("timestamp", int),
            ("command", str),
            ("content", Sequence),
        ],
    )


def is_streaming_notify_response(
    resp_json: Mapping[str, object],
) -> TypeGuard[StreamingNotifyResponse]:
    """StreamingNotifyResponse TypeGuard."""
    return has_keys(resp_json, [("heartbeat", str)])


def streaming_get_responses(resp_json: Mapping[str, object]) -> StreamingResponses:
    """Extract the StreamingResponses from a message."""
    res: StreamingResponses = []
    if "response" in resp_json and isinstance(resp_json["response"], Sequence):
        for resp in resp_json["response"]:
            if is_streaming_response(resp):
                res.append(resp)
    return res


def streaming_get_data_responses(
    resp_json: Mapping[str, object]
) -> StreamingDataResponses:
    """Extract the StreamingDataResponses from a message."""
    res: StreamingDataResponses = []
    if "data" in resp_json and isinstance(resp_json["data"], Sequence):
        for resp in resp_json["data"]:
            if is_streaming_data_response(resp):
                res.append(resp)
    return res


def streaming_get_notify_responses(
    resp_json: Mapping[str, object]
) -> StreamingNotifyResponses:
    """Extract the StreamingNotifyResponses from a message."""
    res: StreamingNotifyResponses = []
    if "notify" in resp_json and isinstance(resp_json["notify"], Sequence):
        for resp in resp_json["notify"]:
            if is_streaming_notify_response(resp):
                res.append(resp)
    return res


def streaming_login_proc(api: StreamingData, resp_json: Mapping[str, object]) -> None:
    """Process received login responses."""
    resps = streaming_get_responses(resp_json)
    for resp in resps:
        if resp["command"] == "LOGIN" and resp["content"]["code"] == 0:
            api._streaming_logged_in.set()  # pylint: disable=W0212
            return


class StreamingConnection:
    """Connection manager for a websockets connection."""

    def __init__(self, uri: str) -> None:
        self._uri = uri
        self._conn: Optional[WebSocketClientProtocol] = None

    @property
    def conn(self) -> WebSocketClientProtocol:
        """
        Narrow the optional connection to not be None, and raise an exception
        if it is.
        """
        if self._conn is None:
            raise RuntimeError(
                f"'{self.__class__.__name__}' object " + "attribute 'conn' is None"
            )
        return self._conn

    @conn.setter
    def conn(self, value: WebSocketClientProtocol) -> None:
        self._conn = value

    async def __aenter__(self) -> WebSocketClientProtocol:
        self.conn = await ws_connect(self._uri)
        if not self.conn.open:
            raise RuntimeError
        return self.conn

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> None:
        await self.conn.close()


class StreamingData:
    """Make streaming API requests and process responses."""

    def __init__(self, user_principals: UserPrincipals) -> None:
        self.user_principals = user_principals
        self._conn_mgr: Optional[StreamingConnection] = None
        self._request_id_gen = id_gen()
        self._recv_processors: MutableSequence[StreamingRecvProc] = [
            streaming_login_proc,
        ]
        self._streaming_logged_in = asyncio.Event()

    @property
    def request_id(self) -> str:
        """Generate a request ID that can be used for new request."""
        return str(self._request_id_gen.__next__())

    @property
    def conn_mgr(self) -> StreamingConnection:
        """
        Narrow the optional connection manager to not be None by creating
        one if it is None.
        """
        if self._conn_mgr is None:
            url = self.user_principals["streamerInfo"]["streamerSocketUrl"]
            uri = f"wss://{url}/ws"
            self._conn_mgr = StreamingConnection(uri)
        return self._conn_mgr

    @attrs_set("conn_mgr.conn")
    async def login(self) -> None:
        """Make a login request."""
        user_principals = self.user_principals
        token_timestamp = user_principals["streamerInfo"]["tokenTimestamp"]
        token_dt = datetime.strptime(token_timestamp, "%Y-%m-%dT%H:%M:%S%z")
        epoch_dt = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
        token_ms = int((token_dt - epoch_dt).total_seconds() * 1000)
        credential = {
            "userid": user_principals["accounts"][0]["accountId"],
            "token": user_principals["streamerInfo"]["token"],
            "company": user_principals["accounts"][0]["company"],
            "segment": user_principals["accounts"][0]["segment"],
            "cddomain": user_principals["accounts"][0]["accountCdDomainId"],
            "usergroup": user_principals["streamerInfo"]["userGroup"],
            "accesslevel": user_principals["streamerInfo"]["accessLevel"],
            "authorized": "Y",
            "timestamp": token_ms,
            "appid": user_principals["streamerInfo"]["appId"],
            "acl": user_principals["streamerInfo"]["acl"],
        }
        data = {
            "requests": [
                {
                    "service": "ADMIN",
                    "requestid": self.request_id,
                    "command": "LOGIN",
                    "account": user_principals["accounts"][0]["accountId"],
                    "source": user_principals["streamerInfo"]["appId"],
                    "parameters": {
                        "credential": urllib.parse.urlencode(credential),
                        "token": user_principals["streamerInfo"]["token"],
                        "version": "1.0",
                    },
                }
            ]
        }
        await self.conn_mgr.conn.send(json.dumps(data))

    @attrs_set("conn_mgr.conn")
    async def subscribe(self, requests: StreamingRequestsPartial) -> None:
        """Await being logged in, the make a subscribe request."""
        full_requests: StreamingRequests = {"requests": []}
        user_principals = self.user_principals
        for request in requests:
            full_request: StreamingRequest = {
                "service": request["service"],
                "requestid": self.request_id,
                "command": "SUBS",
                "account": user_principals["accounts"][0]["accountId"],
                "source": user_principals["streamerInfo"]["appId"],
            }
            if "parameters" in request:
                full_request["parameters"] = request["parameters"]
            full_requests["requests"].append(full_request)
        await self._streaming_logged_in.wait()
        await self.conn_mgr.conn.send(json.dumps(full_requests))

    def append_recv_processor(self, processor: StreamingRecvProc) -> None:
        """Append a processor of received messages."""
        self._recv_processors.append(processor)

    @attrs_set("conn_mgr.conn")
    async def recv_forever(self) -> None:
        """Receive messages forever and pass them off to the processors."""
        while True:
            resp_text = await self.conn_mgr.conn.recv()
            assert isinstance(resp_text, str)
            resp_json = json.loads(resp_text)
            for proc in self._recv_processors:
                proc(self, resp_json)
