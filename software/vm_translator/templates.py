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

FUNCTION_TEMPLATE = """\
                    ({})\
                    """

FUNCTION_VARS = """\
                    @SP
                    M=M+1
                    A=M-1
                    M=0\
                    """

CALL_TEMPLATE = """\
                @{0} // retaddr
                D=A
                @SP
                M=M+1
                A=M-1
                M=D // store retaddr
                @LCL
                D=M
                @SP
                M=M+1
                A=M-1
                M=D // store frame LCL
                @ARG
                D=M
                @SP
                M=M+1
                A=M-1
                M=D // store frame ARG
                @THIS
                D=M
                @SP
                M=M+1
                A=M-1
                M=D // store frame THIS
                @THAT
                D=M
                @SP
                M=M+1
                A=M-1
                M=D // store frame THAT
                D=A+1
                @LCL // func LCL
                M=D // SP location
                @{1} // nArgs offset
                D=A
                @5 // frame offset
                D=D+A
                @SP
                D=M-D
                @ARG // func ARG
                M=D
                @{2} // func addr
                0;JMP
                ({0}) // retaddr\
                """

RETURN_TEMPLATE = """\
                  @LCL
                  D=M
                  @R15 // store endframe, LCL 0
                  M=D
                  @5 // offset
                  D=A
                  @R15
                  D=M-D
                  A=D
                  D=M
                  @R16 //retaddr
                  M=D
                  @SP
                  A=M-1
                  D=M
                  @ARG
                  A=M
                  M=D // set ARG 0 to SP - 1 (return val)
                  D=A
                  @SP // set sp to *arg+1
                  M=D+1
                  @R15 // restore the caller's frame
                  M=M-1
                  A=M
                  D=M
                  @THAT
                  M=D
                  @R15
                  M=M-1
                  A=M
                  D=M
                  @THIS
                  M=D
                  @R15
                  M=M-1
                  A=M
                  D=M
                  @ARG
                  M=D
                  @R15
                  M=M-1
                  A=M
                  D=M
                  @LCL
                  M=D
                  @R16
                  A=M
                  0;JMP
                  """
