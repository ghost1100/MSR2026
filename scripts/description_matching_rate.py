import json
from pathlib import Path
import sys
import pandas as pd

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except Exception:
    print("scikit-learn not found. Please install: pip install scikit-learn")
    sys.exit(1)

CSV_PATHS = [Path('data/raw/aidata.csv'), Path('../data/raw/aidata.csv')]

def load_sample(n_samples: int = 20000, random_state: int = 42) -> pd.DataFrame:
    csv_path = None
    for p in CSV_PATHS:
        if p.exists():
            csv_path = p
            break
    if not csv_path:
        print('ERROR: data/raw/aidata.csv not found')
        sys.exit(1)
    usecols = ['agent', 'title', 'body']
    df = pd.read_csv(csv_path, usecols=usecols, dtype={'agent':'category','title':'string','body':'string'}, low_memory=False)
    # drop rows with both title and body null/empty
    df['title'] = df['title'].fillna('')
    df['body'] = df['body'].fillna('')
    df = df[(df['title'].str.len() > 0) | (df['body'].str.len() > 0)]
    if len(df) > n_samples:
        df = df.sample(n=n_samples, random_state=random_state)
    return df.reset_index(drop=True)

def compute_matching_rate(df: pd.DataFrame, threshold: float = 0.2):
    # Build TF-IDF for title and body jointly to share vocabulary
    texts = pd.concat([df['title'], df['body']], axis=0).astype(str).tolist()
    vec = TfidfVectorizer(min_df=2, max_df=0.95)
    tfidf = vec.fit_transform(texts)
    n = len(df)
    title_mat = tfidf[:n]
    body_mat = tfidf[n:]
    # Cosine similarity per row between title i and body i
    sims = (title_mat.multiply(body_mat)).sum(axis=1).A.ravel()  # fast diag dot
    # Normalize by L2 norms (already normalized by TfidfVectorizer) -> dot is cosine
    df = df.copy()
    df['cosine_similarity'] = sims
    df['match'] = df['cosine_similarity'] >= threshold
    overall_rate = float(df['match'].mean() * 100.0)
    per_agent = (
        df.groupby('agent', observed=True)['match']
          .mean()
          .mul(100.0)
          .round(4)
          .to_dict()
    )
    return {
        'threshold': threshold,
        'sample_size': int(len(df)),
        'overall_matching_rate_pct': overall_rate,
        'per_agent_matching_rate_pct': {str(k): float(v) for k, v in per_agent.items()},
        'notes': 'Cosine similarity between title and body TF-IDF vectors; match if >= threshold.'
    }

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--samples', type=int, default=20000, help='Number of PRs to sample')
    ap.add_argument('--threshold', type=float, default=0.2, help='Cosine similarity threshold for match')
    args = ap.parse_args()

    df = load_sample(n_samples=args.samples)
    result = compute_matching_rate(df, threshold=args.threshold)
    out_path = Path('outputs/description_matching_rate.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    print(f"\nWrote {out_path}")

if __name__ == '__main__':
    main()
