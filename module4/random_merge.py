"""Functional solution (module4) for generating a random list of dictionaries and merging them.

Differences vs existing root script `dict_merger.py`:
- Pure functional decomposition with small, testable functions.
- Deterministic tie-breaking (earliest dict on equal max values).
- Minimal side effects (only printing in demo).
"""
from __future__ import annotations
from typing import Dict, List, Iterable, Tuple
import random
import string

def random_letter_keys(min_keys: int = 1, max_keys: int = 10, *, alphabet: str = string.ascii_lowercase) -> List[str]:
    count = random.randint(min_keys, max_keys)
    return random.sample(alphabet, count)

def make_random_dict(min_keys: int = 1, max_keys: int = 10, value_range: Tuple[int, int] = (0, 100)) -> Dict[str, int]:
    low, high = value_range
    return {k: random.randint(low, high) for k in random_letter_keys(min_keys, max_keys)}

def generate_dict_list(min_dicts: int = 2, max_dicts: int = 10, **dict_kwargs) -> List[Dict[str, int]]:
    n = random.randint(min_dicts, max_dicts)
    return [make_random_dict(**dict_kwargs) for _ in range(n)]

def merge_dicts(dicts: Iterable[Dict[str, int]]) -> Dict[str, int]:
    occurrences: Dict[str, List[Tuple[int, int]]] = {}
    for idx, d in enumerate(dicts, start=1):
        for k, v in d.items():
            occurrences.setdefault(k, []).append((idx, v))
    merged: Dict[str, int] = {}
    for key, pairs in occurrences.items():
        if len(pairs) == 1:
            merged[key] = pairs[0][1]
        else:
            max_pair = min(pairs, key=lambda p: (-p[1], p[0]))  # max value, tie => earliest idx
            idx_of_max, value_of_max = max_pair
            merged[f"{key}_{idx_of_max}"] = value_of_max
    return merged

def demo(seed: int | None = None) -> None:
    if seed is not None:
        random.seed(seed)
    dict_list = generate_dict_list()
    merged = merge_dicts(dict_list)
    print("Generated list of dicts:")
    print(dict_list)
    print("\nMerged dict:")
    print(merged)

def _test_example() -> None:
    data = [
        {'a': 5, 'b': 7, 'g': 11},
        {'a': 3, 'c': 35, 'g': 42}
    ]
    merged = merge_dicts(data)
    assert merged == {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}

def _run_tests() -> None:
    _test_example()
    print("module4 functional tests passed")

if __name__ == "__main__":
    _run_tests()
    demo()