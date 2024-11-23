"""Templates for the VM Translator"""

SEGMENT_TABLE = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT',
}

ARITHMETIC_COMMANDS = {
    'add': """\
           @SP
           A=M-1 // SP-1
           D=M
           A=A-1 // SP-2
           M=D+M
           @SP
           M=M-1\
           """,
    'sub': """\
           @SP
           M=M-1
           A=M
           D=M
           A=A-1
           M=M-D\
           """,
    'neg': """\
           @SP
           A=M-1
           M=-M\
           """,
    'eq': """\
           @SP
           M=M-1
           A=M
           D=M
           A=A-1
           D=M-D
           @TRUE{0}
           D;JEQ
           @FALSE{0}
           D;JNE
           (TRUE{0})
           @SP
           A=M-1
           M=-1
           @END{0}
           0;JMP
           (FALSE{0})
           @SP
           A=M-1
           M=0
           @END{0}
           0;JMP
           (END{0})\
           """,
    'gt': """\
           @SP
           M=M-1
           A=M
           D=M
           A=A-1
           D=M-D
           @TRUE{0}
           D;JGT
           @FALSE{0}
           D;JLE
           (TRUE{0})
           @SP
           A=M-1
           M=-1
           @END{0}
           0;JMP
           (FALSE{0})
           @SP
           A=M-1
           M=0
           @END{0}
           0;JMP
           (END{0})\
           """,
    'lt': """\
           @SP
           M=M-1
           A=M
           D=M
           A=A-1
           D=D-M
           @TRUE{0}
           D;JGT
           @FALSE{0}
           D;JLE
           (TRUE{0})
           @SP
           A=M-1
           M=-1
           @END{0}
           0;JMP
           (FALSE{0})
           @SP
           A=M-1
           M=0
           @END{0}
           0;JMP
           (END{0})\
           """,
    'and': """\
           @SP
           M=M-1
           A=M
           D=M
           A=A-1
           M=M&D\
           """,
    'or': """\
           @SP
           M=M-1
           A=M
           D=M
           A=A-1
           M=M|D\
           """,
    'not': """\
           @SP
           A=M-1
           M=!M\
           """,
}

PUSH_TEMPLATE = """\
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
    @{} // location
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1\
"""

PUSH_OTHER = """\
    @{} // location
    D=M
    @SP
    A=M
    M=D
    @SP
    M=M+1\
"""

POP_TEMPLATE = """\
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

POP_OTHER = """\
    @SP
    M=M-1
    A=M
    D=M
    @{} // location
    M=D\
"""

LABEL_TEMPLATE = """\
                 ({})\
                 """

GOTO_TEMPLATE = """\
                @{}
                0;JMP\
                """

IF_GOTO_TEMPLATE = """\
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @{}
                   D;JNE\
                   """
