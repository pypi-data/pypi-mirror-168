"""A class for interacting with Ogero APIs"""
import logging
from typing import List, Optional
from ogero.const import API_ENDPOINTS, DefaultHeaders, default_headers
from ogero.types import Account, BillInfo, ConsumptionInfo, ErrorResponse, LoginResponse
from ogero.utils import (
    parse_accounts,
    parse_bills,
    parse_consumption_info,
    parse_error_message,
)
import requests

from .exceptions import AuthenticationException


class Ogero:
    """A class for interacting with Ogero APIs"""

    def __init__(
        self,
        username: str,
        password: str,
        session: Optional[requests.Session] = None,
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
            self.session = requests.Session()
        else:
            self.session = session

    def login(self):
        """Logs into the account and caches the session id."""

        url = API_ENDPOINTS["login"]

        headers = default_headers()
        payload = {"Username": self.username, "Password": self.password}

        with self.session.post(url, headers=headers, data=payload) as response:
            self.session_id = None
            self.handle_response_fail(response)
            jsondata: LoginResponse = response.json()

        self.logger.debug("Login response status: %s", response.status_code)
        # self.logger.debug("Dumping login response: %s", json.dumps(jsondata))

        self.session_id = jsondata["SessionID"]

        return True

    def get_accounts(self) -> List[Account]:
        """Get user phone/internet accounts"""

        url = API_ENDPOINTS["dashboard"]

        response = self.request_get(url)
        content = response.content
        accounts = parse_accounts(content)

        self.logger.debug("Dashboard response status: %s", response.status_code)
        self.logger.debug("Dumping accounts response: %s", accounts)

        return accounts

    def get_bill_info(self, account: Account = None) -> BillInfo:
        """Get bill info for phone account
        ```
        @param account: Account - Phone/Internet account
        ```
        """

        url = API_ENDPOINTS["bill"]

        response = self.request_get(url, account)
        content = response.content
        bill_info = parse_bills(content)

        self.logger.debug("Bill response status: %s", response.status_code)
        self.logger.debug("Dumping bill response: %s \n%s", bill_info, bill_info.bills)

        return bill_info

    def get_consumption_info(self, account: Account = None) -> ConsumptionInfo:
        """Get consumption info for internet account
        ```
        @param account: Account - Phone/Internet account
        ```
        """
        url = API_ENDPOINTS["consumption"]

        response = self.request_get(url, account)
        
        content = response.content
        consumption_info = parse_consumption_info(content)

        self.logger.debug("Consumption response status: %s", response.status_code)
        self.logger.debug("Dumping consumption response: %s", consumption_info)

        return consumption_info

    def request_get(
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
            self.login()

        try:
            params = self._get_params(account)
            formatted_url = url.format_map(params)
            response = self.session.get(formatted_url, headers=headers)
            self.handle_response_fail(response)
        except AuthenticationException as ex:
            self.logger.debug(f"AuthenticationException: {ex}")
            self.login()
            params = self._get_params(account)
            formatted_url = url.format_map(params)
            response = self.session.get(formatted_url, headers=headers)

        self.handle_response_fail(response)
        return response

    def _get_params(self, account: Account = None):
        """Generate URL required params
        ```
        @param account: Account - Phone/Internet account
        ```
        """
        if self.session_id is None:
            raise AuthenticationException("Login first")

        return {
            "session_id": self.session_id,
            "username": self.username,
            "phone_account": account.phone if account else "",
            "internet_account": account.internet if account else "",
        }

    def handle_response_fail(
        self,
        response: requests.Response,
    ) -> None:
        """Handles response status codes
        ```
        @param response - requests.Response - the full response object
        ```
        """
        self.logger.debug(
            f"status: {response.status_code}, type: {response.headers.get('content-type')}"
        )
        if (
            response.status_code == 400
            and "application/json" in response.headers.get("content-type")
        ):
            resp: ErrorResponse = response.json()
            msg = resp["error"]["message"]
            self.logger.debug(f"AuthenticationException: {msg}")
            raise AuthenticationException(msg)

        if (
            response.status_code == 200
            and "text/html" in response.headers.get("content-type")
        ):
            content = response.content
            msg = parse_error_message(content)
            if msg is not None and msg.startswith("You are required to login"):
                raise AuthenticationException(msg)

        response.raise_for_status()
