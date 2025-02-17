package main

import "testing"

func TestIsInvalidInstructionEmptyLine(t *testing.T) {
	expected := true
	actual := isInvalidInstruction("")
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestIsInvalidInstructionComments(t *testing.T) {
	expected := true
	actual := isInvalidInstruction("// comment line")
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}
