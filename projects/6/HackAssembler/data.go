package main

const A_INS = 0
const C_INS = 1

type Instruction struct {
	Type       int
	LineNumber int
	Asm        string
	Binary     string
}

var labels = make(map[string]int)
