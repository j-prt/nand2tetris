"""Assembler for the hack machine language"""

import sys

JUMP_TABLE = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


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


# For building C-instructions
def build_dest(dest: str | None):
    if not dest:
        return '000'
    output = ''
    output += '1' if 'A' in dest else '0'
    output += '1' if 'D' in dest else '0'
    output += '1' if 'M' in dest else '0'
    return output


def build_comp(comp):
    pass


def build_jump(jump: str):
    if not jump:
        return '000'
    return JUMP_TABLE[jump]


# Testing
source = read_file(get_path())
source = decomment(source)
print(source)


def parse_line(line: str):
    """Parse individual lines. Assumes complete symbol table."""
    # A-instruction
    if line.startswith('@'):
        if line[1:].isnumeric():
            return build_a(int(line[1:]))
        else:
            # TODO: get value from symbol table
            return line

    # C-instruction
    # These 4 variables determine assignment, CPU command, and jump instructions
    cmd = lhs = rhs = jmp = None
    if ';' in line:
        cmd, jmp = line.split(';')
    if '=' in line:
        lhs, rhs = line.split('=')
        cmd = None
    if rhs:
        rhs = rhs.split(';')[0]

    dest = build_dest(lhs)
    comp = build_comp(cmd or rhs)
    jump = build_jump(jmp)

    return dest, comp, jump


# Testing
source = read_file(get_path())
source = decomment(source)
source = [parse_line(line) for line in source]
print(source)
