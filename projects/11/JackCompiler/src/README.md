# JackCompiler

The Nand2Tetris' Jack compiler written in the Python programming language.

_Note: Python used to simplify the assignment submission proccess._

## Prerequisites

* Python 3.6+

## Usage

To use the compiler, from the src directory, run the command:

Linux/MacOS
```
python JackCompiler.py [-d] <file.jack>|<path-to-jack-files-directory>
```

Outputs a VM file for each Jack source code file

### Options

The optional flag "-d" will cause the compiler to output XML parse trees.

## Running the tests

From the src directory, run the command:

```
python -m unittest tests.py
```

## Authors

* **st003**
