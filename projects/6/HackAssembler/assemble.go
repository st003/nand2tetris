package main

import (
	"os"
	"strconv"
)

func assembleAInstruction(asm string) string {
	// clear out any trailing whitespace and comments
	end := -1
	for i, c := range asm {
		if c == ' ' || c == '/' {
			end = i
			break
		}
	}

	if end != -1 {
		asm = asm[:end]
	}

	value := asm[1:]
	lineNum, ok := labels[value]
	if ok {
		asm = "@" + strconv.Itoa(lineNum)
	}

	// TODO - convert asm into binary

	return asm
}

func assemble(inFile *os.File) ([]Instruction, error) {

	instructions, err := parse(inFile)
	if err != nil {
		return nil, err
	}

	// TODO:
	// load symbol tables
	// parse and assemble asm into machine code

	for i, ins := range instructions {

		if ins.Type == A_INS {
			binary := assembleAInstruction(ins.Asm)
			instructions[i].Binary = binary

		} else {
			instructions[i].Binary = instructions[i].Asm
		}
	}

	return instructions, nil
}
