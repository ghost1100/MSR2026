"""
Enhanced Analysis Runner with Claude API Integration
This script provides options to run analysis with or without Claude API
"""

import sys
import argparse
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.append('src')

from data_loader import load_data_efficiently
from claude_analyzer import ClaudeAnalyzer, create_claude_enhanced_analysis

def run_enhanced_analysis(use_claude=True, sample_size=2000, output_dir='outputs'):
    """
    Run enhanced MSR analysis with optional Claude integration
    
    Args:
        use_claude (bool): Whether to use Claude API for intelligent analysis
        sample_size (int): Number of PRs to analyze (for Claude analysis)
        output_dir (str): Directory to save results
    """
    print("🚀 Starting Enhanced MSR Analysis")
    print(f"🔬 Analysis mode: {'Claude-Enhanced' if use_claude else 'Statistical Only'}")
    print(f"📊 Sample size: {sample_size}")
    
    # Load data
    print("\n📂 Loading data...")
    df = load_data_efficiently()
    print(f"✅ Loaded {len(df)} records")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    figures_path = output_path / 'figures'
    figures_path.mkdir(exist_ok=True)
    
    # Basic statistical analysis
    print("\n📊 Running basic statistical analysis...")
    basic_stats = {
        'total_prs': len(df),
        'unique_agents': df['agent'].nunique(),
        'agent_distribution': df['agent'].value_counts().to_dict(),
        'avg_title_length': df['title'].str.len().mean(),
        'avg_body_length': df['body'].str.len().mean()
    }
    
    print(f"   Total PRs: {basic_stats['total_prs']:,}")
    print(f"   Unique Agents: {basic_stats['unique_agents']}")
    print(f"   Avg Title Length: {basic_stats['avg_title_length']:.1f} chars")
    print(f"   Avg Body Length: {basic_stats['avg_body_length']:.1f} chars")
    
    results = {'basic_stats': basic_stats}
    
    # Claude analysis (if enabled)
    if use_claude:
        try:
            print(f"\n🤖 Running Claude-Enhanced Analysis (sample size: {sample_size})...")
            claude_results = create_claude_enhanced_analysis(df, sample_size=sample_size)
            results['claude_analysis'] = claude_results
            
            print("✅ Claude analysis completed successfully!")
            print(f"   📊 Classified {claude_results['sample_size']} PRs")
            print(f"   🎯 Mean confidence: {claude_results['confidence_stats']['mean_confidence']:.2f}")
            print(f"   🏆 High confidence rate: {claude_results['confidence_stats']['high_confidence_rate']:.1%}")
            
        except Exception as e:
            print(f"❌ Claude analysis failed: {e}")
            print("📊 Continuing with statistical analysis only...")
            results['claude_error'] = str(e)
    
    # Save results
    import json
    results_file = output_path / 'enhanced_analysis_results.json'
    
    # Prepare JSON-serializable results
    json_results = {
        'basic_stats': basic_stats,
        'analysis_mode': 'claude_enhanced' if use_claude else 'statistical_only',
        'sample_size': sample_size if use_claude else len(df)
    }
    
    if 'claude_analysis' in results:
        json_results['claude_summary'] = {
            'type_distribution': results['claude_analysis']['type_distribution'],
            'confidence_stats': results['claude_analysis']['confidence_stats'],
            'agent_quality_summary': {
                agent: {
                    'quality_score': analysis['quality_score'],
                    'consistency_score': analysis['consistency_score'],
                    'pattern_count': len(analysis['patterns'])
                }
                for agent, analysis in results['claude_analysis']['agent_analysis'].items()
            },
            'sample_size': results['claude_analysis']['sample_size']
        }
        
        # Save detailed classified data
        classified_data_file = output_path / 'claude_classified_data.csv'
        results['claude_analysis']['classified_data'].to_csv(classified_data_file, index=False)
        print(f"💾 Classified data saved to: {classified_data_file}")
    
    with open(results_file, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    return results

def main():
    parser = argparse.ArgumentParser(description='Enhanced MSR Analysis with Claude Integration')
    parser.add_argument('--use-claude', action='store_true', default=True,
                       help='Use Claude API for enhanced analysis (default: True)')
    parser.add_argument('--no-claude', action='store_true',
                       help='Skip Claude API, use statistical analysis only')
    parser.add_argument('--sample-size', type=int, default=2000,
                       help='Sample size for Claude analysis (default: 2000)')
    parser.add_argument('--output-dir', type=str, default='outputs',
                       help='Output directory for results (default: outputs)')
    
    args = parser.parse_args()
    
    # Determine Claude usage
    use_claude = args.use_claude and not args.no_claude
    
    # Run analysis
    try:
        results = run_enhanced_analysis(
            use_claude=use_claude,
            sample_size=args.sample_size,
            output_dir=args.output_dir
        )
        print("\n🎉 Analysis completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()