# Module5: Text Normalizer

## Task Requirements
Given a raw, inconsistently cased text:
1. Normalize letter casing (sentence case for each sentence).
2. Build a new sentence from the last word of every existing sentence and append it.
3. Correct only the mistaken standalone word variants of "iz" (any casing) to "is" (not when inside quotes describing the rule).
4. Count all whitespace characters (spaces, newlines, tabs, etc.) in the ORIGINAL text.

## Functional Decomposition
- `get_original_text()` – returns the raw text constant.
- `count_whitespace(text)` – counts every Unicode whitespace character.
- `split_sentences(text)` – extracts sentences by period.
- `normalize_case_sentence(s)` – lowercases entire sentence then capitalizes first letter.
- `fix_iz_words(s)` – replaces whole-word `iz` (any casing) with `is`, skipping quoted segments.
- `build_last_words_sentence(sentences)` – constructs the appended sentence from last words.
- `process_text(raw)` – orchestrator combining all steps.

## Running
```powershell
python module5/text_normalizer.py
```

## Sample Output (Excerpt)
```
Original whitespace count: 88

This is your homework, copy these text to variable. You need to normalize it from letter cases point of view. ... I got 87. Variable view paragraph here mistake tex whitespaces 87.
```

(Whitespace count in original source differs from the provided claim of 87; script reports 88 based on actual characters.)

## Notes / Assumptions
- Sentence detection is period-based; other punctuation not present in source.
- Smart quotes are preserved; occurrences of “iZ” inside quotes are not altered.
- Only basic normalization applied; no grammar or other spelling corrections (e.g., "Tex" / "Carefull").

## Possible Improvements
- More robust sentence segmentation (regex for punctuation). 
- Unit tests for each pure function.
- Option flags via argparse for alternative normalization modes.
