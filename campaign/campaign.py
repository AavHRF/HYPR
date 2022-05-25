import time
from typing import Callable
from collections import deque

# How this works
# the campaign object holds a list of nations which is a stack - first in, last out.
# it is assigned a search function, which is used to add nations to the stack periodically.
# if the stack gets too long, we start discarding excess past the limit
# a function can be called to pop off the nation at the top of the stack
# external scheduler logic should be used to refresh the stack and to determine when to get someone to send a telegram
# we don't handle the sending of telegrams, but we do use the API to figure out who needs one.


class Campaign:
    def __init__(self, name: str, priority: int, tgid: int, search: Callable, args: list, reverse: bool = False):
        """

        :param name: Campaign name
        :param priority: Campaign priority
        :param tgid: TGID assigned to campaign
        :param search: Search function used to generate new campaign targets
        :param args: Arguments to pass to search function
        :param reverse: Run campaign in first-in-first-out order instead of first-in-last-out.
        """
        self.name = name
        self.priority = priority
        self.tgid = tgid
        self.search = search
        self.args = args
        self.reverse = reverse

        self.deque = deque()
        self.last_search = 0

    def update_deque(self) -> None:
        """
        Update the deque of nations to send telegrams using the assigned search function.

        :return:
        """
        # generate list of new nations
        new_nations = self.search(*self.args)
        self.last_search = time.time()

        # add items to deque - oldest at left, newest at right
        for nation in new_nations:
            self.deque.append([nation])

    def reset_deque(self) -> None:
        """
        CLear the deque and repopulate it using the assigned search function.

        :return:
        """

        self.deque.clear()
        self.update_deque()

    def nation(self) -> str:
        """
        Return next nation to be telegrammed and remove from deque.

        If Campaign.reverse is True, the oldest recipient is returned; Otherwise, the newest one is.

        :return: nation name
        """
        if self.reverse:
            return self.deque.popleft()[0]
        else:
            return self.deque.pop()[0]

    def tgid(self) -> int:
        """
        Return TGID for campaign.

        :return: tgid
        """

        return self.tgid

    def priority(self) -> int:
        """
        Return campaign priority

        :return: priority
        """

        return self.priority

    def name(self) -> str:
        """
        Return campaign name
        :return: name
        """
        return self.name

    def last_search(self) -> int:
        """
        Return time the deque was last updated, in Unix time
        :return: last search time in seconds since epoch
        """

        return self.last_search

