"""Simplifies interacting with an ActivityPub server / instance.

This is a minimal implementation only implementing some API calls. API
calls supported will likely be expanded over time. However, do not
expect a full or complete implementation of the ActivityPub API.
"""
import asyncio
import logging
import random
from typing import Any
from typing import Optional
from typing import TypeVar
from urllib.parse import parse_qs
from urllib.parse import urlparse

import aiohttp
import arrow

from . import __display_name__
from . import USER_AGENT

logger = logging.getLogger(__display_name__)


ActivityPubClass = TypeVar("ActivityPubClass", bound="ActivityPub")
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"


class ActivityPub:
    """Simplifies interacting with an ActivityPub server / instance.

    This is a minimal implementation only implementing methods needed
    for the function of MastodonAmnesia
    """

    # It's not that many over. It's using 9 instance attributes (opposed to 7 being
    # deemed the max attributes a class should have)
    # pylint: disable-msg=too-many-instance-attributes

    def __init__(
        self: ActivityPubClass,
        instance: str,
        session: aiohttp.ClientSession,
        access_token: str,
    ) -> None:
        self.instance = instance
        self.authorization = f"Bearer {access_token}"
        self.session = session
        self.pagination_max_id: Optional[str] = None
        self.pagination_min_id: Optional[str] = None
        self.is_instance_pleroma = False
        self.ratelimit_limit = 300
        self.ratelimit_remaining = 300
        self.ratelimit_reset = arrow.now()

    async def verify_credentials(self: ActivityPubClass) -> Any:
        """It verifies the credentials of the user.

        :param self: ActivityPubClass
        :type self: ActivityPubClass
        :return: The response is a JSON object containing the account's information.
        """
        headers = {"Authorization": self.authorization}
        url = f"{self.instance}/api/v1/accounts/verify_credentials"
        async with self.session.get(url=url, headers=headers) as response:
            self.__update_ratelimit(response.headers)
            await ActivityPub.__check_exception(response=response)
            self.__parse_next_prev(links=response.headers.get("Link"))
            return await response.json()

    async def determine_instance_type(self: ActivityPubClass) -> None:
        """It checks if the instance is a Pleroma instance or not.

        :param self: The class itself
        :type self: ActivityPubClass
        """
        instance = self.instance
        if "http" not in self.instance:
            instance = f"https://{self.instance}"

        async with self.session.get(url=f"{instance}/api/v1/instance") as response:
            await ActivityPub.__check_exception(response=response)
            response_dict = await response.json()
        self.instance = instance
        if "Pleroma" in response_dict["version"]:
            self.is_instance_pleroma = True
        logger.debug(
            "ActivityPub.determine_instance_type - is_instance_pleroma = %s",
            self.is_instance_pleroma,
        )

    async def get_account_statuses(
        self: ActivityPubClass,
        account_id: str,
        max_id: Optional[str] = None,
        min_id: Optional[str] = None,
    ) -> Any:
        """It gets the statuses of a given account.

        :param self: The class instance
        :type self: ActivityPubClass
        :param account_id: The account ID of the account you want to get the statuses of
        :type account_id: str
        :param max_id: The ID of the last status you want to get
        :type max_id: Optional[str]
        :param min_id: The ID of the oldest status you want to retrieve
        :type min_id: Optional[str]
        :return: A list of statuses.
        """
        await self.__pre_call_checks()

        headers = {"Authorization": self.authorization}
        paging = "?"
        url = f"{self.instance}/api/v1/accounts/{account_id}/statuses"
        if max_id:
            paging += f"max_id={max_id}"
        if min_id:
            if len(paging) > 1:
                paging += "&"
            paging += f"min_id={min_id}"
        if max_id or min_id:
            url += paging
        logger.debug("ActivityPub.get_account_statuses - url = %s", url)
        async with self.session.get(url=url, headers=headers) as response:
            self.__update_ratelimit(response.headers)
            await ActivityPub.__check_exception(response=response)
            self.__parse_next_prev(links=response.headers.get("Link"))
            return await response.json()

    async def delete_status(self: ActivityPubClass, status_id: str) -> Any:
        """It deletes a status.

        :param self: The class that inherits from ActivityPub
        :type self: ActivityPubClass
        :param status_id: The ID of the status you want to delete
        :type status_id: str
        :return: The response from the server.
        """

        # add random delay of up to 3 seconds in case we are deleting many
        # statuses in a batch
        sleep_for = random.SystemRandom().random() * 3
        logger.debug(
            "ActivityPub.delete_status - status_id = %s - sleep_for = %s",
            status_id,
            sleep_for,
        )
        await asyncio.sleep(delay=sleep_for)

        await self.__pre_call_checks()

        headers = {"Authorization": self.authorization}
        url = f"{self.instance}/api/v1/statuses/{status_id}"
        async with self.session.delete(url=url, headers=headers) as response:
            self.__update_ratelimit(response.headers)
            await ActivityPub.__check_exception(response=response)
            self.__parse_next_prev(links=response.headers.get("Link"))
            return await response.json()

    async def __pre_call_checks(self: ActivityPubClass) -> None:
        """Checks to perform before contacting the instance server.

        For now just looking at rate limits by checking if the rate
        limit is 0 and the rate limit reset time is in the future, raise
        a RatelimitError
        """
        logger.debug(
            "ActivityPub.__pre_call_checks "
            "- Limit remaining: %s "
            "- Limit resetting at %s",
            self.ratelimit_remaining,
            self.ratelimit_reset,
        )
        if self.ratelimit_remaining == 0 and self.ratelimit_reset > arrow.now():
            raise RatelimitError(429, None, "Rate limited")

    @staticmethod
    async def get_auth_token(
        instance_url: str, username: str, password: str, session: aiohttp.ClientSession
    ) -> str:
        """It creates an app, then uses that app to get an access token.

        :param instance_url: The URL of the Mastodon instance you want to connect to
        :type instance_url: str
        :param username: The username of the account you want to get an auth_token for
        :type username: str
        :param password: The password of the account you want to get an auth_token for
        :type password: str
        :param session: aiohttp.ClientSession
        :type session: aiohttp.ClientSession
        :return: The access token is being returned.
        """
        if "http" not in instance_url:
            instance_url = f"https://{instance_url}"

        form_data = aiohttp.FormData()
        form_data.add_field("client_name", USER_AGENT)
        form_data.add_field(
            "client_website",
            "https://codeberg.org/MarvinsMastodonTools/mastodonamnesia",
        )
        form_data.add_field("scopes", "read write")
        form_data.add_field("redirect_uris", REDIRECT_URI)
        async with session.post(
            url=f"{instance_url}/api/v1/apps",
            data=form_data,
        ) as response:
            await ActivityPub.__check_exception(response)
            response_dict = await response.json()

        client_id = response_dict["client_id"]
        client_secret = response_dict["client_secret"]
        form_data = aiohttp.FormData()
        form_data.add_field("client_id", client_id)
        form_data.add_field("client_secret", client_secret)
        form_data.add_field("scope", "read write")
        form_data.add_field("redirect_uris", REDIRECT_URI)
        form_data.add_field("grant_type", "password")
        form_data.add_field("username", username)
        form_data.add_field("password", password)
        async with session.post(
            url=f"{instance_url}/oauth/token",
            data=form_data,
        ) as response:
            await ActivityPub.__check_exception(response)
            response_dict = await response.json()

        return str(response_dict["access_token"])

    def __parse_next_prev(self: ActivityPubClass, links: Optional[str]) -> None:
        """It takes a string of the form `https://example.com/api/v1/timelines/
        home?min_id=12345&max_id=67890` and extracts the values of `min_id` and
        `max_id` from it and stores them in the instance attributes
        pagination_min_id and pagination_max_id.

        :param self: The class that is being parsed
        :type self: ActivityPubClass
        :param links: The links header from the response
        :type links: Optional[str]
        """
        logger.debug("ActivityPub.__parse_next_prev - links = %s", links)

        if links:
            list_of_urls = []
            for comma_links in links.split(sep=", "):
                list_of_urls += comma_links.split(sep="; ")

            self.pagination_min_id = None
            self.pagination_max_id = None
            for url_part in list_of_urls:
                parsed_url = urlparse(url=url_part.lstrip("<").rstrip(">"))
                queries_dict = parse_qs(str(parsed_url.query))
                min_id = queries_dict.get("min_id")
                max_id = queries_dict.get("max_id")
                if min_id:
                    self.pagination_min_id = min_id[0]
                if max_id:
                    self.pagination_max_id = max_id[0]

        logger.debug(
            "ActivityPub.__parse_next_prev - min_id = %s", self.pagination_min_id
        )
        logger.debug(
            "ActivityPub.__parse_next_prev - max_id = %s", self.pagination_max_id
        )

    def __update_ratelimit(self: ActivityPubClass, headers: Any) -> None:
        """If the instance is not Pleroma, update the ratelimit variables.

        :param self: The class that is being updated
        :type self: ActivityPubClass
        :param headers: The headers of the response
        :type headers: Any
        """
        if not self.is_instance_pleroma:
            self.ratelimit_limit = int(headers.get("X-RateLimit-Limit"))
            self.ratelimit_remaining = int(headers.get("X-RateLimit-Remaining"))
            self.ratelimit_reset = arrow.get(headers.get("X-RateLimit-Reset"))
        logger.debug(
            "ActivityPub.__update_ratelimit "
            "- Pleroma Instance: %s "
            "- RateLimit Limit %s",
            self.is_instance_pleroma,
            self.ratelimit_limit,
        )
        logger.debug(
            "ActivityPub.__update_ratelimit "
            "- Limit remaining: %s "
            "- Limit resetting at %s",
            self.ratelimit_remaining,
            self.ratelimit_reset,
        )

    @staticmethod
    async def __check_exception(response: aiohttp.ClientResponse) -> None:
        """If the response status is greater than or equal to 400, then raise
        an appropriate exception.

        :param response: aiohttp.ClientResponse
        :type response: aiohttp.ClientResponse
        """
        logger.debug(
            "ActivityPub.__check_exception - response.headers = %s", response.headers
        )
        logger.debug(
            "ActivityPub.__check_exception - response.status = %s", response.status
        )
        if response.status >= 400:

            error_message = await ActivityPub.__determine_error_message(response)

            if response.status == 401:
                raise UnauthorizedError(response.status, response.reason, error_message)
            if response.status == 403:
                raise ForbiddenError(response.status, response.reason, error_message)
            if response.status == 404:
                raise NotFoundError(response.status, response.reason, error_message)
            if response.status == 409:
                raise ConflictError(response.status, response.reason, error_message)
            if response.status == 410:
                raise GoneError(response.status, response.reason, error_message)
            if response.status == 422:
                raise UnprocessedError(response.status, response.reason, error_message)
            if response.status == 429:
                raise RatelimitError(response.status, response.reason, error_message)
            if response.status < 500:
                raise ClientError(response.status, response.reason, error_message)

            raise ServerError(response.status, response.reason, error_message)

    @staticmethod
    async def __determine_error_message(response: aiohttp.ClientResponse) -> str:
        """If the response is JSON, return the error message from the JSON,
        otherwise return the response text.

        :param response: aiohttp.ClientResponse
        :type response: aiohttp.ClientResponse
        :return: The error message is being returned.
        """

        error_message = "Exception has occurred"
        try:
            content = await response.json()
            error_message = content["error"]
        except (aiohttp.ClientError, KeyError):
            try:
                error_message = await response.text()
            except (aiohttp.ClientError, LookupError):
                pass
        logger.debug(
            "ActivityPub.__determine_error_message - error_message = %s", error_message
        )
        return error_message


class ActivityPubError(Exception):
    """Base class for all mastodon exceptions."""


class NetworkError(ActivityPubError):
    """`NetworkError` is a subclass of `ActivityPubError` that is raised when
    there is a network error."""

    pass


class ApiError(ActivityPubError):
    """`ApiError` is a subclass of `ActivityPubError` that is raised when there
    is an API error."""

    pass


class ClientError(ActivityPubError):
    """`ClientError` is a subclass of `ActivityPubError` that is raised when
    there is a client error."""

    pass


class UnauthorizedError(ClientError):
    """`UnauthorizedError` is a subclass of `ClientError` that is raised when
    the user represented by the auth_token is not authorized to perform a
    certain action."""

    pass


class ForbiddenError(ClientError):
    """`ForbiddenError` is a subclass of `ClientError` that is raised when the
    user represented by the auth_token is forbidden to perform a certain
    action."""

    pass


class NotFoundError(ClientError):
    """`NotFoundError` is a subclass of `ClientError` that is raised when an
    object for an action cannot be found."""

    pass


class ConflictError(ClientError):
    """`ConflictError` is a subclass of `ClientError` that is raised when there
    is a conflict with performing an action."""

    pass


class GoneError(ClientError):
    """`GoneError` is a subclass of `ClientError` that is raised when an object
    for an action has gone / been deleted."""

    pass


class UnprocessedError(ClientError):
    """`UnprocessedError` is a subclass of `ClientError` that is raised when an
    action cannot be processed."""

    pass


class RatelimitError(ClientError):
    """`RatelimitError` is a subclass of `ClientError` that is raised when
    we've reached a limit of number of actions performed quickly."""

    pass


class ServerError(ActivityPubError):
    """`ServerError` is a subclass of `ActivityPubError` that is raised when
    the server / instance encountered an error."""

    pass
