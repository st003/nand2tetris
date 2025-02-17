package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func getFileName(filePath string) (string, error) {

	_, fileNameWithExt := filepath.Split(filePath)

	ext := filepath.Ext(fileNameWithExt)
	if ext != ".asm" {
		return "", fmt.Errorf("file named: \"%v\" does not have required asm extention", fileNameWithExt)
	}

	fileNameParts := strings.Split(fileNameWithExt, ".")
	// NOTE: extention check should prevent an error here
	fileName := fileNameParts[0]

	return fileName, nil
}

func makeOutFile(fileName string, instructions []Instruction) error {

	lines := make([]string, 0)
	for _, ins := range instructions {
		lines = append(lines, ins.Binary)
	}

	fullFileName := fmt.Sprintf("%v.hack", fileName)

	outFile, err := os.Create(fullFileName)
	if err != nil {
		fmt.Println("Error opening outfile.hack:", err)
		return err
	}
	defer outFile.Close()

	_, err = outFile.WriteString(strings.Join(lines, "\n"))
	if err != nil {
		fmt.Println("Unable to write lines to outfile", err)
		return err
	}

	return nil
}
