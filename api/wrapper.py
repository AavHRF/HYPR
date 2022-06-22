import requests
from typing import List, Optional
from requests.exceptions import HTTPError
from xml.etree import ElementTree
from api import NSLeakyBucket


# Globaled ratelimiter and constant API url
# Yes, it's probably bad practice. No, it doesn't matter.
# It's just one file, one scope, and they aren't imported in __init__.py
# It's fine.
API_BASE_URL = "https://www.nationstates.net/cgi-bin/api.cgi"
bucket = NSLeakyBucket()


class Client:
    @property
    def requests_made(self) -> int:
        return self._requests_made

    @requests_made.setter
    def requests_made(self, value: int) -> None:
        self._requests_made = value

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, value: dict) -> None:
        self._headers = value

    @property
    def key(self) -> Optional[str]:
        return self._key if self._key else None

    @key.setter
    def key(self, value: str) -> None:
        self._key = value

    def __init__(self, useragent: str):
        """
        Functions of the API client:
        ns_request - Makes a request to the NationStates API, and parses the response from XML to JSON

        Properties of the class:
        requests_made - The number of requests made to the API
        headers - The headers to send with each request
        key - The NS API client key to use with telegram requests

        Both of the above have setters, so they can be modified mid-run should that become necessary.

        requests_made is incremented for each request made, and is reset to 0 when the ratelimit period
        rolls over. This is to compensate for the happenings endpoint being clunky to attach X-Ratelimit-requests-seen
        to on return due to its complicated structure. Every other endpoint returns a X-Ratelimit-requests-seen value
        in addition to the rest of its data, however, which does make this somewhat redundant. Could definitely use
        some work to hopefully remove this, but it's low-priority for now. If you're reading this and aren't a maintainer,
        but it bugs you, PR a change! We're open source for a reason!

        Update 6/20/2022: I am tempted to deprecate requests_made as NSLeakyBucket is now a class and handles the
        ratelimiting. Additionally, added the API client key as a getter/setter in this class to enable telegram
        sending.

        The key is set to None but can be modified via calling the setter. This enables a clean constructor
        that only takes a useragent in the case that you aren't sending telegrams during a run, but if you are, you can
        set the key via the config file, load it in, and then it will auto-set enabling telegrams. Otherwise, it will
        raise an exception telling you that there is no key.

        :param useragent: An identifying string for the client
        """
        self._headers = {"User-Agent": useragent}
        self._requests_made = 0
        self._key = None

    @bucket
    def ns_request(self, params: dict) -> dict | List[dict]:
        """
        Wrapper to make NS requests less shitty to work with

        :param params: Dict of parameters to send to the API
        :return: Response from the request serialized to JSON or a list of JSON formatted responses
        """
        r = requests.get(API_BASE_URL, headers=self.headers, params=params)

        # Ensure a sane return if the request fails
        try:
            r.raise_for_status()
        except HTTPError:
            self.requests_made += 1
            # Authentication errors
            if r.status_code == 403:
                return {
                    "error": "403",
                    "ratelimit": r.headers["X-Ratelimit-requests-seen"],
                }
            if r.status_code == 409:
                return {
                    "error": "409",
                    "ratelimit": r.headers["X-Ratelimit-requests-seen"],
                }
            if r.status_code == 429:
                return {
                    "error": "429",
                    "ratelimit": r.headers["X-Ratelimit-requests-seen"],
                }

            # Server errors
            if r.status_code == 500:
                return {"error": "500"}
            if r.status_code == 503:
                return {"error": "503"}
            if r.status_code == 504:
                return {"error": "504"}
            if r.status_code == 522:
                return {"error": "522"}
            else:
                return {"error": r.text}

        self.requests_made = int(r.headers["X-ratelimit-requests-seen"])

        # NS still uses XML, so we need to parse it
        try:
            root = ElementTree.fromstring(r.text)
        except ElementTree.ParseError:  # Malformed XML response guard
            return {
                "error": "ParseError",
                "ratelimit": r.headers["X-Ratelimit-requests-seen"],
            }

        # Check through our params to figure out what we're looking for
        if "nation" in params.keys():
            vals = {}
            for child in root:
                # Some tags contain subtags, so we need to check for that
                if len(child) > 0:
                    s = {}
                    for sub in child:
                        s[sub.tag] = sub.text
                    vals[child.tag] = s
                else:
                    vals[child.tag] = child.text
            return vals

        elif "region" in params.keys():
            # This block is an exact copy of the above, but for regions
            # If you modify one, please modify the other
            vals = {}
            for child in root:
                # Some tags contain subtags, so we need to check for that
                if len(child) > 0:
                    s = {}
                    for sub in child:
                        s[sub.tag] = sub.text
                    vals[child.tag] = s
                else:
                    vals[child.tag] = child.text
            return vals

        else:
            # Hitting the world API here, manually break out into individual endpoints
            if "happenings" in params.values():
                happenings = root.find("HAPPENINGS")
                # Happenings have an event ID, a timestamp, and text which is in CDATA tags
                # The event ID is a tag attribute, as opposed to everything else, which is a child tag.
                vals = []
                for event in happenings:
                    event_id = event.attrib["id"]
                    timestamp = event.find("TIMESTAMP").text
                    text = event.find("TEXT").text
                    vals.append(
                        {"event_id": event_id, "timestamp": timestamp, "text": text}
                    )
                return vals

            if "newnations" in params.values():
                # This is a single tag with a list of CSV formatted nations
                return {
                    "newnations": root.find("NEWNATIONS").text.split(","),
                    "ratelimit": r.headers["X-Ratelimit-requests-seen"],
                }

            if "tgq" in params.values():
                # This endpoint returns the telegram queue information
                return {
                    "manual": int(root.find("MANUAL").text),
                    "stamps": int(root.find("MASS").text),
                    "api": int(root.find("API").text),
                    "ratelimit": r.headers["X-Ratelimit-requests-seen"],
                }

            # edge cases for World Assembly API
            if "verify" in params.values():
                # This endpoint returns nation verification information
                return {
                    "verified": True if int(r.text) == 1 else False,
                    "ratelimit": r.headers["X-Ratelimit-requests-seen"],
                }

            if "delegates" in params.values():
                # This is a single tag with a list of CSV formatted nations
                return {
                    "delegates": root.find("DELEGATES").text.split(","),
                    "ratelimit": r.headers["X-Ratelimit-requests-seen"],
                }

            if "members" in params.values():
                # This is a single tag with a list of CSV formatted nations
                return {
                    "members": root.find("MEMBERS").text.split(","),
                    "ratelimit": r.headers["X-Ratelimit-requests-seen"],
                }

            if "sendtg" in params.values():
                # Returns true if the telegram was sent successfully, false otherwise
                return {
                    "queued": True if int(r.text) == 1 else False,
                    "ratelimit": r.headers["X-Ratelimit-requests-seen"],
                }
