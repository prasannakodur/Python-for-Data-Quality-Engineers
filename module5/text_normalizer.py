"""Module5: Functional text normalization task.

Steps (per assignment):
1. Copy provided raw text to a variable.
2. Normalize letter casing (standard sentence capitalization).
3. Create an additional sentence composed of the last word of each existing sentence; append it.
4. Fix misspelling of the standalone word 'iz'/'iZ'/case variants to 'is' ONLY when it's an actual word in sentences, not when inside quotes describing the rule.
5. Count all whitespace characters (spaces, newlines, tabs, etc.) in the ORIGINAL raw text.

Functional decomposition provided; the script prints:
- Original whitespace count
- Normalized paragraph (with appended sentence)
"""
from __future__ import annotations
import re
from typing import List

RAW_TEXT = (
    "  tHis iz your homeWork, copy these Text to variable.\n"\
    "\n"\
    "  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.\n"\
    "\n"\
    "  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.\n"\
    "\n"\
    "  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.\n"
)

# ---------------- Core Pure Functions ---------------- #

def get_original_text() -> str:
    return RAW_TEXT

def count_whitespace(text: str) -> int:
    return sum(1 for ch in text if ch.isspace())

def split_sentences(text: str) -> List[str]:
    """Split text into sentences (keep only non-empty), using '.' as delimiter.
    We work on a flattened version (single spaces) for processing but maintain logic simple.
    """
    # Replace newlines with space to keep sentence integrity then split.
    flat = re.sub(r"\s+", " ", text.strip())
    parts = [p.strip() for p in flat.split('.') if p.strip()]
    return parts

def normalize_case_sentence(s: str) -> str:
    s_lower = s.lower()
    if not s_lower:
        return s_lower
    return s_lower[0].upper() + s_lower[1:]

def fix_iz_words(s: str) -> str:
    """Replace whole-word 'iz' variants with 'is' except when enclosed in quotes (smart or straight).
    Strategy: temporarily protect quoted segments, perform replacement elsewhere, then restore.
    """
    # Protect quoted segments (including smart quotes) with placeholders.
    placeholders = []
    def store(m):
        placeholders.append(m.group(0))
        return f"__Q{len(placeholders)-1}__"
    # Pattern heuristic: match segments wrapped in straight or smart quotes. Simplicity over perfection.
    protected = re.sub(r'(?:["“”])(.*?)(?:["“”])', store, s)
    # Replace whole word iz variants
    protected = re.sub(r'\b[iI][zZ]\b', 'is', protected)
    # Restore
    def restore(m):
        return placeholders[int(m.group(1))]
    restored = re.sub(r'__Q(\d+)__', lambda m: placeholders[int(m.group(1))], protected)
    return restored

def build_last_words_sentence(sentences: List[str]) -> str:
    words = []
    for sent in sentences:
        tokens = sent.split()
        if tokens:
            words.append(tokens[-1].lower())
    if not words:
        return ''
    joined = ' '.join(words)
    return joined[0].upper() + joined[1:] + '.'

def process_text(raw: str) -> str:
    # Count whitespace (original) first.
    ws_count = count_whitespace(raw)
    # Work on content for sentence operations (case + iz fixes) excluding the extra sentence.
    sentences = split_sentences(raw)
    # Normalize case and fix 'iz' per sentence.
    norm_sentences = []
    for s in sentences:
        s_fixed = fix_iz_words(s)
        s_norm = normalize_case_sentence(s_fixed)
        norm_sentences.append(s_norm)
    # Build new sentence
    extra = build_last_words_sentence(norm_sentences)
    # Compose final paragraph
    paragraph = ' '.join(s + '.' for s in norm_sentences)
    if extra:
        paragraph = paragraph + ' ' + extra
    return f"Original whitespace count: {ws_count}\n\n{paragraph}\n"

# ---------------- Script Entrypoint ---------------- #

def main() -> None:
    raw = get_original_text()
    output = process_text(raw)
    print(output)

if __name__ == '__main__':
    main()
