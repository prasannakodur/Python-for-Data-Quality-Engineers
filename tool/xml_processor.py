"""XML Record Processor for Feed Tools

Processes XML files containing one or many records and publishes them to feed files.

Features:
1. Supports multiple record formats (News, PrivateAd, Recipe)
2. Can process single record or array of records
3. Uses default inbox folder or user-provided file path
4. Automatically removes successfully processed files

XML Input Format:
-----------------
Single record:
<record>
    <type>news</type>
    <text>Breaking news story</text>
    <city>New York</city>
</record>

Multiple records:
<records>
    <record>
        <type>news</type>
        <text>First story</text>
        <city>Tokyo</city>
    </record>
    <record>
        <type>privatead</type>
        <text>Selling laptop</text>
        <expiration>2025-12-31</expiration>
    </record>
    <record>
        <type>recipe</type>
        <title>Pasta Carbonara</title>
        <ingredients>pasta, eggs, bacon, parmesan, pepper</ingredients>
    </record>
</records>

Record Types:
- news: requires <text> and <city>
- privatead (or ad): requires <text> and <expiration> (YYYY-MM-DD)
- recipe: requires <title> and <ingredients> (comma or semicolon separated)
"""
from __future__ import annotations
import xml.etree.ElementTree as ET
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Import record factories
try:
    from records import create_news, create_private_ad, create_recipe
except ImportError:
    # Handle case when imported from different directory
    sys.path.insert(0, str(Path(__file__).parent))
    from records import create_news, create_private_ad, create_recipe


class XMLRecordProcessor:
    """Processes XML files and publishes records to feed."""
    
    # Default inbox folder relative to tool directory
    DEFAULT_INBOX = "inbox"
    
    def __init__(self, feed_path: Optional[Path] = None, inbox_dir: Optional[Path] = None):
        """Initialize processor with optional custom paths.
        
        Args:
            feed_path: Optional custom path for feed file (defaults to tool/feed.txt)
            inbox_dir: Optional custom inbox directory (defaults to tool/inbox)
        """
        tool_dir = Path(__file__).parent
        self.feed_path = feed_path or (tool_dir / "feed.txt")
        self.inbox_dir = inbox_dir or (tool_dir / self.DEFAULT_INBOX)
        
        # Ensure directories exist
        self.feed_path.parent.mkdir(parents=True, exist_ok=True)
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
    
    def get_element_text(self, element: ET.Element, tag: str) -> Optional[str]:
        """Safely extract text from XML element.
        
        Returns:
            Element text or None if not found
        """
        child = element.find(tag)
        return child.text.strip() if child is not None and child.text else None
    
    def validate_record(self, record_dict: Dict[str, Any]) -> tuple[bool, str]:
        """Validate a single record has required fields.
        
        Returns:
            (is_valid, error_message)
        """
        if "type" not in record_dict:
            return False, "Record missing 'type' field"
        
        record_type = record_dict["type"].lower()
        
        if record_type == "news":
            if "text" not in record_dict or "city" not in record_dict:
                return False, "News record requires 'text' and 'city' fields"
        
        elif record_type in ("privatead", "ad"):
            if "text" not in record_dict or "expiration" not in record_dict:
                return False, "PrivateAd record requires 'text' and 'expiration' fields"
        
        elif record_type == "recipe":
            if "title" not in record_dict or "ingredients" not in record_dict:
                return False, "Recipe record requires 'title' and 'ingredients' fields"
        
        else:
            return False, f"Unknown record type: {record_type}"
        
        return True, ""
    
    def parse_record_element(self, record_elem: ET.Element) -> Optional[Dict[str, str]]:
        """Parse a single <record> element into a dictionary.
        
        Returns:
            Dictionary of record fields or None if parsing fails
        """
        record_dict = {}
        
        # Extract all child elements
        for child in record_elem:
            tag = child.tag.lower()
            text = child.text.strip() if child.text else ""
            if text:
                record_dict[tag] = text
        
        if not record_dict:
            return None
        
        return record_dict
    
    def process_record(self, record_dict: Dict[str, Any]) -> Optional[str]:
        """Process a single record dictionary and return formatted string.
        
        Returns:
            Formatted record string or None if processing fails
        """
        is_valid, error_msg = self.validate_record(record_dict)
        if not is_valid:
            print(f"  ❌ Validation error: {error_msg}")
            return None
        
        try:
            record_type = record_dict["type"].lower()
            
            if record_type == "news":
                return create_news(record_dict["text"], record_dict["city"])
            
            elif record_type in ("privatead", "ad"):
                return create_private_ad(record_dict["text"], record_dict["expiration"])
            
            elif record_type == "recipe":
                return create_recipe(record_dict["title"], record_dict["ingredients"])
            
        except Exception as e:
            print(f"  ❌ Processing error: {e}")
            return None
        
        return None
    
    def load_xml_file(self, file_path: Path) -> Optional[ET.Element]:
        """Load and parse XML file.
        
        Returns:
            Root element or None if parsing fails
        """
        try:
            tree = ET.parse(file_path)
            return tree.getroot()
        except ET.ParseError as e:
            print(f"❌ XML parsing error in {file_path.name}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error reading {file_path.name}: {e}")
            return None
    
    def process_xml_file(self, file_path: Path) -> Dict[str, int]:
        """Process a single XML file containing one or many records.
        
        Returns:
            Dictionary with processing statistics
        """
        print(f"\n📄 Processing: {file_path.name}")
        
        root = self.load_xml_file(file_path)
        if root is None:
            return {"success": 0, "failed": 1, "total": 0}
        
        # Handle both single <record> and multiple <records><record>...</record></records>
        records = []
        if root.tag.lower() == "record":
            # Single record at root
            records = [root]
        elif root.tag.lower() == "records":
            # Multiple records wrapped in <records>
            records = root.findall("record")
        else:
            # Try to find any <record> elements
            records = root.findall(".//record")
        
        if not records:
            print("  ❌ No <record> elements found in XML")
            return {"success": 0, "failed": 1, "total": 0}
        
        success_count = 0
        failed_count = 0
        appended_records = []
        
        for idx, record_elem in enumerate(records, 1):
            print(f"  Record {idx}/{len(records)}:", end=" ")
            
            record_dict = self.parse_record_element(record_elem)
            if record_dict is None:
                print("❌ Empty or invalid record")
                failed_count += 1
                continue
            
            formatted = self.process_record(record_dict)
            if formatted:
                appended_records.append(formatted)
                success_count += 1
                print(f"✅ {record_dict.get('type', 'unknown').upper()}")
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
        """Process all XML files in the inbox directory.
        
        Returns:
            Dictionary mapping filenames to their processing statistics
        """
        xml_files = list(self.inbox_dir.glob("*.xml"))
        
        if not xml_files:
            print(f"📭 No XML files found in {self.inbox_dir}")
            return {}
        
        print(f"📬 Found {len(xml_files)} XML file(s) in inbox")
        
        results = {}
        for xml_file in xml_files:
            stats = self.process_xml_file(xml_file)
            results[xml_file.name] = stats
        
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
        """Process a single XML file at the specified path.
        
        Args:
            file_path: Path to XML file to process
            
        Returns:
            Dictionary with processing statistics
        """
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return {"success": 0, "failed": 1, "total": 0}
        
        if not file_path.suffix.lower() == '.xml':
            print(f"❌ File must have .xml extension: {file_path}")
            return {"success": 0, "failed": 1, "total": 0}
        
        return self.process_xml_file(file_path)


def main():
    """Main entry point for XML processor."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Process XML files containing feed records"
    )
    parser.add_argument(
        '--file',
        type=Path,
        help="Process a specific XML file"
    )
    parser.add_argument(
        '--inbox',
        type=Path,
        help="Custom inbox directory (default: tool/inbox)"
    )
    parser.add_argument(
        '--feed',
        type=Path,
        help="Custom feed file path (default: tool/feed.txt)"
    )
    
    args = parser.parse_args()
    
    processor = XMLRecordProcessor(
        feed_path=args.feed,
        inbox_dir=args.inbox
    )
    
    if args.file:
        processor.process_file(args.file)
    else:
        processor.process_inbox()


if __name__ == "__main__":
    main()
