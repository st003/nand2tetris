package main

import (
	"bufio"
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

	lines := make([]string, 0, 10)

	scanner := bufio.NewScanner(inFile)
	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, line)
	}

	outFile, err := os.Create("outfile.hack")
	if err != nil {
		fmt.Println("Error opening outfile.hack:", err)
		os.Exit(1)
	}
	defer outFile.Close()

	_, err = outFile.WriteString(strings.Join(lines, "\n"))
	if err != nil {
		fmt.Println("Unable to write lines to outfile", err)
		os.Exit(2)
	}

	start := time.Now()

	fmt.Printf("Assembling %v\n", asmFilePath)

	end := time.Now()
	executionTime := float64(end.UnixMilli()-start.UnixMilli()) / float64(1000)
	fmt.Printf("\nDone. Assembly time: %v seconds\n", executionTime)
}
