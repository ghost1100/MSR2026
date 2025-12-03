import json
import re
import sys
import time
import traceback
from collections import defaultdict
from pathlib import Path

import pandas as pd

CSV_PATHS = [Path('data/raw/aidata.csv'), Path('../data/raw/aidata.csv')]
TEST_RATES_JSON = Path('outputs/test_rates_from_csv.json')

# Keyword list aligned with recompute_test_rates_from_csv.py
KEYWORDS = [
    'test', 'testing', 'spec', 'unittest', 'pytest', 'jest', 'mocha', 'assert',
    'rspec', 'junit', 'testng', 'nunit', 'e2e', 'integration test', 'selenium', 'cypress'
]
PATTERN = re.compile('|'.join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)


def load_counts_tests_from_summary(summary_path: Path):
    if not summary_path.exists():
        return None
    try:
        with open(summary_path, 'r') as f:
            data = json.load(f)
        counts = {}
        tests = {}
        for agent, s in data.get('per_agent', {}).items():
            counts[agent] = int(s.get('total_prs', 0))
            tests[agent] = int(s.get('test_prs', 0))
        return counts, tests
    except Exception:
        return None


def compute_counts_tests_from_csv(csv_path: Path, chunksize: int = 100_000):
    usecols = ['agent', 'title', 'body']
    dtypes = {'agent': 'category', 'title': 'string', 'body': 'string'}
    counts = defaultdict(int)
    tests = defaultdict(int)

    def detect_mask(chunk: pd.DataFrame) -> pd.Series:
        text = (chunk['title'].fillna('') + ' ' + chunk['body'].fillna(''))
        return text.str.contains(PATTERN, na=False, regex=True)

    start = time.time()
    total_rows = 0
    try:
        for i, chunk in enumerate(pd.read_csv(csv_path, usecols=usecols, dtype=dtypes, low_memory=False, chunksize=chunksize), start=1):
            rows = len(chunk)
            total_rows += rows
            if i % 5 == 0:
                print(f"Processed ~{total_rows:,} rows...", flush=True)

            gcount = chunk.groupby('agent', observed=True).size()
            for agent, n in gcount.items():
                counts[str(agent)] += int(n)

            mask = detect_mask(chunk)
            if mask.any():
                gtest = chunk.loc[mask].groupby('agent', observed=True).size()
                for agent, n in gtest.items():
                    tests[str(agent)] += int(n)
    except Exception as e:
        print('ERROR while processing CSV:', e)
        traceback.print_exc()
        sys.exit(1)

    elapsed = time.time() - start
    print(f"Computed counts/tests from CSV in {elapsed:.1f}s")
    return counts, tests


def summarize_from_counts(counts: dict, tests: dict) -> dict:
    out = {'per_agent': {}, 'overall': {}}
    agents = sorted(counts.keys())
    for a in agents:
        tot = int(counts.get(a, 0))
        t = int(tests.get(a, 0))
        pct = (t / tot * 100.0) if tot else 0.0
        out['per_agent'][a] = {'total_prs': tot, 'test_prs': t, 'test_pct': pct}
    overall_tot = int(sum(counts.values()))
    overall_test = int(sum(tests.values()))
    out['overall'] = {
        'total_prs': overall_tot,
        'test_prs': overall_test,
        'test_pct': (overall_test / overall_tot * 100.0) if overall_tot else 0.0,
    }
    return out


# Locate CSV (for fallback computation)
csv_path = None
for p in CSV_PATHS:
    if p.exists():
        csv_path = p
        break
if not csv_path:
    print('ERROR: data/raw/aidata.csv not found')
    raise SystemExit(1)

# Prefer using precomputed per-agent totals/tests if available
loaded = load_counts_tests_from_summary(TEST_RATES_JSON)
if loaded is not None:
    counts, tests = loaded
    print(f"Loaded per-agent totals from {TEST_RATES_JSON}")
else:
    print("Precomputed summary not found; computing from CSV (chunked)...")
    counts, tests = compute_counts_tests_from_csv(csv_path)

# Baseline
baseline = summarize_from_counts(counts, tests)

# Exclude Codex
exclude_counts = {k: v for k, v in counts.items() if k != 'OpenAI_Codex'}
exclude_tests = {k: v for k, v in tests.items() if k != 'OpenAI_Codex'}
exclude_codex = summarize_from_counts(exclude_counts, exclude_tests)

# Reclassify Codex -> Copilot
reclass_counts = dict(counts)
reclass_tests = dict(tests)
if 'OpenAI_Codex' in reclass_counts:
    reclass_counts['Copilot'] = reclass_counts.get('Copilot', 0) + reclass_counts.get('OpenAI_Codex', 0)
    reclass_tests['Copilot'] = reclass_tests.get('Copilot', 0) + reclass_tests.get('OpenAI_Codex', 0)
    del reclass_counts['OpenAI_Codex']
    if 'OpenAI_Codex' in reclass_tests:
        del reclass_tests['OpenAI_Codex']
reclassify_codex_to_copilot = summarize_from_counts(reclass_counts, reclass_tests)

out = {
    'baseline': baseline,
    'exclude_codex': exclude_codex,
    'reclassify_codex_to_copilot': reclassify_codex_to_copilot,
}

Path('outputs').mkdir(parents=True, exist_ok=True)
with open('outputs/sensitivity_codex.json', 'w') as f:
    json.dump(out, f, indent=2)

print('Wrote outputs/sensitivity_codex.json')
