from dataclasses import dataclass
from enum import Enum, auto


class Command(Enum):
    """VM Commands"""

    ARITHMETIC = auto()

    # Memory access
    POP = auto()
    PUSH = auto()

    # Branching
    LABEL = auto()
    GOTO = auto()
    IFGOTO = auto()

    # Function
    FUNCTION = auto()
    CALL = auto()
    RETURN = auto()


@dataclass
class Line:
    raw: str
    arguments: list[str]
    command: str
    command_type: Command
