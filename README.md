# Dictionary Merger Project

## Description
This Python script generates a list of random dictionaries and merges them according to specific rules for handling key conflicts.

## Features

### 1. Random Dictionary Generation
- Creates 2-10 random dictionaries
- Each dictionary has random number of keys (1-10)
- Keys are random lowercase letters
- Values are random integers from 0-100

### 2. Smart Dictionary Merging
- **Duplicate keys**: Takes maximum value and renames key with source dictionary number
- **Unique keys**: Keeps original key name and value
- **Example**: `[{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]` becomes `{'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}`

## Usage

```bash
python dict_merger.py
```

## Output Example
```
=== Dictionary Generator and Merger ===

Generating 2 random dictionaries...
Dict 1: {'o': 3, 'd': 23, 'f': 9, 'q': 79, 'i': 28, 'u': 81, 'e': 3}
Dict 2: {'h': 45, 'm': 6, 'k': 47, 'a': 82, 'f': 89, 'c': 63, 'q': 62}

Generated list of dictionaries:
[{'o': 3, 'd': 23, 'f': 9, 'q': 79, 'i': 28, 'u': 81, 'e': 3}, {'h': 45, 'm': 6, 'k': 47, 'a': 82, 'f': 89, 'c': 63, 'q': 62}]

Final merged dictionary:
{'o': 3, 'd': 23, 'f_2': 89, 'q_1': 79, 'i': 28, 'u': 81, 'e': 3, 'h': 45, 'm': 6, 'k': 47, 'a': 82, 'c': 63}
```

## Author
Prasanna Chandrasheka

## Course
EPAM Data Quality Program - Collections Module