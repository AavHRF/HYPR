from typing import Optional

"""
The following exceptions are raised by the limiter in the event of a check failing.
They each describe a potential condition, and return the number of seconds before
the caller should retry the API request.
"""


class TooManyRequests(Exception):
    """
    Raised by NSLeakyBucket if too many requests to the NS API are made
    within the reset period.
    """

    pass


class TelegramLimitExceeded(Exception):
    """
    Raised by NSLeakyBucket if too many telegram requests are made
    within the reset period.
    """

    pass


class RecruitmentLimitExceeded(Exception):
    """
    Raised by NSLeakyBucket if too many recruitment requests are made
    within the reset period.
    """

    pass


"""
This exception is raised by a campaign search failure.
"""


class SearchException(Exception):
    """
    The campaign search failed for the provided reason.
    """
    pass


"""
These exceptions are raised by the API wrapper when a request fails.
They each describe a potential failure and will describe how the program
should handle the failure.
"""


class APIException(Exception):
    """
    A generic API exception that all other API exceptions inherit from.
    Used primarily for typehinting in generics.
    """

    def __init__(self, message: Optional[str] = None, exit_program: Optional[bool] = False, exit_code: Optional[int] = 1):
        if message:
            super().__init__(message)
        if exit_program:
            exit(exit_code)


class AccessForbidden(APIException):
    """
    Raised when the API returns a 403 status code.
    """
    pass


class Conflict(APIException):
    """
    Raised when the API returns a 409 status code.
    """
    pass


class ServerError(APIException):
    """
    Raised when the API returns a 500 status code.
    """
    pass


class ServiceUnavailable(APIException):
    """
    Raised when the API returns a 503 status code.
    """
    pass


class CloudflareError(APIException):
    """
    Raised when the API returns a 522 status code.
    """
    pass
