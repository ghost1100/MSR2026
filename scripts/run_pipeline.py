"""
Orchestrate end-to-end pipeline:
1. Generate comprehensive dataset CSV
2. Wait for manual verification (interactive or polling)
3. Run evaluation, FP analysis, SQL breakdown, and plotting
4. Produce a final report in outputs/final_run_report.md

Usage:
  python scripts/run_pipeline.py [--no-wait] [--poll-seconds N] [--threshold PERCENT]

Options:
  --no-wait       Skip waiting for manual verification (danger: run analysis on unverified data)
  --poll-seconds N  Poll every N seconds to check manual completion (default 30)
  --threshold PERCENT  Continue when at least this percent of rows have non-empty manual labels (0-100). Default 100.

Examples:
  # Generate dataset and then wait for user to press Enter after manual verification
  python scripts/run_pipeline.py

  # Generate dataset and auto-continue when at least 80% of rows have manual labels
  python scripts/run_pipeline.py --poll-seconds 60 --threshold 80

"""
import argparse
import subprocess
import time
import os
import pandas as pd
from datetime import datetime

CSV_NAME = 'comprehensive_pr_manual_verification_dataset.csv'
OUTPUT_DIR = 'outputs'
REPORT_PATH = os.path.join(OUTPUT_DIR, 'final_run_report.md')


def run_cmd(cmd, check=True):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")
    return res.returncode


def percent_manual_filled(csv_path, manual_col='was test included Y/N'):
    df = pd.read_csv(csv_path, dtype=str).fillna('')
    if manual_col not in df.columns:
        # try other columns
        if 'manual_testing_present' in df.columns:
            manual_col = 'manual_testing_present'
        else:
            return 0.0
    filled = df[manual_col].astype(str).str.strip().replace('', pd.NA).notna().sum()
    total = len(df)
    return 100.0 * filled / total, int(filled), int(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-wait', action='store_true', help='Skip waiting for manual verification')
    parser.add_argument('--poll-seconds', type=int, default=30, help='Poll interval in seconds')
    parser.add_argument('--threshold', type=float, default=100.0, help='Percent of rows with manual label required to continue')
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    start_ts = datetime.utcnow().isoformat() + 'Z'

    # Step 1: Generate dataset
    print('\n== Step 1: Generate comprehensive PR dataset ==')
    # prefer to call the script as a module
    run_cmd('python create_comprehensive_pr_dataset.py')

    if not os.path.exists(CSV_NAME):
        raise FileNotFoundError(f"Expected CSV '{CSV_NAME}' not found after generation")

    # Step 2: Wait for manual verification
    print('\n== Step 2: Manual verification check ==')
    pct, filled, total = percent_manual_filled(CSV_NAME)
    print(f"Current manual label fill: {filled}/{total} rows ({pct:.1f}%)")

    if args.no_wait:
        print('Skipping wait for manual verification (--no-wait)')
    else:
        # If threshold already reached, proceed
        if pct >= args.threshold:
            print(f"Threshold {args.threshold}% reached ({pct:.1f}%) — continuing")
        else:
            print("Waiting for manual verification. Options: press ENTER to continue now, or let this script poll until threshold is reached.")
            print(f"Polling every {args.poll_seconds} seconds until at least {args.threshold}% of rows have manual labels.")
            print("Press Ctrl+C to cancel and continue later.")

            try:
                while True:
                    user_input = None
                    # non-blocking prompt is hard; prompt user to press ENTER to continue immediately
                    print('\nPress ENTER to continue now, or wait for polling to reach threshold...')
                    try:
                        # wait up to poll_seconds for user to press Enter
                        user_input = input_with_timeout(args.poll_seconds)
                    except TimeoutError:
                        user_input = None

                    if user_input is not None:
                        print('User requested to continue now (ENTER pressed)')
                        break

                    pct, filled, total = percent_manual_filled(CSV_NAME)
                    print(f"Polled manual fill: {filled}/{total} rows ({pct:.1f}%)")
                    if pct >= args.threshold:
                        print(f"Threshold reached ({pct:.1f}%) — continuing")
                        break
            except KeyboardInterrupt:
                print('\nInterrupted by user. Exiting before running analysis.')
                return

    # Step 3: Run analysis scripts
    print('\n== Step 3: Run evaluation, analysis, SQL breakdown, and plotting ==')
    # run evaluation
    run_cmd('python scripts/evaluate_auto_testing.py --csv ' + CSV_NAME)
    run_cmd('python scripts/analyze_false_positives.py --csv ' + CSV_NAME)
    run_cmd('python scripts/sql_present_data.py --csv ' + CSV_NAME)
    run_cmd('python scripts/plot_high_predictions.py --csv ' + CSV_NAME)

    # Step 4: Create final report
    print('\n== Step 4: Generate final report ==')
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write('# Final Pipeline Run Report\n\n')
        f.write(f'- Run time (UTC): {datetime.utcnow().isoformat()}Z\n')
        f.write(f'- Dataset generated: {CSV_NAME}\n')
        f.write('- Outputs: outputs/high_prediction_breakdown.csv, outputs/high_prediction_manual_category_breakdown.csv\n')
        f.write('- Figures: outputs/figures/high_by_manual_category.png, outputs/figures/high_pie_manual_category.png\n')
        f.write('\n## Notes\n')
        f.write('Run the scripts in order if you need to re-generate only specific artifacts.\n')
    print('Final report saved to', REPORT_PATH)
    print('Pipeline completed successfully.')


# Utility: input with timeout
import sys
import threading

def _input_worker(result_container):
    try:
        result_container.append(sys.stdin.readline())
    except Exception:
        pass


def input_with_timeout(timeout):
    """Wait for user to press ENTER within 'timeout' seconds. Return the input (string) if pressed, otherwise raise TimeoutError."""
    result = []
    thread = threading.Thread(target=_input_worker, args=(result,))
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    if result:
        return result[0]
    raise TimeoutError()


if __name__ == '__main__':
    main()
