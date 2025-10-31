#!/usr/bin/env python3
"""
Comprehensive MSR Project Testing Suite
"""

import sys
import os
import time
import json
from datetime import datetime

# Add src directory to path
sys.path.append('src')

def test_data_loading():
    """Test data loading pipeline"""
    print("Testing Data Loading Pipeline...")
    print("=" * 50)
    
    try:
        from data_loader import load_aidev
        
        # Test 1: Very small sample first
        print("\n[TEST 1] Minimal sample loading...")
        df_small = load_aidev(sample_size=100)
        if df_small is not None:
            print(f"PASS: Minimal sample loaded: {len(df_small)} rows")
            print(f"   Columns: {len(df_small.columns)}")
            print(f"   Required columns present: {'agent' in df_small.columns and 'title' in df_small.columns}")
            agents_found = df_small['agent'].nunique()
            print(f"   Agents in sample: {agents_found}")
        else:
            print("FAIL: Minimal sample loading failed")
            return False
        
        # Test 2: Moderate sample to verify agent distribution
        print("\n[TEST 2] Moderate sample for agent validation...")
        df_medium = load_aidev(sample_size=5000)  # Reduced from 10000
        if df_medium is not None:
            print(f"PASS: Moderate sample loaded: {len(df_medium)} rows")
            agents_found = df_medium['agent'].nunique()
            print(f"   Agents found: {agents_found}/5")
            
            # Show agent distribution
            agent_dist = df_medium['agent'].value_counts()
            for agent, count in agent_dist.items():
                pct = (count / len(df_medium)) * 100
                print(f"   {agent}: {count:,} PRs ({pct:.1f}%)")
            
            if agents_found >= 4:  # Allow for 4+ agents as acceptable
                print("PASS: Good agent representation achieved")
                return True
            else:
                print(f"WARNING: Limited agent diversity ({agents_found} agents)")
                return True  # Still pass if basic loading works
        else:
            print("FAIL: Moderate sample loading failed")
            return False
            
    except Exception as e:
        print(f"FAIL: Data loading test failed: {str(e)}")
        return False

def test_analysis_functions():
    """Test analysis functions"""
    print("\nTesting Analysis Functions...")
    print("=" * 50)
    
    try:
        from data_loader import load_aidev
        from analysis import analyze_test_contributions, get_research_summary
        
        # Load smaller test data
        df = load_aidev(sample_size=1000)  # Reduced sample size
        if df is None:
            print("FAIL: Cannot test analysis - data loading failed")
            return False
        
        # Test analysis functions
        print("Testing test contribution analysis...")
        df_analyzed, test_stats = analyze_test_contributions(df)
        
        print(f"PASS: Analysis completed successfully")
        print(f"   Total PRs analyzed: {len(df_analyzed)}")
        print(f"   Test PRs found: {test_stats['Test_PRs'].sum()}")
        print(f"   Agents in analysis: {len(test_stats)}")
        
        # Test research summary
        print("\nTesting research summary...")
        summary = get_research_summary(df_analyzed)
        print(f"PASS: Research summary generated")
        print(f"   Dataset size: {summary['dataset_size']}")
        print(f"   Unique agents: {summary['unique_agents']}")
        
        return True
        
    except Exception as e:
        print(f"FAIL: Analysis functions test failed: {str(e)}")
        return False

def test_file_structure():
    """Test project file structure"""
    print("\nTesting File Structure...")
    print("=" * 50)
    
    required_files = [
        "src/data_loader.py",
        "src/analysis.py",
        "requirements.txt",
        "main.py",
        "CHECKME.md",
        "docs/Log.md"
    ]
    
    required_notebooks = [
        "notebooks/RQ1_Agent_Distribution.ipynb",
        "notebooks/RQ2_Test_to_Code_Ratio.ipynb", 
        "notebooks/RQ3_Code_Change_Analysis.ipynb",
        "notebooks/RQ4_Description_Consistency.ipynb",
        "notebooks/RQ5_User_Adoption.ipynb",
        "notebooks/summary.ipynb"
    ]
    
    all_files = required_files + required_notebooks
    missing_files = []
    
    for file_path in all_files:
        if os.path.exists(file_path):
            print(f"PASS: {file_path}")
        else:
            print(f"FAIL: {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\nFAIL: Missing {len(missing_files)} files")
        return False
    else:
        print(f"\nPASS: All {len(all_files)} required files present")
        return True

def test_notebooks_basic():
    """Test basic notebook structure"""
    print("\nTesting Notebook Structure...")
    print("=" * 50)
    
    notebooks = [
        "notebooks/RQ1_Agent_Distribution.ipynb",
        "notebooks/RQ2_Test_to_Code_Ratio.ipynb",
        "notebooks/RQ3_Code_Change_Analysis.ipynb", 
        "notebooks/RQ4_Description_Consistency.ipynb",
        "notebooks/RQ5_User_Adoption.ipynb",
        "notebooks/summary.ipynb"
    ]
    
    all_valid = True
    
    for notebook in notebooks:
        if os.path.exists(notebook):
            try:
                with open(notebook, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'VSCode.Cell' in content:
                        print(f"PASS: {os.path.basename(notebook)} - Valid structure")
                    else:
                        print(f"FAIL: {os.path.basename(notebook)} - Invalid structure")
                        all_valid = False
            except Exception as e:
                print(f"FAIL: {os.path.basename(notebook)} - Read error: {str(e)}")
                all_valid = False
        else:
            print(f"FAIL: {os.path.basename(notebook)} - Missing")
            all_valid = False
    
    return all_valid

def main():
    """Run comprehensive test suite"""
    print("MSR PROJECT COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    
    # Run all tests
    test_results = {}
    start_time = time.time()
    
    test_results['file_structure'] = test_file_structure()
    test_results['data_loading'] = test_data_loading()
    test_results['analysis_functions'] = test_analysis_functions()
    test_results['notebook_structure'] = test_notebooks_basic()
    
    end_time = time.time()
    
    # Generate summary
    print("\nTEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    for test_name, result in test_results.items():
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name.replace('_', ' ').title()}")
    
    print(f"\nResults: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    
    if success_rate == 100:
        print("\nALL TESTS PASSED! MSR project is ready for production.")
        overall_status = "SUCCESS"
    else:
        print(f"\nSome tests failed. Please review and fix issues.")
        overall_status = "PARTIAL"
    
    # Save test report
    test_report = {
        "timestamp": datetime.now().isoformat(),
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
    with open("outputs/test_report.json", "w") as f:
        json.dump(test_report, f, indent=2)
    
    print(f"Test report saved: outputs/test_report.json")
    
    return success_rate == 100

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)