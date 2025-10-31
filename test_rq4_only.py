#!/usr/bin/env python3
"""
Test script to run only RQ4 notebook for debugging
"""

import subprocess
import sys
import os
from datetime import datetime

def test_rq4_notebook():
    """Test RQ4 notebook execution in isolation"""
    print("TESTING RQ4 NOTEBOOK ONLY")
    print("=" * 50)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    notebook_path = "notebooks/RQ4_Description_Consistency.ipynb"
    
    if not os.path.exists(notebook_path):
        print(f"ERROR: Notebook not found: {notebook_path}")
        return False
    
    print(f"\nTesting: {notebook_path}")
    
    try:
        # Execute the notebook
        cmd = [
            sys.executable, "-m", "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            notebook_path
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"SUCCESS: RQ4 notebook executed successfully!")
            print(f"Output: {result.stdout[:500]}...")
            return True
        else:
            print(f"FAILED: Return code {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: Notebook execution exceeded 5 minutes")
        return False
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    success = test_rq4_notebook()
    
    print(f"\n{'='*50}")
    if success:
        print(f"RQ4 TEST PASSED - Ready for full pipeline!")
    else:
        print(f"RQ4 TEST FAILED - Needs more debugging")
    print(f"{'='*50}")
    
    sys.exit(0 if success else 1)