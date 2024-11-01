// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed,
// the screen should be cleared.

// pseudocode
// if KBD != 0:
//   for i in range(len(SCREEN)):
//     SCREEN[i] = -1
// else:
//   for i in range(len(SCREEN)):
//     SCREEN[i] = 0
// goto first if

// Variable setup
@SCREEN
D=A
@row
M=D
@8192 // 8192 * 16 = total pixel count
D=A
@numRows
M=D

(LOOP)
@i
M=0
@KBD
D=M
@BLACK
D;JNE
@CLEAR
D;JEQ

// Check if it's the last row, and if so jump to main loop
// If not, iterate over all rows and set them to black
(BLACK)
@i
D=M
@numRows
D=M-D
@LOOP
D;JEQ

// Get i, get current row addr (i + row), set to black
@i
D=M
@row
D=D+M
A=D
M=-1

// Increment i, restart black loop
@i
M=M+1
@BLACK
0;JMP

(CLEAR)
@i
D=M
@numRows
D=M-D
@LOOP
D;JEQ

// Get i, get current row addr (i + row), set to white
@i
D=M
@row
D=D+M
A=D
M=0

// Increment i, restart clear loop
@i
M=M+1
@CLEAR
0;JMP
