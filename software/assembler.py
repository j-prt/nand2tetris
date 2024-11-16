"""Assembler for the hack machine language"""

import sys

# Get the path to the .asm
try:
    file_path = sys.argv[1]
except IndexError:
    print('Error: no filepath provided.')
    # exit(1)


# For parsing A-instructions
def int_to_bin(num):
    """Converts an integer to its binary format, padded to 15 digits."""
    return f'{num:b}'.rjust(15, '0')


print(int_to_bin(5))
