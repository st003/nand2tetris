package main

import (
	"fmt"
	"os"
	"strconv"
)

func assembleAInstruction(ins Instruction) string {

	// clear out any trailing whitespace and comments
	end := -1
	for i, c := range ins.Asm {
		if c == ' ' || c == '/' {
			end = i
			break
		}
	}

	if end != -1 {
		ins.Asm = ins.Asm[:end]
	}

	// ignore the '@'
	value := ins.Asm[1:]

	// check if instruction contains any labels
	address, ok := labels[value]

	// if no label is found, parse address string to an int
	if !ok {
		intValue, err := strconv.Atoi(value)
		if err != nil {
			// TODO - create new label?
		}

		// TODO - add a a negative number check
		// TODO - add a max address value argument

		address = intValue
	}

	// convert to  binary representation of value
	binary := "0" + fmt.Sprintf("%015b", address)

	return binary
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
			binary := assembleAInstruction(ins)
			instructions[i].Binary = binary

		} else {
			instructions[i].Binary = instructions[i].Asm
		}
	}

	return instructions, nil
}
