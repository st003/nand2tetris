package main

import (
	"strings"
	"testing"
)

func TestAssembleAInstruction_NoWhitespaceOrComments(t *testing.T) {

	input := Instruction{A_INS, 1, 0, "@1", ""}
	actual, err := assembleAInstruction(input)
	expected := "0000000000000001"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(actual) != 16 {
		t.Fatalf("Output does not contain 16 bits")
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestAssembleAInstruction_WhiteSpace(t *testing.T) {

	input := Instruction{A_INS, 1, 0, "@300   ", ""}
	actual, err := assembleAInstruction(input)
	expected := "0000000100101100"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(actual) != 16 {
		t.Fatalf("Output does not contain 16 bits")
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleAInstruction_Comment(t *testing.T) {

	input := Instruction{A_INS, 1, 0, "@1000// comment", ""}
	actual, err := assembleAInstruction(input)
	expected := "0000001111101000"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(actual) != 16 {
		t.Fatalf("Output does not contain 16 bits")
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleAInstruction_R0(t *testing.T) {

	input := Instruction{A_INS, 1, 0, "@R0", ""}
	actual, err := assembleAInstruction(input)
	expected := "0000000000000000"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(actual) != 16 {
		t.Fatalf("Output does not contain 16 bits")
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleAInstruction_SCREEN(t *testing.T) {

	input := Instruction{A_INS, 1, 0, "@SCREEN", ""}
	actual, err := assembleAInstruction(input)
	expected := "0100000000000000"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(actual) != 16 {
		t.Fatalf("Output does not contain 16 bits")
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleAInstruction_KBD(t *testing.T) {

	input := Instruction{A_INS, 1, 0, "@KBD", ""}
	actual, err := assembleAInstruction(input)
	expected := "0110000000000000"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(actual) != 16 {
		t.Fatalf("Output does not contain 16 bits")
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleAInstruction_NegativeLabel(t *testing.T) {
	input := Instruction{A_INS, 1, 0, "@-100", ""}
	_, err := assembleAInstruction(input)
	if err == nil {
		t.Fatalf("Expected error when none was received")
	}
}

func TestAssembleAInstruction_MaxAddress(t *testing.T) {
	input := Instruction{A_INS, 1, 0, "@50000", ""}
	_, err := assembleAInstruction(input)
	if err == nil {
		t.Fatalf("Expected error when none was received")
	}
}

func TestAssembleCInstruction_DeM(t *testing.T) {
	input := Instruction{C_INS, 1, 0, "D=M", ""}
	actual, err := assembleCInstruction(input)
	expected := "1111110000010000"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleCInstruction_DeMmM(t *testing.T) {
	input := Instruction{C_INS, 1, 0, "D=D-M", ""}
	actual, err := assembleCInstruction(input)
	expected := "1111010011010000"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleCInstruction_DsJLE(t *testing.T) {
	input := Instruction{C_INS, 1, 0, "D;JLE", ""}
	actual, err := assembleCInstruction(input)
	expected := "1110001100000110"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleCInstruction_0sJMP(t *testing.T) {
	input := Instruction{C_INS, 1, 0, "0;JMP", ""}
	actual, err := assembleCInstruction(input)
	expected := "1110101010000111"

	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if strings.Compare(actual, expected) != 0 {
		t.Fatalf("Actual value: \"%v\" does not equal expected value: \"%v\"", actual, expected)
	}
}

func TestAssembleCInstruction_Invalid1(t *testing.T) {
	input := Instruction{C_INS, 1, 0, "D =M", ""}
	_, err := assembleCInstruction(input)
	if err == nil {
		t.Fatalf("Expected error when none was received")
	}
}

func TestAssembleCInstruction_Invalid2(t *testing.T) {
	input := Instruction{C_INS, 1, 0, "AMD", ""}
	_, err := assembleCInstruction(input)
	if err == nil {
		t.Fatalf("Expected error when none was received")
	}
}
