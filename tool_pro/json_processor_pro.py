"""JSON Record Processor for Feed Pro Tool

Enhanced JSON processor for tool_pro module with additional features.
Processes JSON files containing one or many records and publishes them to feed_pro.txt

Features:
1. Supports multiple record formats (News, PrivateAd, Recipe)
2. Can process single record or array of records
3. Uses default inbox folder or user-provided file path
4. Automatically removes successfully processed files
5. Integrated with existing file_processor for unified processing

JSON Input Format:
-----------------
Single record:
{
    "type": "news",
    "text": "Breaking news story",
    "city": "New York"
}

Multiple records:
[
    {
        "type": "news",
        "text": "First story",
        "city": "Tokyo"
    },
    {
        "type": "privatead",
        "text": "Selling laptop",
        "expiration": "2025-12-31"
    },
    {
        "type": "recipe",
        "title": "Pasta Carbonara",
        "ingredients": "pasta, eggs, bacon, parmesan, pepper"
    }
]

Record Types:
- news: requires "text" and "city"
- privatead (or ad): requires "text" and "expiration" (YYYY-MM-DD)
- recipe: requires "title" and "ingredients" (comma or semicolon separated)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tool.records import create_news, create_private_ad, create_recipe


class JSONRecordProcessorPro:
    """Enhanced JSON processor for tool_pro module."""
    
    # Default inbox folder (existing inbox directory)
    DEFAULT_INBOX = "inbox"
    
    def __init__(self, feed_path: Optional[Path] = None, inbox_dir: Optional[Path] = None):
        """Initialize processor with optional custom paths.
        
        Args:
            feed_path: Optional custom path for feed file (defaults to tool_pro/feed_pro.txt)
            inbox_dir: Optional custom inbox directory (defaults to tool_pro/inbox)
        """
        tool_pro_dir = Path(__file__).parent
        self.feed_path = feed_path or (tool_pro_dir / "feed_pro.txt")
        self.inbox_dir = inbox_dir or (tool_pro_dir / self.DEFAULT_INBOX)
        
        # Ensure directories exist
        self.feed_path.parent.mkdir(parents=True, exist_ok=True)
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_record(self, record: Dict[str, Any]) -> tuple[bool, str]:
        """Validate a single record has required fields.
        
        Returns:
            (is_valid, error_message)
        """
        if not isinstance(record, dict):
            return False, "Record must be a dictionary"
        
        if "type" not in record:
            return False, "Record missing 'type' field"
        
        record_type = record["type"].lower()
        
        if record_type == "news":
            if "text" not in record or "city" not in record:
                return False, "News record requires 'text' and 'city' fields"
        
        elif record_type in ("privatead", "ad"):
            if "text" not in record or "expiration" not in record:
                return False, "PrivateAd record requires 'text' and 'expiration' fields"
        
        elif record_type == "recipe":
            if "title" not in record or "ingredients" not in record:
                return False, "Recipe record requires 'title' and 'ingredients' fields"
        
        else:
            return False, f"Unknown record type: {record_type}"
        
        return True, ""
    
    def process_record(self, record: Dict[str, Any]) -> Optional[str]:
        """Process a single record and return formatted string.
        
        Returns:
            Formatted record string or None if processing fails
        """
        is_valid, error_msg = self.validate_record(record)
        if not is_valid:
            print(f"  ❌ Validation error: {error_msg}")
            return None
        
        try:
            record_type = record["type"].lower()
            
            if record_type == "news":
                return create_news(record["text"], record["city"])
            
            elif record_type in ("privatead", "ad"):
                return create_private_ad(record["text"], record["expiration"])
            
            elif record_type == "recipe":
                return create_recipe(record["title"], record["ingredients"])
            
        except Exception as e:
            print(f"  ❌ Processing error: {e}")
            return None
        
        return None
    
    def load_json_file(self, file_path: Path) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """Load and parse JSON file.
        
        Returns:
            Parsed JSON (dict or list) or None if parsing fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error in {file_path.name}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error reading {file_path.name}: {e}")
            return None
    
    def process_json_file(self, file_path: Path) -> Dict[str, int]:
        """Process a single JSON file containing one or many records.
        
        Returns:
            Dictionary with processing statistics
        """
        print(f"\n📄 Processing: {file_path.name}")
        
        data = self.load_json_file(file_path)
        if data is None:
            return {"success": 0, "failed": 1, "total": 0}
        
        # Normalize to list
        records = data if isinstance(data, list) else [data]
        
        success_count = 0
        failed_count = 0
        appended_records = []
        
        for idx, record in enumerate(records, 1):
            print(f"  Record {idx}/{len(records)}:", end=" ")
            
            formatted = self.process_record(record)
            if formatted:
                appended_records.append(formatted)
                success_count += 1
                print(f"✅ {record.get('type', 'unknown').upper()}")
            else:
                failed_count += 1
        
        # Append all successful records to feed file
        if appended_records:
            with open(self.feed_path, 'a', encoding='utf-8') as f:
                for rec in appended_records:
                    f.write(rec)
        
        # Delete file if at least one record was successfully processed
        if success_count > 0:
            try:
                file_path.unlink()
                print(f"  🗑️  File deleted after successful processing")
            except Exception as e:
                print(f"  ⚠️  Could not delete file: {e}")
        
        return {
            "success": success_count,
            "failed": failed_count,
            "total": len(records)
        }
    
    def process_inbox(self) -> Dict[str, Dict[str, int]]:
        """Process all JSON files in the inbox directory.
        
        Returns:
            Dictionary mapping filenames to their processing statistics
        """
        json_files = list(self.inbox_dir.glob("*.json"))
        
        if not json_files:
            print(f"📭 No JSON files found in {self.inbox_dir}")
            return {}
        
        print(f"📬 Found {len(json_files)} JSON file(s) in inbox")
        
        results = {}
        for json_file in json_files:
            stats = self.process_json_file(json_file)
            results[json_file.name] = stats
        
        # Print summary
        print(f"\n{'='*50}")
        print("📊 Processing Summary:")
        total_success = sum(r["success"] for r in results.values())
        total_failed = sum(r["failed"] for r in results.values())
        total_records = sum(r["total"] for r in results.values())
        print(f"  Files processed: {len(results)}")
        print(f"  Total records: {total_records}")
        print(f"  Successful: {total_success}")
        print(f"  Failed: {total_failed}")
        
        return results
    
    def process_file(self, file_path: Path) -> Dict[str, int]:
        """Process a single JSON file at the specified path.
        
        Args:
            file_path: Path to JSON file to process
            
        Returns:
            Dictionary with processing statistics
        """
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return {"success": 0, "failed": 1, "total": 0}
        
        if not file_path.suffix.lower() == '.json':
            print(f"❌ File must have .json extension: {file_path}")
            return {"success": 0, "failed": 1, "total": 0}
        
        return self.process_json_file(file_path)
    
    def process_all_formats(self) -> Dict[str, Any]:
        """Process both JSON and TXT files in inbox.
        
        Returns:
            Combined statistics for all file types
        """
        from file_processor import FileFeedProcessor
        
        # Process JSON files
        json_stats = self.process_inbox()
        
        # Process TXT files using existing file processor
        txt_processor = FileFeedProcessor(self.feed_path)
        txt_stats = txt_processor.process_folder(self.inbox_dir)
        
        return {
            "json": json_stats,
            "txt": txt_stats
        }


def main():
    """Main entry point for JSON processor pro."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Process JSON files containing feed records (Pro version)"
    )
    parser.add_argument(
        '--file',
        type=Path,
        help="Process a specific JSON file"
    )
    parser.add_argument(
        '--inbox',
        type=Path,
        help="Custom inbox directory (default: tool_pro/inbox)"
    )
    parser.add_argument(
        '--feed',
        type=Path,
        help="Custom feed file path (default: tool_pro/feed_pro.txt)"
    )
    parser.add_argument(
        '--all-formats',
        action='store_true',
        help="Process both JSON and TXT files"
    )
    
    args = parser.parse_args()
    
    processor = JSONRecordProcessorPro(
        feed_path=args.feed,
        inbox_dir=args.inbox
    )
    
    if args.file:
        processor.process_file(args.file)
    elif args.all_formats:
        processor.process_all_formats()
    else:
        processor.process_inbox()


if __name__ == "__main__":
    main()
