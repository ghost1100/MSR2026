#!/usr/bin/env python3
"""
COMPLETE FILTERING ANALYSIS for MSR2026 Filtering Study
Implements all stages described in the paper with actual computations
"""

import pandas as pd
import numpy as np
import re
import json
from pathlib import Path

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

def detect_bot_accounts(df):
    """Detect automated accounts using pattern matching"""
    print("Detecting bot accounts...")
    
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
    
    # Check usernames for bot patterns
    for pattern in bot_patterns:
        matches = df[df['user'].str.contains(pattern, case=False, na=False, regex=True)]
        if len(matches) > 0:
            bot_users.update(matches['user_id'].unique())
            print(f"  Pattern '{pattern}': {len(matches['user_id'].unique())} users")
    
    return list(bot_users)

def analyze_stage_1_concentration(df):
    """Stage 1: Concentration Analysis (diagnostic only)"""
    print("\n" + "="*60)
    print("STAGE 1: CONCENTRATION ANALYSIS")
    print("="*60)
    
    user_contributions = df['user_id'].value_counts()
    total_records = len(df)
    unique_users = len(user_contributions)
    
    # Basic statistics
    mean_contrib = user_contributions.mean()
    median_contrib = user_contributions.median()
    
    # Gini coefficient
    gini = compute_gini_coefficient(user_contributions.values)
    
    # Shannon entropy for agents
    agent_entropy = compute_shannon_entropy(df['agent'])
    max_agent_entropy = np.log2(df['agent'].nunique())
    normalized_entropy = agent_entropy / max_agent_entropy
    
    # Top percentile analysis
    top_1_pct_count = int(unique_users * 0.01)
    top_1_pct_users = user_contributions.head(top_1_pct_count)
    top_1_pct_share = (top_1_pct_users.sum() / total_records) * 100
    
    top_01_pct_count = int(unique_users * 0.001)
    top_01_pct_users = user_contributions.head(top_01_pct_count)
    top_01_pct_share = (top_01_pct_users.sum() / total_records) * 100
    
    # 99th percentile threshold
    percentile_99 = user_contributions.quantile(0.99)
    
    results = {
        'total_records': total_records,
        'unique_users': unique_users,
        'mean_contrib': mean_contrib,
        'median_contrib': median_contrib,
        'gini_coefficient': gini,
        'shannon_entropy': agent_entropy,
        'normalized_entropy': normalized_entropy,
        'top_1_pct_users': top_1_pct_count,
        'top_1_pct_share': top_1_pct_share,
        'top_01_pct_users': top_01_pct_count,
        'top_01_pct_share': top_01_pct_share,
        'percentile_99_threshold': percentile_99
    }
    
    print(f"Total records: {total_records:,}")
    print(f"Unique users: {unique_users:,}")
    print(f"Mean contributions: {mean_contrib:.1f} PRs per user")
    print(f"Median contributions: {median_contrib:.1f} PRs per user")
    print(f"Gini coefficient: {gini:.3f}")
    print(f"Shannon entropy (agents): {agent_entropy:.3f}")
    print(f"Normalized entropy: {normalized_entropy:.3f}")
    print(f"Top-1% users ({top_1_pct_count:,}): {top_1_pct_share:.1f}% of PRs")
    print(f"Top-0.1% users ({top_01_pct_count:,}): {top_01_pct_share:.1f}% of PRs")
    print(f"99th percentile threshold: {percentile_99:.0f} PRs per user")
    
    return results

def analyze_stage_2_outlier_filtering(df):
    """Stage 2: Statistical Outlier Filtering (99th percentile)"""
    print("\n" + "="*60)
    print("STAGE 2: STATISTICAL OUTLIER FILTERING")
    print("="*60)
    
    user_contributions = df['user_id'].value_counts()
    percentile_99 = user_contributions.quantile(0.99)
    
    # Identify high-volume users
    high_volume_users = user_contributions[user_contributions >= percentile_99].index
    
    # Create filtered dataset
    df_filtered = df[~df['user_id'].isin(high_volume_users)].copy()
    
    # Calculate impact
    accounts_removed = len(high_volume_users)
    prs_removed = len(df) - len(df_filtered)
    prs_removed_pct = (prs_removed / len(df)) * 100
    
    # Calculate new mean contribution
    new_user_contributions = df_filtered['user_id'].value_counts()
    new_mean_contrib = new_user_contributions.mean()
    
    # Agent distribution comparison
    original_dist = df['agent'].value_counts(normalize=True) * 100
    filtered_dist = df_filtered['agent'].value_counts(normalize=True) * 100
    
    results = {
        'accounts_removed': accounts_removed,
        'prs_removed': prs_removed,
        'prs_removed_pct': prs_removed_pct,
        'new_mean_contrib': new_mean_contrib,
        'original_distribution': dict(original_dist),
        'filtered_distribution': dict(filtered_dist),
        'filtered_dataset': df_filtered
    }
    
    print(f"99th percentile threshold: {percentile_99:.0f} PRs per user")
    print(f"Accounts removed: {accounts_removed:,} ({accounts_removed/df['user_id'].nunique()*100:.1f}% of users)")
    print(f"PRs removed: {prs_removed:,} ({prs_removed_pct:.1f}% of all PRs)")
    print(f"New mean contribution: {new_mean_contrib:.1f} PRs per user")
    
    print(f"\nAgent Distribution Changes:")
    for agent in original_dist.index:
        orig_pct = original_dist[agent]
        filt_pct = filtered_dist.get(agent, 0)
        change = filt_pct - orig_pct
        print(f"  {agent}: {orig_pct:.1f}% -> {filt_pct:.1f}% ({change:+.1f}%)")
    
    return results

def analyze_stage_3_bot_filtering(df_filtered):
    """Stage 3: Pattern-Based Bot Account Filtering"""
    print("\n" + "="*60)
    print("STAGE 3: PATTERN-BASED BOT FILTERING")
    print("="*60)
    
    # Detect bot accounts
    bot_user_ids = detect_bot_accounts(df_filtered)
    
    # Create final filtered dataset
    df_final = df_filtered[~df_filtered['user_id'].isin(bot_user_ids)].copy()
    
    # Calculate impact
    bot_accounts = len(bot_user_ids)
    bot_prs_removed = len(df_filtered) - len(df_final)
    
    # Final agent distribution
    final_dist = df_final['agent'].value_counts(normalize=True) * 100
    
    results = {
        'bot_accounts_detected': bot_accounts,
        'bot_prs_removed': bot_prs_removed,
        'final_distribution': dict(final_dist),
        'final_dataset': df_final
    }
    
    print(f"Bot accounts detected: {bot_accounts:,}")
    print(f"Additional PRs removed: {bot_prs_removed:,}")
    
    print(f"\nFinal Debiased Agent Distribution:")
    for agent, pct in final_dist.items():
        print(f"  {agent}: {pct:.1f}%")
    
    return results

def generate_filtering_table(stage1_results, stage2_results):
    """Generate the filtering effects table for the paper"""
    print("\n" + "="*60)
    print("TABLE 1: FILTERING EFFECTS SUMMARY")
    print("="*60)
    
    orig_dist = stage2_results['original_distribution']
    filt_dist = stage2_results['filtered_distribution']
    
    print("Agent           Raw %   Filtered %   D%")
    print("-" * 45)
    
    table_data = []
    for agent in orig_dist:
        raw_pct = orig_dist[agent]
        filtered_pct = filt_dist.get(agent, 0)
        delta = filtered_pct - raw_pct
        
        # Fix agent names for paper
        display_name = agent.replace('_', ' ')
        if display_name == 'OpenAI Codex':
            display_name = 'OpenAI Codex'
        elif display_name == 'Claude Code':
            display_name = 'Claude Code'
        
        print(f"{display_name:<15} {raw_pct:>5.1f}   {filtered_pct:>8.1f}   {delta:>+5.1f}")
        table_data.append({
            'agent': display_name,
            'raw_pct': raw_pct,
            'filtered_pct': filtered_pct,
            'delta': delta
        })
    
    return table_data

def run_complete_filtering_analysis():
    """Run the complete filtering analysis pipeline"""
    print("="*80)
    print("MSR2026 FILTERING STUDY - COMPLETE ANALYSIS")
    print("="*80)
    
    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv('data/raw/aidata.csv')
    print(f"Loaded {len(df):,} records with {df['user_id'].nunique():,} unique users")
    
    # Stage 1: Concentration Analysis
    stage1_results = analyze_stage_1_concentration(df)
    
    # Stage 2: Statistical Outlier Filtering
    stage2_results = analyze_stage_2_outlier_filtering(df)
    
    # Stage 3: Bot Account Filtering
    stage3_results = analyze_stage_3_bot_filtering(stage2_results['filtered_dataset'])
    
    # Generate table for paper
    table_data = generate_filtering_table(stage1_results, stage2_results)
    
    # Save all results
    all_results = {
        'stage1_concentration': stage1_results,
        'stage2_outlier_filtering': stage2_results,
        'stage3_bot_filtering': stage3_results,
        'filtering_table': table_data,
        'metadata': {
            'total_original_records': len(df),
            'total_final_records': len(stage3_results['final_dataset']),
            'total_retention_rate': len(stage3_results['final_dataset']) / len(df)
        }
    }
    
    # Remove datasets from results for JSON serialization
    results_for_json = all_results.copy()
    if 'filtered_dataset' in results_for_json['stage2_outlier_filtering']:
        del results_for_json['stage2_outlier_filtering']['filtered_dataset']
    if 'final_dataset' in results_for_json['stage3_bot_filtering']:
        del results_for_json['stage3_bot_filtering']['final_dataset']
    
    # Save results
    output_file = 'outputs/complete_filtering_analysis.json'
    Path(output_file).parent.mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results_for_json, f, indent=2, default=str)
    
    print(f"\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print(f"Results saved to: {output_file}")
    print(f"Original dataset: {len(df):,} records")
    print(f"Final filtered dataset: {all_results['metadata']['total_final_records']:,} records")
    print(f"Overall retention rate: {all_results['metadata']['total_retention_rate']:.1%}")
    print("="*80)
    
    return all_results

if __name__ == "__main__":
    results = run_complete_filtering_analysis()