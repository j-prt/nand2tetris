"""
Translator for converting VM Code (Hack bytecode) to Hack Assembly.
This time, using the proposed implementation in NAND2Tetris II.
"""

from enum import Enum, auto


class Command(Enum):
    """VM Commands"""

    # Arithmetic/Logical commands
    ADD = auto()
    SUB = auto()
    NEG = auto()
    EQ = auto()
    GT = auto()
    LT = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    # Memory access commands
    POP = auto()
    PUSH = auto()


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
        self.current = self.current.split('//')[0]
        operands = self.current.split()
        command = Command[operands[0].upper()]
        print(command)


class CodeWriter:
    def __init__(self, file_name):
        self.file = open(file_name + '.asm', 'w')

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.close()

    def close(self):
        self.file.close()


def main():
    pass


with Parser('SimpleAdd.vm') as parser:
    while parser.load_next():
        line = parser.parse()
