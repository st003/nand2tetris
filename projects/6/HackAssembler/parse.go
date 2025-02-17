package main

import (
	"bufio"
	"os"
)

type Instruction struct {
	LineNumber int
	Asm        string
	Binary     string
}

func parse(inFile *os.File) []Instruction {
	instructions := make([]Instruction, 0)
	lineNum := 0 // TODO - verify if hack asm line numbers start at 0

	scanner := bufio.NewScanner(inFile)
	for scanner.Scan() {
		ins := Instruction{
			lineNum,
			scanner.Text(),
			scanner.Text(),
		}
		instructions = append(instructions, ins)

		lineNum++
	}

	return instructions
}
