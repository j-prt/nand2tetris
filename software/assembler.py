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


def read_file(path):
    """Reads file contents into memory, returning a list of rows"""
    try:
        with open(path, 'r') as f:
            source = f.readlines()
            return source
    except FileNotFoundError:
        print('Error: file does not exist')
        exit(1)


# For parsing A-instruction addresses
def int_to_bin(addr):
    """Converts an integer to its binary format, padded to 15 digits."""
    return f'{addr:b}'.rjust(15, '0')


def build_a(addr):
    """Completes A-instructions when given an int address"""
    addr = int_to_bin(addr)
    return '0' + addr


read_file(get_path())
