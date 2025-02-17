package main

import (
	"strings"
	"testing"
)

func TestAssembleAInstructionNoWhitespaceOrComments(t *testing.T) {
	actual := assembleAInstruction("@256")
	expected := "@256"
	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestAssembleAInstructionWhiteSpace(t *testing.T) {
	input := "@256   "
	actual := assembleAInstruction(input)
	expected := "@256"
	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleAInstructionComment(t *testing.T) {
	input := "@256// comment"
	actual := assembleAInstruction(input)
	expected := "@256"
	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}
