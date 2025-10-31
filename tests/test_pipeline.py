#!/usr/bin/env python3
"""
Simple pipeline test for MSR project with progressive scaling
"""
import os
import sys
import time
from datetime import datetime

# Add src directory to path
sys.path.append('src')
from data_loader import load_aidev
from analysis import analyze_test_contributions
from cache_utils import SmartCache

def test_pipeline(sample_size=1000):
    """Test the complete analysis pipeline with specified sample size"""
    print("MSR Project Pipeline Test")
    print("=" * 50)
    print(f"Sample size: {sample_size:,} rows")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Load data
        print(f"\n[1/4] Loading data sample...")
        start_time = time.time()
        df = load_aidev(sample_size=sample_size)
        load_time = time.time() - start_time
        print(f"   Loaded {len(df):,} rows in {load_time:.2f}s")
        
        # 2. Run test contribution analysis
        print(f"\n[2/4] Analyzing test contributions...")
        analysis_start = time.time()
        df_analyzed, test_stats = analyze_test_contributions(df, use_cache=True)
        analysis_time = time.time() - analysis_start
        print(f"   Analysis completed in {analysis_time:.2f}s")
        
        # 3. Display results
        print(f"\n[3/4] Results summary:")
        print(f"   Total PRs: {len(df_analyzed):,}")
        print(f"   Test PRs: {test_stats['Test_PRs'].sum():,}")
        print(f"   Test ratio: {(test_stats['Test_PRs'].sum() / len(df_analyzed) * 100):.1f}%")
        print(f"   Memory usage: {df_analyzed.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        # 4. Agent breakdown
        print(f"\n[4/4] Agent breakdown:")
        for agent in test_stats.index:
            print(f"   {agent}: {test_stats.loc[agent, 'Test_PRs']} test PRs / {test_stats.loc[agent, 'Total_PRs']} total ({test_stats.loc[agent, 'Test_Percentage']}%)")
        
        print(f"\n[SUCCESS] Pipeline test completed!")
        print(f"Total time: {load_time + analysis_time:.2f}s")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Get sample size from environment or command line
    sample_size = int(os.getenv('SAMPLE_SIZE', '1000'))
    
    if len(sys.argv) > 1:
        sample_size = int(sys.argv[1])
    
    success = test_pipeline(sample_size)
    sys.exit(0 if success else 1)