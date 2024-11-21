"""
Translator for converting VM Code (Hack bytecode) to Hack Assembly.
This time, using the proposed implementation in NAND2Tetris II.
"""

from dataclasses import dataclass
from enum import Enum, auto
from textwrap import dedent

ARITHMETIC_COMMANDS = {
    'add': """\
           // add
           @SP
           A=M-1 // SP-1
           D=M
           A=A-1 // SP-2
           M=D+M
           @SP
           M=M-1\
           """,
    'sub': """\
           // sub
           @SP
           M=M-1
           A=M
           D=M
           @SP
           M=M-1
           A=M
           M=M-D\
           """,
    'neg': 0,
    'eq': 0,
    'gt': 0,
    'lt': 0,
    'and': 0,
    'or': 0,
    'not': 0,
}

PUSH_TEMPLATE = """\
    // push template
    @{} // offset
    D=A
    @{} // segment
    A=M+D
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1\
"""

PUSH_CONST = """\
    // push const
    @{} // location
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1\
"""

POP_TEMPLATE = """\
    // pop template
    @{} // offset
    D=A
    @{} // segment
    A=M+D
    D=A
    @R13
    M=D
    @SP
    M=M-1
    A=M
    D=M
    @R13
    A=M
    M=D\
"""

POP_CONST = """\
    // pop const
    @SP
    M=M-1
    A=M
    D=M
    @{} // location
    A=M
    M=D\
"""

SEGMENT_TABLE = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT',
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
        self.file_name = file_name
        self.file = open(file_name + '.asm', 'w')

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.close()

    def close(self):
        self.file.close()

    def to_assembly(self, line: Line):
        match line.command_type:
            case Command.ARITHMETIC:
                current = ARITHMETIC_COMMANDS[line.command]
            case Command.POP:
                seg, num = line.arguments
                if seg in SEGMENT_TABLE:
                    current = POP_TEMPLATE.format(num, seg)
                else:
                    loc = self._resolve_segment(seg, num)
                    current = POP_CONST.format(loc)
            case Command.PUSH:
                seg, num = line.arguments
                if seg == 'constant':
                    current = PUSH_CONST.format(num)
                elif seg in SEGMENT_TABLE:
                    current = PUSH_TEMPLATE.format(num, SEGMENT_TABLE[seg])
                else:
                    loc = self._resolve_segment(seg, num)
                    current = PUSH_CONST.format(loc)

        self.current = current

    def _resolve_segment(self, seg, num):
        if seg == 'static':
            loc = self.file_name + '.' + num
        if seg == 'temp':
            loc = str(5 + int(num))
        if seg == 'pointer':
            if num == '0':
                loc = 'THIS'
            if num == '1':
                loc == 'THAT'
        return loc

    def write(self):
        asm = dedent(self.current) + '\n'
        self.file.write(asm)


def main():
    pass


with Parser('SimpleAdd.vm') as parser:
    with CodeWriter('SimpleAdd') as writer:
        while parser.load_next():
            line = parser.parse()
            writer.to_assembly(line)
            writer.write()
