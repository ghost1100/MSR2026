#!/usr/bin/env python3
"""
Real Dataset Analysis for MSR 2026 Dataset Characterization Paper
This script performs ACTUAL analysis on the real dataset to provide accurate numbers.
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def load_analysis_results():
    """Load the actual analysis results."""
    with open('outputs/comprehensive_full_dataset_analysis.json', 'r') as f:
        data = json.load(f)
    return data

def extract_real_numbers(data):
    """Extract real, verified numbers from the analysis."""
    
    # Basic dataset info
    total_records = data['dataset_info']['total_records']
    unique_users = data['dataset_info']['unique_users']
    
    # Agent distribution (REAL numbers)
    agent_counts = data['agent_distribution']['counts']
    agent_percentages = data['agent_distribution']['percentages']
    
    # Agent-specific details (REAL numbers)
    agent_details = data['test_behavior']['agent_behavior']
    
    # Missing data calculation
    total_test_prs = data['test_behavior']['total_test_prs'] 
    total_non_test_prs = data['test_behavior']['total_non_test_prs']
    
    real_numbers = {
        'total_records': total_records,
        'unique_users': unique_users,
        'agent_counts': agent_counts,
        'agent_percentages': agent_percentages,
        'agent_details': agent_details,
        'test_prs': total_test_prs,
        'non_test_prs': total_non_test_prs
    }
    
    return real_numbers

def create_summary_table(real_numbers):
    """Create a summary table with REAL numbers."""
    
    agent_details = real_numbers['agent_details']
    
    summary_data = []
    for agent, details in agent_details.items():
        summary_data.append({
            'Agent': agent.replace('_', ' '),
            'Total PRs': f"{details['total_prs']:,}",
            'Unique Users': f"{details['unique_users']:,}",
            'PRs/User': f"{details['total_prs']/details['unique_users']:.1f}",
            'Avg Title Length': f"{details['avg_title_length']:.1f}",
            'Avg Body Length': f"{details['avg_body_length']:.1f}",
            'Closed Rate': f"{details['closed_rate']:.1%}",
            'Test Rate': f"{details['test_rate']:.1%}"
        })
    
    return pd.DataFrame(summary_data)

def identify_quality_issues(real_numbers):
    """Identify actual data quality issues from real analysis."""
    
    agent_details = real_numbers['agent_details']
    
    issues = []
    
    # Check for single-user categories
    for agent, details in agent_details.items():
        if details['unique_users'] == 1:
            issues.append(f"{agent}: Single user across {details['total_prs']:,} PRs")
        elif details['total_prs'] / details['unique_users'] > 100:
            issues.append(f"{agent}: High PRs/user ratio ({details['total_prs']/details['unique_users']:.1f})")
    
    # Check for extreme imbalances
    total_prs = sum(details['total_prs'] for details in agent_details.values())
    max_prs = max(details['total_prs'] for details in agent_details.values())
    min_prs = min(details['total_prs'] for details in agent_details.values())
    
    if max_prs / min_prs > 10:
        issues.append(f"Extreme imbalance: {max_prs/min_prs:.1f}:1 ratio between largest and smallest categories")
    
    # Check for metadata variations
    title_lengths = [details['avg_title_length'] for details in agent_details.values()]
    if max(title_lengths) / min(title_lengths) > 2:
        issues.append(f"Title length variation: {min(title_lengths):.1f} to {max(title_lengths):.1f} characters")
    
    body_lengths = [details['avg_body_length'] for details in agent_details.values()]
    if max(body_lengths) / min(body_lengths) > 5:
        issues.append(f"Body length variation: {min(body_lengths):.1f} to {max(body_lengths):.1f} characters")
    
    return issues

def generate_paper_statistics(real_numbers):
    """Generate statistics for the paper using REAL numbers."""
    
    total_records = real_numbers['total_records']
    unique_users = real_numbers['unique_users']
    agent_counts = real_numbers['agent_counts']
    agent_percentages = real_numbers['agent_percentages']
    agent_details = real_numbers['agent_details']
    
    # Main statistics
    stats = {
        'dataset_size': f"{total_records:,}",
        'unique_users': f"{unique_users:,}",
        'dominant_agent': f"OpenAI Codex: {agent_counts['OpenAI_Codex']:,} PRs ({agent_percentages['OpenAI_Codex']:.1f}%)",
        'agent_breakdown': []
    }
    
    # Agent breakdown
    for agent, count in agent_counts.items():
        percentage = agent_percentages[agent]
        stats['agent_breakdown'].append(f"{agent.replace('_', ' ')}: {count:,} PRs ({percentage:.1f}%)")
    
    # User patterns
    stats['user_patterns'] = []
    for agent, details in agent_details.items():
        users = details['unique_users']
        prs = details['total_prs']
        ratio = prs / users
        stats['user_patterns'].append(f"{agent.replace('_', ' ')}: {users:,} users, {ratio:.1f} PRs/user")
    
    # Quality issues
    stats['quality_issues'] = identify_quality_issues(real_numbers)
    
    return stats

def main():
    """Main analysis function."""
    
    print("Loading real analysis results...")
    data = load_analysis_results()
    
    print("Extracting real numbers...")
    real_numbers = extract_real_numbers(data)
    
    print("Creating summary table...")
    summary_table = create_summary_table(real_numbers)
    print("\nDataset Summary (REAL NUMBERS):")
    print(summary_table.to_string(index=False))
    
    print("\nGenerating paper statistics...")
    stats = generate_paper_statistics(real_numbers)
    
    print(f"\nDataset Size: {stats['dataset_size']} PRs")
    print(f"Unique Users: {stats['unique_users']}")
    print(f"Dominant Agent: {stats['dominant_agent']}")
    
    print("\nAgent Distribution:")
    for breakdown in stats['agent_breakdown']:
        print(f"  - {breakdown}")
    
    print("\nUser Patterns:")
    for pattern in stats['user_patterns']:
        print(f"  - {pattern}")
    
    print("\nQuality Issues Identified:")
    for issue in stats['quality_issues']:
        print(f"  - {issue}")
    
    # Save results for paper
    with open('outputs/real_paper_statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\nReal statistics saved to outputs/real_paper_statistics.json")
    print("These are the ACTUAL numbers that should be used in the paper.")

if __name__ == "__main__":
    main()