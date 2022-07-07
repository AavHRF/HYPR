[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# HYPR
High performance API recruitment software for NationStates written in Python

# Why HYPR?
HYPR was designed to be a simple, easy to use, and yet powerful telegram API client for NationStates.
It was constructed due to a need for incredibly flexible and powerful API clients that simply did not exist in an
open-source context. It features advanced targeting features, and allows you to extend the functionality of the client
with your own filters (called [Campaigns](docs/campaigns.md)).

# Features
- [ ] 100% API compliance at all times - fails safe, not open
- [ ] Runs in the background, no need to keep a window open
- [x] Cross-platform - run on Windows, Linux, or MacOS
- [ ] Weighted bin targeting methods - rank your targets in order of preference

# Contributing
Make a PR, before you commit run `pre_commit.sh` to ensure that the files get formatted properly.
We use [black](https://black.readthedocs.io/en/stable/) to format the code. Please make sure your dev environment
is configured as such. Additionally, we build in Python 3.10 in order to support match case statements. You cannot
use any older versions of Python, as they will fail.

# Documentation
We maintain a [documentation repository](docs) that you can look through to find developer-designed documentation.
Additionally, this readme will contain instructions on how to run HYPR on your machine once it has entered beta.