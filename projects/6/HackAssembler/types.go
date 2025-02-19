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

// LABELS & SYMBOLS

var labels = make(map[string]int)
