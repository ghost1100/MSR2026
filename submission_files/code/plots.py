# Visualization functions for AIDev dataset analysis
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_agent_distribution(df, figsize=(12, 8)):
    """Plot agent distribution analysis"""
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Agent counts
    agent_counts = df['agent'].value_counts()
    agent_counts.plot(kind='pie', ax=axes[0], autopct='%1.1f%%', startangle=90)
    axes[0].set_title(' Agent Distribution')
    axes[0].set_ylabel('')
    
    # State distribution
    state_counts = df['state'].value_counts()
    state_counts.plot(kind='bar', ax=axes[1], color=['lightgreen', 'lightcoral', 'lightblue'])
    axes[1].set_title(' PR State Distribution')
    axes[1].set_xlabel('PR State')
    axes[1].set_ylabel('Count')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def plot_test_analysis(df, figsize=(15, 12)):
    """Plot comprehensive test analysis"""
    if 'is_test_pr' not in df.columns:
        print("Error: 'is_test_pr' column not found. Run analyze_test_contributions() first.")
        return None
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Test vs Non-test PRs
    test_counts = df['is_test_pr'].value_counts()
    test_counts.index = ['Non-Test PRs', 'Test PRs']
    test_counts.plot(kind='pie', ax=axes[0,0], autopct='%1.1f%%', colors=['lightcoral', 'lightgreen'])
    axes[0,0].set_title(' Test vs Non-Test PRs')
    axes[0,0].set_ylabel('')
    
    # Test PRs by Agent
    test_by_agent = df.groupby('agent')['is_test_pr'].sum()
    test_by_agent.plot(kind='bar', ax=axes[0,1], color='skyblue')
    axes[0,1].set_title(' Test PRs by Agent')
    axes[0,1].set_xlabel('Agent')
    axes[0,1].set_ylabel('Number of Test PRs')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Test percentage by Agent
    test_pct_by_agent = df.groupby('agent')['is_test_pr'].mean() * 100
    test_pct_by_agent.plot(kind='bar', ax=axes[1,0], color='orange')
    axes[1,0].set_title(' Test Contribution Rate by Agent (%)')
    axes[1,0].set_xlabel('Agent')
    axes[1,0].set_ylabel('Test PR Percentage')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Agent vs State heatmap
    agent_state_crosstab = pd.crosstab(df['agent'], df['state'])
    sns.heatmap(agent_state_crosstab, annot=True, fmt='d', ax=axes[1,1], cmap='Blues')
    axes[1,1].set_title(' Agent vs PR State Heatmap')
    
    plt.tight_layout()
    return fig

def plot_timeline_analysis(df, figsize=(15, 12)):
    """Plot timeline analysis if datetime columns are available"""
    if 'created_at' not in df.columns:
        print("Error: 'created_at' column not found.")
        return None
    
    try:
        df = df.copy()
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['created_month'] = df['created_at'].dt.to_period('M')
        df['created_dow'] = df['created_at'].dt.day_name()
        df['created_hour'] = df['created_at'].dt.hour
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        # Monthly trends
        monthly_total = df.groupby('created_month').size()
        monthly_total.plot(kind='line', ax=axes[0,0], marker='o', color='blue')
        axes[0,0].set_title(' PRs per Month')
        axes[0,0].set_xlabel('Month')
        axes[0,0].set_ylabel('Number of PRs')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Day of week patterns
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_counts = df['created_dow'].value_counts().reindex(dow_order)
        dow_counts.plot(kind='bar', ax=axes[0,1], color='green')
        axes[0,1].set_title(' PRs by Day of Week')
        axes[0,1].set_xlabel('Day of Week')
        axes[0,1].set_ylabel('Number of PRs')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Hourly patterns
        hourly_counts = df['created_hour'].value_counts().sort_index()
        hourly_counts.plot(kind='bar', ax=axes[1,0], color='orange')
        axes[1,0].set_title(' PRs by Hour of Day')
        axes[1,0].set_xlabel('Hour')
        axes[1,0].set_ylabel('Number of PRs')
        
        # Agent activity over time
        agent_timeline = df.groupby(['created_month', 'agent']).size().unstack(fill_value=0)
        agent_timeline.plot(kind='line', ax=axes[1,1], marker='o')
        axes[1,1].set_title(' Agent Activity Over Time')
        axes[1,1].set_xlabel('Month')
        axes[1,1].set_ylabel('Number of PRs')
        axes[1,1].legend(title='Agent')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        print(f"Error in timeline analysis: {e}")
        return None

def create_research_dashboard(df, figsize=(20, 15)):
    """Create comprehensive research dashboard"""
    from src.analysis import analyze_test_contributions
    
    # Ensure test analysis is done
    df_analyzed, test_by_agent = analyze_test_contributions(df)
    
    fig, axes = plt.subplots(3, 3, figsize=figsize)
    fig.suptitle(' AIDev Dataset Research Dashboard', fontsize=16, fontweight='bold')
    
    # Row 1: Basic distributions
    agent_counts = df_analyzed['agent'].value_counts()
    agent_counts.plot(kind='bar', ax=axes[0,0], color='skyblue')
    axes[0,0].set_title('Agent Distribution')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    state_counts = df_analyzed['state'].value_counts()
    state_counts.plot(kind='pie', ax=axes[0,1], autopct='%1.1f%%')
    axes[0,1].set_title('PR States')
    
    test_counts = df_analyzed['is_test_pr'].value_counts()
    test_counts.index = ['Non-Test', 'Test']
    test_counts.plot(kind='bar', ax=axes[0,2], color=['coral', 'lightgreen'])
    axes[0,2].set_title('Test vs Non-Test PRs')
    
    # Row 2: Agent analysis
    test_by_agent['Test_PRs'].plot(kind='bar', ax=axes[1,0], color='orange')
    axes[1,0].set_title('Test PRs by Agent')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    test_by_agent['Test_Percentage'].plot(kind='bar', ax=axes[1,1], color='purple')
    axes[1,1].set_title('Test Contribution Rate (%)')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    # Cross-tab heatmap
    crosstab = pd.crosstab(df_analyzed['agent'], df_analyzed['state'])
    sns.heatmap(crosstab, annot=True, fmt='d', ax=axes[1,2], cmap='Blues')
    axes[1,2].set_title('Agent vs State')
    
    # Row 3: Additional insights
    if 'user' in df_analyzed.columns:
        user_counts = df_analyzed['user'].value_counts().head(10)
        user_counts.plot(kind='barh', ax=axes[2,0], color='lightcoral')
        axes[2,0].set_title('Top 10 Contributors')
    
    # Title/body length analysis
    if 'title' in df_analyzed.columns and 'body' in df_analyzed.columns:
        df_analyzed['title_length'] = df_analyzed['title'].str.len()
        df_analyzed['body_length'] = df_analyzed['body'].str.len()
        
        axes[2,1].scatter(df_analyzed['title_length'], df_analyzed['body_length'], alpha=0.6)
        axes[2,1].set_title('Title vs Body Length')
        axes[2,1].set_xlabel('Title Length')
        axes[2,1].set_ylabel('Body Length')
    
    # Summary stats
    summary_text = f"""
    Dataset Summary:
    • Total PRs: {len(df_analyzed):,}
    • Test PRs: {df_analyzed['is_test_pr'].sum():,} ({df_analyzed['is_test_pr'].mean()*100:.1f}%)
    • Agents: {df_analyzed['agent'].nunique()}
    • Users: {df_analyzed['user'].nunique() if 'user' in df_analyzed.columns else 'N/A'}
    • States: {', '.join(df_analyzed['state'].unique())}
    """
    axes[2,2].text(0.1, 0.5, summary_text, transform=axes[2,2].transAxes,
                fontsize=10, verticalalignment='center')
    axes[2,2].set_xlim(0, 1)
    axes[2,2].set_ylim(0, 1)
    axes[2,2].axis('off')
    axes[2,2].set_title('Summary Statistics')
    
    plt.tight_layout()
    return fig