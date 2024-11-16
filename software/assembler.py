"""Assembler for the hack machine language"""

import sys


# Get the path to the .asm
def get_path():
    try:
        file_path = sys.argv[1]
    except IndexError:
        print('Error: no filepath provided.')
        exit(1)
    else:
        return file_path


def read_file(path: str):
    """Reads file contents into memory, returning a list of lines"""
    try:
        with open(path, 'r') as f:
            source = f.readlines()
            return source
    except FileNotFoundError:
        print('Error: file does not exist')
        exit(1)


def decomment(source: list[str]):
    """Trims whitespace, removes comments"""
    output = []
    for line in source:
        line = line.strip()
        if line:
            line = line.split('//')[0]
            if line:
                output.append(line)

    return output


# For parsing A-instruction addresses
def int_to_bin(addr: int):
    """Converts an integer to its binary format, padded to 15 digits."""
    return f'{addr:b}'.rjust(15, '0')


def build_a(addr: int):
    """Completes A-instructions when given an int address"""
    addr = int_to_bin(addr)
    return '0' + addr


source = read_file(get_path())
source = decomment(source)
print(source)


def parse_line(line: str):
    # A-instruction
    if line.startswith('@'):
        return build_a(int(line[1:]))
    return line


source = read_file(get_path())
source = decomment(source)
source = [parse_line(line) for line in source]
print(source)
