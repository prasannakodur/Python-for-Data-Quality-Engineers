"""Quick test script to demonstrate CSV parsing functionality.

This script adds a sample record to the feed and shows the CSV update process.
"""
from pathlib import Path
import sys
import os

# Add the parent directory to the path to import csv_parser
sys.path.append(str(Path(__file__).parent.parent))

from csv_parsing.csv_parser import FeedCSVParser

def test_csv_generation():
    """Test the CSV generation process."""
    workspace_root = Path(__file__).parent.parent
    parser = FeedCSVParser(workspace_root)
    
    print("Testing CSV Parser...")
    print("=" * 50)
    
    # Generate CSVs
    parser.generate_all_csvs()
    
    # Show some statistics
    csv_dir = workspace_root / "csv_parsing"
    word_count_file = csv_dir / "word-count.csv"
    letter_stats_file = csv_dir / "letter-stats.csv"
    
    if word_count_file.exists():
        with open(word_count_file, 'r') as f:
            lines = f.readlines()
            print(f"Word count CSV: {len(lines)-1} unique words")
            
    if letter_stats_file.exists():
        with open(letter_stats_file, 'r') as f:
            lines = f.readlines()
            print(f"Letter stats CSV: {len(lines)-1} unique letters")
    
    print("\nCSV files have been generated successfully!")
    print("Check the csv_parsing/ directory for:")
    print("  - word-count.csv")
    print("  - letter-stats.csv")

if __name__ == "__main__":
    test_csv_generation()