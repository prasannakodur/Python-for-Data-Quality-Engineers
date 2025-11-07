"""Pro feed tool: extends interactive feed with file-based ingestion.

Usage:
  python tool_pro/feed_pro_tool.py --interactive            # interactive entry
  python tool_pro/feed_pro_tool.py --in sample_input.txt    # process single file
  python tool_pro/feed_pro_tool.py --inbox                  # process all .txt files in inbox folder
  python tool_pro/feed_pro_tool.py --feed alt_feed.txt      # custom feed output path
  python tool_pro/feed_pro_tool.py --demo                   # append sample records (manual mode)

On successful processing of an input file, that file is deleted.
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import List

# Reuse original interactive tool's factories
try:
    from tool.records import TYPE_MAP  # for interactive mode
    from tool.records import create_news, create_private_ad, create_recipe
except ImportError:
    TYPE_MAP = {}

from file_processor import FileFeedProcessor

DEFAULT_FEED = Path(__file__).with_name("feed_pro.txt")
DEFAULT_INBOX = Path(__file__).with_name("inbox")

# ---------------- Arg Parsing ---------------- #

def parse_args(argv: List[str]):
    args = {
        "interactive": False,
        "in_file": None,
        "inbox": False,
        "feed": DEFAULT_FEED,
        "demo": False,
    }
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--interactive":
            args["interactive"] = True
        elif a == "--inbox":
            args["inbox"] = True
        elif a == "--in" and i + 1 < len(argv):
            args["in_file"] = Path(argv[i+1])
            i += 1
        elif a == "--feed" and i + 1 < len(argv):
            args["feed"] = Path(argv[i+1])
            i += 1
        elif a == "--demo":
            args["demo"] = True
        i += 1
    return args

# ---------------- Interactive Mode ---------------- #

def interactive(feed: Path):
    if not TYPE_MAP:
        print("Interactive mode unavailable: TYPE_MAP missing.")
        return
    from tool.feed_tool import append_record  # reuse existing function
    print("Pro Feed Interactive Mode\n")
    while True:
        print("Select record type:")
        for k, (label, _, prompts) in TYPE_MAP.items():
            print(f"  {k}. {label}")
        print("  q. Quit")
        choice = input("Enter choice: ").strip()
        if choice.lower() == 'q':
            break
        if choice not in TYPE_MAP:
            print("Invalid choice.\n")
            continue
        label, factory, prompts = TYPE_MAP[choice]
        inputs = [input(f"{p}: ").strip() for p in prompts]
        try:
            record_str = factory(*inputs)
        except Exception as e:
            print(f"Error: {e}\n")
            continue
        append_record(feed, record_str)
        print(f"{label} appended.\n")

# ---------------- Demo Records ---------------- #

def demo(feed: Path):
    recs = [
        create_news("Conference scheduled", "Berlin"),
        create_private_ad("Selling mountain bike", "2026-01-10"),
        create_recipe("Avocado Toast", "bread, avocado, salt, pepper, lemon"),
    ]
    feed.parent.mkdir(parents=True, exist_ok=True)
    with feed.open("a", encoding="utf-8") as f:
        for r in recs:
            f.write(r)
    print(f"Demo records appended to {feed}")

# ---------------- Main Logic ---------------- #

def main(argv: List[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    processor = FileFeedProcessor(args["feed"])

    if args["demo"]:
        demo(args["feed"])

    if args["interactive"]:
        interactive(args["feed"])

    if args["in_file"]:
        file_path = args["in_file"]
        if not file_path.exists():
            print(f"Input file not found: {file_path}")
        else:
            stats = processor.process_file(file_path)
            print(f"Processed {file_path.name}: {stats}")

    if args["inbox"]:
        inbox = DEFAULT_INBOX
        inbox.mkdir(parents=True, exist_ok=True)
        results = processor.process_folder(inbox)
        if not results:
            print("No .txt files found in inbox.")
        else:
            for fname, stat in results.items():
                print(f"Inbox processed {fname}: {stat}")

    if not any([args["interactive"], args["in_file"], args["inbox"], args["demo"]]):
        print("No action specified. Use --interactive | --in <file> | --inbox | --demo")

if __name__ == "__main__":
    main()
