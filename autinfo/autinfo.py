import asyncio
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    import aiohttp

    _async_support = True
except ModuleNotFoundError:
    _async_support = False

try:
    import requests

    _sync_support = True
except ModuleNotFoundError:
    _sync_support = False

from .config import URL, URL_LOGIN, URL_MESSAGES
from .utils import change_unicode, csrf


class BaseAutInfo:
    URL = URL
    URL_MESSAGES = URL_MESSAGES
    URL_LOGIN = URL_LOGIN

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    @staticmethod
    def format_data(text: str) -> List[Tuple[str, str]]:
        return re.findall(r"(\d{1,12})\(([^)]+)\)", text)

    def get_login_data(self, csrf_token: str) -> Dict[str, Any]:
        return {
            "_csrf": csrf_token,
            "username": self.username,
            "password": self.password,
            "login": "ورود",
        }


class AutInfoAsync(BaseAutInfo):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password)
        if not _async_support:
            raise ImportError("Install aiohttp via `pip install aiohttp`")
        self.session: Optional["aiohttp.ClientSession"] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()  # type: ignore
        await self.login()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        if self.session:
            await self.session.close()

    async def login(self) -> bool:
        if not self.session:
            return False
        async with self.session.get(self.URL) as response:
            csrf_token = csrf(await response.text())
        async with self.session.post(
            self.URL_LOGIN, data=self.get_login_data(csrf_token)
        ) as login_response:
            if login_response.status <= 400:
                return True
            raise Exception(
                "Login failed with status code: {}".format(login_response.status)
            )

    async def get(self, student_id: int) -> List[Tuple[str, str]] | None:
        if not self.session:
            return None
        async with self.session.get(
            self.URL_MESSAGES % change_unicode(str(student_id))
        ) as response:
            return self.format_data(await response.text())

    async def get_range(self, start: int, end: int) -> list[List[Tuple[str, str]]]:
        results = await asyncio.gather(*(self.get(i) for i in range(start, end + 1)))
        return [res for res in results if res]


class AutInfoSync(BaseAutInfo):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password)
        if not _sync_support:
            raise ImportError("Install requests via `pip install requests`")
        self.session = requests.Session()  # type: ignore
        self.login()

    def login(self) -> bool:
        response = self.session.get(self.URL)
        csrf_token = csrf(response.text)
        self.session.post(self.URL_LOGIN, data=self.get_login_data(csrf_token))
        return True

    def get(self, student_id: int) -> List[Tuple[str, str]]:
        response = self.session.get(self.URL_MESSAGES % change_unicode(str(student_id)))
        return self.format_data(response.text)

    def get_range(self, start: int, end: int) -> list[Tuple[str, str]]:
        return [res[0] for i in range(start, end + 1) if (res := self.get(i))]
