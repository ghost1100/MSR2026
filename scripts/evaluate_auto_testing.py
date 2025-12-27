"""
Evaluate automatic testing detection against manual labels.
Saves a CSV with counts and prints precision/recall/F1 for two thresholds:
 - 'High' confidence only
 - 'High' or 'Medium' confidence

Usage:
    python scripts/evaluate_auto_testing.py --csv comprehensive_pr_manual_verification_dataset.csv

Outputs:
 - prints summary to stdout
 - writes `outputs/auto_testing_evaluation.csv` with confusion matrix rows
"""
import argparse
import pandas as pd
import os
import sys


def normalize_manual_label(x):
    if pd.isna(x):
        return ''
    s = str(x).strip().lower()
    if s == '':
        return ''
    # Handle explicit errors / missing indications
    if 'error' in s or '404' in s or 'n/a' in s or 'unknown' in s:
        return ''
    # Negative indicators should be detected first
    if 'no tests' in s or s in ('no', 'n', 'none', 'none included') or 'none' in s or 'not included' in s:
        return 'no'
    # Partial mentions
    if 'partial' in s or 'partially' in s:
        return 'partial'
    # Positive mentions (include words like 'included', 'testing included', 'extensive testing')
    if 'testing included' in s or 'extensive testing' in s or 'comprehensive testing' in s or 'included' in s or 'testing' in s:
        return 'yes'
    # Fallback: return raw
    return s


def compute_metrics(df, predicted_mask, actual_mask):
    tp = int(((predicted_mask) & (actual_mask)).sum())
    fp = int(((predicted_mask) & (~actual_mask)).sum())
    fn = int(((~predicted_mask) & (actual_mask)).sum())
    tn = int((~predicted_mask & ~actual_mask).sum())
    precision = tp / (tp + fp) if (tp + fp) > 0 else float('nan')
    recall = tp / (tp + fn) if (tp + fn) > 0 else float('nan')
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else float('nan')
    return {
        'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn,
        'Precision': precision, 'Recall': recall, 'F1': f1
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='comprehensive_pr_manual_verification_dataset.csv')
    parser.add_argument('--out', default='outputs/auto_testing_evaluation.csv')
    args = parser.parse_args()

    if not os.path.exists(args.csv):
        print(f"CSV not found: {args.csv}")
        sys.exit(1)

    df = pd.read_csv(args.csv, dtype=str).fillna('')

    # Prefer explicit manual column (some files use 'was test included Y/N')
    lower_cols = {c.lower(): c for c in df.columns}
    if 'was test included y/n' in lower_cols:
        df['manual_testing_present'] = df[lower_cols['was test included y/n']].fillna('')
    elif 'manual_testing_present' in lower_cols:
        df['manual_testing_present'] = df[lower_cols['manual_testing_present']].fillna('')
    else:
        # try permissive search
        manual_col = None
        for k, v in lower_cols.items():
            if 'manual' in k and 'test' in k:
                manual_col = v
                break
        if manual_col:
            df['manual_testing_present'] = df[manual_col].fillna('')
        else:
            df['manual_testing_present'] = ''

    df['manual_norm'] = df['manual_testing_present'].apply(normalize_manual_label)

    # If 'test detection' confidence exists, use it directly (e.g., 'High', 'Medium', 'Low')
    if 'test detection' in lower_cols:
        df['auto_conf'] = df[lower_cols['test detection']].astype(str).str.strip().str.lower()
        # try to get keyword count if available (some exports put counts in auto_testing_keywords_found)
        if 'auto_testing_keywords_found' in lower_cols:
            # sometimes this column contains numbers (counts), sometimes comma-separated keywords
            s = df[lower_cols['auto_testing_keywords_found']].astype(str).str.strip()
            if s.str.isnumeric().all():
                df['auto_keywords_count'] = pd.to_numeric(s, errors='coerce').fillna(0).astype(int)
            else:
                df['auto_keywords_count'] = s.apply(lambda x: len([t for t in x.split(',') if t.strip()]))
        else:
            df['auto_keywords_count'] = 0
    else:
        # fall back to keyword columns or recompute from title/body
        if 'auto_testing_keywords_found' in lower_cols and df[lower_cols['auto_testing_keywords_found']].astype(str).str.strip().str.isnumeric().all():
            df['auto_keywords_count'] = pd.to_numeric(df[lower_cols['auto_testing_keywords_found']], errors='coerce').fillna(0).astype(int)
        elif 'auto_testing_keywords_count' in lower_cols:
            df['auto_keywords_count'] = pd.to_numeric(df[lower_cols['auto_testing_keywords_count']], errors='coerce').fillna(0).astype(int)
        else:
            testing_keywords = [
                'test', 'testing', 'tests', 'unit test', 'integration test', 'e2e test',
                'pytest', 'junit', 'jest', 'mocha', 'jasmine', 'rspec', 'minitest',
                'assert', 'expect', 'should', 'mock', 'stub', 'spy',
                'coverage', 'tdd', 'bdd', 'spec', 'describe', 'it(',
                'test case', 'test suite', 'test file', 'test directory'
            ]
            def count_from_row(r):
                text = f"{r.get('pr_title','')} {r.get('pr_body','') or ''}".lower()
                found = [kw for kw in testing_keywords if kw in text]
                return len(found)
            df['auto_keywords_count'] = df.apply(count_from_row, axis=1)
            df['auto_conf'] = df['auto_keywords_count'].apply(lambda n: 'high' if n>=3 else ('medium' if n>=1 else 'low'))

    # Ensure auto_conf exists
    if 'auto_conf' not in df.columns:
        df['auto_conf'] = df['auto_keywords_count'].apply(lambda n: 'high' if n>=3 else ('medium' if n>=1 else 'low'))

    # Define actual/predicted masks
    actual_yes = df['manual_norm'] == 'yes'
    actual_partial = df['manual_norm'] == 'partial'
    pred_high = df['auto_conf'] == 'high'
    pred_high_medium = df['auto_conf'].isin(['high', 'medium'])

    results = []
    for label, mask in [('High only', pred_high), ('High or Medium', pred_high_medium)]:
        metrics = compute_metrics(df, mask, actual_yes)
        metrics['Setting'] = label
        metrics['Predicted_Pos'] = int(mask.sum())
        metrics['Actual_Pos'] = int(actual_yes.sum())
        results.append(metrics)

    results_df = pd.DataFrame(results).set_index('Setting')

    # Print summary
    print('\n=== Automatic testing detection evaluation ===\n')
    print(f"Total records: {len(df)}")
    print(f"Manually marked testing present (YES): {int(actual_yes.sum())}")
    print(f"Manually marked partial: {int(actual_partial.sum())}\n")

    print(results_df.to_string(float_format=lambda x: f"{x:.3f}" if isinstance(x, float) else str(x)))

    # Save per-row evaluation for inspection (include both columns when present)
    eval_cols = ['pr_id', 'agent', 'pr_title', 'manual_testing_present', 'manual_norm', 'auto_conf', 'auto_keywords_count']
    df_eval = df[[c for c in eval_cols if c in df.columns]].copy()
    df_eval['pred_high'] = pred_high
    df_eval['pred_high_medium'] = pred_high_medium
    outdir = os.path.dirname(args.out)
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir)
    df_eval.to_csv(args.out, index=False)
    print(f"\nPer-row evaluation saved to: {args.out}")


if __name__ == '__main__':
    main()
