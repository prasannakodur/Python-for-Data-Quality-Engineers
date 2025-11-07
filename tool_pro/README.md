# tool_pro: File-Based Feed Ingestion

## Overview
Extends the original `tool` feed system with a class-based file ingestion workflow. Allows users to batch-submit records via structured text files and optionally process an inbox directory.

## Input File Format
A file contains one or more record blocks. Blocks are separated by a line with three dashes:
```
---
```
Inside each block, lines follow `KEY: VALUE` format. Supported keys by type:

### News
```
TYPE: News
TEXT: Market reaches all-time high
CITY: Tokyo
```
### Ad (Private Advertisement)
```
TYPE: Ad
TEXT: Looking for a roommate near central park
EXPIRES: 2025-12-15  # YYYY-MM-DD
```
### Recipe (Unique Type)
```
TYPE: Recipe
TITLE: Veggie Soup
INGREDIENTS: carrots, potatoes, onion, celery, peas, salt, pepper
```
Separator line after each block:
```
---
```

## Processing Rules
- Each block parsed independently.
- Invalid blocks (missing required keys or malformed lines) are skipped.
- Successful records appended to feed file (`feed_pro.txt` by default).
- File deletion occurs if at least one record was successfully appended.

## Components
- `file_processor.py`: Contains `FileFeedProcessor` with methods:
  - `process_file(path)` → stats dict (`success`, `failed`, `total_blocks`)
  - `process_folder(folder)` → per-file stats
- `feed_pro_tool.py`: CLI front-end supporting interactive, single-file, inbox, and demo modes.
- Reuses factories (`create_news`, `create_private_ad`, `create_recipe`) from original `tool` package.

## Usage Examples
Process a single file:
```powershell
python tool_pro/feed_pro_tool.py --in tool_pro/sample_input.txt
```
Process all `.txt` files in inbox:
```powershell
python tool_pro/feed_pro_tool.py --inbox
```
Interactive mode (same as original but writing to pro feed):
```powershell
python tool_pro/feed_pro_tool.py --interactive
```
Append demo records:
```powershell
python tool_pro/feed_pro_tool.py --demo
```
Custom feed output path:
```powershell
python tool_pro/feed_pro_tool.py --feed myfeed.txt --in tool_pro/sample_input.txt
```

## Sample Stats Output
```
Processed sample_input.txt: {'success': 4, 'failed': 0, 'total_blocks': 4}
```

## Extending
Add a new TYPE by:
1. Implementing a factory in `tool/records.py` (or new module).
2. Updating parser mapping logic in `_record_to_string` of `FileFeedProcessor`.
3. Documenting required keys here.

## Error Handling
- Missing keys or bad date formats result in block failure; other blocks still processed.
- File not removed if zero records appended.

## Notes
- Feed output strings include their own separators from factories.
- Inbox processing deletes each file only after successful append(s).
