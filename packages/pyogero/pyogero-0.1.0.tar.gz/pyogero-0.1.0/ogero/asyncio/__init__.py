""" aiohttp support for Ogero """

import logging
import sys
from typing import List, Optional

from ..types import Account, BillInfo, ConsumptionInfo, ErrorResponse, LoginResponse
from ..utils import (
    parse_accounts,
    parse_bills,
    parse_consumption_info,
    parse_error_message,
)
from ..const import API_ENDPOINTS, DefaultHeaders, default_headers
from ..exceptions import AuthenticationException

try:
    import aiohttp
    from aiohttp.client import ClientResponse
except ImportError as error_message:
    print(f"Failed to import aiohttp, bailing: {error_message}", file=sys.stderr)
    sys.exit(1)


class Ogero:
    """aiohttp class for interacting with Ogero APIs"""

    def __init__(
        self,
        username: str,
        password: str,
        session: Optional[aiohttp.client.ClientSession] = None,
        debug: bool = False,
        logger: logging.Logger = logging.getLogger(),
    ):
        """Setup function
        ```
        @param username: str - username for Ogero account
        @param password: str - password for Ogero account
        @param debug: bool - debug mode
        @param logger: Logger
        ```
        """

        if not (username and password):
            raise AuthenticationException(
                "You need to supply both username and password"
            )

        self.username = username
        self.password = password
        self.debug = debug
        self.logger = logger
        self.session_id = None

        if not session:
            self.session = aiohttp.ClientSession()
        else:
            self.session = session

    async def login(self):
        """Logs into the account and caches the session id."""

        url = API_ENDPOINTS["login"]

        headers = default_headers()
        payload = {"Username": self.username, "Password": self.password}

        async with self.session.post(url, headers=headers, data=payload) as response:
            self.session_id = None
            await self.handle_response_fail(response)
            jsondata: LoginResponse = await response.json()

        self.logger.debug("Login response status: %s", response.status)
        # self.logger.debug("Dumping login response: %s", json.dumps(jsondata))

        self.session_id = jsondata["SessionID"]

        return True

    async def get_accounts(self, account: Account = None) -> List[Account]:
        """Get user phone/internet accounts"""

        url = API_ENDPOINTS["dashboard"]

        response = await self.request_get(url, account)
        await self.handle_response_fail(response)
        content = await response.text()
        accounts = parse_accounts(content)

        self.logger.debug("Dashboard response status: %s", response.status)
        self.logger.debug("Dumping accounts response: %s", accounts)

        return accounts

    async def get_bill_info(self, account: Account = None) -> BillInfo:
        """Get bill info for phone account
        ```
        @param account: Account - Phone/Internet account
        ```
        """

        url = API_ENDPOINTS["bill"]

        response = await self.request_get(url, account)
        await self.handle_response_fail(response)
        content = await response.text()
        bill_info = parse_bills(content)

        self.logger.debug("Bill response status: %s", response.status)
        self.logger.debug("Dumping bill response: %s \n%s", bill_info, bill_info.bills)

        return bill_info

    async def get_consumption_info(self, account: Account = None) -> ConsumptionInfo:
        """Get consumption info for internet account
        ```
        @param account: Account - Phone/Internet account
        ```
        """

        url = API_ENDPOINTS["consumption"]

        response = await self.request_get(url, account)
        await self.handle_response_fail(response)
        content = await response.text()
        consumption_info = parse_consumption_info(content)

        self.logger.debug("Consumption response status: %s", response.status)
        self.logger.debug("Dumping consumption response: %s", consumption_info)

        return consumption_info

    async def request_get(
        self,
        url: str,
        account: Account = None,
        headers: DefaultHeaders = default_headers(),
    ):
        """Send get request and check if session is active
        ```
        @param url: str - Endpoint url
        @param account: Account - Phone/Internet account
        @param headers: DefaultHeaders
        ```
        """
        if self.session_id is None:
            await self.login()

        try:
            params = self._get_params(account)
            formatted_url = url.format_map(params)
            response = await self.session.get(formatted_url, headers=headers)
            await self.handle_response_fail(response)
        except AuthenticationException as ex:
            self.logger.debug(f"AuthenticationException: {ex}")
            await self.login()
            params = self._get_params(account)
            formatted_url = url.format_map(params)
            response = await self.session.get(formatted_url, headers=headers)

        return response

    def _get_params(self, account: Account = None):

        if self.session_id is None:
            raise AuthenticationException("Login first")

        return {
            "session_id": self.session_id,
            "username": self.username,
            "phone_account": account.phone if account else "",
            "internet_account": account.internet if account else "",
        }

    async def handle_response_fail(
        self,
        response: ClientResponse,
    ) -> None:
        """Handles response status codes.
        ```
        @param response - aiohttp.Response - the full response object
        ```
        """

        if response.status == 400 and response.content_type == "application/json":
            resp: ErrorResponse = await response.json()
            msg = resp["error"]["message"]
            self.logger.debug(f"AuthenticationException: {msg}")
            raise AuthenticationException(msg)

        if response.status == 200 and response.content_type == "text/html":
            content = await response.text()
            msg = parse_error_message(content)
            if msg is not None and msg.startswith("You are required to login"):
                raise AuthenticationException(msg)

        response.raise_for_status()
