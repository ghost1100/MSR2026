#!/usr/bin/env python3
"""
Claude-Enhanced Analysis Runner for MSR Project
Executes AI-powered analysis pipeline on AIDev dataset with intelligent sampling
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src directory to Python path
sys.path.append('src')

def main():
    """
    Execute Claude-enhanced analysis pipeline with error handling and results management.
    
    Pipeline stages:
    1. Environment validation (API key, dependencies)
    2. Data loading with intelligent sampling
    3. Claude-powered PR classification and agent analysis
    4. Results export and summary generation
    """
    print("MSR Claude-Enhanced Analysis")
    print("=" * 50)
    
    # Validate Claude API credentials
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("ANTHROPIC_API_KEY not found in .env file")
        print("Please ensure your .env file contains a valid Claude API key")
        sys.exit(1)
    
    print("Claude API key found")
    
    # Validate required dependencies
    try:
        from claude_analyzer import create_claude_enhanced_analysis
        from data_loader import load_aidev
        print("Dependencies available")
    except ImportError as e:
        print(f"Missing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Load AIDev dataset with error handling
    print("\nLoading data...")
    try:
        df = load_aidev()
        print(f"Loaded {len(df):,} PR records")
    except Exception as e:
        print(f"Failed to load data: {e}")
        sys.exit(1)
    
    # Execute Claude analysis pipeline
    print("\nStarting Claude-Enhanced Analysis...")
    print("This will analyze PR types, consistency, and agent patterns")
    
    # Configure sample size for cost optimization
    sample_size = 2000  # Adjust based on API budget and analysis needs
    print(f"Analyzing sample of {sample_size:,} PRs (from {len(df):,} total)")
    
    try:
        results = create_claude_enhanced_analysis(df, sample_size=sample_size)
        
        print("\nAnalysis Complete!")
        print("=" * 50)
        
        # Display comprehensive results summary
        print("SUMMARY RESULTS:")
        print(f"   Sample Size: {results['sample_size']:,} PRs")
        print(f"   Total Dataset: {results['total_size']:,} PRs")
        print(f"   Mean Confidence: {results['confidence_stats']['mean_confidence']:.2f}")
        print(f"   High Confidence Rate: {results['confidence_stats']['high_confidence_rate']:.1%}")
        
        print("\nPR TYPE DISTRIBUTION:")
        for pr_type, count in results['type_distribution'].items():
            percentage = count / results['sample_size'] * 100
            print(f"   {pr_type.capitalize()}: {count} ({percentage:.1f}%)")
        
        print("\nAGENT QUALITY SCORES:")
        for agent, analysis in results['agent_analysis'].items():
            print(f"   {agent}: Quality {analysis['quality_score']:.1f}/10, Consistency {analysis['consistency_score']:.1f}/10")
        
        # Export results for further analysis
        output_dir = Path('outputs')
        output_dir.mkdir(exist_ok=True)
        
        # Save detailed classifications for research use
        classified_file = output_dir / 'claude_enhanced_classifications.csv'
        results['classified_data'].to_csv(classified_file, index=False)
        
        # Save summary statistics and insights
        import json
        summary_file = output_dir / 'claude_analysis_summary.json'
        summary_data = {
            'type_distribution': results['type_distribution'],
            'confidence_stats': results['confidence_stats'],
            'agent_analysis': results['agent_analysis'],
            'sample_size': results['sample_size'],
            'total_size': results['total_size']
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"\nResults saved to:")
        print(f"   Classifications: {classified_file}")
        print(f"   Summary: {summary_file}")
        
        print("\nNext Steps:")
        print("   1. Review the classification results in the CSV file")
        print("   2. Run the Claude_Enhanced_Analysis.ipynb notebook for detailed visualizations")
        print("   3. Integrate insights into your research questions")
        
    except Exception as e:
        print(f"\nAnalysis failed: {e}")
        print("Please check your API key and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()