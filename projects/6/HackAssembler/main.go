package main

import (
	"fmt"
	"time"
	"os"
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

	// TODO - assemble(inFile, outFile)

	end := time.Now()
	executionTime := float64(end.UnixMilli() - start.UnixMilli()) / float64(1000)
	fmt.Printf("\nDone. Assembly time: %v seconds\n", executionTime)
}


func assemble(inFile File) {
	
}
