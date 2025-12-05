"""
GENUINE DATASET ANALYSIS - Computing Real Statistics from Actual aidata.csv
This script performs ACTUAL analysis on the real dataset, not fabricated numbers.
"""
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
from collections import Counter

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def load_real_dataset():
    """Load the actual aidata.csv dataset"""
    print("=" * 80)
    print("LOADING ACTUAL DATASET FROM aidata.csv")
    print("=" * 80)
    
    csv_path = "data/raw/aidata.csv"
    if not os.path.exists(csv_path):
        print(f"ERROR: Dataset not found at {csv_path}")
        return None
    
    print(f"Loading dataset from: {csv_path}")
    
    # Load with optimized dtypes for memory efficiency
    dtype_optimizations = {
        'agent': 'category',
        'state': 'category',
        'user': 'string',
        'title': 'string',
        'body': 'string'
    }
    
    df = pd.read_csv(csv_path, low_memory=False, dtype=dtype_optimizations)
    
    print(f"✓ Dataset loaded successfully!")
    print(f"✓ Total records: {len(df):,}")
    print(f"✓ Columns: {list(df.columns)}")
    print(f"✓ Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    return df

def compute_real_statistics(df):
    """Compute REAL statistics from the actual dataset"""
    print("\n" + "=" * 80)
    print("COMPUTING REAL STATISTICS FROM ACTUAL DATA")
    print("=" * 80)
    
    # Basic dataset info
    total_records = len(df)
    print(f"Total Pull Requests: {total_records:,}")
    
    # Agent distribution (REAL NUMBERS)
    agent_counts = df['agent'].value_counts()
    print(f"\nAgent Distribution (REAL COUNTS):")
    for agent, count in agent_counts.items():
        percentage = (count / total_records) * 100
        print(f"  {agent}: {count:,} ({percentage:.2f}%)")
    
    # State distribution
    state_counts = df['state'].value_counts()
    print(f"\nPR State Distribution:")
    for state, count in state_counts.items():
        percentage = (count / total_records) * 100
        print(f"  {state}: {count:,} ({percentage:.2f}%)")
    
    # User statistics (REAL NUMBERS)
    unique_users = df['user'].nunique()
    print(f"\nUser Statistics:")
    print(f"  Unique users: {unique_users:,}")
    
    # PRs per user analysis
    user_pr_counts = df['user'].value_counts()
    print(f"  Average PRs per user: {user_pr_counts.mean():.2f}")
    print(f"  Median PRs per user: {user_pr_counts.median():.2f}")
    print(f"  Max PRs by single user: {user_pr_counts.max()}")
    
    # Top contributors
    print(f"\nTop 10 Users by PR Count:")
    for i, (user, count) in enumerate(user_pr_counts.head(10).items(), 1):
        print(f"  {i}. {user}: {count} PRs")
    
    # Data quality checks
    print(f"\nData Quality Checks:")
    print(f"  Records with missing titles: {df['title'].isna().sum():,}")
    print(f"  Records with missing bodies: {df['body'].isna().sum():,}")
    print(f"  Records with empty titles: {(df['title'] == '').sum():,}")
    print(f"  Records with empty bodies: {(df['body'] == '').sum():,}")
    
    return {
        'total_records': total_records,
        'agent_counts': agent_counts.to_dict(),
        'state_counts': state_counts.to_dict(),
        'unique_users': unique_users,
        'user_statistics': {
            'average_prs_per_user': float(user_pr_counts.mean()),
            'median_prs_per_user': float(user_pr_counts.median()),
            'max_prs_per_user': int(user_pr_counts.max()),
            'top_10_users': user_pr_counts.head(10).to_dict()
        },
        'data_quality': {
            'missing_titles': int(df['title'].isna().sum()),
            'missing_bodies': int(df['body'].isna().sum()),
            'empty_titles': int((df['title'] == '').sum()),
            'empty_bodies': int((df['body'] == '').sum())
        }
    }

def generate_real_visualizations(df, stats):
    """Generate real visualizations from actual data"""
    print("\n" + "=" * 80)
    print("GENERATING REAL VISUALIZATIONS FROM ACTUAL DATA")
    print("=" * 80)
    
    # Set style
    plt.style.use('seaborn-v0_8')
    
    # Create figures directory
    os.makedirs('docs', exist_ok=True)
    
    # 1. Agent Distribution Pie Chart (REAL DATA)
    print("Creating agent distribution pie chart...")
    plt.figure(figsize=(10, 8))
    agent_counts = pd.Series(stats['agent_counts'])
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    wedges, texts, autotexts = plt.pie(agent_counts.values, 
                                       labels=agent_counts.index, 
                                       autopct='%1.1f%%',
                                       startangle=90,
                                       colors=colors[:len(agent_counts)])
    
    plt.title('Distribution of AI Agents in Pull Requests\n(Real Data from aidata.csv)', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add total count
    plt.figtext(0.5, 0.02, f'Total Pull Requests: {stats["total_records"]:,}', 
                ha='center', fontsize=12, style='italic')
    
    plt.tight_layout()
    plt.savefig('docs/real_agent_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: docs/real_agent_distribution.png")
    
    # 2. User Activity Distribution (REAL DATA)
    print("Creating user activity histogram...")
    plt.figure(figsize=(12, 6))
    
    user_pr_counts = df['user'].value_counts()
    
    # Create histogram
    plt.subplot(1, 2, 1)
    plt.hist(user_pr_counts, bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel('Number of PRs per User')
    plt.ylabel('Number of Users')
    plt.title('Distribution of User Activity\n(Real Data)', fontweight='bold')
    plt.yscale('log')
    
    # Create box plot for better view of distribution
    plt.subplot(1, 2, 2)
    plt.boxplot(user_pr_counts, vert=True)
    plt.ylabel('Number of PRs per User')
    plt.title('User Activity Box Plot\n(Real Data)', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('docs/real_user_activity_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: docs/real_user_activity_distribution.png")
    
    # 3. Agent Comparison Bar Chart (REAL DATA)
    print("Creating agent comparison bar chart...")
    plt.figure(figsize=(12, 8))
    
    agent_counts = pd.Series(stats['agent_counts'])
    
    bars = plt.bar(range(len(agent_counts)), agent_counts.values, 
                   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'][:len(agent_counts)])
    
    plt.xlabel('AI Agent', fontweight='bold')
    plt.ylabel('Number of Pull Requests', fontweight='bold')
    plt.title('Pull Request Count by AI Agent\n(Real Data from aidata.csv)', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.xticks(range(len(agent_counts)), agent_counts.index, rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, value in zip(bars, agent_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + value*0.01,
                f'{value:,}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('docs/real_agent_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: docs/real_agent_comparison.png")
    
    plt.close('all')
    print("✓ All visualizations generated successfully!")

def save_real_results(stats):
    """Save real statistics to JSON file"""
    print("\n" + "=" * 80)
    print("SAVING REAL ANALYSIS RESULTS")
    print("=" * 80)
    
    # Add metadata
    results = {
        'analysis_metadata': {
            'analysis_date': datetime.now().isoformat(),
            'dataset_source': 'data/raw/aidata.csv',
            'analysis_type': 'GENUINE_DATASET_ANALYSIS',
            'note': 'These are REAL statistics computed from actual aidata.csv file'
        },
        'statistics': stats
    }
    
    # Save to outputs directory
    os.makedirs('outputs', exist_ok=True)
    output_path = 'outputs/genuine_analysis_results.json'
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✓ Real analysis results saved to: {output_path}")

def main():
    """Main analysis function"""
    print("GENUINE DATASET ANALYSIS")
    print("Computing REAL statistics from actual aidata.csv file")
    print("This replaces all fabricated numbers with genuine analysis")
    
    # Load real dataset
    df = load_real_dataset()
    if df is None:
        return
    
    # Compute real statistics  
    stats = compute_real_statistics(df)
    
    # Generate real visualizations
    generate_real_visualizations(df, stats)
    
    # Save results
    save_real_results(stats)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE - ALL NUMBERS ARE NOW REAL!")
    print("=" * 80)
    print("Key Real Statistics:")
    print(f"  • Total PRs: {stats['total_records']:,}")
    print(f"  • Unique Users: {stats['unique_users']:,}")
    print(f"  • Average PRs/User: {stats['user_statistics']['average_prs_per_user']:.2f}")
    
    print("\nAgent Breakdown (Real Numbers):")
    for agent, count in stats['agent_counts'].items():
        percentage = (count / stats['total_records']) * 100
        print(f"  • {agent}: {count:,} ({percentage:.1f}%)")
    
    print("\nReal visualizations saved:")
    print("  • docs/real_agent_distribution.png")  
    print("  • docs/real_user_activity_distribution.png")
    print("  • docs/real_agent_comparison.png")
    
    print(f"\nReal analysis data: outputs/genuine_analysis_results.json")

if __name__ == "__main__":
    main()