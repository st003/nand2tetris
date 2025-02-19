package main

import (
	"strings"
	"testing"
)

func TestAssembleAInstructionNoWhitespaceOrComments(t *testing.T) {

	input := Instruction{A_INS, 0, "@1", ""}
	actual := assembleAInstruction(input)
	expected := "0000000000000001"

	if len(actual) != 16 {
		t.Fatalf("Output does not contain 16 bits")
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestAssembleAInstructionWhiteSpace(t *testing.T) {

	input := Instruction{A_INS, 0, "@300   ", ""}
	actual := assembleAInstruction(input)
	expected := "0000000100101100"

	if len(actual) != 16 {
		t.Fatalf("Output does not contain 16 bits")
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleAInstructionComment(t *testing.T) {

	input := Instruction{A_INS, 0, "@1000// comment", ""}
	actual := assembleAInstruction(input)
	expected := "0000001111101000"

	if len(actual) != 16 {
		t.Fatalf("Output does not contain 16 bits")
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}
