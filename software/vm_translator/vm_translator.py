"""
Translator for converting VM Code (Hack bytecode) to Hack Assembly.
This time, using the proposed implementation in NAND2Tetris II.
"""

import sys
from textwrap import dedent

from auxiliary import Command, Line
from templates import (
    ARITHMETIC_COMMANDS,
    POP_OTHER,
    POP_TEMPLATE,
    PUSH_CONST,
    PUSH_OTHER,
    PUSH_TEMPLATE,
    SEGMENT_TABLE,
)


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
        self.conditional_count = 0
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
                if line.command in ['eq', 'gt', 'lt']:
                    current = ARITHMETIC_COMMANDS[line.command].format(
                        self.conditional_count
                    )
                    self.conditional_count += 1
                else:
                    current = ARITHMETIC_COMMANDS[line.command]
            case Command.POP:
                seg, num = line.arguments
                if seg in SEGMENT_TABLE:
                    current = POP_TEMPLATE.format(num, SEGMENT_TABLE[seg])
                else:
                    loc = self._resolve_segment(seg, num)
                    current = POP_OTHER.format(loc)
            case Command.PUSH:
                seg, num = line.arguments
                if seg == 'constant':
                    current = PUSH_CONST.format(num)
                elif seg in SEGMENT_TABLE:
                    current = PUSH_TEMPLATE.format(num, SEGMENT_TABLE[seg])
                else:
                    loc = self._resolve_segment(seg, num)
                    current = PUSH_OTHER.format(loc)

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
                loc = 'THAT'
        return loc

    def write(self):
        asm = dedent(self.current) + '\n'
        self.file.write(asm)


def get_path():
    """Extracts path from command line arguments"""
    try:
        file_path = sys.argv[1]
    except IndexError:
        print('Error: no filepath provided.')
        exit(1)
    else:
        return file_path


def main():
    path = get_path()
    with Parser(path) as parser:
        with CodeWriter(path.split('.')[0]) as writer:
            while parser.load_next():
                line = parser.parse()
                writer.to_assembly(line)
                writer.write()


if __name__ == '__main__':
    main()
