# Module4 Functional Dictionary Merger

This folder contains a functional style implementation of the random dictionary generation + merge task.

## Implementation Highlights
- Separate pure functions: `random_letter_keys`, `make_random_dict`, `generate_dict_list`, `merge_dicts`.
- Merge rule: for duplicate keys choose maximum value, rename to `key_<dict_index>` using 1-based index of dict that held the max. Tie on value chooses earliest dict.
- Unique keys remain unchanged.

## Example
Input list: `[{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]`
Merged: `{'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}`

## Running
```powershell
python module4/random_merge.py
```
Add `demo(seed=123)` for reproducible output.

## Tests
Minimal assertion inside `_test_example()` validates spec.

## Comparison
Root `dict_merger.py` is an imperative, print-heavy flow; this version isolates logic for easier unit testing and reuse.
