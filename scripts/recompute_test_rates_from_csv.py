import pandas as pd
import re
try:
    from src.test_detection import detect_tests as robust_detect_tests
except Exception:
    robust_detect_tests = None
from collections import defaultdict
import sys, time, traceback
from pathlib import Path

CSV_PATHS = [Path('data/raw/aidata.csv'), Path('../data/raw/aidata.csv')]

# Keyword list aligned with project narrative (substring matches, case-insensitive)
KEYWORDS = [
    'test', 'testing', 'spec', 'unittest', 'pytest', 'jest', 'mocha', 'assert',
    'rspec', 'junit', 'testng', 'nunit', 'e2e', 'integration test', 'selenium', 'cypress'
]

# Build a regex that approximates "any substring contains any keyword" behavior
# We escape keywords except spaces to retain phrases like "integration test"
pattern_parts = []
for kw in KEYWORDS:
    if ' ' in kw:
        pattern_parts.append(re.escape(kw))
    else:
        pattern_parts.append(re.escape(kw))
PATTERN = re.compile('|'.join(pattern_parts), re.IGNORECASE)

def detect_text(title: str, body: str) -> bool:
    """Layered detection: use robust detector if available, else keyword fallback."""
    if robust_detect_tests:
        return robust_detect_tests(title, body)
    text = f"{title}\n{body}"
    return bool(PATTERN.search(text))

# Locate CSV
csv_path = None
for p in CSV_PATHS:
    if p.exists():
        csv_path = p
        break

if not csv_path:
    print('ERROR: data/raw/aidata.csv not found')
    raise SystemExit(1)

print(f'Reading: {csv_path}')

usecols = ['agent','title','body']
dtypes = {'agent': 'category', 'title': 'string', 'body': 'string'}
chunksize = 100_000

# Accumulators
counts = defaultdict(int)
tests = defaultdict(int)

def detect_mask(chunk: pd.DataFrame) -> pd.Series:
    titles = chunk['title'].fillna('')
    bodies = chunk['body'].fillna('')
    return pd.Series([detect_text(t, b) for t, b in zip(titles, bodies)], index=chunk.index)

start = time.time()
total_rows = 0
try:
    for i, chunk in enumerate(pd.read_csv(csv_path, usecols=usecols, dtype=dtypes, low_memory=False, chunksize=chunksize), start=1):
        rows = len(chunk)
        total_rows += rows
        if i % 5 == 0:
            print(f"Processed ~{total_rows:,} rows...", flush=True)

        # Counts per agent in this chunk
        gcount = chunk.groupby('agent', observed=True).size()
        for agent, n in gcount.items():
            counts[str(agent)] += int(n)

        # Tests per agent in this chunk
        mask = detect_mask(chunk)
        if mask.any():
            gtest = chunk.loc[mask].groupby('agent', observed=True).size()
            for agent, n in gtest.items():
                tests[str(agent)] += int(n)
except Exception as e:
    print('ERROR while processing CSV:', e)
    traceback.print_exc()
    sys.exit(1)

# Summarize
agents = sorted(counts.keys())
summary = { 'per_agent': {}, 'overall': {} }
for a in agents:
    tot = counts[a]
    t = tests.get(a, 0)
    pct = (t / tot * 100.0) if tot else 0.0
    summary['per_agent'][a] = {
        'total_prs': tot,
        'test_prs': t,
        'test_pct': pct
    }

overall_tot = sum(counts.values())
overall_test = sum(tests.values())
overall_pct = (overall_test / overall_tot * 100.0) if overall_tot else 0.0
summary['overall'] = {
    'total_prs': overall_tot,
    'test_prs': overall_test,
    'test_pct': overall_pct
}

# Write JSON summary for reliable retrieval
from pathlib import Path
import json
out_path = Path('outputs/test_rates_from_csv.json')
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, 'w') as f:
    json.dump(summary, f, indent=2)

elapsed = time.time() - start
print(f"\nWrote summary to {out_path} in {elapsed:.1f}s")

# Also print a concise table to stdout
print('\nPer-agent test contribution rates (from raw CSV):')
print('Agent, Total_PRs, Test_PRs, Test_%')
for a in agents:
    s = summary['per_agent'][a]
    print(f"{a}, {s['total_prs']:,}, {s['test_prs']:,}, {s['test_pct']:.2f}%")
o = summary['overall']
print('\nOverall:')
print(f"Total_PRs = {o['total_prs']:,}, Test_PRs = {o['test_prs']:,}, Test_% = {o['test_pct']:.2f}%")
