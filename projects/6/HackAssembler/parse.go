package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func getInstructionType(line string) int {
	if line[0] == '@' {
		return A_INS
	}
	return C_INS
}

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

func isLabelLine(ins Instruction) bool {
	return ins.Asm[0] == '('
}

func parseLabelLine(ins Instruction) error {
	trimmed := strings.TrimLeft(ins.Asm, "(")
	parts := strings.Split(trimmed, ")")

	// LABEL) should return a minimum of two strings
	if len(parts) < 2 {
		return fmt.Errorf("syntax error at line %v. Label missing closing parenthesis: %v", ins.FileLine, ins.Asm)
	}

	label := parts[0]
	labels[label] = ins.ProgramLine

	return nil
}

func parse(inFile *os.File) ([]Instruction, error) {

	instructions := make([]Instruction, 0)

	fileLineNum := 0
	programLineNum := 0

	scanner := bufio.NewScanner(inFile)
	for scanner.Scan() {

		line := strings.Trim(scanner.Text(), " ")

		// always increment the file line number
		fileLineNum++

		if isEmptyOrCommentLine(line) {
			continue
		}

		ins := Instruction{
			getInstructionType(line),
			fileLineNum,
			programLineNum,
			line,
			"",
		}

		if isLabelLine(ins) {
			err := parseLabelLine(ins)
			if err != nil {
				return nil, err
			}
			continue
		}

		instructions = append(instructions, ins)

		// only increment the program line number if
		// comment/whitespace/label checks pass
		programLineNum++
	}

	return instructions, nil
}
