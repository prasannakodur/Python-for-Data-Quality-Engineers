# User Generated News Feed Tool

## Overview
A simple CLI tool enabling users to publish records to a text-based feed in a consistent format.
Each record is appended at the end of `tool/feed.txt` (or a custom path via `--file`).

## Record Types
1. News
   - Input: text, city
   - Auto fields: current timestamp
   - Format:
     ```
     NEWS: <text>
     City: <city>
     Published: <timestamp>
     ----------------------------------------
     ```
2. Private Ad
   - Input: text, expiration date (YYYY-MM-DD)
   - Auto fields: current timestamp, days left (0 if expired; if past expiration displays EXPIRED)
   - Format:
     ```
     PRIVATE AD: <text>
     Expires: <YYYY-MM-DD> (Days left: X | or EXPIRED)
     Published: <timestamp>
     ----------------------------------------
     ```
3. Recipe (Unique Type)
   - Input: recipe title, ingredients (comma or semicolon separated)
   - Auto fields: ingredient count, average ingredient name length, complexity label (SIMPLE <=4, MODERATE 5-8, COMPLEX >8), timestamp
   - Format:
     ```
     RECIPE: <title>
     Ingredients (<count>): <list>
     Avg name length: <n> | Complexity: <label>
     Published: <timestamp>
     ----------------------------------------
     ```

## Functional Design
- Record creation functions (`create_news`, `create_private_ad`, `create_recipe`) return a finalized string including separator.
- No shared mutable state beyond appending to file.
- `feed_tool.py` orchestrates input capture and appends using `append_record`.

## Usage
Interactive mode:
```powershell
python tool/feed_tool.py
```
Demo mode (append sample records):
```powershell
python tool/feed_tool.py --demo
```
Custom feed file path:
```powershell
python tool/feed_tool.py --file custom_feed.txt --demo
```

## Error Handling
- Invalid date format raises an exception; record not appended.
- Empty ingredient tokens are filtered.

## Extending
Add new types by updating `TYPE_MAP` in `records.py`:
```python
TYPE_MAP["4"] = ("NewTypeLabel", factory_function, ["Prompt 1", "Prompt 2"])  # etc
```

## Demo
Run `--demo` then inspect `tool/feed.txt` to see sample output.
