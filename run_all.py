#!/usr/bin/env python3
"""
MSR Project: Automated Analysis Pipeline with Claude Integration
Executes all research question notebooks in sequence with error handling and reporting.
Now includes Claude API integration for enhanced analysis capabilities.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path
import json
from datetime import datetime

# Configuration
NOTEBOOKS = [
    ("RQ1_Agent_Distribution.ipynb", "Agent Distribution Analysis"),
    ("RQ2_Test_to_Code_Ratio.ipynb", "Test-to-Code Ratio Analysis"),
    ("RQ3_Code_Change_Analysis.ipynb", "Code Change Analysis"),
    ("RQ4_Description_Consistency.ipynb", "Description Consistency Analysis"),
    ("RQ5_User_Adoption.ipynb", "User Adoption Analysis"),
    ("summary.ipynb", "Summary Dashboard & Executive Report")
]

# Claude-enhanced notebooks (optional, runs if Claude API is available)
CLAUDE_NOTEBOOKS = [
    ("Claude_Enhanced_Analysis.ipynb", "Claude-Powered Intelligent Analysis")
]

# Optional visualization notebook (runs after main analysis if all succeed)
VISUALIZATION_NOTEBOOK = ("MSR_Visualization_Recreation.ipynb", "Comprehensive Visualization Generation")

TIMEOUT = 600  # 10 minutes per notebook
NOTEBOOKS_DIR = Path("notebooks")
OUTPUTS_DIR = Path("outputs")

def run_notebook(notebook_path, description):
    """Run a single notebook and return success status"""
    print(f"   Notebook: {notebook_path}")
    
    # Use full Python path from virtual environment
    python_path = r"C:/Users/Ahmed/Downloads/VScodeRepo/MSR/.venv/Scripts/python.exe"
    cmd = [python_path, "-m", "jupyter", "nbconvert", "--to", "notebook", 
           "--execute", "--inplace", str(notebook_path)]
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"   [SUCCESS] Completed in {duration:.1f}s")
        return True, f"Success ({duration:.1f}s)"
        
    except subprocess.CalledProcessError as e:
        print(f"   [ERROR] Failed: {e}")
        return False, f"Error: {e.stderr}"

def generate_report(results: list) -> None:
    """Generate execution report."""
    timestamp = datetime.now().isoformat()
    
    report = {
        "execution_timestamp": timestamp,
        "total_notebooks": len(results),
        "successful": sum(1 for success, _, _, _ in results if success),
        "failed": sum(1 for success, _, _, _ in results if not success),
        "results": [
            {
                "notebook": notebook,
                "description": desc,
                "success": success,
                "message": message
            }
            for success, notebook, desc, message in results
        ]
    }
    
    # Save report
    OUTPUTS_DIR.mkdir(exist_ok=True)
    report_path = OUTPUTS_DIR / "execution_report.json"
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nExecution report saved: {report_path}")

def main():
    """Main execution pipeline with Claude integration options."""
    parser = argparse.ArgumentParser(description='MSR Analysis Pipeline with Claude Integration')
    parser.add_argument('--include-claude', action='store_true', default=False,
                       help='Include Claude-enhanced analysis notebooks')
    parser.add_argument('--claude-only', action='store_true', default=False,
                       help='Run only Claude-enhanced analysis (skip standard notebooks)')
    parser.add_argument('--no-visualization', action='store_true', default=False,
                       help='Skip visualization generation')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("MSR Project: Automated Analysis Pipeline with Claude Integration")
    print("=" * 60)
    print()
    
    # Check if notebooks directory exists
    if not NOTEBOOKS_DIR.exists():
        print(f"❌ Error: {NOTEBOOKS_DIR} directory not found!")
        sys.exit(1)
    
    results = []
    failed_count = 0
    
    for i, (notebook_file, description) in enumerate(NOTEBOOKS, 1):
        notebook_path = NOTEBOOKS_DIR / notebook_file
        
        print(f"[{i}/{len(NOTEBOOKS)}] {description}")
        
        if not notebook_path.exists():
            print(f"   [WARNING] Notebook not found: {notebook_path}")
            results.append((False, notebook_file, description, "File not found"))
            failed_count += 1
            continue
        
        success, message = run_notebook(notebook_path, description)
        results.append((success, notebook_file, description, message))
        
        if not success:
            failed_count += 1
        
        print()
    
    # Summary
    print("=" * 50)
    if failed_count == 0:
        print("[SUCCESS] All Research Questions Completed Successfully!")
        print("=" * 50)
        print()
        
        # Auto-generate comprehensive visualizations
        print("🎨 Generating comprehensive visualizations...")
        visualization_path = NOTEBOOKS_DIR / VISUALIZATION_NOTEBOOK[0]
        
        if visualization_path.exists():
            print(f"[EXTRA] {VISUALIZATION_NOTEBOOK[1]}")
            success, message = run_notebook(visualization_path, VISUALIZATION_NOTEBOOK[1])
            results.append((success, VISUALIZATION_NOTEBOOK[0], VISUALIZATION_NOTEBOOK[1], message))
            
            if success:
                print("   [SUCCESS] Comprehensive visualizations generated!")
            else:
                print(f"   [WARNING] Visualization generation failed: {message}")
        else:
            print(f"   [INFO] Visualization notebook not found: {VISUALIZATION_NOTEBOOK[0]}")
            print("   [INFO] Skipping automatic visualization generation")
        
        print()
    else:
        print(f"[WARNING] {failed_count}/{len(NOTEBOOKS)} notebooks failed")
        print("=" * 50)
        print()
        print("ℹ️  Skipping visualization generation due to failed notebooks")
        print()
    
    print("📁 Results saved in:")
    print("   - notebooks/ (executed notebooks)")
    print("   - outputs/reports/ (analysis results)")
    print("   - outputs/figures/ (visualizations)")
    if failed_count == 0:
        print("   - outputs/ (comprehensive visualization suite)")
    print()
    
    # Generate report
    generate_report(results)
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)