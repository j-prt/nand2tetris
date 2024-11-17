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

COMP_TABLE = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '110000',
    '!D': '001101',
    '!A': '110001',
    '-D': '001111',
    '-A': '110011',
    'D+1': '011111',
    'A+1': '110111',
    'D-1': '001110',
    'A-1': '110010',
    'D+A': '000010',
    'D-A': '010011',
    'A-D': '000111',
    'D&A': '000000',
    'D|A': '010101',
}

symbol_table = {
    'SCREEN': 16384,
    'KDB': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
}

max_reg = 15


def get_path():
    """Extracts path from command line arguments"""
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


# Helper functions for register symbols
def is_register(r: str):
    return r[1] == 'R' and r[2:].isnumeric() and 0 <= int(r[2:]) <= 15


def get_register(r: str):
    return int(r[2:])


# Helper functions for parsing A-instruction addresses
def int_to_bin(addr: int):
    """Converts an integer to its binary format, padded to 15 digits."""
    return f'{addr:b}'.rjust(15, '0')


def build_a(addr: int):
    """Completes A-instructions when given an int address"""
    addr = int_to_bin(addr)
    return '0' + addr


# Helper functions for building C-instructions
def build_dest(dest: str | None):
    if not dest:
        return '000'
    output = '1' if 'A' in dest else '0'
    output += '1' if 'D' in dest else '0'
    output += '1' if 'M' in dest else '0'
    return output


def build_comp(comp: str):
    if 'M' in comp:
        output = '1'
        comp = comp.replace('M', 'A')
    else:
        output = '0'
    return output + COMP_TABLE[comp]


def build_jump(jump: str):
    if not jump:
        return '000'
    return JUMP_TABLE[jump]


def scan_symbols(source: list[str]):
    output = []
    offset = 0
    for line in range(len(source)):
        print(offset)
        if source[line].startswith('(') and source[line].endswith(')'):
            new_symbol = source[line][1:-1]
            symbol_table[new_symbol] = line - offset
            offset += 1
        else:
            output.append(source[line])
    return output


def parse_line(line: str):
    """Parse individual lines. Assumes complete symbol table."""
    # A-instruction
    if line.startswith('@'):
        if (addr := line[1:]).isnumeric():
            return build_a(int(addr))
        else:
            if is_register(line):
                reg = get_register(line)
                return build_a(reg)
            elif addr in symbol_table:
                return build_a(symbol_table[addr])
            else:
                global max_reg
                symbol_table[addr] = max_reg + 1
                max_reg += 1
                return build_a(max_reg)

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

    print(line, lhs, rhs, cmd, jmp)

    return '111' + comp + dest + jump


path = get_path()
source = read_file(path)
source = decomment(source)
source = scan_symbols(source)
print(source)
print(symbol_table)
source = [parse_line(line) for line in source]
print(source)

with open(f'{path.split('.')[0]}.hack', 'w') as f:
    f.write('\n'.join(source))
