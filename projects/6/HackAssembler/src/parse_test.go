package main

import "testing"

func TestGetInstructionType_A(t *testing.T) {
	actual := getInstructionType("@256")
	if actual != A_INS {
		t.Fatalf("Actual value: %v does not equal expected value true", actual)
	}
}

func TestGetInstructionType_C(t *testing.T) {
	actual := getInstructionType("0;JMP")
	if actual != C_INS {
		t.Fatalf("Actual value: %v does not equal expected value false", actual)
	}
}

func TestIsisEmptyOrCommentLine_EmptyLine(t *testing.T) {
	expected := true
	actual := isEmptyOrCommentLine("")
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestIsisEmptyOrCommentLine_Comment(t *testing.T) {
	expected := true
	actual := isEmptyOrCommentLine("// comment line")
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestIsLabelLine_IsLabel(t *testing.T) {
	input := Instruction{-1, 1, 0, "(LABEL)", ""}
	expected := true
	actual := isLabelLine(input)
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}
func TestIsLabelLine_IsNotLabel(t *testing.T) {
	input := Instruction{-1, 1, 0, "@LABEL", ""}
	expected := false
	actual := isLabelLine(input)
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestParseLabelLine_MissingParenthesis(t *testing.T) {
	input := Instruction{-1, 1, 0, "(LABEL", ""}
	err := parseLabelLine(input)
	if err == nil {
		t.Fatalf("Expected error when none was received")
	}
}

func TestParseLabelLine_Success(t *testing.T) {
	input := Instruction{-1, 1, 0, "(LABEL)", ""}
	err := parseLabelLine(input)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
}
