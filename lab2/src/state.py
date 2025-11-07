from pathlib import Path
from src import constants as ct


class ShellState:
    def __init__(self):
        self.cwd = ct.BASE_DIR
