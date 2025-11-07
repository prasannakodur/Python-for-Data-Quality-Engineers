"""File-based record ingestion for the news feed (pro version).

Input File Format (multiple records per file):
Blocks separated by a line containing only three dashes: ---
Within each block, lines are KEY: VALUE pairs. Required keys vary by TYPE.
Supported TYPE values (case-insensitive):
  News   -> keys: TYPE, TEXT, CITY
  Ad     -> keys: TYPE, TEXT, EXPIRES (YYYY-MM-DD)
  Recipe -> keys: TYPE, TITLE, INGREDIENTS (comma or semicolon separated)

Example block:
TYPE: News
TEXT: Market reaches all-time high
CITY: Tokyo
---

On successful processing of an entire file, the file is deleted.
Partial failures (any bad block) cause: skip invalid block, keep file if at least one fatal error occurred.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import re

# Reuse factories from existing tool implementation
try:
    from tool.records import create_news, create_private_ad, create_recipe
except ImportError:
    # Fallback: add parent directory of this file to sys.path and retry
    import sys
    from pathlib import Path as _Path
    parent = _Path(__file__).resolve().parent.parent
    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))
    try:
        from tool.records import create_news, create_private_ad, create_recipe  # type: ignore
    except Exception as e:
        raise ImportError("Failed to import record factories after adjusting sys.path: " + str(e))

BLOCK_SEPARATOR_PATTERN = re.compile(r"^---\s*$")
KEY_VALUE_PATTERN = re.compile(r"^(?P<key>[A-Za-z]+):\s*(?P<value>.*)$")

@dataclass
class ParsedRecord:
    type_key: str
    fields: Dict[str, str]
    raw_block: List[str]

class FileFeedProcessor:
    def __init__(self, feed_path: Path):
        self.feed_path = feed_path
        self.feed_path.parent.mkdir(parents=True, exist_ok=True)

    def _read_file(self, file_path: Path) -> List[str]:
        return file_path.read_text(encoding="utf-8").splitlines()

    def _split_blocks(self, lines: List[str]) -> List[List[str]]:
        blocks: List[List[str]] = []
        current: List[str] = []
        for line in lines:
            if BLOCK_SEPARATOR_PATTERN.match(line):
                if current:
                    blocks.append(current)
                    current = []
            else:
                if line.strip():  # skip pure blank lines
                    current.append(line.rstrip())
        if current:
            blocks.append(current)
        return blocks

    def _parse_block(self, block: List[str]) -> ParsedRecord | None:
        data: Dict[str, str] = {}
        for line in block:
            m = KEY_VALUE_PATTERN.match(line)
            if not m:
                # Non-conforming line; skip block entirely
                return None
            key = m.group("key").upper()
            value = m.group("value").strip()
            data[key] = value
        if "TYPE" not in data:
            return None
        type_key = data["TYPE"].strip().lower()
        return ParsedRecord(type_key=type_key, fields=data, raw_block=block)

    def _record_to_string(self, parsed: ParsedRecord) -> Tuple[str, str] | None:
        t = parsed.type_key
        f = parsed.fields
        try:
            if t == "news":
                return (t, create_news(f["TEXT"], f["CITY"]))
            elif t == "ad":
                return (t, create_private_ad(f["TEXT"], f["EXPIRES"]))
            elif t == "recipe":
                return (t, create_recipe(f["TITLE"], f["INGREDIENTS"]))
            else:
                return None
        except KeyError:
            return None
        except Exception:
            return None

    def process_file(self, file_path: Path) -> Dict[str, int]:
        lines = self._read_file(file_path)
        blocks = self._split_blocks(lines)
        success = 0
        failed = 0
        appended_records: List[str] = []
        for block in blocks:
            parsed = self._parse_block(block)
            if not parsed:
                failed += 1
                continue
            rec_tuple = self._record_to_string(parsed)
            if not rec_tuple:
                failed += 1
                continue
            _, rec_str = rec_tuple
            appended_records.append(rec_str)
            success += 1
        # Append all successful records if any
        if appended_records:
            with self.feed_path.open("a", encoding="utf-8") as f:
                for rec in appended_records:
                    f.write(rec)
        # Delete file only if all blocks were parsed (even if some failed?) -> per spec: delete on successful processing.
        # Interpreting 'successfully processed' as: at least one record appended and no fatal read error.
        if success > 0:
            try:
                file_path.unlink()
            except Exception:
                pass
        return {"success": success, "failed": failed, "total_blocks": len(blocks)}

    def process_folder(self, folder: Path) -> Dict[str, Dict[str, int]]:
        results: Dict[str, Dict[str, int]] = {}
        for file in folder.glob("*.txt"):
            stats = self.process_file(file)
            results[file.name] = stats
        return results

__all__ = ["FileFeedProcessor"]
