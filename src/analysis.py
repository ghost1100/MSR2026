
# Reusable Analysis Functions for AIDev Dataset
import pandas as pd
import numpy as np

def contains_test_keywords(text, keywords=None):
    """Check if text contains any test-related keywords"""
    if keywords is None:
        keywords = ['test', 'testing', 'spec', 'unittest', 'pytest', 'jest', 'mocha', 'assert']

    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    return any(keyword in text_lower for keyword in keywords)

def analyze_test_contributions(df):
    """Analyze test contributions in a DataFrame"""
    df = df.copy()
    df['has_test_in_title'] = df['title'].apply(lambda x: contains_test_keywords(x))
    df['has_test_in_body'] = df['body'].apply(lambda x: contains_test_keywords(x))
    df['is_test_pr'] = df['has_test_in_title'] | df['has_test_in_body']

    # Agent-specific analysis
    test_by_agent = df.groupby('agent')['is_test_pr'].agg(['count', 'sum', 'mean']).round(3)
    test_by_agent.columns = ['Total_PRs', 'Test_PRs', 'Test_Ratio']
    test_by_agent['Test_Percentage'] = (test_by_agent['Test_Ratio'] * 100).round(1)

    return df, test_by_agent

def get_research_summary(df):
    """Generate comprehensive research summary"""
    summary = {
        'dataset_size': len(df),
        'unique_agents': df['agent'].nunique(),
        'unique_users': df['user'].nunique(),
        'test_pr_rate': (df['is_test_pr'].sum() / len(df)) * 100 if 'is_test_pr' in df.columns else None,
        'state_distribution': df['state'].value_counts().to_dict(),
        'agent_distribution': df['agent'].value_counts().to_dict()
    }
    return summary

def calculate_test_code_ratios(df):
    """Calculate test-to-code ratios for overall dataset and by agent"""
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
