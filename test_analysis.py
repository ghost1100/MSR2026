# Test script for core analysis functions
# Validates analysis module functionality with sample data
import sys
sys.path.append('src')
import pandas as pd
from analysis import analyze_test_contributions, get_research_summary

print('Testing Analysis Functions...')

# Load small sample for testing without memory issues
df = pd.read_csv('data/raw/aidata.csv', nrows=100, low_memory=False)
print(f'Loaded sample: {len(df)} rows')

# Test core analysis function
df_analyzed, test_stats = analyze_test_contributions(df)
print(f'Analysis complete: {len(test_stats)} agents analyzed')

# Test summary generation
summary = get_research_summary(df_analyzed)
print(f'Summary generated: {summary["dataset_size"]} rows, {summary["unique_agents"]} agents')
print('Core analysis functions working!')