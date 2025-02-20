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

		// if not an int, create a new variable label
		if err != nil {
			intValue, labels[value] = varLabelAddress, varLabelAddress
			// next new variable will get a new address
			varLabelAddress++
		}

		if intValue < 0 {
			return "", fmt.Errorf("syntax error at line %v. Label cannot represent negative number", ins.FileLine)
		}

		if intValue > MAX_ADDRESS {
			return "", fmt.Errorf("syntax error at line %v. Address value cannot exceed %v", ins.FileLine, MAX_ADDRESS)
		}

		address = intValue
	}

	// convert to binary representation of value
	binary := "0" + fmt.Sprintf("%015b", address)

	return binary, nil
}

func assembleCInstruction(ins Instruction) (string, error) {

	// default values
	const opt = "111"
	var comp string
	dest := "000"
	jump := "000"

	equalsPos := 0
	semiPos := 0

	// locate '=' and ';' characters and skip trailing whitespace/comments
	insEnd := len(ins.Asm)
	for i, c := range ins.Asm {
		if c == '=' {
			equalsPos = i
		} else if c == ';' {
			semiPos = i
		} else if c == ' ' || c == '/' {
			insEnd = i
			break
		}
	}

	cleanAsm := ins.Asm[:insEnd]

	// c-instructions must have either a '=' or a ';'
	if (equalsPos == 0) && (semiPos == 0) {
		return "", fmt.Errorf("sytanx error at line %v. \"%v\" is not a valid c-instruction", ins.FileLine, cleanAsm)
	}

	var compStart int
	var symbol string
	var ok bool

	// get dest symbol
	if equalsPos > 0 {
		var ok bool
		symbol = cleanAsm[:equalsPos]
		dest, ok = destSymbols[symbol]
		if !ok {
			return "", fmt.Errorf("sytanx error at line %v. \"%v\" is not a valid dest symbol", ins.FileLine, symbol)
		}
		compStart = equalsPos + 1
	}

	// get comp symbol
	if semiPos > 0 {
		symbol = cleanAsm[compStart:semiPos]
	} else {
		symbol = cleanAsm[compStart:]
	}

	comp, ok = compSymbols[symbol]
	if !ok {
		return "", fmt.Errorf("sytanx error at line %v. \"%v\" is not a valid comp symbol", ins.FileLine, symbol)
	}

	// get jump symbol
	if semiPos > 0 {
		symbol = cleanAsm[(semiPos + 1):]
		if len(symbol) > 0 {
			jump, ok = jumpSymbols[symbol]
			if !ok {
				return "", fmt.Errorf("sytanx error at line %v. \"%v\" is not a valid jump symbol", ins.FileLine, symbol)
			}
		}
	}

	if len(comp) == 0 {
		return "", fmt.Errorf("comp bits have not been set for instruction at line %v", ins.FileLine)
	}

	binary := opt + comp + dest + jump

	return binary, nil
}

func assemble(inFile *os.File) ([]Instruction, error) {

	instructions, err := parse(inFile)
	if err != nil {
		return nil, err
	}

	for i, ins := range instructions {

		var binary string
		var err error

		if ins.Type == A_INS {
			binary, err = assembleAInstruction(ins)
		} else {
			binary, err = assembleCInstruction(ins)
		}

		if err != nil {
			return nil, err
		}
		instructions[i].Binary = binary
	}

	return instructions, nil
}
