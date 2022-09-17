from tools.interface import Console
from exceptions import *


class Handler:

    def __init__(self, console: Console):
        self.console = console

    def handle(self, error: Exception):
