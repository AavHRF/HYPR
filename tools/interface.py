from typing import List, Optional
from colorama import Fore, Style
from os import system, name
import logging


class Console:
    """
    This class implements a standardized console interface for the HYPR client that also manages logging.
    It is initialized once in the main function, and should not be called elsewhere. Upon initialization,
    it takes a logger object as an argument. It then encapsulates the input/output functions into a single
    class that removes the need to remember logging from the developer's mind.

    Methods:

        cout(message: str, level: str) -> None
            Prints a message to the console with appropriate formatting.
            If the message is a fatal error, the program will exit.

        cin(prompt: str, options: List[str]) -> str
            Prompts the user for input, and validates the input against a list of options, or returns the input.
            Returns the user's input.

        menu(title: str, options: List[str]) -> int
            Prints a menu to the console, and prompts the user for input.
            Returns the user's input.

    Staticmethods:

        clear() -> None
            Clears the console.
    """

    def __init__(self, logger):
        self.logger: logging.Logger = logger

    def cout(self, message: str, level: str) -> None:
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
            self.logger.debug(message)
        elif level.lower() == "info":
            print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} {message}")
            self.logger.info(message)
        elif level.lower() == "warn":
            print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {message}")
            self.logger.warning(message)
        elif level.lower() == "error":
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
            self.logger.error(message)
        elif level.lower() == "critical" or level.lower() == "fatal":
            print(f"{Fore.RED}[FATAL]{Style.RESET_ALL} {message}")
            self.logger.critical(message)
            raise SystemExit(1)

    def menu(self, title: str, options: List[str]) -> int:
        print(f"{Fore.BLUE}[{title}]{Style.RESET_ALL}")
        self.logger.info("Menu invoked.")
        for i, option in enumerate(options):
            print(f"{Fore.BLUE}[{i}]:{Style.RESET_ALL} {option}")
        return int(self.cin(f">", [str(i) for i in range(len(options))]))

    @staticmethod
    def cin(prompt: str, options: Optional[List[str]] = None) -> str:
        """
        Handles user input validation and returns the user's choice.
        Note: The user's input is returned as-is, and is not sanitized in any way, including case.

        :param prompt: str The prompt to display to the user.
        :param options: List[str] A list of valid options.
        :return: str The user's choice.
        """
        if options is not None:
            while True:
                u = input(f"{Fore.GREEN}[INPUT]{Style.RESET_ALL} {prompt} ")
                if u.lower().replace(" ", "_") in [
                    option.lower().replace(" ", "_") for option in options
                ]:
                    return u
                else:
                    print(
                        f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} Invalid input. Please try again."
                    )
        else:
            return input(f"{Fore.GREEN}[INPUT]{Style.RESET_ALL} {prompt} ")

    @staticmethod
    def clear() -> None:
        """
        Clears the terminal screen.
        """
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")

    @staticmethod
    def invoke(command: str) -> None:
        """
        Invokes a command in the terminal.
        Does not check platform type before execution.

        :param command:
        :return:
        """
        _ = system(command)
        return None
