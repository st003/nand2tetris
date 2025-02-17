package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Instruction struct {
	Type       int
	LineNumber int
	Asm        string
	Binary     string
}

const A_INS = 0
const C_INS = 1

var labels = make(map[string]int)

func isEmptyOrCommentLine(line string) bool {
	if len(line) == 0 {
		return true

	} else if line[0] == '/' {
		// NOTE: technically a comment line should start with //
		// but since '/' is not a valid character in hack asm, checking
		// for only a single '/' has the same effect
		return true
	}

	return false
}

func isLabelLine(line string) bool {
	return line[0] == '('
}

func getInstructionType(line string) int {
	if line[0] == '@' {
		return A_INS
	}
	return C_INS
}

func parseLabelLine(line string, lineNum int) error {
	trimmed := strings.TrimLeft(line, "(")
	parts := strings.Split(trimmed, ")")

	// LABEL) should return a minimum of two strings
	if len(parts) < 2 {
		return fmt.Errorf("syntax error with label instruction: %v", line)
	}

	label := parts[0]
	labelCopy := strings.Clone(label)
	labelCopy = strings.ToUpper(labelCopy)

	if strings.Compare(label, labelCopy) != 0 {
		return fmt.Errorf("syntax error. Label instruction must be uppercase: %v", label)
	}

	labels[label] = lineNum

	return nil
}

func parse(inFile *os.File) ([]Instruction, error) {

	instructions := make([]Instruction, 0)
	lineNum := 0

	scanner := bufio.NewScanner(inFile)
	for scanner.Scan() {
		line := strings.Trim(scanner.Text(), " ")

		if isEmptyOrCommentLine(line) {
			continue
		}

		if isLabelLine(line) {
			err := parseLabelLine(line, lineNum)
			if err != nil {
				return nil, err
			}
			continue
		}

		ins := Instruction{
			getInstructionType(line),
			lineNum,
			line,
			"",
		}

		instructions = append(instructions, ins)
		lineNum++
	}

	return instructions, nil
}

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
