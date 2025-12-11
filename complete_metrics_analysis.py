#!/usr/bin/env python3
"""
Complete analysis including both Gini coefficient and Shannon entropy
for the MSR2026 Filtering Study dataset (932,791 records)
"""

import pandas as pd
import numpy as np
from scipy import stats

def compute_gini_coefficient(values):
    """Compute Gini coefficient for distribution inequality"""
    values = np.array(values)
    values = np.sort(values)
    n = len(values)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * values)) / (n * np.sum(values)) - (n + 1) / n

def compute_shannon_entropy(series):
    """Compute Shannon entropy for distribution diversity"""
    value_counts = series.value_counts()
    probabilities = value_counts / len(series)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

def analyze_complete_dataset_metrics():
    """Analyze both Gini coefficient and Shannon entropy for the complete dataset"""
    print("=" * 80)
    print("COMPLETE DATASET: GINI COEFFICIENT & SHANNON ENTROPY ANALYSIS")
    print("=" * 80)
    
    # Load complete dataset
    df = pd.read_csv('data/raw/aidata.csv')
    print(f"Dataset size: {len(df):,} records")
    
    # User contribution analysis
    user_contributions = df['user_id'].value_counts()
    print(f"Unique users: {len(user_contributions):,}")
    
    # Gini coefficient for user contribution inequality
    gini_users = compute_gini_coefficient(user_contributions.values)
    print(f"\n1. USER CONTRIBUTION INEQUALITY:")
    print(f"   Gini Coefficient: {gini_users:.3f}")
    print(f"   Interpretation: {'High inequality' if gini_users > 0.6 else 'Moderate inequality' if gini_users > 0.4 else 'Low inequality'}")
    
    # Shannon entropy for user contribution diversity
    # Note: For large datasets, we use log of user contributions to make entropy meaningful
    user_contribution_bins = pd.cut(user_contributions.values, bins=20)
    entropy_users = compute_shannon_entropy(user_contribution_bins)
    print(f"   Shannon Entropy (binned): {entropy_users:.3f}")
    
    # Agent distribution analysis
    agent_counts = df['agent'].value_counts()
    print(f"\n2. AGENT DISTRIBUTION ANALYSIS:")
    
    # Gini coefficient for agent distribution
    gini_agents = compute_gini_coefficient(agent_counts.values)
    print(f"   Gini Coefficient: {gini_agents:.3f}")
    print(f"   Interpretation: {'Highly unbalanced' if gini_agents > 0.6 else 'Moderately unbalanced' if gini_agents > 0.4 else 'Balanced'}")
    
    # Shannon entropy for agent distribution
    entropy_agents = compute_shannon_entropy(df['agent'])
    print(f"   Shannon Entropy: {entropy_agents:.3f}")
    print(f"   Max possible entropy: {np.log2(len(agent_counts)):.3f}")
    print(f"   Normalized entropy: {entropy_agents / np.log2(len(agent_counts)):.3f}")
    
    # Detailed agent breakdown
    print(f"\n3. AGENT DISTRIBUTION DETAILS:")
    total_records = len(df)
    for agent, count in agent_counts.items():
        pct = (count / total_records) * 100
        print(f"   {agent}: {count:,} PRs ({pct:.1f}%)")
    
    # User distribution per agent
    print(f"\n4. USER PATTERNS PER AGENT:")
    for agent in agent_counts.index:
        agent_df = df[df['agent'] == agent]
        agent_users = agent_df['user_id'].value_counts()
        agent_gini = compute_gini_coefficient(agent_users.values)
        agent_entropy = compute_shannon_entropy(pd.cut(agent_users.values, bins=min(10, len(agent_users))))
        
        print(f"   {agent}:")
        print(f"     Users: {len(agent_users):,}")
        print(f"     PRs per user (avg): {len(agent_df) / len(agent_users):.1f}")
        print(f"     Gini coefficient: {agent_gini:.3f}")
        print(f"     Shannon entropy: {agent_entropy:.3f}")
    
    return {
        'dataset_size': len(df),
        'unique_users': len(user_contributions),
        'user_gini': gini_users,
        'user_entropy': entropy_users,
        'agent_gini': gini_agents,
        'agent_entropy': entropy_agents,
        'agent_counts': dict(agent_counts)
    }

if __name__ == "__main__":
    results = analyze_complete_dataset_metrics()
    print(f"\n" + "=" * 80)
    print("SUMMARY FOR PAPER:")
    print(f"User contribution Gini: {results['user_gini']:.3f}")
    print(f"Agent distribution entropy: {results['agent_entropy']:.3f}")
    print("=" * 80)