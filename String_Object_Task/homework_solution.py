"""
String Object Task - Homework Solution
Text processing assignment with case normalization, sentence creation, spelling correction, and whitespace counting.
"""

import re
import string

def main():
    # Step 1: Copy the text to a variable
    homework_text = """homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix"iZ" with correct "is", but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

    print("Original text:")
    print(repr(homework_text))
    print("\n" + "="*80 + "\n")
    
    # Step 2: Process the text
    processed_text = process_homework_text(homework_text)
    
    print("Final processed text:")
    print(processed_text)
    print("\n" + "="*80 + "\n")
    
    # Step 3: Count whitespace characters
    whitespace_count = count_whitespace_characters(homework_text)
    print(f"Total whitespace characters in original text: {whitespace_count}")


def process_homework_text(text):
    """Process the homework text according to all requirements"""
    
    # Step 1: Fix spelling mistakes - replace 'iZ' with 'is' only when it's a mistake
    # We need to be careful: "iZ" should become "is", but "Iz" at the beginning might be intentional
    text = fix_spelling_mistakes(text)
    
    # Step 2: Normalize letter cases (proper sentence case)
    text = normalize_letter_cases(text)
    
    # Step 3: Create sentence with last words and add to end
    text = add_last_words_sentence(text)
    
    return text


def fix_spelling_mistakes(text):
    """Fix 'iZ' with 'is' only when it's a spelling mistake"""
    print("Step 1: Fixing spelling mistakes...")
    
    # Replace 'iZ' with 'is' only when it's a spelling mistake
    # Looking at the text: "it iZ misspeLLing here" and "last iz TO calculate"
    # The instruction says to fix "iZ" but ONLY when it Iz a mistake
    # So we need to be careful about "Iz" vs "iZ"
    
    # Replace lowercase 'iz' with 'is' (clear mistakes)
    fixed_text = text.replace(' iz ', ' is ')
    # Replace 'iZ' (mixed case) with 'is' when it's clearly wrong
    fixed_text = fixed_text.replace(' iZ ', ' is ')
    
    print("Spelling fixes applied.")
    return fixed_text


def normalize_letter_cases(text):
    """Normalize text from letter cases point of view (proper sentence case)"""
    print("Step 2: Normalizing letter cases...")
    
    # Split text into sentences and normalize each one
    # First, let's handle the colon case and sentence beginnings properly
    lines = text.split('\n')
    normalized_lines = []
    
    for line in lines:
        if line.strip():
            # Convert to lowercase first
            line = line.lower()
            # Capitalize first letter of the line if it contains text
            if line.strip():
                # Find first alphabetic character and capitalize it
                line = re.sub(r'^(\s*)([a-z])', lambda m: m.group(1) + m.group(2).upper(), line)
                # Capitalize letters after sentence endings (. ! ?)
                line = re.sub(r'([.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), line)
        normalized_lines.append(line)
    
    normalized_text = '\n'.join(normalized_lines)
    print("Letter case normalization completed.")
    return normalized_text


def add_last_words_sentence(text):
    """Create one more sentence with last words of each existing sentence and add to end"""
    print("Step 3: Creating sentence from last words...")
    
    # Find all sentences (text ending with ., !, or ?)
    sentences = re.findall(r'[^.!?]*[.!?]', text)
    
    last_words = []
    for sentence in sentences:
        # Remove punctuation and extra whitespace, then get the last word
        clean_sentence = sentence.strip().rstrip('.!?').strip()
        if clean_sentence:
            words = clean_sentence.split()
            if words:
                last_words.append(words[-1])
    
    print(f"Found {len(sentences)} sentences with last words: {last_words}")
    
    # Create new sentence from last words
    if last_words:
        new_sentence = " ".join(last_words) + "."
        # Add the new sentence to the end of the paragraph
        text = text.rstrip() + " " + new_sentence.capitalize()
    
    print("Last words sentence added.")
    return text


def count_whitespace_characters(text):
    """Count all whitespace characters (spaces, tabs, newlines, etc.)"""
    print("Step 4: Counting whitespace characters...")
    
    # Count all whitespace characters using string.whitespace
    # This includes: space, tab, newline, vertical tab, form feed, carriage return
    whitespace_count = sum(1 for char in text if char in string.whitespace)
    
    # Let's also show the breakdown
    space_count = text.count(' ')
    newline_count = text.count('\n')
    tab_count = text.count('\t')
    other_whitespace = whitespace_count - space_count - newline_count - tab_count
    
    print(f"Whitespace breakdown:")
    print(f"  Spaces: {space_count}")
    print(f"  Newlines: {newline_count}")
    print(f"  Tabs: {tab_count}")
    print(f"  Other whitespace: {other_whitespace}")
    print(f"  Total whitespace: {whitespace_count}")
    
    return whitespace_count


if __name__ == "__main__":
    main()