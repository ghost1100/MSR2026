#!/usr/bin/env python3
"""
Filtering Analysis for MSR 2026 Dataset
This implements the methodological contribution: user-level debiasing filters
"""

import pandas as pd
import numpy as np
from scipy import stats

def load_dataset():
    """Load the aidata.csv dataset"""
    df = pd.read_csv('data/raw/aidata.csv')
    print(f"Raw dataset loaded: {len(df)} records")
    return df

def compute_gini_coefficient(values):
    """Compute Gini coefficient for distribution inequality"""
    sorted_values = np.sort(values)
    n = len(values)
    cumsum = np.cumsum(sorted_values)
    return (n + 1 - 2 * np.sum(cumsum) / cumsum[-1]) / n

def compute_entropy(series):
    """Compute Shannon entropy for distribution diversity"""
    counts = series.value_counts()
    probs = counts / len(series)
    return -np.sum(probs * np.log2(probs))

def analyze_dataset(df, name):
    """Comprehensive analysis of a dataset version"""
    print(f"\n=== {name} ===")
    
    # Basic counts
    total_prs = len(df)
    unique_users = df['user'].nunique()
    
    # Agent distribution
    agent_counts = df['agent'].value_counts()
    copilot_pct = (agent_counts.get('Copilot', 0) / total_prs) * 100
    claude_pct = (agent_counts.get('Claude_Code', 0) / total_prs) * 100
    
    # User activity patterns
    user_pr_counts = df['user'].value_counts()
    median_prs_per_user = user_pr_counts.median()
    max_prs_per_user = user_pr_counts.max()
    top_user_pct = (max_prs_per_user / total_prs) * 100
    
    # Closure rate
    closure_rate = (df['state'] == 'closed').mean() * 100
    
    # Statistical measures
    gini = compute_gini_coefficient(user_pr_counts.values)
    entropy = compute_entropy(df['user'])
    
    results = {
        'name': name,
        'total_prs': total_prs,
        'unique_users': unique_users,
        'copilot_pct': copilot_pct,
        'claude_pct': claude_pct,
        'median_prs_per_user': median_prs_per_user,
        'max_prs_per_user': max_prs_per_user,
        'top_user_pct': top_user_pct,
        'closure_rate': closure_rate,
        'gini_coefficient': gini,
        'entropy': entropy
    }
    
    print(f"Total PRs: {total_prs:,}")
    print(f"Unique Users: {unique_users:,}")
    print(f"Copilot: {copilot_pct:.1f}%")
    print(f"Claude Code: {claude_pct:.1f}%")
    print(f"Median PRs/user: {median_prs_per_user}")
    print(f"Max PRs (single user): {max_prs_per_user:,}")
    print(f"Top user percentage: {top_user_pct:.1f}%")
    print(f"Closure rate: {closure_rate:.1f}%")
    print(f"Gini coefficient: {gini:.4f}")
    print(f"Entropy: {entropy:.2f} bits")
    
    return results

def main():
    """Run the complete filtering analysis"""
    
    # Load raw dataset
    df_raw = load_dataset()
    
    # Analysis 1: Raw dataset
    results_raw = analyze_dataset(df_raw, "Raw Dataset")
    
    # Filter A: Remove dominant system account
    top_user = df_raw['user'].value_counts().index[0]
    print(f"\nRemoving top user: '{top_user}'")
    df_no_top = df_raw[df_raw['user'] != top_user].copy()
    results_no_top = analyze_dataset(df_no_top, "Filter A: No System Account")
    
    # Filter B: Remove extreme automation (99.9th percentile cut)
    user_counts = df_raw['user'].value_counts()
    threshold = user_counts.quantile(0.999)
    print(f"\nUsing 99.9th percentile threshold: {threshold} PRs")
    
    # Get users below threshold
    users_below_threshold = user_counts[user_counts <= threshold].index
    df_human_scale = df_raw[df_raw['user'].isin(users_below_threshold)].copy()
    results_human_scale = analyze_dataset(df_human_scale, "Filter B: Human-Scale Usage")
    
    # Summary comparison table
    print("\n" + "="*80)
    print("FILTERING RESULTS SUMMARY")
    print("="*80)
    
    datasets = [results_raw, results_no_top, results_human_scale]
    
    print(f"{'Metric':<25} {'Raw':<15} {'No System':<15} {'Human-Scale':<15}")
    print("-" * 75)
    print(f"{'Total PRs':<25} {results_raw['total_prs']:<15,} {results_no_top['total_prs']:<15,} {results_human_scale['total_prs']:<15,}")
    print(f"{'Unique Users':<25} {results_raw['unique_users']:<15,} {results_no_top['unique_users']:<15,} {results_human_scale['unique_users']:<15,}")
    print(f"{'Copilot %':<25} {results_raw['copilot_pct']:<15.1f} {results_no_top['copilot_pct']:<15.1f} {results_human_scale['copilot_pct']:<15.1f}")
    print(f"{'Claude Code %':<25} {results_raw['claude_pct']:<15.1f} {results_no_top['claude_pct']:<15.1f} {results_human_scale['claude_pct']:<15.1f}")
    print(f"{'Median PRs/user':<25} {results_raw['median_prs_per_user']:<15.1f} {results_no_top['median_prs_per_user']:<15.1f} {results_human_scale['median_prs_per_user']:<15.1f}")
    print(f"{'Closure Rate %':<25} {results_raw['closure_rate']:<15.1f} {results_no_top['closure_rate']:<15.1f} {results_human_scale['closure_rate']:<15.1f}")
    print(f"{'Gini Coefficient':<25} {results_raw['gini_coefficient']:<15.4f} {results_no_top['gini_coefficient']:<15.4f} {results_human_scale['gini_coefficient']:<15.4f}")
    print(f"{'Entropy (bits)':<25} {results_raw['entropy']:<15.2f} {results_no_top['entropy']:<15.2f} {results_human_scale['entropy']:<15.2f}")
    
    # Key finding determination
    print("\n" + "="*80)
    print("CRITICAL FINDINGS FOR PAPER")
    print("="*80)
    
    # Check for distribution flip
    copilot_change = results_human_scale['copilot_pct'] - results_raw['copilot_pct']
    claude_change = results_human_scale['claude_pct'] - results_raw['claude_pct']
    
    print(f"Copilot percentage change: {copilot_change:+.1f}%")
    print(f"Claude Code percentage change: {claude_change:+.1f}%")
    
    # Check for dataset collapse
    collapse_ratio = results_human_scale['total_prs'] / results_raw['total_prs']
    print(f"Dataset retention after filtering: {collapse_ratio:.1%}")
    
    # Determine paper type
    if abs(copilot_change) > 10:
        print("\n🟢 CASE 1: AGENT DISTRIBUTION SIGNIFICANTLY CHANGES")
        print("   → Paper about automation-induced distortion")
    elif results_human_scale['claude_pct'] < 1:
        print("\n🟡 CASE 2: CLAUDE NEARLY DISAPPEARS") 
        print("   → Paper about phantom adoption patterns")
    elif collapse_ratio < 0.2:
        print("\n🔴 CASE 3: DATASET SEVERELY COLLAPSES")
        print("   → Paper about automation contamination")
    else:
        print("\n⚪ UNEXPECTED CASE: Review results manually")
        
    # Export results for paper integration
    import json
    
    def convert_numpy(obj):
        """Convert numpy types to native Python types for JSON serialization"""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(v) for v in obj]
        return obj
    
    all_results = {
        'raw': convert_numpy(results_raw),
        'no_system_account': convert_numpy(results_no_top),  
        'human_scale': convert_numpy(results_human_scale),
        'filtering_effects': convert_numpy({
            'copilot_change': copilot_change,
            'claude_change': claude_change,
            'dataset_retention': collapse_ratio,
            'top_user_removed': top_user,
            'percentile_threshold': threshold
        })
    }
    
    with open('filtering_analysis_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nResults exported to: filtering_analysis_results.json")
    
    # Return the 5 key numbers requested
    print("\n" + "="*50)
    print("THE 5 KEY NUMBERS:")
    print("="*50)
    print(f"1. PRs after removing top user: {results_no_top['total_prs']:,}")
    print(f"2. Copilot % after removing top user: {results_no_top['copilot_pct']:.1f}%")
    print(f"3. Claude % after removing top user: {results_no_top['claude_pct']:.1f}%")
    print(f"4. PRs after 99.9th percentile filtering: {results_human_scale['total_prs']:,}")
    print(f"5. Median PRs/user after human-scale filtering: {results_human_scale['median_prs_per_user']:.1f}")
    
    return all_results

if __name__ == "__main__":
    results = main()