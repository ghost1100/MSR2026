#!/usr/bin/env python3
"""
Complete MSR Analysis Pipeline Test
Tests all research questions with progressive scaling
"""
import os
import sys
import time
import json
from datetime import datetime

# Add src directory to path
sys.path.append('src')
from data_loader import load_aidev
from analysis import analyze_test_contributions

def run_rq1_analysis(df):
    """Run RQ1: Agent Distribution Analysis"""
    print("\n[RQ1] Agent Distribution Analysis")
    print("-" * 40)
    
    # Agent distribution
    agent_counts = df['agent'].value_counts()
    agent_percentages = (agent_counts / len(df) * 100).round(2)
    
    print(f"Total PRs: {len(df):,}")
    print(f"Unique agents: {df['agent'].nunique()}")
    
    for agent, count in agent_counts.items():
        percentage = agent_percentages[agent]
        print(f"  {agent}: {count:,} PRs ({percentage}%)")
    
    return {
        'agent_counts': agent_counts.to_dict(),
        'agent_percentages': agent_percentages.to_dict(),
        'total_prs': len(df),
        'unique_agents': df['agent'].nunique()
    }

def run_rq2_analysis(df):
    """Run RQ2: Test-to-Code Ratio Analysis"""
    print("\n[RQ2] Test-to-Code Ratio Analysis")
    print("-" * 40)
    
    # Use our cached analysis function
    df_analyzed, test_stats = analyze_test_contributions(df, use_cache=True)
    
    # Calculate ratios
    total_prs = len(df_analyzed)
    test_prs = test_stats['Test_PRs'].sum()
    test_ratio = test_prs / total_prs * 100
    
    print(f"Total PRs: {total_prs:,}")
    print(f"Test PRs: {test_prs:,}")
    print(f"Test Ratio: {test_ratio:.1f}%")
    
    print(f"\nBy Agent:")
    for agent in test_stats.index:
        agent_test_pct = test_stats.loc[agent, 'Test_Percentage']
        agent_test_prs = test_stats.loc[agent, 'Test_PRs']
        agent_total_prs = test_stats.loc[agent, 'Total_PRs']
        print(f"  {agent}: {agent_test_prs}/{agent_total_prs} ({agent_test_pct}%)")
    
    return {
        'total_prs': total_prs,
        'test_prs': test_prs,
        'test_ratio': test_ratio,
        'by_agent': test_stats.to_dict('index')
    }

def run_rq3_placeholder(df):
    """Run RQ3: Code Change Analysis (placeholder)"""
    print("\n[RQ3] Code Change Analysis")
    print("-" * 40)
    print("Note: GitHub API integration required for full analysis")
    
    # Basic analysis of available fields
    if 'additions' in df.columns and 'deletions' in df.columns:
        total_additions = df['additions'].sum()
        total_deletions = df['deletions'].sum()
        print(f"Total additions: {total_additions:,}")
        print(f"Total deletions: {total_deletions:,}")
        return {'additions': total_additions, 'deletions': total_deletions}
    else:
        print("Code change metrics not available in current dataset")
        return {'status': 'github_api_required'}

def run_rq4_analysis(df):
    """Run RQ4: Description Consistency Analysis"""
    print("\n[RQ4] Description Consistency Analysis")
    print("-" * 40)
    
    # Basic text analysis
    df['title_length'] = df['title'].str.len()
    df['body_length'] = df['body'].str.len()
    df['title_words'] = df['title'].str.split().str.len()
    df['body_words'] = df['body'].str.split().str.len()
    
    avg_title_length = df['title_length'].mean()
    avg_body_length = df['body_length'].mean()
    avg_title_words = df['title_words'].mean()
    avg_body_words = df['body_words'].mean()
    
    print(f"Average title length: {avg_title_length:.1f} characters")
    print(f"Average body length: {avg_body_length:.1f} characters")
    print(f"Average title words: {avg_title_words:.1f}")
    print(f"Average body words: {avg_body_words:.1f}")
    
    return {
        'avg_title_length': avg_title_length,
        'avg_body_length': avg_body_length,
        'avg_title_words': avg_title_words,
        'avg_body_words': avg_body_words
    }

def run_rq5_placeholder(df):
    """Run RQ5: User Adoption Analysis (placeholder)"""
    print("\n[RQ5] User Adoption Analysis")
    print("-" * 40)
    print("Note: User experience classification requires additional data")
    
    # Basic user analysis
    unique_users = df['user'].nunique() if 'user' in df.columns else 'N/A'
    print(f"Unique users: {unique_users}")
    
    return {'unique_users': unique_users}

def run_complete_analysis(sample_size=10000):
    """Run complete analysis pipeline"""
    print("MSR PROJECT - COMPLETE ANALYSIS PIPELINE")
    print("=" * 60)
    print(f"Sample size: {sample_size:,} rows")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    print(f"\n[DATA] Loading sample...")
    start_time = time.time()
    df = load_aidev(sample_size=sample_size)
    load_time = time.time() - start_time
    print(f"Loaded {len(df):,} rows in {load_time:.2f}s")
    
    # Run all research questions
    results = {
        'metadata': {
            'analysis_date': datetime.now().isoformat(),
            'sample_size': len(df),
            'load_time': load_time
        }
    }
    
    try:
        results['rq1'] = run_rq1_analysis(df)
        results['rq2'] = run_rq2_analysis(df)
        results['rq3'] = run_rq3_placeholder(df)
        results['rq4'] = run_rq4_analysis(df)
        results['rq5'] = run_rq5_placeholder(df)
        
        print(f"\n[SUCCESS] All research questions completed!")
        
        # Save results
        os.makedirs('outputs/reports', exist_ok=True)
        results_file = f'outputs/reports/complete_analysis_{sample_size}.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Results saved to: {results_file}")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Analysis failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Get sample size from command line or environment
    sample_size = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.getenv('SAMPLE_SIZE', '10000'))
    
    success = run_complete_analysis(sample_size)
    sys.exit(0 if success else 1)