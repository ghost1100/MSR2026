#!/usr/bin/env python3
"""
MSR Analysis with Visualizations
Complete analysis pipeline with charts and graphs
"""
import os
import sys
import time
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

# Add src directory to path
sys.path.append('src')
from data_loader import load_aidev
from analysis import analyze_test_contributions

def create_rq1_visualizations(df, output_dir):
    """Create RQ1 visualizations"""
    print("  Creating RQ1 visualizations...")
    
    # Agent distribution
    agent_counts = df['agent'].value_counts()
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('RQ1: Agent Distribution Analysis', fontsize=16, fontweight='bold')
    
    # Bar chart
    agent_counts.plot(kind='bar', ax=axes[0], color='skyblue')
    axes[0].set_title('Agent Distribution (Count)')
    axes[0].set_xlabel('Agent')
    axes[0].set_ylabel('Number of PRs')
    axes[0].tick_params(axis='x', rotation=45)
    
    # Pie chart
    agent_counts.plot(kind='pie', ax=axes[1], autopct='%1.1f%%')
    axes[1].set_title('Agent Distribution (Percentage)')
    axes[1].set_ylabel('')
    
    plt.tight_layout()
    
    # Save figure
    rq1_path = os.path.join(output_dir, 'RQ1_agent_distribution.png')
    plt.savefig(rq1_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return rq1_path

def create_rq2_visualizations(df, test_stats, output_dir):
    """Create RQ2 visualizations"""
    print("  Creating RQ2 visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('RQ2: Test-to-Code Ratio Analysis', fontsize=16, fontweight='bold')
    
    # Overall test vs non-test
    test_counts = df['is_test_pr'].value_counts()
    test_counts.index = ['Non-Test PRs', 'Test PRs']
    test_counts.plot(kind='pie', ax=axes[0,0], autopct='%1.1f%%', colors=['lightcoral', 'lightgreen'])
    axes[0,0].set_title('Overall: Test vs Non-Test PRs')
    axes[0,0].set_ylabel('')
    
    # Test PRs by agent
    test_by_agent = test_stats['Test_PRs']
    test_by_agent.plot(kind='bar', ax=axes[0,1], color='orange')
    axes[0,1].set_title('Test PRs by Agent')
    axes[0,1].set_xlabel('Agent')
    axes[0,1].set_ylabel('Number of Test PRs')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Test percentage by agent
    test_pct_by_agent = test_stats['Test_Percentage']
    test_pct_by_agent.plot(kind='bar', ax=axes[1,0], color='green')
    axes[1,0].set_title('Test Contribution Rate by Agent (%)')
    axes[1,0].set_xlabel('Agent')
    axes[1,0].set_ylabel('Test PR Percentage')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Agent comparison table
    axes[1,1].axis('tight')
    axes[1,1].axis('off')
    table_data = test_stats[['Total_PRs', 'Test_PRs', 'Test_Percentage']].round(1)
    table = axes[1,1].table(cellText=table_data.values,
                           rowLabels=table_data.index,
                           colLabels=table_data.columns,
                           cellLoc='center',
                           loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    axes[1,1].set_title('Test Statistics by Agent')
    
    plt.tight_layout()
    
    # Save figure
    rq2_path = os.path.join(output_dir, 'RQ2_test_analysis.png')
    plt.savefig(rq2_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return rq2_path

def create_rq4_visualizations(df, output_dir):
    """Create RQ4 visualizations"""
    print("  Creating RQ4 visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('RQ4: Description Consistency Analysis', fontsize=16, fontweight='bold')
    
    # Title length distribution
    df['title_length'].hist(bins=30, ax=axes[0,0], color='lightblue', alpha=0.7)
    axes[0,0].set_title('Title Length Distribution')
    axes[0,0].set_xlabel('Characters')
    axes[0,0].set_ylabel('Frequency')
    
    # Body length distribution
    df['body_length'].hist(bins=30, ax=axes[0,1], color='lightgreen', alpha=0.7)
    axes[0,1].set_title('Body Length Distribution')
    axes[0,1].set_xlabel('Characters')
    axes[0,1].set_ylabel('Frequency')
    
    # Title vs Body length scatter
    sample_data = df.sample(min(1000, len(df)))  # Sample for performance
    axes[1,0].scatter(sample_data['title_length'], sample_data['body_length'], alpha=0.6)
    axes[1,0].set_title('Title vs Body Length')
    axes[1,0].set_xlabel('Title Length')
    axes[1,0].set_ylabel('Body Length')
    
    # Word count comparison
    metrics = ['title_words', 'body_words']
    avg_values = [df['title_words'].mean(), df['body_words'].mean()]
    axes[1,1].bar(metrics, avg_values, color=['orange', 'purple'])
    axes[1,1].set_title('Average Word Counts')
    axes[1,1].set_ylabel('Average Words')
    
    plt.tight_layout()
    
    # Save figure
    rq4_path = os.path.join(output_dir, 'RQ4_description_analysis.png')
    plt.savefig(rq4_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return rq4_path

def create_summary_dashboard(results, output_dir):
    """Create overall summary dashboard"""
    print("  Creating summary dashboard...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'MSR Project Summary Dashboard - {results["metadata"]["sample_size"]:,} PRs', 
                fontsize=18, fontweight='bold')
    
    # Agent distribution pie
    agent_data = results['rq1']['agent_counts']
    agents = list(agent_data.keys())
    counts = list(agent_data.values())
    
    axes[0,0].pie(counts, labels=agents, autopct='%1.1f%%')
    axes[0,0].set_title('Agent Distribution')
    
    # Test contribution rates
    if 'by_agent' in results['rq2']:
        agent_test_rates = {}
        for agent, data in results['rq2']['by_agent'].items():
            agent_test_rates[agent] = data['Test_Percentage']
        
        agents = list(agent_test_rates.keys())
        rates = list(agent_test_rates.values())
        axes[0,1].bar(agents, rates, color='green')
        axes[0,1].set_title('Test Contribution Rate by Agent (%)')
        axes[0,1].set_ylabel('Test Percentage')
        axes[0,1].tick_params(axis='x', rotation=45)
    
    # Text metrics
    if 'rq4' in results:
        text_metrics = ['Title Length', 'Body Length', 'Title Words', 'Body Words']
        text_values = [
            results['rq4']['avg_title_length'],
            results['rq4']['avg_body_length'] / 100,  # Scale down for visibility
            results['rq4']['avg_title_words'],
            results['rq4']['avg_body_words'] / 10     # Scale down for visibility
        ]
        
        bars = axes[1,0].bar(text_metrics, text_values, color=['blue', 'green', 'orange', 'red'])
        axes[1,0].set_title('Text Analysis Metrics (Scaled)')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, text_values):
            height = bar.get_height()
            axes[1,0].text(bar.get_x() + bar.get_width()/2., height + max(text_values)*0.01,
                          f'{value:.1f}', ha='center', va='bottom')
    
    # Key statistics table
    axes[1,1].axis('tight')
    axes[1,1].axis('off')
    
    stats_data = [
        ['Total PRs', f"{results['metadata']['sample_size']:,}"],
        ['Unique Agents', str(results['rq1']['unique_agents'])],
        ['Test PRs', f"{results['rq2']['test_prs']:,}"],
        ['Test Ratio', f"{results['rq2']['test_ratio']:.1f}%"],
        ['Unique Users', str(results.get('rq5', {}).get('unique_users', 'N/A'))],
        ['Avg Title Length', f"{results.get('rq4', {}).get('avg_title_length', 0):.1f} chars"],
        ['Load Time', f"{results['metadata']['load_time']:.2f}s"]
    ]
    
    table = axes[1,1].table(cellText=stats_data,
                           colLabels=['Metric', 'Value'],
                           cellLoc='center',
                           loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    axes[1,1].set_title('Key Statistics')
    
    plt.tight_layout()
    
    # Save figure
    dashboard_path = os.path.join(output_dir, 'MSR_Summary_Dashboard.png')
    plt.savefig(dashboard_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return dashboard_path

def run_analysis_with_visualizations(sample_size=10000):
    """Run complete analysis with visualizations"""
    print("MSR PROJECT - ANALYSIS WITH VISUALIZATIONS")
    print("=" * 60)
    print(f"Sample size: {sample_size:,} rows")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create output directories
    figures_dir = 'outputs/figures'
    reports_dir = 'outputs/reports'
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    # Load data
    print(f"\n[DATA] Loading sample...")
    start_time = time.time()
    df = load_aidev(sample_size=sample_size)
    load_time = time.time() - start_time
    print(f"Loaded {len(df):,} rows in {load_time:.2f}s")
    
    # Run analysis (reuse existing functions)
    print(f"\n[ANALYSIS] Running research questions...")
    
    # RQ1: Agent Distribution
    agent_counts = df['agent'].value_counts()
    agent_percentages = (agent_counts / len(df) * 100).round(2)
    
    # RQ2: Test Analysis with visualizations
    df_analyzed, test_stats = analyze_test_contributions(df, use_cache=True)
    
    # RQ4: Text Analysis
    df['title_length'] = df['title'].str.len()
    df['body_length'] = df['body'].str.len()
    df['title_words'] = df['title'].str.split().str.len()
    df['body_words'] = df['body'].str.split().str.len()
    
    # Create visualizations
    print(f"\n[VISUALIZATIONS] Creating charts and graphs...")
    
    created_files = []
    
    # RQ1 visualizations
    rq1_path = create_rq1_visualizations(df, figures_dir)
    created_files.append(rq1_path)
    
    # RQ2 visualizations
    rq2_path = create_rq2_visualizations(df_analyzed, test_stats, figures_dir)
    created_files.append(rq2_path)
    
    # RQ4 visualizations
    rq4_path = create_rq4_visualizations(df, figures_dir)
    created_files.append(rq4_path)
    
    # Compile results
    results = {
        'metadata': {
            'analysis_date': datetime.now().isoformat(),
            'sample_size': len(df),
            'load_time': load_time
        },
        'rq1': {
            'agent_counts': agent_counts.to_dict(),
            'agent_percentages': agent_percentages.to_dict(),
            'total_prs': len(df),
            'unique_agents': df['agent'].nunique()
        },
        'rq2': {
            'total_prs': len(df_analyzed),
            'test_prs': test_stats['Test_PRs'].sum(),
            'test_ratio': (test_stats['Test_PRs'].sum() / len(df_analyzed) * 100),
            'by_agent': test_stats.to_dict('index')
        },
        'rq4': {
            'avg_title_length': df['title_length'].mean(),
            'avg_body_length': df['body_length'].mean(),
            'avg_title_words': df['title_words'].mean(),
            'avg_body_words': df['body_words'].mean()
        },
        'rq5': {
            'unique_users': df['user'].nunique() if 'user' in df.columns else 'N/A'
        }
    }
    
    # Create summary dashboard
    dashboard_path = create_summary_dashboard(results, figures_dir)
    created_files.append(dashboard_path)
    
    # Save results
    results_file = os.path.join(reports_dir, f'analysis_with_visuals_{sample_size}.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Print summary
    print(f"\n[SUCCESS] Analysis completed with visualizations!")
    print(f"\nFiles created:")
    print(f"  Results: {results_file}")
    for file_path in created_files:
        print(f"  Visualization: {file_path}")
    
    print(f"\n[SUMMARY] Key Findings:")
    print(f"  • Total PRs analyzed: {len(df):,}")
    print(f"  • Unique agents: {df['agent'].nunique()}")
    print(f"  • Test contribution rate: {results['rq2']['test_ratio']:.1f}%")
    print(f"  • Most active agent: {agent_counts.index[0]} ({agent_counts.iloc[0]:,} PRs)")
    
    return True

if __name__ == "__main__":
    # Get sample size from command line or environment
    sample_size = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.getenv('SAMPLE_SIZE', '10000'))
    
    success = run_analysis_with_visualizations(sample_size)
    sys.exit(0 if success else 1)