#!/usr/bin/env python3
"""
Run all MSR project notebooks in sequence
"""

import os
import sys
import subprocess
import time

def run_notebook(notebook_path):
    """Run a single notebook and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {os.path.basename(notebook_path)}")
    print(f"{'='*60}")
    
    try:
        # Use jupyter nbconvert to execute the notebook
        cmd = [
            sys.executable, "-m", "jupyter", "nbconvert", 
            "--to", "notebook", 
            "--execute", 
            "--inplace",
            notebook_path
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(notebook_path))
        end_time = time.time()
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {os.path.basename(notebook_path)} ({end_time - start_time:.1f}s)")
            return True
        else:
            print(f"❌ FAILED: {os.path.basename(notebook_path)}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR running {os.path.basename(notebook_path)}: {str(e)}")
        return False

def main():
    print("🚀 MSR Project - Notebook Automation Suite")
    print("=" * 60)
    
    # Get the notebooks directory
    notebooks_dir = os.path.join(os.path.dirname(__file__), "notebooks")
    
    if not os.path.exists(notebooks_dir):
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        return
    
    # List of notebooks to run in order
    notebooks = [
        "RQ1_Agent_Distribution.ipynb",
        "RQ2_Test_to_Code_Ratio.ipynb", 
        "RQ3_Code_Change_Analysis.ipynb",
        "RQ4_Description_Consistency.ipynb",
        "RQ5_User_Adoption.ipynb",
        "summary.ipynb"
    ]
    
    results = {}
    total_start = time.time()
    
    # Run each notebook
    for notebook in notebooks:
        notebook_path = os.path.join(notebooks_dir, notebook)
        
        if not os.path.exists(notebook_path):
            print(f"⚠️  Notebook not found: {notebook}")
            results[notebook] = False
            continue
            
        success = run_notebook(notebook_path)
        results[notebook] = success
    
    total_time = time.time() - total_start
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 AUTOMATION SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    for notebook, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {notebook}")
    
    print(f"\n🎯 Results: {successful}/{total} notebooks completed successfully")
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    print(f"📈 Success rate: {successful/total*100:.1f}%")
    
    if successful == total:
        print("\n🎉 ALL NOTEBOOKS COMPLETED SUCCESSFULLY!")
    else:
        print(f"\n⚠️  {total - successful} notebook(s) failed. Check the output above for details.")

if __name__ == "__main__":
    main()