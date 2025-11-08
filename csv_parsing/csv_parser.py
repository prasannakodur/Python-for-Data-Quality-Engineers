"""CSV Parser for Feed Files

Processes text content from tool/feed.txt and tool_pro/feed_pro.txt to generate:
1. word-count.csv - all words preprocessed to lowercase with counts
2. letter-stats.csv - letter statistics including count_all, count_uppercase, percentage

CSVs are regenerated each time new records are added to feed files.
"""
from __future__ import annotations
import csv
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

class FeedCSVParser:
    """Parses feed files and generates CSV statistics."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.csv_dir = self.workspace_root / "csv_parsing"
        self.feed_files = [
            self.workspace_root / "tool" / "feed.txt",
            self.workspace_root / "tool_pro" / "feed_pro.txt"
        ]
        
    def extract_text_content(self) -> str:
        """Extract all text content from feed files, excluding structural elements."""
        all_text = ""
        
        for feed_file in self.feed_files:
            if not feed_file.exists():
                continue
                
            with open(feed_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove separator lines (dashes)
            content = re.sub(r'^-+$', '', content, flags=re.MULTILINE)
            
            # Extract meaningful text content, skip metadata-like lines
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Skip structural/metadata lines
                if (line.startswith('Published:') or 
                    line.startswith('City:') or
                    line.startswith('Expires:') or
                    line.startswith('Avg name length:') or
                    line.startswith('Ingredients (')):
                    continue
                
                # Remove prefixes like "NEWS:", "PRIVATE AD:", "RECIPE:"
                line = re.sub(r'^(NEWS|PRIVATE AD|RECIPE):\s*', '', line)
                
                if line:
                    all_text += line + " "
        
        return all_text.strip()
    
    def generate_word_count_csv(self, text: str) -> None:
        """Generate word-count.csv with lowercase words and their counts."""
        # Extract words (letters only, convert to lowercase)
        words = re.findall(r'[a-zA-Z]+', text.lower())
        word_counts = Counter(words)
        
        # Sort by word alphabetically
        sorted_words = sorted(word_counts.items())
        
        csv_path = self.csv_dir / "word-count.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['word', 'count'])  # Header
            writer.writerows(sorted_words)
    
    def generate_letter_stats_csv(self, text: str) -> None:
        """Generate letter-stats.csv with letter statistics (excluding spaces)."""
        # Extract only letters (no spaces or punctuation)
        letters_only = re.sub(r'[^a-zA-Z]', '', text)
        
        if not letters_only:
            # Create empty CSV with headers if no letters found
            csv_path = self.csv_dir / "letter-stats.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['letter', 'count_all', 'count_uppercase', 'percentage'])
            return
        
        # Count all letters and uppercase letters
        letter_counts = Counter(letters_only.lower())
        uppercase_counts = Counter(c.lower() for c in letters_only if c.isupper())
        total_letters = len(letters_only)
        
        # Generate statistics for each letter
        stats = []
        for letter in sorted(letter_counts.keys()):
            count_all = letter_counts[letter]
            count_uppercase = uppercase_counts.get(letter, 0)
            percentage = (count_all / total_letters) * 100
            
            stats.append([
                letter, 
                count_all, 
                count_uppercase, 
                f"{percentage:.2f}"
            ])
        
        csv_path = self.csv_dir / "letter-stats.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['letter', 'count_all', 'count_uppercase', 'percentage'])
            writer.writerows(stats)
    
    def generate_all_csvs(self) -> None:
        """Generate both CSV files from current feed content."""
        # Ensure CSV directory exists
        self.csv_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract text content from all feed files
        text_content = self.extract_text_content()
        
        # Generate both CSV files
        self.generate_word_count_csv(text_content)
        self.generate_letter_stats_csv(text_content)
        
        print(f"Generated CSV files in {self.csv_dir}:")
        print(f"  - word-count.csv")
        print(f"  - letter-stats.csv")
    
    def get_feed_modification_times(self) -> Dict[Path, float]:
        """Get modification times for all feed files."""
        times = {}
        for feed_file in self.feed_files:
            if feed_file.exists():
                times[feed_file] = feed_file.stat().st_mtime
            else:
                times[feed_file] = 0
        return times

def main():
    """Main function to generate CSV files."""
    workspace_root = Path(__file__).parent.parent
    parser = FeedCSVParser(workspace_root)
    parser.generate_all_csvs()

if __name__ == "__main__":
    main()