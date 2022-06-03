import time
import api.wrapper
import re
from collections import deque


# How this works
# the campaign object holds a list of nations which is a stack - first in, last out.
# it is assigned a search function, which is used to add nations to the stack periodically.
# if the stack gets too long, we start discarding excess past the limit
# a function can be called to pop off the nation at the top of the stack
# external scheduler logic should be used to refresh the stack and to determine when to get someone to send a telegram
# we don't handle the sending of telegrams, but we do use the API to figure out who needs one.

# Base campaign class


class Campaign:
    def __init__(
        self,
        name: str,
        priority: int,
        tgid: int,
        recruitment: bool,
        handler: api.wrapper.Client,
        search_params: dict,
    ):
        """
        :param name: Campaign name
        :param priority: Campaign priority
        :param tgid: TGID assigned to campaign
        :param recruitment: True if campaign is recruitment, used to help schedule appropriately
        :param handler: api.wrapper.Client instance for accessing NS API safely
        :param search_params: Parameters for search.
        """

        self._name = name
        self._priority = priority
        self._tgid = tgid
        self._recruitment = recruitment
        self.handler = handler
        self.search_params = search_params
        self._last_search = 0

        # create deque, with maximum length if necessary
        self.deque = deque(maxlen=480)

        # If True, deques are processed in reverse - oldest first.
        self.reverse = False

        # If True, search once and never search again.
        self.one_time = False

        # hook for custom init functionality.
        self.post_init()

    def post_init(self, *args, **kwargs) -> None:
        """
        Called by __init__(). Override and pass arguments when custom functionality is needed.
        """
        pass

    def update_deque(self) -> None:
        """
        Update the deque of nations to send telegrams using the assigned search function.

        :return:
        """

        # special logic for one-time searches - never refresh the deque again once it's been generated.
        if self.one_time is True:
            if self.last_search == 0:
                new_nations = self._search()
                self.last_search = time.time()
                # add items to deque - oldest at left, newest at right
                if self.reverse:
                    self.deque.extendleft(new_nations)
                else:
                    self.deque.extend(new_nations)
            else:
                # TODO: should pass a log message warning that the deque is not being refreshed anymore.
                pass
        else:
            new_nations = self._search()
            self.last_search = time.time()

            # add items to deque - oldest at left, newest at right
            if self.reverse:
                self.deque.extendleft(new_nations)
            else:
                self.deque.extend(new_nations)

    def _search(self) -> list:
        """
        Defines campaign search functionality for a Campaign. End user should never call this.

        If age matters, order should be oldest to newest to ensure deque limits discard correctly.

        :return: list of nations
        """
        pass

    def reset_deque(self) -> None:
        """
        CLear the deque and repopulate it using the assigned search function.

        :return:
        """

        self.deque.clear()
        self.update_deque()

    @property
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

    @property
    def tgid(self) -> int:
        """
        Return TGID for campaign.

        :return: tgid
        """

        return self._tgid

    @property
    def priority(self) -> int:
        """
        Return campaign priority

        :return: priority
        """

        return self._priority

    @property
    def name(self) -> str:
        """
        Return campaign name
        :return: name
        """
        return self._name

    @property
    def is_recruitment(self) -> bool:
        """
        Return recruitment type. You must set this yourself correctly for proper ratelimiting!

        :return: True if campaign is recruitment
        """

        return self._recruitment

    @property
    def last_search(self) -> int:
        """
        Return time the deque was last updated, in Unix time
        :return: last search time in seconds since epoch
        """

        return self._last_search

    @last_search.setter
    def last_search(self, value):
        self._last_search = value


# subclasses for key scenarios


class NewlyFounded(Campaign):
    """
    Recruits newly founded nations.
    """

    def _search(self) -> list:
        return self.handler.ns_request(params={"q": "newnations"})["newnations"]


class Residents(Campaign):
    """
    Targets all residents of a region. Runs once.
    """

    def post_init(self) -> None:
        # no deque limit - regions can be huge
        self.deque = deque()
        self.one_time = True

    def _search(self) -> list:
        return self.handler.ns_request(
            params={"region": self.search_params["region"], "q": "nations"}
        )["NATIONS"].split(":")


class Ejections(Campaign):
    """
    Targets new ejections.
    """

    def _search(self) -> list:
        region = self.search_params["region"]
        client = self.handler

        if region is None:
            events = client.ns_request(params={"q": "happenings", "filter": "eject"})
        else:
            events = client.ns_request(
                params={
                    "q": "happenings",
                    "filter": "eject",
                    "view": f"region.{region}",
                }
            )

        nations = []
        for event in events:
            nations.append(re.search(r"[\w-]+(?=@@ was)", event["text"]).group(0))

        return nations


class Exits(Campaign):
    """
    Targets nations leaving a region.
    """

    def _search(self) -> list:
        region = self.search_params["region"]
        client = self.handler

        events = client.ns_request(
            params={"q": "happenings", "filter": "move", "view": f"region.{region}"}
        )
        nations = []
        for event in events:
            destination = re.search(r"[\w-]+(?=%%\.)", event["text"]).group(0)
            source = re.search(r"[\w-]+(?=%% to)", event["text"]).group(0)
            if source == region and destination != "the_rejected_realms":
                nations.append(re.search(r"[\w-]+(?=@@ relo)", event["text"]).group(0))

        return nations


class Entrances(Campaign):
    """
    Targets nations entering a region.
    """

    def _search(self) -> list:
        region = self.search_params["region"]
        client = self.handler

        events = client.ns_request(
            params={"q": "happenings", "filter": "move", "view": f"region.{region}"}
        )

        nations = []
        for event in events:
            destination = re.search(r"[\w-]+(?=%%\.)", event["text"]).group(0)
            if destination == region:
                nations.append(re.search(r"[\w-]+(?=@@ relo)", event["text"]).group(0))

        return nations


class WorldAssemblyAdmissions(Campaign):
    """
    Targets nations newly admitted to the World Assembly
    """

    def _search(self) -> list:
        region = self.search_params["region"]
        client = self.handler

        if region is None:
            events = client.ns_request(params={"q": "happenings", "filter": "member"})
        else:
            events = client.ns_request(
                params={
                    "q": "happenings",
                    "filter": "member",
                    "view": f"region.{region}",
                }
            )

        nations = []
        for event in events:
            check = re.search(r"[\w-]+(?=@@ was admitted)", event["text"])
            if check is not None:
                nations.append(check.group(0))

        return nations


class WorldAssemblyResignations(Campaign):
    def _search(self) -> list:
        region = self.search_params["region"]
        client = self.handler

        if region is None:
            events = client.ns_request(params={"q": "happenings", "filter": "member"})
        else:
            events = client.ns_request(
                params={
                    "q": "happenings",
                    "filter": "member",
                    "view": f"region.{region}",
                }
            )

        nations = []
        for event in events:
            check = re.search(r"[\w-]+(?=@@ resigned)", event["text"])
            if check is not None:
                nations.append(check.group(0))

        return nations


class NewEndorsements(Campaign):
    """
    Targets nations recently endorsing a specific nation.
    """

    def _search(self) -> list:
        nation = self.search_params["nation"]
        region = self.search_params["region"]
        client = self.handler

        if region is None:
            events = client.ns_request(params={"q": "happenings", "filter": "endo"})
        else:
            events = client.ns_request(
                params={"q": "happenings", "filter": "endo", "view": f"region.{region}"}
            )

        nations = []
        for event in events:
            endorser = re.search(r"[\w-]+(?=@@ en)", event["text"])
            endorsee = re.search(r"[\w-]+(?=@@\.)", event["text"])

            if endorser is not None and endorsee.group(0) == nation:
                nations.append(endorser.group(0))

        return nations


class NewWithdrawnEndorsements(Campaign):
    """
    Targets nations recently withdrawing an endorsement of a specific nation.
    """

    def _search(self) -> list:
        nation = self.search_params["nation"]
        region = self.search_params["region"]
        client = self.handler

        if region is None:
            events = client.ns_request(params={"q": "happenings", "filter": "endo"})
        else:
            events = client.ns_request(
                params={"q": "happenings", "filter": "endo", "view": f"region.{region}"}
            )

        nations = []
        for event in events:
            endorser = re.search(r"[\w-]+(?=@@ wi)", event["text"])
            endorsee = re.search(r"[\w-]+(?=@@\.)", event["text"])

            if endorser is not None and endorsee.group(0) == nation:
                nations.append(endorser.group(0))

        return nations


class Endorsements(Campaign):
    """
    Targets all nations currently endorsing a specific nation.
    """

    def post_init(self) -> None:
        self.one_time = True

        # no deque limit for this - endo lists can be huge
        self.deque = deque()

    def _search(self) -> list:
        nation = self.search_params["nation"]
        client = self.handler
        return client.ns_request(params={"nation": nation, "q": "endorsements"})[
            "ENDORSEMENTS"
        ].split(",")


class WorldAssemblyDelegates(Campaign):
    """
    Targets all World Assembly Delegates
    """

    def post_init(self) -> None:
        self.one_time = True

        # no deque limit for this - there are a lot of WADs
        self.deque = deque()

    def _search(self) -> list:
        client = self.handler
        return client.ns_request(params={"wa": "1", "q": "delegates"})["delegates"]


class WorldAssemblyMembers(Campaign):
    """
    Targets all World Assembly members
    """

    def post_init(self) -> None:
        self.one_time = True
        # no deque limit for this - there are a lot of WA members
        self.deque = deque()

    def _search(self) -> list:
        client = self.handler
        return client.ns_request(params={"wa": "1", "q": "members"})["members"]
