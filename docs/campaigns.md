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

## Key Scenarios

- Newly founded nations
- Refounded nations
- Ejected nations
- Nations exiting a region
- Nations entering a region
- Nations residing within a region with a specific residency length
- Nation joining WA, optionally limited to a single region
- Nation leaving WA, optionally limited to a single region
- Nation endorsing a specific nation
- Nation withdrawing endorsement from a specific nation
- All residents of a region
- All World Assembly Delegates
- All World Assembly Members