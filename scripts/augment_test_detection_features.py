import json
from pathlib import Path
from collections import defaultdict, Counter
import pandas as pd

try:
    from src.test_detection import detect_tests as robust_detect_tests
except Exception:
    robust_detect_tests = None

CSV_PATHS = [Path('data/raw/aidata.csv'), Path('../data/raw/aidata.csv')]

SIZE_COLUMNS = ['additions', 'deletions', 'changed_files', 'files_count', 'total_changes']
USER_COLUMNS = ['user_id', 'author_id', 'author_login', 'user_login']

def locate_csv():
    for p in CSV_PATHS:
        if p.exists():
            return p
    print('ERROR: data/raw/aidata.csv not found')
    raise SystemExit(1)

def detect_text(title: str, body: str) -> bool:
    if robust_detect_tests:
        return robust_detect_tests(title, body)
    # fallback simple keyword
    kw = ['test','spec','assert','pytest','unittest','jest','@Test','junit']
    text = f"{title}\n{body}".lower()
    return any(k in text for k in kw)

def compute_buckets(df: pd.DataFrame) -> pd.Series:
    # derive a size metric
    size = None
    if 'total_changes' in df.columns:
        size = df['total_changes']
    elif 'additions' in df.columns and 'deletions' in df.columns:
        size = (df['additions'].fillna(0).astype('Int64') + df['deletions'].fillna(0).astype('Int64')).astype('Int64')
    elif 'changed_files' in df.columns:
        size = df['changed_files'].fillna(0).astype('Int64')
    elif 'files_count' in df.columns:
        size = df['files_count'].fillna(0).astype('Int64')
    else:
        return pd.Series(['unknown'] * len(df), index=df.index)
    # bucket by magnitude
    bins = [0, 10, 50, 200, 1000, 5000, 10000]
    labels = ['0-10','11-50','51-200','201-1k','1k-5k','5k-10k','>10k']
    binned = pd.cut(size.fillna(0).astype(int), bins=bins + [10**9], labels=labels, right=True, include_lowest=True)
    binned = binned.astype(str).fillna('unknown')
    return binned

def main():
    csv_path = locate_csv()
    # Try to read optional columns if present
    probe = pd.read_csv(csv_path, nrows=1)
    cols = set(probe.columns)
    usecols = ['agent','title','body']
    size_cols = [c for c in SIZE_COLUMNS if c in cols]
    user_cols = [c for c in USER_COLUMNS if c in cols]
    usecols += size_cols + user_cols

    dtypes = {'agent': 'category', 'title': 'string', 'body': 'string'}
    for c in size_cols:
        dtypes[c] = 'Int64'
    for c in user_cols:
        dtypes[c] = 'string'

    chunksize = 50_000
    per_agent_counts = defaultdict(int)
    per_agent_tests = defaultdict(int)
    per_bucket_counts = defaultdict(int)
    per_bucket_tests = defaultdict(int)
    per_user_tests = Counter()

    processed = 0
    max_rows = 200_000  # cap for quick run; adjust as needed
    for chunk in pd.read_csv(csv_path, usecols=usecols, dtype=dtypes, low_memory=False, chunksize=chunksize):
        if processed >= max_rows:
            break
        chunk['title'] = chunk['title'].fillna('')
        chunk['body'] = chunk['body'].fillna('')
        # size buckets
        buckets = compute_buckets(chunk)
        # detection
        mask = [detect_text(t, b) for t, b in zip(chunk['title'], chunk['body'])]
        # agent aggregates
        gcount = chunk.groupby('agent', observed=True).size()
        for agent, n in gcount.items():
            per_agent_counts[str(agent)] += int(n)
        if any(mask):
            gtest = chunk.loc[mask].groupby('agent', observed=True).size()
            for agent, n in gtest.items():
                per_agent_tests[str(agent)] += int(n)
        # bucket aggregates
        bcount = buckets.value_counts()
        for lab, n in bcount.items():
            per_bucket_counts[str(lab)] += int(n)
        if any(mask):
            btest = buckets[pd.Series(mask, index=chunk.index)].value_counts()
            for lab, n in btest.items():
                per_bucket_tests[str(lab)] += int(n)
        # per-user tests (top K)
        if user_cols:
            user_key = user_cols[0]
            users = chunk[user_key].fillna('')
            tested_users = users[pd.Series(mask, index=chunk.index)]
            per_user_tests.update(tested_users.astype(str).tolist())
        processed += len(chunk)
    print(f"Processed ~{processed} rows")

    # summarize
    agents = sorted(per_agent_counts.keys())
    per_agent = {}
    for a in agents:
        tot = per_agent_counts[a]
        t = per_agent_tests.get(a, 0)
        per_agent[a] = {
            'total_prs': tot,
            'test_prs': t,
            'test_pct': (t / tot * 100.0) if tot else 0.0
        }

    buckets_sorted = sorted(per_bucket_counts.keys())
    per_size_bucket = {}
    for b in buckets_sorted:
        tot = per_bucket_counts[b]
        t = per_bucket_tests.get(b, 0)
        per_size_bucket[b] = {
            'total_prs': tot,
            'test_prs': t,
            'test_pct': (t / tot * 100.0) if tot else 0.0
        }

    top_users = per_user_tests.most_common(50)
    summary = {
        'per_agent': per_agent,
        'per_size_bucket': per_size_bucket,
        'top_users_by_test_prs': [{'user': u, 'test_prs': int(n)} for u, n in top_users],
        'notes': {
            'size_columns_used': size_cols,
            'user_column_used': user_cols[0] if user_cols else None
        }
    }

    repo_root = Path(__file__).resolve().parent.parent
    out_path = repo_root / 'outputs' / 'test_detection_augmentation.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {out_path}")

if __name__ == '__main__':
    main()
