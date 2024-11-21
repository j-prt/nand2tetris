"""
Translator for converting VM Code (Hack bytecode) to Hack Assembly.
This time, using the proposed implementation in NAND2Tetris II.
"""

from dataclasses import dataclass
from enum import Enum, auto

ARITHMETIC_COMMANDS = {
    'add': 0,
    'sub': 0,
    'neg': 0,
    'eq': 0,
    'gt': 0,
    'lt': 0,
    'and': 0,
    'or': 0,
    'not': 0,
}


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


class Parser:
    def __init__(self, path):
        if path[-3:] != '.vm':
            raise ValueError('Specified file should end in .vm')
        self.file = open(path, 'r')

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.close()

    def close(self):
        self.file.close()

    def load_next(self):
        self.current = self.file.readline()

        # Opportunistically skip comments and empty lines
        if self.current.startswith('//') or self.current.startswith('\n'):
            return self.load_next()
        if self.current != '':
            return True
        else:
            return False

    def parse(self):
        line = self.current.split('//')[0].strip()
        command, *arguments = line.split()
        if command in ARITHMETIC_COMMANDS:
            command_type = Command.ARITHMETIC
        else:
            command_type = Command[command.upper()]
        return Line(arguments, command, command_type)


class CodeWriter:
    def __init__(self, file_name):
        self.file = open(file_name + '.asm', 'w')

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.close()

    def close(self):
        self.file.close()

    def to_assembly(self, line: Line):
        if line.command_type == Command.ARITHMETIC:
            return ARITHMETIC_COMMANDS[line.command]


def main():
    pass


with Parser('SimpleAdd.vm') as parser:
    with CodeWriter('SimpleAdd') as writer:
        while parser.load_next():
            line = parser.parse()
            writer.to_assembly(line)
