// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
(LOOP)
@KBD
D=M
@BLACK
D;JGT
@R0
M=0
@CONTINUE
0;JMP
(BLACK)
@R0
M=0
M=!M
(CONTINUE)
@31
D=A
@R1
M=D
@256
D=A
@R2
M=D
@SCREEN
D=A
@R3
M=D
(FILL)
@R0
D=M
@R3
A=M
M=D
D=A+1
@R3
M=D
@R1
DM=M-1
@ENDOFLINE
D;JEQ
@FILL
0;JMP
(ENDOFLINE)
@32
D=A
@R1
M=D
@R2
DM=M-1
@ENDOFSCREEN
D;JEQ
@FILL
0;JMP
(ENDOFSCREEN)
@LOOP
0;JMP