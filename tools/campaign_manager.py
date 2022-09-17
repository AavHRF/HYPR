from tools.interface import Console
from campaign import Campaign
from os import listdir
from os.path import isfile, join
import pickle


# This file contains a lot of functions that can be invoked from the menu
# in order to help manage campaigns, or provide a neat little box to store
# a tad of complicated spaghetti logic surrounding how campaigns are handled.


def save_campaign(campaign: Campaign, c: Console) -> None:
    """
    Saves the campaign as a .hypr file.
    :param campaign: Campaign
    :param c: Console
    :return:
    """
    campaign_type = type(campaign).__name__
    with open(f"data/{campaign_type}_{campaign.name}.hypr", "w") as f:
        pickle.dump(campaign, f, protocol=pickle.HIGHEST_PROTOCOL)
        c.cout(f"Saved {campaign_type} {campaign.name}", "info")


def load_campaign(c: Console) -> Campaign:
    """
    Loads a campaign from a .hypr file and returns it as a Campaign object.
    :param c: Console
    :return:
    """
    allowed_options = [
        f.strip(".hypr") for f in listdir("data") if isfile(join("data", f))
    ]
    camp = c.cin(
        "Please enter the name of the campaign you wish to load: ", allowed_options
    )
    with open(f"data/{camp}.hypr", "r") as f:
        return pickle.load(f)


def custom_campaign(c: Console) -> Campaign:
    """
    Creates a custom campaign and returns it as a Campaign object.
    :param c: Console
    :return:
    """
    raise NotImplementedError("This feature is not yet implemented.")
    # noinspection PyUnreachableCode
    name = c.cin("Please enter the name of the campaign: ")