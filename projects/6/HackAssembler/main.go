package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

func main() {

	args := os.Args

	if len(args) != 2 {
		fmt.Println("Usage: ha asmfile")
		os.Exit(0)
	}

	asmFilePath := args[1]

	inFile, err := os.Open(asmFilePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		os.Exit(1)
	}
	defer inFile.Close()

	start := time.Now()

	fmt.Printf("Assembling %v\n", asmFilePath)
	instructions := parse(inFile)

	end := time.Now()

	err = makeOutFile(instructions)
	if err != nil {
		os.Exit(2)
	}

	executionTime := float64(end.UnixMilli()-start.UnixMilli()) / float64(1000)
	fmt.Printf("\nDone. Assembly time: %v seconds\n", executionTime)
}

func makeOutFile(instructions []Instruction) error {

	lines := make([]string, 0)
	for _, ins := range instructions {
		lines = append(lines, ins.Binary)
	}

	// TODO - dynamically get file name
	outFile, err := os.Create("outfile.hack")
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
