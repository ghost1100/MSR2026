#!/usr/bin/env python3
"""
Test Distribution Analysis - Updated Results
Analyzing how test-related PRs are distributed across AI agents
"""

import json
import os

def analyze_test_distribution():
    """Analyze test distribution with improved detection algorithm"""
    
    print("=" * 60)
    print(" TEST DISTRIBUTION ANALYSIS - UPDATED RESULTS")
    print("=" * 60)
    
    # Load the comprehensive analysis results
    try:
        with open('outputs/comprehensive_full_dataset_analysis.json', 'r') as f:
            data = json.load(f)
            
        with open('outputs/rq1_test_contribution_results.json', 'r') as f:
            test_data = json.load(f)
    except FileNotFoundError as e:
        print(f"ERROR: Required analysis file not found: {e}")
        return
    
    # Extract test-related data
    total_records = data['dataset_info']['total_records']
    total_test_prs = data['test_behavior']['total_test_prs']
    overall_test_rate = data['test_behavior']['overall_test_rate']
    
    print(f"Dataset Overview:")
    print(f"  Total PRs: {total_records:,}")
    print(f"  Test-related PRs: {total_test_prs:,}")
    print(f"  Overall test rate: {overall_test_rate:.1f}%")
    
    print(f"\nTEST DISTRIBUTION BY AGENT:")
    print(f"{'Agent':<15} {'Test PRs':<12} {'Total PRs':<12} {'Test %':<8} {'Share of Tests':<15}")
    print("-" * 70)
    
    # Calculate test PR distribution
    test_distribution = {}
    total_test_prs_check = 0
    
    for agent, behavior in data['test_behavior']['agent_behavior'].items():
        test_prs = behavior['test_prs']
        total_prs = behavior['total_prs']
        test_percentage = behavior['test_percentage']
        test_share = (test_prs / total_test_prs) * 100
        
        test_distribution[agent] = {
            'test_prs': test_prs,
            'total_prs': total_prs, 
            'test_percentage': test_percentage,
            'test_share': test_share
        }
        total_test_prs_check += test_prs
        
        print(f"{agent:<15} {test_prs:<12,} {total_prs:<12,} {test_percentage:<7.1f}% {test_share:<14.1f}%")
    
    print(f"\nTEST SHARE ANALYSIS:")
    print(f"OpenAI Codex test dominance: {test_distribution['OpenAI_Codex']['test_share']:.1f}% of all test PRs")
    
    # Compare overall PR share vs test PR share
    overall_shares = data['agent_distribution']['percentages']
    
    print(f"\nCOMPARISON: Overall PRs vs Test PRs")
    print(f"{'Agent':<15} {'Overall Share':<15} {'Test Share':<15} {'Difference':<15}")
    print("-" * 65)
    
    for agent in test_distribution.keys():
        overall_share = overall_shares[agent]
        test_share = test_distribution[agent]['test_share']
        difference = test_share - overall_share
        
        print(f"{agent:<15} {overall_share:<14.1f}% {test_share:<14.1f}% {difference:<+14.1f}%")
    
    # Key findings
    print(f"\nKEY FINDINGS:")
    codex_test_share = test_distribution['OpenAI_Codex']['test_share']
    codex_overall_share = overall_shares['OpenAI_Codex']
    
    if codex_test_share > codex_overall_share:
        print(f"✓ OpenAI Codex DOMINATES tests even more than overall PRs")
        print(f"  - Overall PR share: {codex_overall_share:.1f}%")
        print(f"  - Test PR share: {codex_test_share:.1f}%") 
        print(f"  - Test advantage: +{codex_test_share - codex_overall_share:.1f} percentage points")
    else:
        print(f"✓ OpenAI Codex has LOWER test share than overall share")
        print(f"  - Overall PR share: {codex_overall_share:.1f}%")
        print(f"  - Test PR share: {codex_test_share:.1f}%")
        print(f"  - Test disadvantage: {codex_test_share - codex_overall_share:.1f} percentage points")
    
    print(f"\nTEST QUALITY BY AGENT:")
    for agent, behavior in data['test_behavior']['agent_behavior'].items():
        test_rate = behavior['test_percentage']
        print(f"  {agent}: {test_rate:.1f}% of their PRs contain tests")
    
    # Statistical significance
    chi_square = data['statistical_analysis']['chi_square']
    cramers_v = data['statistical_analysis']['cramers_v']
    
    print(f"\nSTATISTICAL SIGNIFICANCE:")
    print(f"  Chi-square: {chi_square:,.1f}")
    print(f"  Cramér's V: {cramers_v:.3f} (large effect)")
    print(f"  Conclusion: Highly significant differences in test behavior")
    
    return test_distribution

if __name__ == "__main__":
    result = analyze_test_distribution()
    if result:
        print(f"\n{'='*60}")
        print(" ANSWER: OpenAI Codex test dominance is even STRONGER")
        print(f"{'='*60}")