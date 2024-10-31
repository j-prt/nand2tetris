// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.


// pseudocode

// R2 = R0 * R1
// acc = 0
// for i in range(R1):
//   acc = acc + R0
// R2 = acc

// Set up required variables
@R2
M=0
@R1
D=M
@i
M=0

// Main loop
(LOOP)
// End condition
@i
D=M
@R1
D=M-D
@END
D;JEQ

// Else, accumulate
@R0
D=M
@R2
M=M+D

// Increment
@i
M=M+1

@LOOP
0;JMP

// End
(END)
@END
0;JMP
