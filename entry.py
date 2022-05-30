from colorama import init
from os import path
from webbrowser import open as open_url
from api import Client
from tools import cout, menu, clear
from time import sleep
from typing import Tuple


def load_config() -> dict:
    """
    Loads the config file and returns a dictionary of the config.
    Raises an exception if the config file is not found.

    :raises FileNotFoundError: This exception is raised if the config file is not found in the working directory.
    :return: dict
    """
    if path.exists("config.cfg"):
        config = {}
        with open("config.cfg", "r") as f:
            for line in f.readlines():
                if line.startswith("#"):
                    continue
                else:
                    k, v = line.split("=")
                    config[k.strip()] = v.strip()
        return config
    else:
        with open("config.cfg", "w") as f:
            f.write("# See docs/config.md for a standard configuration template.")
        raise FileNotFoundError


def verify_prompt() -> Tuple[str, str]:
    """
    Spawns a verification prompt to confirm the user's identity
    Returns the nation and the token that they input
    This function serves two purposes:
    1: to ensure API compliance
    2: to reduce boilerplate code by providing a single function to handle the prompt
    instead of multiple prompt copy-pastes.
    :return: tuple(str, str)
    """
    cout("HYPR requires that you verify your identity before continuing.", "info")
    nt = input(
        "Please enter your nation. Do not include the pretitle (e.g. 'The Republic of'): "
    ).strip(" ").lower().replace(" ", "_")
    cout("Now opening the NationStates Login Verification page...", "info")
    cout("Please log into the nation, and copy the verification code.", "info")
    cout("Once you have copied the verification code, paste it below.", "info")
    open_url(f"https://nationstates.net/page=verify_login?nation={nt}")
    tk = input().strip(" ")
    cout("Now verifying your identity...", "info")
    return nt, tk


if __name__ == "__main__":
    init() # Colorama init, don't remove or stuff Will Break™
    cout("HYPR is starting up...", "info")
    cout("Loading config...", "debug")

    # Load the config file.
    try:
        config = load_config()
    except FileNotFoundError:
        cout("The configuration file does not appear to contain a valid configuration.\nA new config file will be "
             "created in the working directory.\nPlease edit it, and then restart the program.", "fatal")

    cout("Config loaded.", "debug")
    nation, token = verify_prompt()
    # noinspection PyUnboundLocalVariable
    ua_string = f"HYPR // v{config['version']} // Developed by https://github.com/AavHRF // In use by {nation} " \
                f"(Unverified). // Should there be serious concerns about the operation of this program, please " \
                f"open an issue at https://github.com/AavHRF/HYPR/issues."
    api = Client(ua_string)
    response = api.ns_request({"a": "verify", "nation": nation, "checksum": token})

    # Confirm the response.
    while True:
        if response["verified"]:
            # The nation is verified. Modify the user agent to reflect this, and then break out of the loop.
            cout(f"Succesfully verified {nation}.", "info")
            ua_string = f"HYPR // v{config['version']} // Developed by https://github.com/AavHRF // In use by {nation} " \
                        f"(Verified). // Should there be serious concerns about the operation of this program, please " \
                        f"open an issue at https://github.com/AavHRF/HYPR/issues."
            api.headers = {"User-Agent": ua_string}
            break
        else:
            # The nation is not verified. Prompt the user to try again so we can confirm their identity.
            cout("Verification failed. Please try again.", "warn")
            nation, token = verify_prompt()
            response = api.ns_request({"a": "verify", "nation": nation, "checksum": token})

    # Load the menu.
    cout("Loading menu...", "debug")
    sleep(1)
    clear()
    options = [
        "Enable/Disable a campaign",
        "Add a region to offensive targeting",
        "Set home region",
        "Set telegram",
        "Set API key",
    ]
    selected = menu("Main Menu", options)
