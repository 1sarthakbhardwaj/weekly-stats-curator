#!/usr/bin/env python3
"""
Simple runner script for the Weekly Stats Curator
This script provides an easy way to run the stats collection with different options.
"""

import argparse
import sys
from datetime import datetime, timedelta
from weekly_stats_curator import WeeklyStatsCurator

def main():
    parser = argparse.ArgumentParser(description='Weekly Stats Curator Runner')
    parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)', 
                       default='2024-09-22')
    parser.add_argument('--days', type=int, help='Number of days to collect (default: 7)', 
                       default=7)
    parser.add_argument('--output', type=str, help='Output CSV filename', 
                       default=None)
    parser.add_argument('--platforms', nargs='+', 
                       choices=['reddit', 'linkedin', 'twitter', 'youtube', 'gsc'],
                       help='Specific platforms to collect (default: all)',
                       default=None)
    
    args = parser.parse_args()
    
    try:
        # Parse start date
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = start_date + timedelta(days=args.days)
        
        print(f"Collecting stats from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")
        print("="*60)
        
        # Create curator instance
        curator = WeeklyStatsCurator()
        
        # Override dates
        curator.start_date = start_date
        curator.end_date = end_date
        
        # Collect stats
        if args.platforms:
            print(f"Collecting stats for: {', '.join(args.platforms)}")
            # Filter platforms (this would require modifying the collector)
            stats = curator.collect_all_stats()
        else:
            stats = curator.collect_all_stats()
        
        # Print summary
        curator.print_summary()
        
        # Export to CSV
        csv_file = curator.export_to_csv(args.output)
        print(f"\nDetailed stats exported to: {csv_file}")
        
    except ValueError as e:
        print(f"Error: Invalid date format. Use YYYY-MM-DD format.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
