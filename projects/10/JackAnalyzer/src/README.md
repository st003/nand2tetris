# JackAnalyzer

The lexer and parser portion of the Nand2Tetris' Jack compiler written in the Python programming language.

_Note: Python used to simplify the assignment submission proccess._

## Prerequisites

* Python 3.6+

## Usage

To use the analyzer, from the src directory, run the command:

Linux/MacOS
```
python JackAnalyzer.py [-d] <file.jack>|<path-to-jack-files-directory>
```

Outputs two XML files for each Jack source code file:

1. A flat XML with all of the tokens identified
2. A complex XML file with tokens, statements, and expressions

### Options

The optional flag "-d" will cause each XML to include the string "DEBUG" in the file name.

## Running the tests

From the src directory, run the command:

```
python -m unittest tests.py
```

## Authors

* **st003**
