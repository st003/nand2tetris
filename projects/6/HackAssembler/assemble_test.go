package main

import "testing"

func TestIsInvalidInstructionEmptyLine(t *testing.T) {
	expected := true
	actual := isEmptyOrCommentLine("")
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestIsInvalidInstructionComments(t *testing.T) {
	expected := true
	actual := isEmptyOrCommentLine("// comment line")
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestIsLabelLineIsLabel(t *testing.T) {
	expected := true
	actual := isLabelLine("(LABEL)")
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}
func TestIsLabelLineIsNotLabel(t *testing.T) {
	expected := false
	actual := isLabelLine("@LABEL")
	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}

func TestParseLabelLineMissingParenthesis(t *testing.T) {
	err := parseLabelLine("(LABEL", 0)
	if err == nil {
		t.Fatalf("Expected error when none was received")
	}
}

func TestParseLabelLineLowercase(t *testing.T) {
	err := parseLabelLine("(label)", 0)
	if err == nil {
		t.Fatalf("Expected error when none was received")
	}
}
func TestParseLabelLineSuccess(t *testing.T) {
	err := parseLabelLine("(LABEL)", 0)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
}
