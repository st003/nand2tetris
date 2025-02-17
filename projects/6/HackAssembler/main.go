package main

import (
	"fmt"
	"os"
	"time"
)

func main() {

	args := os.Args
	if len(args) != 2 {
		fmt.Println("Usage: ha inFile")
		os.Exit(0)
	}
	inFilePath := args[1]

	fileName, err := getFileName(inFilePath)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	inFile, err := os.Open(inFilePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		os.Exit(2)
	}
	defer inFile.Close()

	fmt.Printf("Assembling %v\n", inFilePath)
	start := time.Now()

	instructions, err := assemble(inFile)
	if err != nil {
		fmt.Println(err)
		os.Exit(3)
	}

	end := time.Now()

	err = makeOutFile(fileName, instructions)
	if err != nil {
		fmt.Println(err)
		os.Exit(4)
	}

	executionTime := float64(end.UnixMilli()-start.UnixMilli()) / float64(1000)
	fmt.Printf("\nDone. Assembly time: %v seconds\n", executionTime)
	os.Exit(0)
}
