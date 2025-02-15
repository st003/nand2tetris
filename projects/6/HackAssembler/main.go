package main

import (
	"fmt"
	"os"
)


func main() {

	args := os.Args

	if len(args) != 2 {
		fmt.Println("Usage: ha asm_file")
		os.Exit(0)
	}

	fmt.Printf("Assembling %v ...\n", args[1])
	os.Exit(0)
}
