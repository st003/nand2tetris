package main

import "os"

func assemble(inFile *os.File) ([]Instruction, error) {

	instructions, err := parse(inFile)
	if err != nil {
		return nil, err
	}

	// TODO:
	// load symbol tables
	// parse and assemble asm into machine code

	for i := range instructions {
		instructions[i].Binary = instructions[i].Asm
	}

	return instructions, nil
}
