package main

// STRUCTS

type Instruction struct {
	Type       int
	LineNumber int
	Asm        string
	Binary     string
}

// CONSTANTS

const A_INS = 0
const C_INS = 1

// A Hack computer data address is 15-bits
const MAX_ADDRESS = 32_767

// LABELS & SYMBOLS

// Hack ASM specification states variable label address
// start at 16
var varLabelAddress int = 16

// predefined labels from the Hack ASM specification
var labels = map[string]int{
	"R0":     0,
	"R1":     1,
	"R2":     2,
	"R3":     3,
	"R4":     4,
	"R5":     5,
	"R6":     6,
	"R7":     7,
	"R8":     8,
	"R9":     9,
	"R10":    10,
	"R11":    11,
	"R12":    12,
	"R13":    13,
	"R14":    14,
	"R15":    15,
	"SP":     0,
	"LCL":    1,
	"ARG":    2,
	"THIS":   3,
	"THAT":   4,
	"SCREEN": 16_384,
	"KBD":    24_576,
}
