from typing import List
from colorama import Fore, Style
from os import system, name


def cout(message: str, level: str) -> None:
    """
    Prints a message to the console with appropriate formatting.
    If the message is a fatal error, the program will exit.

    :param message: str The message to print.
    :param level: str The level of the message.
    :return:
    """
    if level.lower() not in ["debug", "info", "warn", "error", "critical", "fatal"]:
        raise ValueError(f"Invalid output level: {level}")
    if level.lower() == "debug":
        print(f"{Fore.BLUE}[DEBUG]{Style.RESET_ALL} {message}")
    elif level.lower() == "info":
        print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} {message}")
    elif level.lower() == "warn":
        print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {message}")
    elif level.lower() == "error":
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
    elif level.lower() == "critical" or level.lower() == "fatal":
        print(f"{Fore.RED}[FATAL]{Style.RESET_ALL} {message}")
        raise SystemExit(1)


def menu(title: str, options: List[str]) -> int:
    print(f"{Fore.BLUE}[{title}]{Style.RESET_ALL}")
    for i, option in enumerate(options):
        print(f"{Fore.BLUE}[{i}]:{Style.RESET_ALL} {option}")
    return int(cin(f">", [str(i) for i in range(len(options))]))


def cin(prompt: str, options: List[str]) -> str:
    """
    Handles user input validation and returns the user's choice.
    Note: The user's input is returned as-is, and is not sanitized in any way, including case.

    :param prompt: str The prompt to display to the user.
    :param options: List[str] A list of valid options.
    :return: str The user's choice.
    """
    while True:
        u = input(f"{Fore.GREEN}[INPUT]{Style.RESET_ALL} {prompt} ")
        if u.lower() in [option.lower() for option in options]:
            return u
        else:
            print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} Invalid input. Please try again.")


def clear() -> None:
    """
    Clears the terminal screen.
    """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
