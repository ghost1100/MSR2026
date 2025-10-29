
"""
Core analysis functions for AIDev dataset research
Provides statistical analysis and test detection capabilities
"""
import pandas as pd
import numpy as np

def contains_test_keywords(text, keywords=None):
    """
    Check if text contains test-related keywords
    
    Args:
        text: String to search (PR title or body)
        keywords: List of test keywords to search for
    
    Returns:
        bool: True if any test keywords found
    """
    if keywords is None:
        # Common test-related terms across programming languages
        keywords = ['test', 'testing', 'spec', 'unittest', 'pytest', 'jest', 'mocha', 'assert']

    if pd.isna(text):
        return False
    
    text_lower = str(text).lower()
    return any(keyword in text_lower for keyword in keywords)

def analyze_test_contributions(df):
    """
    Analyze test contributions across AI agents
    
    Args:
        df: DataFrame with 'title', 'body', 'agent' columns
    
    Returns:
        tuple: (enhanced_df, test_summary_by_agent)
    """
    df = df.copy()
    
    # Detect test-related PRs by analyzing title and body content
    df['has_test_in_title'] = df['title'].apply(lambda x: contains_test_keywords(x))
    df['has_test_in_body'] = df['body'].apply(lambda x: contains_test_keywords(x))
    df['is_test_pr'] = df['has_test_in_title'] | df['has_test_in_body']

    # Calculate test contribution rates by agent
    test_by_agent = df.groupby('agent')['is_test_pr'].agg(['count', 'sum', 'mean']).round(3)
    test_by_agent.columns = ['Total_PRs', 'Test_PRs', 'Test_Ratio']
    test_by_agent['Test_Percentage'] = (test_by_agent['Test_Ratio'] * 100).round(1)

    return df, test_by_agent

def get_research_summary(df):
    """
    Generate comprehensive dataset summary statistics
    
    Args:
        df: AIDev DataFrame
    
    Returns:
        dict: Summary statistics including agent distribution and test rates
    """
    summary = {
        'dataset_size': len(df),
        'unique_agents': df['agent'].nunique(),
        'unique_users': df['user'].nunique() if 'user' in df.columns else None,
        'test_pr_rate': (df['is_test_pr'].sum() / len(df)) * 100 if 'is_test_pr' in df.columns else None,
        'state_distribution': df['state'].value_counts().to_dict() if 'state' in df.columns else None,
        'agent_distribution': df['agent'].value_counts().to_dict()
    }
    return summary
