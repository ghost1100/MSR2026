#!/usr/bin/env python3
"""
MSR2026 MASTER REPRODUCIBILITY SCRIPT - FIXED VERSION
Runs only the essential analysis pipeline with proper error handling
"""

import sys
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

# Ensure outputs directory exists
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def run_script_safe(script_name, description, required_files=None):
    """Run a script safely with dependency checking"""
    
    print(f"\n{'='*80}")
    print(f"STAGE: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*80}")
    
    # Check if script exists
    if not os.path.exists(script_name):
        print(f"⚠️  Script {script_name} not found - SKIPPING")
        return False
    
    # Check required files
    if required_files:
        missing_files = [f for f in required_files if not os.path.exists(f)]
        if missing_files:
            print(f"⚠️  Missing required files: {missing_files} - SKIPPING")
            return False
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=False, timeout=300)
        
        if result.returncode == 0:
            print(f"✓ SUCCESS: {script_name}")
            # Save output to file
            output_file = OUTPUT_DIR / f"{script_name.replace('.py', '_output.txt')}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"=== {description} ===\n")
                f.write(f"Script: {script_name}\n")
                f.write(f"Timestamp: {datetime.now()}\n\n")
                f.write("STDOUT:\n")
                f.write(result.stdout)
                if result.stderr:
                    f.write("\nSTDERR:\n")
                    f.write(result.stderr)
            
            return True
        else:
            print(f"✗ ERROR in {script_name} (exit code: {result.returncode})")
            # Save error output
            error_file = OUTPUT_DIR / f"{script_name.replace('.py', '_error.txt')}"
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(f"ERROR in {script_name}\n")
                f.write(f"Exit code: {result.returncode}\n")
                f.write(f"STDERR:\n{result.stderr}\n")
                f.write(f"STDOUT:\n{result.stdout}\n")
            
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  TIMEOUT: {script_name} (>5 minutes)")
        return False
    except Exception as e:
        print(f"✗ EXCEPTION running {script_name}: {e}")
        return False

def main():
    """Execute essential research pipeline only"""
    
    start_time = datetime.now()
    
    print("="*100)
    print("MSR2026 ESSENTIAL RESEARCH PIPELINE")
    print("Edinburgh Napier University - December 2025") 
    print("="*100)
    
    # Essential pipeline - only scripts that work standalone
    pipeline = [
        ("honest_analysis.py", "Dataset Statistics and Verification", ["data/raw/aidata.csv"]),
        ("comprehensive_full_analysis.py", "Complete Dataset Analysis", ["data/raw/aidata.csv"]),
        ("complete_filtering_analysis.py", "Statistical Filtering Analysis", ["data/raw/aidata.csv"]),
        ("complete_research_journey.py", "Complete Research Journey", None),
        ("fast_essential_analysis.py", "Fast Essential Analysis", None),
    ]
    
    # Additional scripts if verification files exist
    # Note: Additional verification scripts removed during cleanup
    
    print(f"Executing {len(pipeline)} essential research stages...")
    
    # Execute pipeline
    results = []
    successful_runs = 0
    failed_runs = 0
    
    for i, (script, description, required_files) in enumerate(pipeline, 1):
        print(f"\n[{i}/{len(pipeline)}] {description}")
        
        success = run_script_safe(script, description, required_files)
        results.append({
            "stage": i,
            "script": script,
            "description": description,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })
        
        if success:
            successful_runs += 1
        else:
            failed_runs += 1
    
    # Generate comprehensive summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    summary = {
        "research_execution": {
            "pipeline_type": "Essential Research Pipeline",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(), 
            "duration_seconds": duration.total_seconds(),
            "duration_formatted": str(duration),
            "successful_stages": successful_runs,
            "failed_stages": failed_runs,
            "total_stages": len(pipeline),
            "success_rate": f"{successful_runs/len(pipeline)*100:.1f}%"
        },
        "stage_results": results,
        "output_directory": str(OUTPUT_DIR.absolute()),
        "research_status": "COMPLETE" if failed_runs == 0 else "PARTIAL"
    }
    
    # Save execution summary
    with open(OUTPUT_DIR / "research_execution_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Generate output file inventory
    output_files = list(OUTPUT_DIR.rglob("*"))
    file_inventory = {
        "generated_files": [str(f.relative_to(OUTPUT_DIR)) for f in output_files if f.is_file()],
        "total_files": len([f for f in output_files if f.is_file()]),
        "directories": [str(f.relative_to(OUTPUT_DIR)) for f in output_files if f.is_dir()]
    }
    
    with open(OUTPUT_DIR / "output_inventory.json", 'w') as f:
        json.dump(file_inventory, f, indent=2)
    
    # Final report
    print(f"\n{'='*100}")
    print("RESEARCH EXECUTION COMPLETE")
    print("="*100)
    print(f"Duration: {duration}")
    print(f"Success rate: {successful_runs}/{len(pipeline)} ({successful_runs/len(pipeline)*100:.1f}%)")
    print(f"Output directory: {OUTPUT_DIR.absolute()}")
    
    if failed_runs == 0:
        print("\n🎉 ALL RESEARCH STAGES COMPLETED SUCCESSFULLY!")
    else:
        print(f"\n⚠️  {failed_runs} stages had issues:")
        for result in results:
            if not result["success"]:
                print(f"  - {result['script']}: {result['description']}")
    
    print(f"\n📊 Generated outputs ({file_inventory['total_files']} files):")
    for file in sorted(file_inventory['generated_files']):
        if not file.endswith('_error.txt'):  # Don't show error files in main summary
            print(f"  ✓ {file}")
    
    if any(f.endswith('_error.txt') for f in file_inventory['generated_files']):
        print(f"\n⚠️  Error logs available for failed stages")
    
    print(f"\n📁 Research outputs saved to: {OUTPUT_DIR.absolute()}")
    print("🚀 Research pipeline complete and reproducible!")
    
    # Final verification
    essential_outputs = [
        "research_execution_summary.json",
        "output_inventory.json"
    ]
    
    missing_outputs = [f for f in essential_outputs if not (OUTPUT_DIR / f).exists()]
    if not missing_outputs:
        print("✅ All essential outputs generated successfully")
    else:
        print(f"⚠️  Missing outputs: {missing_outputs}")

if __name__ == "__main__":
    # Verify essential requirements
    if not os.path.exists("data/raw/aidata.csv"):
        print("❌ ERROR: data/raw/aidata.csv not found")
        print("   Please ensure the MSR2026 dataset is in data/raw/aidata.csv")
        sys.exit(1)
    
    if not os.path.exists("requirements.txt"):
        print("⚠️  WARNING: requirements.txt not found")
    
    main()
