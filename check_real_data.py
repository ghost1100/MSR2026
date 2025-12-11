#!/usr/bin/env python3
"""
CRITICAL VERIFICATION: Check what's actually in the dataset
"""

import pandas as pd
import numpy as np

def check_actual_dataset():
    """Verify what's actually in the dataset vs what we claim"""
    print("=" * 80)
    print("CRITICAL VERIFICATION: ACTUAL DATASET CONTENT")
    print("=" * 80)
    
    df = pd.read_csv('data/raw/aidata.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"\nACTUAL COLUMNS:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. {col}")
    
    print(f"\nACTUAL AGENT LABELS:")
    agent_counts = df['agent'].value_counts()
    for agent, count in agent_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {agent}: {count:,} ({pct:.1f}%)")
    
    print(f"\nTOTAL UNIQUE AGENTS: {len(agent_counts)}")
    print(f"TOTAL RECORDS: {len(df):,}")
    
    # Check if we have the user column we claim
    if 'user_id' in df.columns:
        unique_users = df['user_id'].nunique()
        print(f"UNIQUE USERS: {unique_users:,}")
    elif 'user' in df.columns:
        unique_users = df['user'].nunique()
        print(f"UNIQUE USERS (via 'user' column): {unique_users:,}")
    else:
        print("WARNING: No user_id or user column found!")
        print(f"Available columns: {list(df.columns)}")
    
    print(f"\nSAMPLE OF ACTUAL DATA:")
    print(df.head(3).to_string())
    
    return df

if __name__ == "__main__":
    df = check_actual_dataset()