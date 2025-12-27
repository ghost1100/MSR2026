"""
Analyze false positives and false negatives from auto testing predictions.
Saves:
 - outputs/false_positives.csv
 - outputs/false_negatives.csv
 - outputs/false_positive_summary.txt
 - outputs/false_negative_summary.txt
 - outputs/false_positive_examples.csv (sample)

Usage:
    python scripts/analyze_false_positives.py --csv comprehensive_pr_manual_verification_dataset.csv

"""
import argparse
import pandas as pd
import os
from collections import Counter

TEST_KEYWORDS = [
    'test', 'testing', 'tests', 'unit test', 'integration test', 'e2e test',
    'pytest', 'junit', 'jest', 'mocha', 'jasmine', 'rspec', 'minitest',
    'assert', 'expect', 'should', 'mock', 'stub', 'spy',
    'coverage', 'tdd', 'bdd', 'spec', 'describe', 'it(',
    'test case', 'test suite', 'test file', 'test directory'
]


def summarize_texts(texts, top_n=20):
    counts = Counter()
    for t in texts:
        if not isinstance(t, str):
            continue
        txt = t.lower()
        for kw in TEST_KEYWORDS:
            if kw in txt:
                counts[kw] += 1
    return counts.most_common(top_n)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='comprehensive_pr_manual_verification_dataset.csv')
    args = parser.parse_args()

    df = pd.read_csv(args.csv, dtype=str).fillna('')

    # Normalize manual label column similar to evaluation script
    if 'was test included Y/N' in df.columns:
        manual_col = 'was test included Y/N'
    elif 'manual_testing_present' in df.columns:
        manual_col = 'manual_testing_present'
    else:
        manual_col = None

    def norm_manual(s):
        s = str(s).strip().lower()
        if s == '':
            return ''
        if 'error' in s or '404' in s:
            return ''
        if 'no tests' in s or 'no' == s or 'none' in s or 'not included' in s:
            return 'no'
        if 'partial' in s:
            return 'partial'
        if 'testing included' in s or 'comprehensive testing' in s or 'extensive testing' in s or 'included' in s or 'testing' in s:
            return 'yes'
        return s

    if manual_col:
        df['manual_norm'] = df[manual_col].apply(norm_manual)
    else:
        df['manual_norm'] = ''

    # Use existing 'test detection' as auto_conf if present
    if 'test detection' in df.columns:
        df['auto_conf'] = df['test detection'].astype(str).str.strip().str.lower()
    else:
        df['auto_conf'] = 'low'

    # Predicted high
    pred_high = df['auto_conf'] == 'high'
    actual_yes = df['manual_norm'] == 'yes'

    fp = df[pred_high & (~actual_yes)].copy()
    fn = df[(~pred_high) & (actual_yes)].copy()

    outdir = 'outputs'
    os.makedirs(outdir, exist_ok=True)

    fp.to_csv(os.path.join(outdir, 'false_positives.csv'), index=False)
    fn.to_csv(os.path.join(outdir, 'false_negatives.csv'), index=False)

    # Summarize false positives
    fp_titles = fp['pr_title'].astype(str).tolist()
    fp_bodies = fp['pr_body'].astype(str).tolist()
    fp_texts = [f"{t} {b}" for t, b in zip(fp_titles, fp_bodies)]
    fp_kw = summarize_texts(fp_texts, top_n=50)

    # Summarize languages and agents (use manual_language_detected if repo_language missing)
    lang_col = 'repo_language' if 'repo_language' in df.columns else ('manual_language_detected' if 'manual_language_detected' in df.columns else None)
    if lang_col:
        top_langs = fp[lang_col].fillna('').astype(str).str.lower().value_counts().head(10)
    else:
        top_langs = []
    top_agents = fp['agent'].fillna('').astype(str).value_counts().head(10)

    with open(os.path.join(outdir, 'false_positive_summary.txt'), 'w', encoding='utf-8') as f:
        f.write(f"False Positives: {len(fp)}\n\n")
        f.write("Top testing keywords found in FP rows:\n")
        for k, v in fp_kw:
            f.write(f"  {k}: {v}\n")
        f.write('\nTop languages in FPs (using ' + (lang_col or 'none') + '):\n')
        if hasattr(top_langs, 'items'):
            for lang, count in top_langs.items():
                f.write(f"  {lang}: {count}\n")
        else:
            for lang, count in top_langs.items():
                f.write(f"  {lang}: {count}\n")
        f.write('\nTop agents in FPs:\n')
        for ag, count in top_agents.items():
            f.write(f"  {ag}: {count}\n")

    # Determine likely cause categories for FPs (False Positives)
    causes = Counter()
    for t in fp_texts:
        txt = (t or '').lower()
        if 'docker' in txt or 'container' in txt:
            causes['infra / docker mention'] += 1
        if 'docs' in txt or 'documentation' in txt or 'readme' in txt:
            causes['documentation changes'] += 1
        if 'ci' in txt or 'workflow' in txt or 'github action' in txt:
            causes['ci / workflow mention'] += 1
        # keyword-only hits (short 'test' mentions that are not actual tests)
        if any(kw in txt for kw in ['test', 'testing']) and 'test' not in txt.split():
            # best-effort heuristic
            causes['ambiguous keyword usage'] += 1
    fpath = os.path.join(outdir, 'false_positive_causes.txt')
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write('Likely causes (heuristic counts):\n')
        for k, v in causes.most_common():
            f.write(f"  {k}: {v}\n")

    # Save sample examples
    fp.sample(min(50, len(fp))).to_csv(os.path.join(outdir, 'false_positive_examples.csv'), index=False)
    fn.sample(min(50, len(fn))).to_csv(os.path.join(outdir, 'false_negative_examples.csv'), index=False)

    # Also print small summary to stdout
    print(f"False positives: {len(fp)} (saved to outputs/false_positives.csv)")
    print(f"False negatives: {len(fn)} (saved to outputs/false_negatives.csv)")
    print('Summary saved to outputs/false_positive_summary.txt')

if __name__ == '__main__':
    main()
