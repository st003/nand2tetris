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

	file, err := os.Open(asmFilePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		os.Exit(1)
	}
	defer file.Close()

	start := time.Now()

	fmt.Printf("Assembling %v\n", asmFilePath)

	end := time.Now()
	executionTime := float64(end.UnixMilli() - start.UnixMilli()) / float64(1000)
	fmt.Printf("\nDone. Assembly time: %v seconds\n", executionTime)
}
