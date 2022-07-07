import time
from typing import Optional, Callable

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
Ratelimiter code is below. It uses a leaky bucket to ratelimit the
requests to the NS API. Notably, it does not ensure that only one request
is made at a time.
"""


class NSLeakyBucket:
    """
    Implementation of a Leaky Bucket ratelimiting concept for accessing the NS API
    within the API specification.
    """

    def __init__(self):

        self._max_requests: int = 45  # This gives a five-call grace buffer in case another program is being run by
        # accident
        self._reset_time: int = 0
        self._reset_period: int = 30
        self._last_call_made: Optional[int] = None
        self._requests_made = 0

    def __call__(self, func: Callable, *args, **kwargs):
        # Check to see if the call period has rolled over
        if time.time().__trunc__() >= self._reset_time:
            self._requests_made = 0
            self.reset_time = time.time().__trunc__() + self._reset_period

        self._requests_made += 1
        if self.requests_made >= self._max_requests:
            raise TooManyRequests(self.reset_time)
        else:
            self.last_call_made = time.time().__trunc__()
            return func(*args, **kwargs)

    @property
    def reset_time(self) -> Optional[int]:
        if self._reset_time == 0:
            return None
        else:
            return self._reset_time

    @reset_time.setter
    def reset_time(self, value: int) -> None:
        self._reset_time = value

    @property
    def last_call_made(self) -> Optional[int]:
        return self._last_call_made

    @last_call_made.setter
    def last_call_made(self, value: Optional[int]) -> None:
        self._last_call_made = value

    @property
    def max_requests(self) -> int:
        return self._max_requests

    @property
    def requests_made(self) -> int:
        return self._requests_made
