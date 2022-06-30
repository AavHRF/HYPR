# Campaigns

## Design Overview

A HYPR campaign defines the following information that can be used by a scheduler to prioritize and send NationStates
telegrams:

- Campaign name - human readable campaign name
- Priority - used to prioritize API time between multiple campaigns
- TGID - ID for template that will be used to send telegrams
- Recruitment flag - Identifies a campaign to the scheduler as a recruitment campaign

Campaigns also implement the following key functionality:

- Recipient deque - a deque of nations identified by the search function that should receive telegrams. Accessing a 
  nation from the deque removes.
- Search function - arbitrary code that identifies nations that should be added to the deque.

Campaigns do not schedule any searches or telegrams on their own. Instead, they expose methods that can be used by 
an external scheduler/telgrammer to refresh their deques and send telegrams.

All campaigns are subclasses of `campaign.campaign.Campaign`. See pre-defined campaigns for examples.

## Tests

`campaign/test_campaign.py` includes methods that can be used to dry-run pre-made campaigns and make sure
they're doing what they should be doing. They _generally_ work  - except that it's tricky to catch a withdrawn endorsement
event, since those rely on the same feed as new endorsements, so they tend to be crowded out. Campaigns requiring a
target nation or region are hardcoded to use `east_durthang` / `the_pacific` since most of the campaign search events
are reliably created in a feeder (usually by its delegate). If the tests start failing, check to see if there's a new
delegate.

These aren't true unit tests - don't use them to validate commits since withdrawn endorsements fail pretty reliably even
when working correctly.

## Key Scenarios

- [x] Newly founded nations
- [x] Refounded nations
- [x] Ejected nations
- [x] Nations exiting a region
- [x] Nations entering a region
- [ ] Nations residing within a region with a specific residency length 
- [x] Nation joining WA, optionally limited to a single region
- [x] Nation leaving WA, optionally limited to a single region
- [x] Nation endorsing a specific nation
- [x] Nation withdrawing endorsement from a specific nation
- [x] All residents of a region
- [x] All World Assembly Delegates
- [x] All World Assembly Members