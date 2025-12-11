#!/usr/bin/env python3
"""
MSR2026 Filtering Study - Master Reproducibility Script

This script reproduces all analysis results for the paper:
"User-Level Debiasing in AI Tool Adoption Studies: Addressing Automation Artifacts in Large-Scale Repository Data"

Author: Ahmed Mursal, Edinburgh Napier University
Date: December 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import re
import sys
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def setup_directories():
    """Create organized output directory structure"""
    base_dir = Path('outputs/submission_ready')
    subdirs = ['figures', 'data', 'analysis_results', 'paper_materials']
    
    for subdir in [base_dir] + [base_dir / sub for sub in subdirs]:
        subdir.mkdir(exist_ok=True)
    
    return base_dir

def load_dataset():
    """Load and validate the MSR 2026 dataset"""
    print("📊 Loading MSR 2026 AI Development dataset...")
    
    data_path = Path('data/raw/aidata.csv')
    if not data_path.exists():
        print("❌ Dataset not found. Please ensure aidata.csv is in data/raw/")
        sys.exit(1)
    
    df = pd.read_csv(data_path)
    print(f"✅ Dataset loaded: {len(df):,} records, {df['user_id'].nunique():,} users")
    return df

def compute_gini_coefficient(values):
    """Compute Gini coefficient for inequality measurement"""
    values = np.array(values)
    values = np.sort(values)
    n = len(values)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * values)) / (n * np.sum(values)) - (n + 1) / n

def compute_shannon_entropy(series):
    """Compute Shannon entropy for diversity measurement"""
    value_counts = series.value_counts()
    probabilities = value_counts / len(series)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

def stage1_concentration_analysis(df, output_dir):
    """Stage 1: Raw dataset analysis and concentration metrics"""
    print("\n🔍 Stage 1: Concentration Analysis")
    
    # Basic statistics
    agent_counts = df['agent'].value_counts()
    total_records = len(df)
    user_contributions = df['user_id'].value_counts()
    unique_users = len(user_contributions)
    
    # Concentration metrics
    gini = compute_gini_coefficient(user_contributions.values)
    agent_entropy = compute_shannon_entropy(df['agent'])
    max_agent_entropy = np.log2(len(agent_counts))
    normalized_entropy = agent_entropy / max_agent_entropy
    
    # Percentile analysis
    top_1_pct_count = int(unique_users * 0.01)
    top_1_pct_share = (user_contributions.head(top_1_pct_count).sum() / total_records) * 100
    top_01_pct_count = int(unique_users * 0.001)
    top_01_pct_share = (user_contributions.head(top_01_pct_count).sum() / total_records) * 100
    percentile_99 = user_contributions.quantile(0.99)
    
    results = {
        'total_records': total_records,
        'unique_users': unique_users,
        'agent_distribution': {agent: count for agent, count in agent_counts.items()},
        'agent_percentages': {agent: (count/total_records)*100 for agent, count in agent_counts.items()},
        'gini_coefficient': gini,
        'shannon_entropy': agent_entropy,
        'normalized_entropy': normalized_entropy,
        'top_1_pct_share': top_1_pct_share,
        'top_01_pct_share': top_01_pct_share,
        'percentile_99_threshold': percentile_99,
        'mean_contrib': user_contributions.mean(),
        'median_contrib': user_contributions.median()
    }
    
    # Save results
    with open(output_dir / 'analysis_results' / 'stage1_concentration.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"   Gini coefficient: {gini:.3f}")
    print(f"   Shannon entropy: {agent_entropy:.3f} (normalized: {normalized_entropy:.3f})")
    print(f"   99th percentile threshold: {percentile_99:.0f} PRs per user")
    
    return results

def stage2_outlier_filtering(df, percentile_99, output_dir):
    """Stage 2: Statistical outlier filtering (99th percentile)"""
    print("\n⚡ Stage 2: Statistical Outlier Filtering")
    
    user_contributions = df['user_id'].value_counts()
    high_volume_users = user_contributions[user_contributions >= percentile_99].index
    
    # Create filtered dataset
    df_filtered = df[~df['user_id'].isin(high_volume_users)].copy()
    
    # Calculate impact
    accounts_removed = len(high_volume_users)
    prs_removed = len(df) - len(df_filtered)
    prs_removed_pct = (prs_removed / len(df)) * 100
    
    # Distribution comparison
    original_dist = df['agent'].value_counts(normalize=True) * 100
    filtered_dist = df_filtered['agent'].value_counts(normalize=True) * 100
    
    filtering_changes = []
    for agent in original_dist.index:
        orig_pct = original_dist[agent]
        filt_pct = filtered_dist.get(agent, 0)
        change = filt_pct - orig_pct
        filtering_changes.append({
            'agent': agent,
            'raw_pct': orig_pct,
            'filtered_pct': filt_pct,
            'delta': change
        })
    
    results = {
        'accounts_removed': accounts_removed,
        'prs_removed': prs_removed,
        'prs_removed_pct': prs_removed_pct,
        'filtering_changes': filtering_changes,
        'original_distribution': dict(original_dist),
        'filtered_distribution': dict(filtered_dist)
    }
    
    # Save results and data
    with open(output_dir / 'analysis_results' / 'stage2_filtering.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    df_filtered.to_csv(output_dir / 'data' / 'stage2_filtered_dataset.csv', index=False)
    
    print(f"   Accounts removed: {accounts_removed:,} ({accounts_removed/df['user_id'].nunique()*100:.1f}% of users)")
    print(f"   PRs removed: {prs_removed:,} ({prs_removed_pct:.1f}% of all PRs)")
    
    return results, df_filtered

def detect_bot_accounts(df):
    """Detect automated accounts using pattern matching"""
    bot_patterns = [
        r'.*bot.*',           # Contains 'bot' (case insensitive)
        r'.*\[bot\].*',       # Contains '[bot]'
        r'.*-ci$',            # Ends with '-ci'
        r'.*-automation$',    # Ends with '-automation'
        r'.*dependabot.*',    # Dependabot variations
        r'.*renovate.*',      # Renovate bot
        r'.*github-actions.*', # GitHub Actions
        r'.*codecov.*',       # Codecov bot
        r'.*greenkeeper.*',   # Greenkeeper bot
    ]
    
    bot_users = set()
    pattern_counts = {}
    
    for pattern in bot_patterns:
        matches = df[df['user'].str.contains(pattern, case=False, na=False, regex=True)]
        if len(matches) > 0:
            pattern_users = matches['user_id'].unique()
            bot_users.update(pattern_users)
            pattern_counts[pattern] = len(pattern_users)
    
    return list(bot_users), pattern_counts

def stage3_bot_filtering(df_filtered, output_dir):
    """Stage 3: Pattern-based bot account filtering"""
    print("\n🤖 Stage 3: Bot Account Detection and Filtering")
    
    bot_user_ids, pattern_counts = detect_bot_accounts(df_filtered)
    
    # Create final filtered dataset
    df_final = df_filtered[~df_filtered['user_id'].isin(bot_user_ids)].copy()
    
    # Calculate impact
    bot_accounts = len(bot_user_ids)
    bot_prs_removed = len(df_filtered) - len(df_final)
    final_dist = df_final['agent'].value_counts(normalize=True) * 100
    
    results = {
        'bot_accounts_detected': bot_accounts,
        'bot_prs_removed': bot_prs_removed,
        'pattern_counts': pattern_counts,
        'final_distribution': dict(final_dist)
    }
    
    # Save results and data
    with open(output_dir / 'analysis_results' / 'stage3_bot_filtering.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    df_final.to_csv(output_dir / 'data' / 'final_filtered_dataset.csv', index=False)
    
    print(f"   Bot accounts detected: {bot_accounts:,}")
    print(f"   Additional PRs removed: {bot_prs_removed:,}")
    
    return results, df_final

def main():
    """Main execution function"""
    print("🚀 MSR 2026 Filtering Study - Complete Reproducibility Analysis")
    print("=" * 70)
    
    # Setup
    output_dir = setup_directories()
    df = load_dataset()
    
    # Run analysis pipeline
    stage1_results = stage1_concentration_analysis(df, output_dir)
    stage2_results, df_filtered = stage2_outlier_filtering(df, stage1_results['percentile_99_threshold'], output_dir)
    stage3_results, df_final = stage3_bot_filtering(df_filtered, output_dir)
    
    # Final summary
    print("\n" + "=" * 70)
    print("🎉 ANALYSIS COMPLETE!")
    print("=" * 70)
    print(f"📁 All results saved to: {output_dir}")
    print(f"📊 Original dataset: {len(df):,} records")
    print(f"📊 Final dataset: {len(df_final):,} records")
    print(f"📊 Retention rate: {len(df_final)/len(df):.1%}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)