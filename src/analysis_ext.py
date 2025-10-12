"""
Additional analysis functions for MSR project
This file contains functions that may be missing from the main analysis.py
"""
import pandas as pd
import numpy as pd

def calculate_test_code_ratios(df):
    """Calculate test-to-code ratios for overall dataset and by agent"""
    from analysis import analyze_test_contributions
    
    # Ensure test analysis is done
    if 'is_test_pr' not in df.columns:
        df, _ = analyze_test_contributions(df)
    
    # Overall statistics
    test_prs = df['is_test_pr'].sum()
    code_prs = len(df) - test_prs  # Non-test PRs are considered "code" PRs
    total_prs = len(df)
    test_ratio = test_prs / total_prs if total_prs > 0 else 0
    test_to_code_ratio = test_prs / code_prs if code_prs > 0 else float('inf')
    
    overall_stats = {
        'test_prs': str(test_prs),
        'code_prs': str(code_prs),
        'total_prs': total_prs,
        'test_ratio': test_ratio,
        'test_to_code_ratio': test_to_code_ratio
    }
    
    # By agent statistics
    by_agent_stats = {}
    for agent in df['agent'].unique():
        agent_df = df[df['agent'] == agent]
        agent_test_prs = agent_df['is_test_pr'].sum()
        agent_code_prs = len(agent_df) - agent_test_prs
        agent_total_prs = len(agent_df)
        agent_test_ratio = agent_test_prs / agent_total_prs if agent_total_prs > 0 else 0
        agent_test_to_code_ratio = agent_test_prs / agent_code_prs if agent_code_prs > 0 else float('inf')
        
        by_agent_stats[agent] = {
            'test_prs': str(agent_test_prs),
            'code_prs': str(agent_code_prs),
            'total_prs': agent_total_prs,
            'test_ratio': agent_test_ratio,
            'test_to_code_ratio': agent_test_to_code_ratio
        }
    
    return {
        'overall': overall_stats,
        'by_agent': by_agent_stats
    }