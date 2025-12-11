#!/usr/bin/env python3
"""
Verification script to check all numbers claimed in the MSR2026 Filtering Study paper
against the actual dataset.
"""

import pandas as pd
import numpy as np

def verify_dataset_numbers():
    """Verify all statistics claimed in the paper"""
    print("=" * 80)
    print("VERIFICATION: MSR2026 FILTERING STUDY PAPER CLAIMS")
    print("=" * 80)
    
    # Load dataset
    df = pd.read_csv('data/raw/aidata.csv')
    
    # Basic dataset stats
    total_records = len(df)
    unique_users = df['user_id'].nunique()
    
    print(f"\n1. BASIC DATASET STATISTICS:")
    print(f"   Paper claims: 932,791 records")
    print(f"   Actual data:  {total_records:,} records")
    print(f"   ✓ MATCH" if total_records == 932791 else f"   ✗ MISMATCH")
    
    print(f"\n   Paper claims: 72,189 unique users")  
    print(f"   Actual data:  {unique_users:,} unique users")
    print(f"   ✓ MATCH" if unique_users == 72189 else f"   ✗ MISMATCH")
    
    # Agent distribution
    print(f"\n2. AGENT DISTRIBUTION:")
    counts = df['agent'].value_counts().sort_values(ascending=False)
    total = len(df)
    
    paper_claims = {
        'OpenAI_Codex': (814522, 87.3),
        'Copilot': (50447, 5.4), 
        'Cursor': (32941, 3.5),
        'Devin': (29744, 3.2),
        'Claude_Code': (5137, 0.6)
    }
    
    for agent in paper_claims:
        if agent in counts:
            actual_count = counts[agent]
            actual_pct = (actual_count/total)*100
            claimed_count, claimed_pct = paper_claims[agent]
            
            print(f"\n   {agent}:")
            print(f"     Paper: {claimed_count:,} PRs ({claimed_pct}%)")
            print(f"     Actual: {actual_count:,} PRs ({actual_pct:.1f}%)")
            
            count_match = actual_count == claimed_count
            pct_match = abs(actual_pct - claimed_pct) < 0.1
            
            if count_match and pct_match:
                print(f"     ✓ MATCH")
            else:
                print(f"     ✗ MISMATCH")
        else:
            print(f"\n   {agent}: NOT FOUND in dataset")
    
    # User contribution analysis
    print(f"\n3. USER CONTRIBUTION PATTERNS:")
    user_contributions = df['user_id'].value_counts()
    mean_contrib = user_contributions.mean()
    median_contrib = user_contributions.median()
    
    print(f"   Paper claims: Mean = 12.9 PRs per user")
    print(f"   Actual data:  Mean = {mean_contrib:.1f} PRs per user")
    print(f"   ✓ MATCH" if abs(mean_contrib - 12.9) < 0.1 else f"   ✗ MISMATCH")
    
    print(f"\n   Paper claims: Median = 2 PRs per user")
    print(f"   Actual data:  Median = {median_contrib:.1f} PRs per user") 
    print(f"   ✓ MATCH" if abs(median_contrib - 2.0) < 0.1 else f"   ✗ MISMATCH")
    
    # Gini coefficient
    def gini_coefficient(x):
        """Calculate Gini coefficient"""
        x = np.array(x)
        x = np.sort(x)
        n = len(x)
        index = np.arange(1, n + 1)
        return (2 * np.sum(index * x)) / (n * np.sum(x)) - (n + 1) / n
    
    gini = gini_coefficient(user_contributions.values)
    print(f"\n   Paper claims: Gini coefficient = 0.846")
    print(f"   Actual data:  Gini coefficient = {gini:.3f}")
    print(f"   ✓ MATCH" if abs(gini - 0.846) < 0.01 else f"   ✗ MISMATCH")
    
    # Top 1% analysis
    top_1_pct_threshold = int(len(user_contributions) * 0.01)
    top_1_pct_users = user_contributions.head(top_1_pct_threshold)
    top_1_pct_share = (top_1_pct_users.sum() / total_records) * 100
    
    print(f"\n   Paper claims: Top-1% users contribute 42.3% of PRs")
    print(f"   Actual data:  Top-1% users contribute {top_1_pct_share:.1f}% of PRs")
    print(f"   ✓ MATCH" if abs(top_1_pct_share - 42.3) < 1.0 else f"   ✗ MISMATCH")
    
    # 99th percentile threshold
    percentile_99 = user_contributions.quantile(0.99)
    print(f"\n   Paper claims: 99th percentile threshold = 215 PRs")
    print(f"   Actual data:  99th percentile threshold = {percentile_99:.0f} PRs")
    print(f"   ✓ MATCH" if abs(percentile_99 - 215) < 5 else f"   ✗ MISMATCH")
    
    print(f"\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    verify_dataset_numbers()