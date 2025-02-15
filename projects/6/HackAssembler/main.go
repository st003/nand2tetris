package main

import (
	"fmt"
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

	fmt.Printf("Assembling %v\n", asmFilePath)
}
