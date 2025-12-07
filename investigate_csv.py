#!/usr/bin/env python3
"""
Investigate the aidata.csv file to understand the parsing discrepancy
"""

import pandas as pd
import csv
import os

def investigate_csv():
    file_path = 'data/raw/aidata.csv'
    
    print("=" * 60)
    print("CSV FILE INVESTIGATION")
    print("=" * 60)
    
    # File size
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
    
    # Count lines manually
    with open(file_path, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    print(f"Total lines (manual count): {line_count:,}")
    print(f"Expected records (excluding header): {line_count - 1:,}")
    
    # Try pandas with different settings
    print("\nPandas reading attempts:")
    
    try:
        df1 = pd.read_csv(file_path)
        print(f"  Standard pandas read: {len(df1):,} records")
        
        df2 = pd.read_csv(file_path, low_memory=False)
        print(f"  Low memory=False: {len(df2):,} records")
        
        df3 = pd.read_csv(file_path, engine='python')
        print(f"  Python engine: {len(df3):,} records")
        
        # Check if there are any parsing errors
        df4 = pd.read_csv(file_path, error_bad_lines=False, warn_bad_lines=True)
        print(f"  With error handling: {len(df4):,} records")
        
    except Exception as e:
        print(f"  Error reading with pandas: {e}")
    
    # Try CSV reader
    print("\nCSV module reading:")
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
            print(f"  CSV reader: {len(rows):,} rows total")
            print(f"  CSV reader records: {len(rows)-1:,} (excluding header)")
    except Exception as e:
        print(f"  Error with CSV reader: {e}")
    
    # Check for potential issues
    print("\nChecking for potential parsing issues:")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Sample some lines to check structure
    print(f"  Header: {lines[0].strip()}")
    print(f"  Line 2: {lines[1][:100]}...")
    print(f"  Line 100: {lines[100][:100]}...")
    print(f"  Line 1000: {lines[1000][:100]}...")
    
    # Check if pandas is stopping at a specific line
    try:
        df_chunk = pd.read_csv(file_path, nrows=50000)
        print(f"\nReading first 50k rows: {len(df_chunk):,} records")
        
        df_chunk2 = pd.read_csv(file_path, skiprows=50000, nrows=50000)
        print(f"Reading rows 50k-100k: {len(df_chunk2):,} records")
        
    except Exception as e:
        print(f"Error with chunked reading: {e}")

if __name__ == "__main__":
    investigate_csv()