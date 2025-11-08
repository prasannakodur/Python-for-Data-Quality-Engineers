# CSV Parsing Module

Analyzes text content from feed files (`tool/feed.txt` and `tool_pro/feed_pro.txt`) and generates CSV statistics.

## Generated CSV Files

### 1. word-count.csv
- Contains all words from feed files preprocessed to lowercase
- Columns: `word`, `count`
- Sorted alphabetically by word

### 2. letter-stats.csv  
- Contains letter statistics (space characters excluded)
- Columns: `letter`, `count_all`, `count_uppercase`, `percentage`
- Shows frequency analysis of letters in the text content

## Usage

### One-time Generation
Generate CSV files from current feed content:
```powershell
python csv_parsing/csv_parser.py
```

### Monitor Mode
Automatically regenerate CSVs when feed files are updated:
```powershell
python csv_parsing/feed_monitor.py --watch
```

### Custom Check Interval
Monitor with custom interval (default: 2 seconds):
```powershell
python csv_parsing/feed_monitor.py --watch --interval 5
```

## Features

- **Automatic Processing**: Extracts meaningful text content, excluding metadata lines
- **Clean Text Extraction**: Removes structural elements like separators, timestamps, and prefixes  
- **Real-time Updates**: Monitor mode detects file changes and regenerates CSVs automatically
- **Comprehensive Analysis**: Processes content from both `tool` and `tool_pro` feed files
- **Robust Parsing**: Handles various record types (NEWS, PRIVATE AD, RECIPE) uniformly

## File Structure
```
csv_parsing/
├── csv_parser.py      # Core CSV generation logic
├── feed_monitor.py    # File monitoring and CLI interface  
├── README.md          # This documentation
├── word-count.csv     # Generated word statistics
└── letter-stats.csv   # Generated letter statistics
```

## Example Output

**word-count.csv:**
```csv
word,count
and,3
big,1
event,1
launch,1
...
```

**letter-stats.csv:**
```csv
letter,count_all,count_uppercase,percentage
a,15,2,8.45
b,8,1,4.51
c,12,0,6.77
...
```

## Integration

The CSV files are automatically regenerated each time new records are added to the feed files, ensuring statistics are always up-to-date with the latest content.