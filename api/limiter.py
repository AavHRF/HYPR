import time
from typing import Optional, Callable
from exceptions import TooManyRequests


class NSLeakyBucket:
    """
    Implementation of a Leaky Bucket ratelimiting concept for accessing the NS API
    within the API specification.
    """

    def __init__(self, func: Callable):

        self._max_requests: int = 45  # This gives a five-call grace buffer in case another program is being run by
        # accident
        self._reset_time: int = 0
        self._reset_period: int = 30
        self._last_call_made: Optional[int] = None
        self._requests_made = 0

        self.func = func

    def __call__(self, *args, **kwargs):
        # Check to see if the call period has rolled over
        if time.time().__trunc__() >= self._reset_time:
            self._requests_made = 0
            self.reset_time = time.time().__trunc__() + self._reset_period

        self._requests_made += 1
        if self._requests_made >= self._max_requests:
            raise TooManyRequests(self.reset_time)
        else:
            self.last_call_made = time.time().__trunc__()
            return self.func(*args, **kwargs)

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
