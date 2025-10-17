package main

import "testing"

func TestGetFileNameMissingExtention(t *testing.T) {
	filePath := "path/to/file"
	_, err := getFileName(filePath)
	if err == nil {
		t.Fatalf("Expected error to be thrown for missing or incorrect extention")
	}
}

func TestGetFileNameWrongExtention(t *testing.T) {
	filePath := "path/to/file.abc"
	_, err := getFileName(filePath)
	if err == nil {
		t.Fatalf("Expected error to be thrown for missing or incorrect extention")
	}
}

func TestGetFileNameSuccess(t *testing.T) {
	expected := "file"
	filePath := "path/to/file.asm"

	actual, err := getFileName(filePath)

	if err != nil {
		t.Fatalf("Expected success. Error was raised: %v", err)
	}

	if actual != expected {
		t.Fatalf("Actual value: %v does not equal expected value: %v", actual, expected)
	}
}
