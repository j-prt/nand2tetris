"""
Translator for converting VM Code (Hack bytecode) to Hack Assembly.
This time, using the proposed implementation in NAND2Tetris II.
"""

import sys
from pathlib import Path
from textwrap import dedent

from auxiliary import Command, Line
from templates import (
    ARITHMETIC_COMMANDS,
    BOOT_CODE,
    CALL_TEMPLATE,
    FUNCTION_TEMPLATE,
    FUNCTION_VARS,
    GOTO_TEMPLATE,
    IF_GOTO_TEMPLATE,
    LABEL_TEMPLATE,
    POP_OTHER,
    POP_TEMPLATE,
    PUSH_CONST,
    PUSH_OTHER,
    PUSH_TEMPLATE,
    RETURN_TEMPLATE,
    SEGMENT_TABLE,
)


class Parser:
    def __init__(self, path: Path):
        if path.suffix != '.vm':
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

        # To opportunistically skip comments and empty lines
        is_comment = self.current.lstrip().startswith('//')
        is_whitespace = self.current.isspace()

        if is_comment or is_whitespace:
            return self.load_next()
        if self.current != '':
            return True
        else:
            return False

    def parse(self):
        raw = self.current.split('//')[0].strip()
        command, *arguments = raw.split()
        if command in ARITHMETIC_COMMANDS:
            command_type = Command.ARITHMETIC
        else:
            # Dealing with the - in if-goto
            command_type = ''.join(command.split('-')).upper()
            command_type = Command[command_type]
        return Line(raw, arguments, command, command_type)


class CodeWriter:
    def __init__(
        self, file_name, mode='one', dir_name: Path = None, dir_path: Path = None
    ):
        self.conditional_count = 0
        self.label_count = 0
        self.return_count = 0
        self.func_name = ''
        self.file_name = file_name
        if mode == 'one':
            self.file = open(file_name + '.asm', 'w')
        if mode == 'many':
            output_path = (dir_path / dir_name).with_suffix('.asm')
            if output_path.exists():
                self.file = open(output_path, 'a')
            else:
                self.file = open(output_path, 'w')
                self._boot()

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.close()

    def close(self):
        self.file.close()

    def to_assembly(self, line: Line):
        match line.command_type:
            case Command.ARITHMETIC:
                current = self._arithmetic(line)
            case Command.POP:
                current = self._pop(line)
            case Command.PUSH:
                current = self._push(line)
            case Command.LABEL:
                current = self._label(line)
            case Command.GOTO:
                current = self._goto(line)
            case Command.IFGOTO:
                current = self._if_goto(line)
            case Command.FUNCTION:
                current = self._function(line)
            case Command.CALL:
                current = self._call(line)
            case Command.RETURN:
                current = self._return()

        self.current = current
        self.raw = '// ' + line.raw + '\n'

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

    def _arithmetic(self, line: Line):
        if line.command in ['eq', 'gt', 'lt']:
            assembly = ARITHMETIC_COMMANDS[line.command].format(self.conditional_count)
            self.conditional_count += 1
        else:
            assembly = ARITHMETIC_COMMANDS[line.command]
        return assembly

    def _pop(self, line: Line):
        seg, num = line.arguments
        if seg in SEGMENT_TABLE:
            assembly = POP_TEMPLATE.format(num, SEGMENT_TABLE[seg])
        else:
            loc = self._resolve_segment(seg, num)
            assembly = POP_OTHER.format(loc)
        return assembly

    def _push(self, line: Line):
        seg, num = line.arguments
        if seg == 'constant':
            assembly = PUSH_CONST.format(num)
        elif seg in SEGMENT_TABLE:
            assembly = PUSH_TEMPLATE.format(num, SEGMENT_TABLE[seg])
        else:
            loc = self._resolve_segment(seg, num)
            assembly = PUSH_OTHER.format(loc)
        return assembly

    def _label(self, line: Line):
        return LABEL_TEMPLATE.format(self.func_name + '$' + line.arguments[0])

    def _goto(self, line: Line):
        return GOTO_TEMPLATE.format(self.func_name + '$' + line.arguments[0])

    def _if_goto(self, line: Line):
        return IF_GOTO_TEMPLATE.format(self.func_name + '$' + line.arguments[0])

    def _function(self, line: Line):
        label, n_vars = line.arguments
        self.func_name = label
        self.return_count = 0
        assembly = FUNCTION_TEMPLATE.format(label)
        for i in range(int(n_vars)):
            assembly += '\n' + FUNCTION_VARS
        return assembly

    def _call(self, line: Line):
        label, n_args = line.arguments
        return_addr = self.func_name + '$' + 'ret.' + str(self.return_count)
        self.return_count += 1
        return CALL_TEMPLATE.format(return_addr, n_args, label)

    def _return(self):
        return RETURN_TEMPLATE

    def _boot(self):
        call_args = 'Sys.init$ret.0', 0, 'Sys.init'
        asm = dedent(BOOT_CODE) + '\n' + dedent(CALL_TEMPLATE.format(*call_args)) + '\n'
        self.file.write(asm)

    def write(self):
        asm = self.raw + dedent(self.current) + '\n'
        self.file.write(asm)


def get_path():
    """Extracts path from command line arguments"""
    try:
        file_path = sys.argv[1]
    except IndexError:
        print('Error: no filepath provided.')
        exit(1)
    else:
        return Path(file_path)


def translate_one(path: Path):
    with Parser(path) as parser:
        with CodeWriter(path.stem) as writer:
            while parser.load_next():
                line = parser.parse()
                writer.to_assembly(line)
                writer.write()


def translate_many(path: Path):
    files = path.glob('*.vm')
    for file in files:
        with Parser(file) as parser:
            with CodeWriter(file.stem, 'many', path.stem, path) as writer:
                while parser.load_next():
                    line = parser.parse()
                    writer.to_assembly(line)
                    writer.write()


def main():
    path = get_path()
    if path.is_dir():
        translate_many(path)
    else:
        translate_one(path)


if __name__ == '__main__':
    main()
