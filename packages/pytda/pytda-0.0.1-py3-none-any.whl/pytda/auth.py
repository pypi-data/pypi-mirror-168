"""Get TD Ameritrade (non-streaming) API access tokens."""

from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
import os.path
import re
from typing import Optional, Tuple
import urllib.parse

import requests

DEFAULT_AUTH_URL_TEMPLATE = (
    "https://auth.tdameritrade.com/auth"
    + "?response_type=code"
    + "&redirect_uri={{ redirect_uri }}"
    + "&client_id={{ client_id }}"
)
AUTH_CODE_PATTERN = re.compile(r"code=(.+)")


def fill_template(template: str, values: Mapping[str, str]) -> str:
    """Return a template with the values filled in."""
    for key, value in values.items():
        template = template.replace(f"{{{{ {key} }}}}", value)
    return template


class ITokenStore(metaclass=ABCMeta):
    """Interface to store and retrieve access and refresh tokens."""

    @abstractmethod
    def store(self, access_token: str, refresh_token: str) -> None:
        """Persist tokens."""

    @abstractmethod
    def get(self) -> Optional[Tuple[str, str]]:
        """Retrieve persisted tokens."""


class FileTokenStore(ITokenStore):
    """Store tokens in, and retrieve them from a text file."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def store(self, access_token: str, refresh_token: str) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file_ptr:
            file_ptr.writelines([f"{access_token}\n", f"{refresh_token}\n"])

    def get(self) -> Optional[Tuple[str, str]]:
        if not os.path.isfile(self.file_path):
            return None
        with open(self.file_path, "r", encoding="utf-8") as file_ptr:
            access_token, refresh_token = file_ptr.read().splitlines()
        if not (access_token or refresh_token):
            return None
        return (access_token, refresh_token)


class Auth:
    """Assist in getting auth codes, and request access and refresh tokens."""

    def __init__(
        self,
        client_id: str,
        redirect_uri: str,
        auth_url_template: str = DEFAULT_AUTH_URL_TEMPLATE,
        token_store: Optional[ITokenStore] = None,
    ) -> None:
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.auth_url_template = auth_url_template
        self.token_store = token_store
        if self.token_store:
            tokens = self.token_store.get()
            if tokens:
                self.access_token, self.refresh_token = tokens
        if not hasattr(self, "access_token"):
            self.request_access_tokens(auth_code=self.prompt_auth_code())

    @property
    def auth_url(self) -> str:
        """URL for a user to login and request an auth code."""
        return fill_template(
            self.auth_url_template,
            {
                "client_id": urllib.parse.quote(self.client_id, safe=""),
                "redirect_uri": urllib.parse.quote(self.redirect_uri, safe=""),
            },
        )

    def prompt_auth_code(self) -> str:
        """Prompt the user to get and input an auth code."""
        print("Please go the URL below and get an authorization code.")
        print(self.auth_url)
        code_input = input("Authorization code: ").strip()
        code_match = AUTH_CODE_PATTERN.search(code_input)
        code = code_match.group(1) if code_match else code_input
        return urllib.parse.unquote(code)

    def request_access_tokens(
        self, auth_code: Optional[str] = None, refresh: bool = False
    ) -> None:
        """Request access or refresh tokens."""
        data = {
            "access_type": "offline",
            "client_id": self.client_id,
        }
        if not refresh:
            if not auth_code:
                raise ValueError("auth_code is required, unless refresh=True")
            data.update(
                {
                    "grant_type": "authorization_code",
                    "code": auth_code,
                    "redirect_uri": self.redirect_uri,
                }
            )
        else:
            data.update(
                {
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                }
            )
        res = requests.post("https://api.tdameritrade.com/v1/oauth2/token", data=data)
        if res.status_code != 200:
            res.raise_for_status()
        res_json = res.json()
        self.access_token = res_json["access_token"]
        self.refresh_token = res_json["refresh_token"]
        if self.token_store:
            self.token_store.store(self.access_token, self.refresh_token)
