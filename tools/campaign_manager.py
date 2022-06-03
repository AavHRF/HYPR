from tools.interface import Console
from campaign import Campaign
from json import dump, load
from os import listdir
from os.path import isfile, join


# This file contains a lot of functions that can be invoked from the menu
# in order to help manage campaigns, or provide a neat little box to store
# a tad of complicated spaghetti logic surrounding how campaigns are handled.


def save_campaign(campaign: Campaign, c: Console) -> None:
    """
    Saves the campaign as a JSON file.
    :param campaign: Campaign
    :param c: Console
    :return:
    """
    campaign_type = type(campaign).__name__
    # If only there was a better option than JSON for this...
    # Alas, we are not using databases.
    sav_obj = {
        "name": campaign.name,
        "priority": campaign.priority,
        "tgid": campaign.tgid,
        "recruitment": campaign.is_recruitment,
        "search_params": campaign.search_params,
    }
    with open(f"data/{campaign_type}_{campaign.name}.json", "w") as f:
        dump(sav_obj, f)
        c.cout(f"Saved {campaign_type} {campaign.name}", "info")
        return


def load_campaign(c: Console) -> dict:
    """
    Loads a campaign from a JSON file.
    :param c: Console
    :return:
    """
    allowed_options = [
        f.strip(".json") for f in listdir("data") if isfile(join("data", f))
    ]
    camp = c.cin(
        "Please enter the name of the campaign you wish to load: ", allowed_options
    )
    with open(f"data/{camp}.json", "r") as f:
        return load(f)
