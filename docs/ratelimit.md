# Ratelimiting in HYPR

HYPR implements a [leaky bucket](https://en.wikipedia.org/wiki/Leaky_bucket) ratelimiter to ensure safe access to the
NationStates API. To ensure proper ratelimiting, ensure all requests made to the NationStates API are made via the same 
[*Client*](../api/wrapper.py) instance. Actual rate-limiting is implemented via decorators specified in
[limiter.py](../api/limiter.py).

## Key Considerations

- The API client immediately attempts to execute API queries. It does not space out queries.
- If executing an API query would lead to a rate limit violation, it discards the request and raises a `TooManyRequests`
  exception.
- The ratelimiter does not attempt to accommodate for any other API clients running in parallel.
- HYPR does not implement website scraping or website scraping rate limiting, which is subject to a different set of 
  rules and considerations.

## Expected Behavior

Requests are immediately executed when `Client.ns_request()` is called unless that request would lead to a rate limit
violation (conservatively defined as 45 requests per 30 seconds), in which case a `TooManyRequests` exception is raised
and the request is discarded. `TooManyRequests` returns the length of time needed to wait before sending a request to
comply with the rate limit.

The following code provides an example of how to safely query the API:

```python
import time
from api.wrapper import Client
from api.limiter import TooManyRequests

user = input("User Nation or Email: ")
api = Client(useragent=f"HYPR Demonstration Script in use by {user}")

while True:
    try:
      request = api.ns_request(params={"q": "happenings", "filter": "eject"})
      break
    except TooManyRequests as e:
      time.sleep(e.args[0])
print(request)
```

In this example, an API request is made. If the request is successful, the loop immediately breaks and the result is
printed to the terminal. However, if the request would lead to a ratelimit violation, the API client raises a 
`TooManyRequests` exception along with the length of time needed to sleep before a new query can be made safely.