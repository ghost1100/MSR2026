
# Analysis functions for MSR project
import pandas as pd
import numpy as np
from datetime import datetime

def contains_test_keywords(text):
    """Check if text contains test-related keywords"""
    if pd.isna(text) or not isinstance(text, str):
        return False

    test_keywords = ['test', 'testing', 'spec', 'unittest', 'pytest', 'jest', 'mocha', 'assert']
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in test_keywords)

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
