package main

import (
	"bufio"
	"os"
	"strings"
)

type Instruction struct {
	LineNumber int
	Asm        string
	Binary     string
}

func isInvalidInstruction(line string) bool {
	line = strings.Trim(line, " ")

	if len(line) == 0 {
		return true

	} else if line[0] == '/' {
		// NOTE: technically a comment line should start with //
		// but since / is not a valid character in hack asm, checking
		// for only a single / has the same effect
		return true
	}

	return false
}

func parse(inFile *os.File) []Instruction {

	instructions := make([]Instruction, 0)
	lineNum := 0 // TODO - verify if hack asm line numbers start at 0

	scanner := bufio.NewScanner(inFile)
	for scanner.Scan() {
		line := scanner.Text()

		if isInvalidInstruction(line) {
			continue
		}

		ins := Instruction{lineNum, line, ""}
		instructions = append(instructions, ins)
		lineNum++
	}

	return instructions
}

func assemble(inFile *os.File) []Instruction {
	instructions := parse(inFile)

	for i := range instructions {
		instructions[i].Binary = instructions[i].Asm
	}

	return instructions
}
