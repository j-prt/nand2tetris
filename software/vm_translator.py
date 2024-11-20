"""
Translator for converting VM Code (Hack bytecode) to Hack Assembly.
This time, using the proposed implementation in NAND2Tetris II.
"""


class Parser:
    def __init__(self, path):
        if path[-3:] != '.vm':
            raise ValueError('Specified file should end in .vm')
        self.file = open(path, 'r')

    def __enter__(self):
        return self.file

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.file.close()


class CodeWriter:
    pass


def main():
    pass


with Parser('SimpleAdd.vm') as parser:
    print('parser', parser)
