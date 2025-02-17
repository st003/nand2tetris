package main

import (
	"fmt"
	"os"
	"time"
)

func main() {

	args := os.Args
	if len(args) != 2 {
		fmt.Println("Usage: ha asmfile")
		os.Exit(0)
	}
	asmFilePath := args[1]

	fileName, err := getFileName(asmFilePath)
	if err != nil {
		os.Exit(1)
	}

	inFile, err := os.Open(asmFilePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		os.Exit(2)
	}
	defer inFile.Close()

	start := time.Now()

	fmt.Printf("Assembling %v\n", asmFilePath)
	instructions := parse(inFile)

	end := time.Now()

	err = makeOutFile(fileName, instructions)
	if err != nil {
		os.Exit(3)
	}

	executionTime := float64(end.UnixMilli()-start.UnixMilli()) / float64(1000)
	fmt.Printf("\nDone. Assembly time: %v seconds\n", executionTime)
}
