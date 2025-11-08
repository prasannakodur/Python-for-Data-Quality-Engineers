"""Feed Monitor and CSV Generator

Monitors feed files for changes and automatically regenerates CSV files when new records are added.
Can be run in watch mode or as a one-time generator.

Usage:
  python csv_parsing/feed_monitor.py                 # Generate CSVs once
  python csv_parsing/feed_monitor.py --watch         # Monitor for changes
  python csv_parsing/feed_monitor.py --watch --interval 5  # Custom check interval
"""
from __future__ import annotations
import argparse
import sys
import time
from pathlib import Path
from csv_parser import FeedCSVParser

class FeedMonitor:
    """Monitors feed files and regenerates CSVs when changes occur."""
    
    def __init__(self, workspace_root: Path, check_interval: float = 2.0):
        self.parser = FeedCSVParser(workspace_root)
        self.check_interval = check_interval
        self.last_mod_times = {}
        
    def check_for_changes(self) -> bool:
        """Check if any feed files have been modified since last check."""
        current_times = self.parser.get_feed_modification_times()
        
        if not self.last_mod_times:
            # First run - consider all files as changed
            self.last_mod_times = current_times
            return True
            
        # Check for any changes
        for feed_file, current_time in current_times.items():
            last_time = self.last_mod_times.get(feed_file, 0)
            if current_time > last_time:
                print(f"Change detected in {feed_file.name}")
                self.last_mod_times = current_times
                return True
                
        return False
    
    def run_once(self) -> None:
        """Generate CSV files once."""
        print("Generating CSV files from current feed content...")
        self.parser.generate_all_csvs()
        
    def watch_mode(self) -> None:
        """Run in watch mode, monitoring for file changes."""
        print(f"Monitoring feed files for changes (checking every {self.check_interval}s)...")
        print("Press Ctrl+C to stop monitoring.")
        
        try:
            # Initial generation
            if self.check_for_changes():
                self.parser.generate_all_csvs()
                
            while True:
                time.sleep(self.check_interval)
                if self.check_for_changes():
                    print("Regenerating CSV files...")
                    self.parser.generate_all_csvs()
                    
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")

def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Monitor feed files and generate CSV statistics"
    )
    parser.add_argument(
        '--watch', 
        action='store_true',
        help="Run in watch mode to monitor for file changes"
    )
    parser.add_argument(
        '--interval', 
        type=float, 
        default=2.0,
        help="Check interval in seconds for watch mode (default: 2.0)"
    )
    
    args = parser.parse_args()
    
    # Get workspace root (parent directory of csv_parsing)
    workspace_root = Path(__file__).parent.parent
    
    # Create monitor
    monitor = FeedMonitor(workspace_root, args.interval)
    
    if args.watch:
        monitor.watch_mode()
    else:
        monitor.run_once()

if __name__ == "__main__":
    main()