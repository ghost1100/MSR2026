import pandas as pd
from collections import defaultdict
from pathlib import Path

csv_path = Path('data/raw/aidata.csv')
if not csv_path.exists():
    alt = Path('../data/raw/aidata.csv')
    csv_path = alt if alt.exists() else csv_path

if not csv_path.exists():
    print('ERROR: data/raw/aidata.csv not found')
    raise SystemExit(1)

usecols = ['agent','user']
chunksize = 200_000
unique_by_agent = defaultdict(set)

for chunk in pd.read_csv(csv_path, usecols=usecols, dtype={'agent':'category','user':'string'}, low_memory=False, chunksize=chunksize):
    for agent, user in zip(chunk['agent'], chunk['user']):
        if pd.isna(agent) or pd.isna(user):
            continue
        unique_by_agent[str(agent)].add(str(user))

summary = {agent: len(users) for agent, users in unique_by_agent.items()}
print('Unique users per agent:')
for agent in sorted(summary.keys()):
    print(f'- {agent}: {summary[agent]:,}')
print('\nTOTAL unique users across all agents:', len(set().union(*unique_by_agent.values())))
