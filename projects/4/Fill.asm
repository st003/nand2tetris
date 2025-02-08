// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// Keyboard:
//
// @KBD is the start address for the keyboard map
// when no key is selected, the value of @KBD is 0
// Any other key has a value greater than 0

// Display:
//
// The screen resolution is 512x256
// 32 "columns" (also know as word) of 16-bit numbers make up a single row
// The decimal value of -1 is the same as all 16-bits being set to 1
// @SCREEN is the start address for the display map
// memory address of "world" = (32 * row) + col / 16
// where row is 0-255 and col is 0-512
//
// To set a specific bit in a word, do col % 16 to figure out what value to be
// set in the word

// program is infinite loop
(START)

    // always start with display color white
    @color
    M=0

    // get value of keyboard map
    @KBD
    D=M

    // if D is greater than 0, keyboard is pressed
    @BLACK
    D;JGT

    // otherwise jump to DISPLAY
    @DISPLAY
    0;JMP

(BLACK)
    @color
    M=-1

(DISPLAY)
    // declare variables for i, len, and cursor
    @i
    M=1

    // set total number of iterations. In this case 32x255
    @8160
    D=A
    @len
    M=D

    // set our cursor to start where the display map starts
    @SCREEN
    D=A
    @cursor
    M=D

(RENDER)
    @i
    D=M

    // subtract value at @len from i. Because we increment i later,
    // this difference will get smaller each iteration
    @len
    D=D-M

    // if d greater than 0, terminate loop, and jump to START
    @START
    D;JGT

    // otherwise, get current @color
    @color
    D=M

    // set address register to value at cursor, which changes M
    // and now set the register at M to @color
    @cursor
    A=M
    M=D

    // move address value stored in cursor foward 1
    @cursor
    M=M+1

    // update i
    @i
    M=M+1

    // jump to render
    @RENDER
    0;JMP
