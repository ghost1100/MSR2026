#!/usr/bin/env python3
"""
HONEST ANALYSIS: Only compute what we can actually verify
"""

import pandas as pd
import numpy as np

def compute_honest_statistics():
    """Compute only the statistics we can actually calculate"""
    print("=" * 80)
    print("HONEST ANALYSIS - ONLY VERIFIED STATISTICS")
    print("=" * 80)
    
    df = pd.read_csv('data/raw/aidata.csv')
    
    # Basic facts we can verify
    print(f"Dataset size: {len(df):,}")
    print(f"Unique users: {df['user_id'].nunique():,}")
    
    # Agent distribution (CORRECTED NAMES)
    print(f"\nACTUAL AGENT DISTRIBUTION:")
    agent_counts = df['agent'].value_counts()
    total = len(df)
    for agent, count in agent_counts.items():
        pct = (count / total) * 100
        print(f"  {agent}: {count:,} PRs ({pct:.1f}%)")
    
    # User contribution statistics
    user_contributions = df['user_id'].value_counts()
    mean_contrib = user_contributions.mean()
    median_contrib = user_contributions.median()
    
    print(f"\nUSER CONTRIBUTION STATISTICS:")
    print(f"  Mean contributions per user: {mean_contrib:.1f}")
    print(f"  Median contributions per user: {median_contrib:.1f}")
    print(f"  Mean/Median ratio: {mean_contrib/median_contrib:.1f}x")
    
    # Gini coefficient (ACTUALLY COMPUTE IT)
    def gini_coefficient(x):
        x = np.array(x)
        x = np.sort(x)
        n = len(x)
        index = np.arange(1, n + 1)
        return (2 * np.sum(index * x)) / (n * np.sum(x)) - (n + 1) / n
    
    gini = gini_coefficient(user_contributions.values)
    print(f"  Gini coefficient: {gini:.3f}")
    
    # Shannon entropy (ACTUALLY COMPUTE IT)  
    def shannon_entropy(series):
        value_counts = series.value_counts()
        probabilities = value_counts / len(series)
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy
    
    # For user distribution entropy, we need to bin the data
    user_bins = pd.cut(user_contributions.values, bins=20, labels=False)
    user_entropy = shannon_entropy(pd.Series(user_bins))
    
    # For agent distribution entropy
    agent_entropy = shannon_entropy(df['agent'])
    max_agent_entropy = np.log2(len(agent_counts))
    normalized_agent_entropy = agent_entropy / max_agent_entropy
    
    print(f"  Shannon entropy (agents): {agent_entropy:.3f}")
    print(f"  Max possible agent entropy: {max_agent_entropy:.3f}")
    print(f"  Normalized agent entropy: {normalized_agent_entropy:.3f}")
    
    # Top user analysis
    top_1_pct_count = int(len(user_contributions) * 0.01)
    top_1_pct_users = user_contributions.head(top_1_pct_count)
    top_1_pct_share = (top_1_pct_users.sum() / total) * 100
    
    print(f"\nCONCENTRATION ANALYSIS:")
    print(f"  Top 1% users ({top_1_pct_count:,} users): {top_1_pct_share:.1f}% of PRs")
    
    # 99th percentile
    percentile_99 = user_contributions.quantile(0.99)
    print(f"  99th percentile threshold: {percentile_99:.0f} PRs per user")
    
    # Users exceeding 99th percentile
    high_volume_users = (user_contributions >= percentile_99).sum()
    high_volume_prs = user_contributions[user_contributions >= percentile_99].sum()
    high_volume_share = (high_volume_prs / total) * 100
    
    print(f"  Users at/above 99th percentile: {high_volume_users:,}")
    print(f"  PRs from high-volume users: {high_volume_prs:,} ({high_volume_share:.1f}%)")
    
    print(f"\n" + "=" * 80)
    print("SUMMARY: These are the ONLY statistics we can honestly claim")
    print("=" * 80)
    
    return {
        'total_records': total,
        'unique_users': df['user_id'].nunique(),
        'agent_counts': dict(agent_counts),
        'gini': gini,
        'agent_entropy': agent_entropy,
        'normalized_agent_entropy': normalized_agent_entropy,
        'mean_contrib': mean_contrib,
        'median_contrib': median_contrib,
        'top_1_pct_share': top_1_pct_share,
        'percentile_99': percentile_99
    }

if __name__ == "__main__":
    results = compute_honest_statistics()