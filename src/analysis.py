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

def calculate_test_code_ratios(df):
    """Calculate comprehensive test-to-code ratios for RQ2"""
    ratios = {}
    
    # Ensure test analysis is done
    if 'is_test_pr' not in df.columns:
        df, _ = analyze_test_contributions(df)
    
    # Overall ratios
    total_prs = len(df)
    test_prs = df['is_test_pr'].sum()
    code_prs = total_prs - test_prs
    
    ratios['overall'] = {
        'test_prs': test_prs,
        'code_prs': code_prs,
        'total_prs': total_prs,
        'test_ratio': test_prs / total_prs if total_prs > 0 else 0,
        'test_to_code_ratio': test_prs / code_prs if code_prs > 0 else float('inf')
    }
    
    # Agent-specific ratios
    ratios['by_agent'] = {}
    for agent in df['agent'].unique():
        agent_data = df[df['agent'] == agent]
        agent_test_prs = agent_data['is_test_pr'].sum()
        agent_total_prs = len(agent_data)
        agent_code_prs = agent_total_prs - agent_test_prs
        
        ratios['by_agent'][agent] = {
            'test_prs': agent_test_prs,
            'code_prs': agent_code_prs,
            'total_prs': agent_total_prs,
            'test_ratio': agent_test_prs / agent_total_prs if agent_total_prs > 0 else 0,
            'test_to_code_ratio': agent_test_prs / agent_code_prs if agent_code_prs > 0 else float('inf')
        }
    
    return ratios

def analyze_text_consistency(df):
    """Analyze text consistency for RQ4"""
    df = df.copy()
    
    # Basic text metrics
    df['title_length'] = df['title'].str.len()
    df['title_words'] = df['title'].str.split().str.len()
    df['body_length'] = df['body'].str.len()
    df['body_words'] = df['body'].str.split().str.len()
    
    # Consistency metrics
    df['title_body_ratio'] = df['title_length'] / (df['body_length'] + 1)
    
    # Quality indicators
    df['has_detailed_body'] = df['body_words'] > 10
    df['title_descriptive'] = df['title_words'] > 3
    
    consistency_stats = {
        'avg_title_length': df['title_length'].mean(),
        'avg_body_length': df['body_length'].mean(),
        'detailed_descriptions_pct': (df['has_detailed_body'].sum() / len(df)) * 100,
        'descriptive_titles_pct': (df['title_descriptive'].sum() / len(df)) * 100
    }
    
    return df, consistency_stats

def classify_users(df):
    """Classify users by experience for RQ5"""
    user_activity = df.groupby('user').agg({
        'id': 'count',
        'agent': lambda x: list(x.unique()),
        'created_at': ['min', 'max'] if 'created_at' in df.columns else ['count', 'count'],
        'state': lambda x: (x == 'closed').sum() / len(x)
    }).round(3)
    
    user_activity.columns = ['total_prs', 'agents_used', 'first_pr', 'last_pr', 'success_rate']
    user_activity['agents_count'] = user_activity['agents_used'].apply(len)
    
    if 'created_at' in df.columns:
        try:
            user_activity['days_active'] = (pd.to_datetime(user_activity['last_pr']) - 
                                           pd.to_datetime(user_activity['first_pr'])).dt.days
        except:
            user_activity['days_active'] = 0
    else:
        user_activity['days_active'] = 0
    
    # Classification logic
    def classify_user(row):
        if row['total_prs'] <= 5 or row['days_active'] <= 30:
            return 'newcomer'
        elif row['total_prs'] > 20 and row['days_active'] > 90:
            return 'experienced'
        else:
            return 'regular'
    
    user_activity['user_type'] = user_activity.apply(classify_user, axis=1)
    
    return user_activity

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

def export_research_results(results, filename, output_dir="../outputs"):
    """Export research results to JSON"""
    import json
    import os
    from datetime import datetime
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Add metadata
    export_data = {
        'export_date': datetime.now().isoformat(),
        'results': results
    }
    
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)
    
    return filepath