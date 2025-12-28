#!/usr/bin/env python3
"""
MSR2026 CLEAN REPLICATION SCRIPT
Error-free execution of complete research pipeline

This script runs the complete analysis pipeline with all Unicode issues resolved.
Generates comprehensive research outputs with full transparency about limitations.

Usage: python clean_replication.py
"""

import subprocess
import sys
import os
import json
from datetime import datetime

def print_header(title, width=80):
    print("=" * width)
    print(f" {title}")
    print("=" * width)

def print_stage(stage, description, width=60):
    print(f"\n[STAGE {stage}] {description}")
    print("-" * width)

def run_analysis_script(script_name, description):
    """Run an analysis script and return success status"""
    print(f"\nExecuting: {script_name}")
    print(f"Purpose: {description}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,  # Show output in real-time
            timeout=900,  # 15 minute timeout
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print(f"SUCCESS: {script_name} completed without errors")
            return True
        else:
            print(f"ERROR: {script_name} failed with exit code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: {script_name} exceeded 15 minutes")
        return False
    except Exception as e:
        print(f"EXCEPTION in {script_name}: {str(e)}")
        return False

def main():
    """Execute the complete replication pipeline"""
    start_time = datetime.now()
    
    print_header("MSR2026 CLEAN REPLICATION PIPELINE")
    print("[REDACTED INSTITUTION] - December 2025")
    print("Complete research with honest assessment of limitations")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define analysis pipeline
    pipeline = [
        ("honest_analysis.py", "Dataset statistics with methodology explanation"),
        ("comprehensive_full_analysis.py", "Multi-language test detection and Chi-square analysis"),
        ("complete_filtering_analysis.py", "User concentration and bias assessment"),
        ("complete_research_journey.py", "Research evolution documentation with limitations")
    ]
    
    results = {}
    successful_stages = 0
    
    # Execute each stage
    for i, (script, description) in enumerate(pipeline, 1):
        print_stage(i, description.upper())
        
        if os.path.exists(script):
            success = run_analysis_script(script, description)
            results[script] = {
                'status': 'success' if success else 'failed',
                'description': description,
                'timestamp': datetime.now().isoformat()
            }
            
            if success:
                successful_stages += 1
        else:
            print(f"SKIPPED: {script} not found")
            results[script] = {
                'status': 'skipped',
                'description': description,
                'reason': 'file_not_found'
            }
    
    # Final summary
    total_time = datetime.now() - start_time
    
    print_header("REPLICATION COMPLETE")
    print(f"Execution time: {total_time}")
    print(f"Successful stages: {successful_stages}/{len(pipeline)}")
    
    # Save execution summary
    summary = {
        'execution_metadata': {
            'start_time': start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'duration_seconds': total_time.total_seconds(),
            'successful_stages': successful_stages,
            'total_stages': len(pipeline)
        },
        'stage_results': results,
        'dataset_info': {
            'total_records': 932791,
            'unique_users': 72189,
            'agents': ['OpenAI_Codex', 'Copilot', 'Cursor', 'Devin', 'Claude_Code']
        }
    }
    
    os.makedirs('outputs', exist_ok=True)
    with open('outputs/clean_replication_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    if successful_stages == len(pipeline):
        print("STATUS: FULL SUCCESS - All analysis completed")
        print("RESEARCH: Complete dataset analysis with honest limitations")
        print("OUTPUTS: Check outputs/ directory for all generated files")
        return True
    else:
        print(f"STATUS: PARTIAL SUCCESS - {successful_stages}/{len(pipeline)} completed")
        print("CHECK: Review error messages above for failed stages")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\nReplication {'successful' if success else 'completed with issues'}")
    sys.exit(0 if success else 1)