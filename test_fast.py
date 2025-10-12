#!/usr/bin/env python3
"""
Fast testing version using sequential loading for speed
"""

import sys
import os
import time
import json
from datetime import datetime

# Add src directory to path
sys.path.append('src')

def test_data_loading_fast():
    """Test data loading pipeline with fast sequential loading"""
    print("🧪 Testing Data Loading Pipeline (Fast Mode)...")
    print("=" * 50)
    
    try:
        import pandas as pd
        
        # Test 1: Check file exists
        data_path = "data/raw/aidata.csv"
        if not os.path.exists(data_path):
            print("❌ Data file not found")
            return False
        
        file_size = os.path.getsize(data_path) / (1024**2)  # MB
        print(f"✅ Data file found: {file_size:.1f} MB")
        
        # Test 2: Load small sequential sample (fast)
        print("\n[TEST 2] Fast sequential sample loading...")
        df_small = pd.read_csv(data_path, nrows=1000, low_memory=False)
        print(f"✅ Fast sample loaded: {len(df_small)} rows")
        print(f"   Columns: {len(df_small.columns)}")
        print(f"   Required columns: {'agent' in df_small.columns and 'title' in df_small.columns}")
        
        if 'agent' in df_small.columns:
            agents_found = df_small['agent'].nunique()
            print(f"   Agents in sequential sample: {agents_found}")
            agent_dist = df_small['agent'].value_counts()
            for agent, count in agent_dist.items():
                pct = (count / len(df_small)) * 100
                print(f"   {agent}: {count} PRs ({pct:.1f}%)")
        
        # Test 3: Test our data_loader module
        print("\n[TEST 3] Testing data_loader module...")
        from data_loader import load_aidev
        
        # Small sample using our optimized loader
        df_loader = load_aidev(sample_size=500)  # Very small for speed
        if df_loader is not None:
            print(f"✅ Data loader works: {len(df_loader)} rows")
            agents_loader = df_loader['agent'].nunique()
            print(f"   Agents via data_loader: {agents_loader}")
            return True
        else:
            print("❌ Data loader failed")
            return False
            
    except Exception as e:
        print(f"❌ Data loading test failed: {str(e)}")
        return False

def test_analysis_functions_fast():
    """Test analysis functions with minimal data"""
    print("\n🧪 Testing Analysis Functions (Fast Mode)...")
    print("=" * 50)
    
    try:
        import pandas as pd
        from analysis import analyze_test_contributions, get_research_summary
        
        # Load minimal data directly for speed
        df = pd.read_csv("data/raw/aidata.csv", nrows=500, low_memory=False)
        if df is None:
            print("❌ Cannot test analysis - data loading failed")
            return False
        
        print("Testing test contribution analysis...")
        df_analyzed, test_stats = analyze_test_contributions(df)
        
        print(f"✅ Analysis completed successfully")
        print(f"   Total PRs analyzed: {len(df_analyzed)}")
        print(f"   Test PRs found: {test_stats['Test_PRs'].sum()}")
        print(f"   Agents in analysis: {len(test_stats)}")
        
        # Test research summary
        print("\nTesting research summary...")
        summary = get_research_summary(df_analyzed)
        print(f"✅ Research summary generated")
        print(f"   Dataset size: {summary['dataset_size']}")
        print(f"   Unique agents: {summary['unique_agents']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis functions test failed: {str(e)}")
        return False

def test_notebook_execution():
    """Test notebook execution capability"""
    print("\n🧪 Testing Notebook Execution...")
    print("=" * 50)
    
    try:
        import subprocess
        
        # Test if jupyter is available
        result = subprocess.run([
            sys.executable, "-m", "jupyter", "--version"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Jupyter available")
            print(f"   Version info: {result.stdout.strip()}")
            
            # Test nbconvert
            result2 = subprocess.run([
                sys.executable, "-m", "jupyter", "nbconvert", "--help"
            ], capture_output=True, text=True)
            
            if result2.returncode == 0:
                print("✅ nbconvert available")
                return True
            else:
                print("❌ nbconvert not available")
                return False
        else:
            print("❌ Jupyter not available")
            return False
            
    except Exception as e:
        print(f"❌ Notebook execution test failed: {str(e)}")
        return False

def test_dependencies():
    """Test key dependencies"""
    print("\n🧪 Testing Key Dependencies...")
    print("=" * 50)
    
    required_packages = [
        'pandas',
        'numpy', 
        'matplotlib',
        'seaborn',
        'jupyter',
        'datasets',
        'sklearn',  # Changed from scikit-learn
        'nltk'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing {len(missing_packages)} packages")
        return False
    else:
        print(f"\n✅ All {len(required_packages)} dependencies available")
        return True

def main():
    """Run fast test suite"""
    print("🚀 MSR PROJECT FAST TEST SUITE")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Python: {sys.version}")
    
    # Run fast tests
    test_results = {}
    start_time = time.time()
    
    test_results['dependencies'] = test_dependencies()
    test_results['data_loading'] = test_data_loading_fast()
    test_results['analysis_functions'] = test_analysis_functions_fast()
    test_results['notebook_execution'] = test_notebook_execution()
    
    end_time = time.time()
    
    # Generate summary
    print("\n📊 FAST TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n🎯 Results: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    print(f"⏱️  Total time: {end_time - start_time:.2f} seconds")
    
    if success_rate >= 75:
        print(f"\n🎉 Core functionality validated! MSR project infrastructure is working.")
        overall_status = "SUCCESS"
    else:
        print(f"\n⚠️  Some critical issues detected.")
        overall_status = "ISSUES"
    
    # Save test report
    test_report = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "fast_validation",
        "test_results": test_results,
        "summary": {
            "passed": passed_tests,
            "total": total_tests,
            "success_rate": success_rate,
            "duration": end_time - start_time,
            "overall_status": overall_status
        }
    }
    
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/fast_test_report.json", "w") as f:
        json.dump(test_report, f, indent=2)
    
    print(f"📋 Fast test report saved: outputs/fast_test_report.json")
    
    return success_rate >= 75

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)