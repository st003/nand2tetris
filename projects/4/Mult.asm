// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// pseudo code written with C
//
// int R0 = ?;
// int R1 = ?;
// int R2 = 0;
//
// for (int i = 0; i < R1; i++) {
//    R2 = R2 + R0;
// }

    // declare variables for i and sum

    @i
    M=1

    @sum
    M=0

// start of loop
(LOOP)
    // set value of i into D
    @i
    D=M

    // subtract value at R0 from D. Because we increment i later,
    // this difference will get smaller each iteration
    @R0
    D=D-M

    // if d greater than 0, jump to STOP
    @STOP
    D;JGT

    // get the current value of sum
    @sum
    D=M

    // select the value at R1 and increment to D
    @R1
    D=D+M

    // set sum with the value of D
    @sum
    M=D

    // increment i by 1
    @i
    M=M+1

    // jump to beginning of the loop
    @LOOP
    0;JMP

(STOP)
    // get the value of sum...
    @sum
    D=M

    // ...and set it into R2
    @R2
    M=D

(END)
    // inifite loop at end of program
    @END
    0;JMP
