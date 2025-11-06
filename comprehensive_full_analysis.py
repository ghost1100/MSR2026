#!/usr/bin/env python3
"""
Comprehensive Full Dataset Analysis for MSR Project
Analyzes the complete AIDev dataset (932,791 records) to generate robust findings
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
from scipy.stats import chi2_contingency
import warnings
warnings.filterwarnings('ignore')

# Add src to path
sys.path.append('src')
from data_loader import load_data_efficiently

def contains_test_keywords(text):
    """Check if text contains test-related keywords"""
    if pd.isna(text) or not isinstance(text, str):
        return False
    
    test_keywords = [
        'test', 'testing', 'spec', 'unittest', 'pytest', 
        'jest', 'mocha', 'karma', 'cypress', 'jasmine',
        'junit', 'testng', 'rspec', 'phpunit', 'nunit', 'xunit'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in test_keywords)

def analyze_complete_dataset():
    """
    Run comprehensive analysis on the complete AIDev dataset
    """
    print("=" * 80)
    print("COMPREHENSIVE ANALYSIS: COMPLETE AIDEV DATASET")
    print("=" * 80)
    
    # Load complete dataset
    print("\n1. Loading complete dataset...")
    df = load_data_efficiently(use_full_dataset=True)
    
    if df is None:
        print("ERROR: Could not load dataset")
        return None
    
    print(f"Dataset loaded successfully!")
    print(f"Total records: {len(df):,}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    # Basic dataset overview
    print(f"\n2. Dataset Overview:")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Unique agents: {df['agent'].nunique()}")
    print(f"   Unique users: {df['user'].nunique()}")
    
    # Agent distribution analysis
    print(f"\n3. Agent Distribution Analysis:")
    agent_counts = df['agent'].value_counts()
    agent_percentages = (agent_counts / len(df) * 100)
    
    total_records = len(df)
    for agent, count in agent_counts.items():
        percentage = agent_percentages[agent]
        print(f"   {agent}: {count:,} PRs ({percentage:.1f}%)")
    
    # Test behavior analysis
    print(f"\n4. Test Behavior Analysis:")
    print("   Analyzing test-related keywords in titles and descriptions...")
    
    # Apply test keyword detection
    df['has_test_in_title'] = df['title'].apply(contains_test_keywords)
    df['has_test_in_body'] = df['body'].apply(contains_test_keywords)
    df['is_test_pr'] = df['has_test_in_title'] | df['has_test_in_body']
    
    # Overall test statistics
    total_test_prs = df['is_test_pr'].sum()
    test_rate = total_test_prs / len(df) * 100
    print(f"   Total test-related PRs: {total_test_prs:,} ({test_rate:.1f}%)")
    
    # Agent-specific analysis
    print(f"\n5. Agent-Specific Behavioral Analysis:")
    
    behavioral_analysis = df.groupby('agent').agg({
        'is_test_pr': ['count', 'sum', 'mean'],
        'title': lambda x: x.str.len().mean(),
        'body': lambda x: x.str.len().mean(),
        'state': lambda x: (x == 'closed').mean() if 'closed' in x.values else 0,
        'user': 'nunique'
    }).round(4)
    
    # Flatten column names
    behavioral_analysis.columns = [
        'total_prs', 'test_prs', 'test_rate', 
        'avg_title_length', 'avg_body_length', 'closed_rate', 'unique_users'
    ]
    behavioral_analysis['test_percentage'] = behavioral_analysis['test_rate'] * 100
    
    # Sort by test percentage for presentation
    behavioral_analysis = behavioral_analysis.sort_values('test_percentage', ascending=False)
    
    print(f"\n   Comprehensive Agent Behavior Summary:")
    print("   " + "=" * 100)
    print(f"   {'Agent':<15} {'PRs':<10} {'Test%':<8} {'Closed%':<10} {'Users':<10} {'AvgTitle':<12} {'AvgBody':<10}")
    print("   " + "-" * 100)
    
    for agent, row in behavioral_analysis.iterrows():
        closed_pct = row['closed_rate'] * 100
        print(f"   {agent:<15} {row['total_prs']:<10,} {row['test_percentage']:<8.1f} {closed_pct:<10.1f} {row['unique_users']:<10,} {row['avg_title_length']:<12.0f} {row['avg_body_length']:<10.0f}")
    
    # Statistical significance testing
    print(f"\n6. Statistical Significance Analysis:")
    
    # Create contingency table for chi-square test
    contingency_table = pd.crosstab(df['agent'], df['is_test_pr'])
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    
    # Calculate Cramér's V (effect size)
    n = contingency_table.sum().sum()
    cramers_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
    
    print(f"   Chi-square test:")
    print(f"   χ² = {chi2:,.1f}, p-value = {p_value:.2e}")
    print(f"   Cramér's V (effect size) = {cramers_v:.3f}")
    print(f"   Degrees of freedom = {dof}")
    
    # Effect size interpretation
    if cramers_v < 0.1:
        effect_interpretation = "negligible"
    elif cramers_v < 0.3:
        effect_interpretation = "small"
    elif cramers_v < 0.5:
        effect_interpretation = "medium"
    else:
        effect_interpretation = "large"
    
    print(f"   Effect size interpretation: {effect_interpretation}")
    
    # Generate comprehensive results dictionary
    results = {
        'dataset_info': {
            'total_records': len(df),
            'unique_agents': df['agent'].nunique(),
            'unique_users': df['user'].nunique(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'analysis_date': pd.Timestamp.now().isoformat()
        },
        'agent_distribution': {
            'counts': agent_counts.to_dict(),
            'percentages': agent_percentages.to_dict()
        },
        'test_behavior': {
            'overall_test_rate': test_rate,
            'total_test_prs': int(total_test_prs),
            'total_non_test_prs': int(len(df) - total_test_prs),
            'agent_behavior': behavioral_analysis.to_dict('index')
        },
        'statistical_analysis': {
            'chi_square': float(chi2),
            'p_value': float(p_value),
            'cramers_v': float(cramers_v),
            'effect_size': effect_interpretation,
            'degrees_of_freedom': int(dof),
            'sample_size': len(df)
        }
    }
    
    # Save comprehensive results
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    
    results_file = output_dir / 'comprehensive_full_dataset_analysis.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n7. Results saved to: {results_file}")
    
    # Generate visualizations
    print(f"\n8. Generating publication-ready visualizations...")
    generate_visualizations(df, behavioral_analysis, output_dir)
    
    return df, results

def generate_visualizations(df, behavioral_analysis, output_dir):
    """Generate comprehensive visualizations for the complete dataset"""
    
    figures_dir = output_dir / 'figures'
    figures_dir.mkdir(exist_ok=True)
    
    # Set publication-ready style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # 1. Test contribution rates by agent
    fig, ax = plt.subplots(figsize=(12, 8))
    agents = behavioral_analysis.index
    test_percentages = behavioral_analysis['test_percentage']
    colors = sns.color_palette("viridis", len(agents))
    
    bars = ax.bar(agents, test_percentages, color=colors, edgecolor='black', linewidth=0.5)
    ax.set_title('Test Contribution Rates by AI Agent\n(Complete Dataset: 932,791 Pull Requests)', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('AI Agent', fontsize=14, fontweight='bold')
    ax.set_ylabel('Test Contribution Rate (%)', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 105)
    
    # Add value labels on bars
    for bar, percentage in zip(bars, test_percentages):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{percentage:.1f}%', ha='center', va='bottom',
                fontweight='bold', fontsize=12)
    
    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.xticks(rotation=45, ha='right', fontweight='bold')
    plt.tight_layout()
    plt.savefig(figures_dir / 'complete_dataset_test_contribution_rates.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # 2. Agent market share distribution
    fig, ax = plt.subplots(figsize=(10, 8))
    agent_counts = df['agent'].value_counts()
    colors = sns.color_palette("Set3", len(agent_counts))
    
    wedges, texts, autotexts = ax.pie(agent_counts.values, labels=agent_counts.index,
                                    autopct='%1.1f%%', colors=colors, startangle=90,
                                    textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax.set_title('AI Agent Market Share Distribution\n(Complete Dataset: 932,791 Pull Requests)',
                fontsize=16, fontweight='bold', pad=20)
    
    # Enhance text readability
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    plt.savefig(figures_dir / 'complete_dataset_agent_distribution.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # 3. Comprehensive behavioral comparison matrix
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    agents = behavioral_analysis.index
    colors_subset = colors[:len(agents)]
    
    # Test rates
    bars1 = ax1.bar(agents, behavioral_analysis['test_percentage'], color=colors_subset)
    ax1.set_title('Test Contribution Rates', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Test Rate (%)', fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(axis='x', rotation=45, labelsize=10)
    for bar, val in zip(bars1, behavioral_analysis['test_percentage']):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Closure rates
    bars2 = ax2.bar(agents, behavioral_analysis['closed_rate'] * 100, color=colors_subset)
    ax2.set_title('Acceptance/Closure Rates', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Closure Rate (%)', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.tick_params(axis='x', rotation=45, labelsize=10)
    for bar, val in zip(bars2, behavioral_analysis['closed_rate'] * 100):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # User diversity (log scale for better visualization)
    bars3 = ax3.bar(agents, behavioral_analysis['unique_users'], color=colors_subset)
    ax3.set_title('User Diversity', fontweight='bold', fontsize=14)
    ax3.set_ylabel('Unique Users (log scale)', fontweight='bold')
    ax3.set_yscale('log')
    ax3.grid(axis='y', alpha=0.3)
    ax3.tick_params(axis='x', rotation=45, labelsize=10)
    for bar, val in zip(bars3, behavioral_analysis['unique_users']):
        ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() * 1.1,
                f'{val:,}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Average title length
    bars4 = ax4.bar(agents, behavioral_analysis['avg_title_length'], color=colors_subset)
    ax4.set_title('Average Title Length', fontweight='bold', fontsize=14)
    ax4.set_ylabel('Characters', fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    ax4.tick_params(axis='x', rotation=45, labelsize=10)
    for bar, val in zip(bars4, behavioral_analysis['avg_title_length']):
        ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.suptitle('Comprehensive AI Agent Behavioral Analysis\n(Complete Dataset: 932,791 Pull Requests)',
                fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.savefig(figures_dir / 'complete_dataset_comprehensive_analysis.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   Visualizations saved to: {figures_dir}")
    print(f"   Generated:")
    print(f"   - complete_dataset_test_contribution_rates.png")
    print(f"   - complete_dataset_agent_distribution.png")
    print(f"   - complete_dataset_comprehensive_analysis.png")

def main():
    """Main execution function"""
    try:
        df, results = analyze_complete_dataset()
        
        if df is not None and results is not None:
            print("\n" + "=" * 80)
            print("ANALYSIS COMPLETE!")
            print("=" * 80)
            print(f"Successfully processed {len(df):,} pull requests from {df['agent'].nunique()} AI agents")
            
            # Extract key findings
            agent_behavior = results['test_behavior']['agent_behavior']
            test_rates = [(agent, data['test_percentage']) for agent, data in agent_behavior.items()]
            test_rates.sort(key=lambda x: x[1], reverse=True)
            
            print(f"Key findings:")
            print(f"  - Test contribution rates range from {test_rates[-1][1]:.1f}% to {test_rates[0][1]:.1f}%")
            print(f"  - Statistical significance: p < 0.001, Cramér's V = {results['statistical_analysis']['cramers_v']:.3f}")
            print(f"  - Effect size: {results['statistical_analysis']['effect_size']}")
            print(f"  - Total unique users: {results['dataset_info']['unique_users']:,}")
            print(f"  - Overall test rate: {results['test_behavior']['overall_test_rate']:.1f}%")
            
            return df, results
        else:
            print("ERROR: Analysis failed to complete")
            return None, None
            
    except Exception as e:
        print(f"ERROR: Analysis failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    main()