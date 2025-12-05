"""
Script to download the AIDev dataset from HuggingFace
Run this first before running any analysis scripts
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import load_aidev

if __name__ == "__main__":
    print("=" * 60)
    print("Downloading AIDev dataset from HuggingFace...")
    print("=" * 60)
    
    # Download from HuggingFace and save locally
    df = load_aidev(
        local_path="data/raw/aidata.csv",
        from_huggingface=True,
        config="all_pull_request"
    )
    
    if df is not None:
        print("\n" + "=" * 60)
        print(f"✓ Successfully downloaded {len(df):,} records")
        print(f"✓ Dataset saved to: data/raw/aidata.csv")
        print("=" * 60)
        print("\nYou can now run:")
        print("  - comprehensive_full_analysis.py")
        print("  - regenerate_pie_chart.py")
        print("  - Any other analysis scripts")
    else:
        print("\n✗ Failed to download dataset")
        sys.exit(1)
