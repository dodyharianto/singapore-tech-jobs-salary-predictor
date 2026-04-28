"""
Script for scraping Google Jobs, scheduled to run weekly
"""
import sys
import os
from datetime import datetime
from scrape import scrape_google_jobs, save_raw_data

# Parent directories to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'Starting Google Jobs Scraping at {current_datetime}')
    
    df = scrape_google_jobs(query='tech jobs', page_limit=5)
    
    if df is not None and len(df) > 0:
        print('Saving raw data.')
        output_path = save_raw_data(df, source='google')
        
        print(f'Rows obtained: {len(df)}')
        print(f'Saved to: {output_path}')
        exit_code = 0
    else:
        print(f'Something went wrong when scraping Google Jobs')
        exit_code = 1
    return exit_code

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
