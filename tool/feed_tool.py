"""Interactive feed tool for user-generated records.

Usage:
  python tool/feed_tool.py              # interactive mode
  python tool/feed_tool.py --demo       # add sample records
  python tool/feed_tool.py --file path  # specify alternative feed file

Records are appended to a feed file (default: tool/feed.txt). Each record ends with a separator line.
Functional approach: separate pure creation (records.py) from side-effect append.
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Callable, List
from records import TYPE_MAP

DEFAULT_FEED = Path(__file__).with_name("feed.txt")

# ---------------- Core Functions ---------------- #

def append_record(feed_path: Path, record_str: str) -> None:
    feed_path.parent.mkdir(parents=True, exist_ok=True)
    with feed_path.open("a", encoding="utf-8") as f:
        f.write(record_str)

def interactive(feed_path: Path) -> None:
    print("User Generated News Feed Tool\n")
    while True:
        print("Select record type:")
        for key, (label, _, _) in TYPE_MAP.items():
            print(f"  {key}. {label}")
        print("  q. Quit")
        choice = input("Enter choice: ").strip()
        if choice.lower() == 'q':
            print("Exiting.")
            break
        if choice not in TYPE_MAP:
            print("Invalid option. Try again.\n")
            continue
        label, factory, prompts = TYPE_MAP[choice]
        inputs: List[str] = []
        for p in prompts:
            val = input(f"{p}: ").rstrip('\n')
            inputs.append(val)
        try:
            record_str = factory(*inputs)
        except Exception as e:
            print(f"Error creating {label}: {e}\n")
            continue
        append_record(feed_path, record_str)
        print(f"{label} published.\n")

def demo(feed_path: Path) -> None:
    from records import create_news, create_private_ad, create_recipe
    sample = [
        create_news("Big launch event announced", "New York"),
        create_private_ad("Selling vintage guitar", "2025-12-31"),
        create_recipe("Chocolate Cake", "flour, sugar, cocoa powder, eggs, butter, vanilla, salt"),
    ]
    for rec in sample:
        append_record(feed_path, rec)
    print(f"Demo records appended to {feed_path}.")

# ---------------- Entrypoint ---------------- #

def parse_args(argv: List[str]):
    feed = DEFAULT_FEED
    demo_flag = False
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == '--demo':
            demo_flag = True
        elif arg == '--file' and i + 1 < len(argv):
            feed = Path(argv[i+1])
            i += 1
        i += 1
    return feed, demo_flag

def main(argv: List[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    feed_path, demo_flag = parse_args(argv)
    if demo_flag:
        demo(feed_path)
    else:
        interactive(feed_path)

if __name__ == '__main__':
    main()
