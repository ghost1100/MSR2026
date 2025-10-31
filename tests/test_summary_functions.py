#!/usr/bin/env python3
"""
Quick test of summary notebook functions
"""

import sys
sys.path.append('src')
from data_loader import load_aidev
from analysis import analyze_test_contributions, calculate_test_code_ratios, get_research_summary

print("Testing Summary Notebook Functions")
print("=" * 50)

# Load small test sample
print("Loading test data...")
df = load_aidev(sample_size=1000)
print(f"PASS: Loaded {len(df)} rows")

# Test analysis functions
print("\nTesting test contributions analysis...")
df_analyzed, test_stats = analyze_test_contributions(df)
print(f"PASS: Test analysis complete: {test_stats['Test_PRs'].sum()} test PRs found")

# Test ratios calculation
print("\nTesting test-to-code ratios calculation...")
ratios = calculate_test_code_ratios(df_analyzed)
print(f"PASS: Ratios calculated: {ratios['overall']['test_ratio']:.3f} overall test ratio")

# Test research summary
print("\nTesting research summary...")
summary = get_research_summary(df_analyzed)
print(f"PASS: Summary generated: {summary['unique_agents']} agents, {summary['dataset_size']} PRs")

print("\nAll summary functions working correctly!")
print("The summary notebook should now execute without errors.")