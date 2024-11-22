from dataclasses import dataclass
from enum import Enum, auto


class Command(Enum):
    """VM Commands"""

    ARITHMETIC = auto()
    POP = auto()
    PUSH = auto()


@dataclass
class Line:
    arguments: list[str]
    command: str
    command_type: Command
