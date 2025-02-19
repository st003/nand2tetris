package main

import (
	"fmt"
	"os"
	"strconv"
)

func assembleAInstruction(ins Instruction) (string, error) {

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
			labels[value] = varLabelAddress
			intValue = varLabelAddress
			// increment varLabelAddress so next new variable will get a new address
			varLabelAddress++
		}

		if intValue < 0 {
			return "", fmt.Errorf("syntax error at line %v. Label cannot represent negative number", ins.LineNumber)
		}

		if intValue > MAX_ADDRESS {
			return "", fmt.Errorf("syntax error at line %v. Address value cannot exceed %v", ins.LineNumber, MAX_ADDRESS)
		}

		address = intValue
	}

	// convert to  binary representation of value
	binary := "0" + fmt.Sprintf("%015b", address)

	return binary, nil
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
			binary, err := assembleAInstruction(ins)
			if err != nil {
				return nil, err
			}
			instructions[i].Binary = binary

		} else {
			instructions[i].Binary = instructions[i].Asm
		}
	}

	return instructions, nil
}
