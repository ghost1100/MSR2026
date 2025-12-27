"""
Compute agreement between auto 'High' predictions and manual labels.
Prints:
 - total manual-labeled rows
 - High -> manual Yes count
 - High -> manual No/None count (manual 'no' or blank)
 - Agreement rate (matches / manual_labeled_total)
"""
import pandas as pd
import sys

CSV='comprehensive_pr_manual_verification_dataset.csv'
try:
    df=pd.read_csv(CSV,dtype=str).fillna('')
except Exception as e:
    print('Error reading CSV:',e)
    sys.exit(1)

# Determine columns
man_col = 'was test included Y/N' if 'was test included Y/N' in df.columns else ('manual_testing_present' if 'manual_testing_present' in df.columns else None)
auto_col = 'test detection' if 'test detection' in df.columns else ('auto_conf' if 'auto_conf' in df.columns else None)

if man_col is None or auto_col is None:
    print('Required columns not found. Found columns:', list(df.columns))
    sys.exit(1)

# normalize manual label
def normalize_manual_label(x):
    s=str(x).strip().lower()
    if s=='':
        return ''
    if 'error' in s or '404' in s or 'n/a' in s or 'unknown' in s:
        return ''
    if 'no tests' in s or s in ('no','n','none') or 'not included' in s:
        return 'no'
    if 'partial' in s or 'partially' in s:
        return 'partial'
    if 'testing included' in s or 'extensive testing' in s or 'comprehensive testing' in s or 'included' in s or 'testing' in s:
        return 'yes'
    return s

# normalize auto

df['manual_norm'] = df[man_col].apply(normalize_manual_label)
df['auto_conf'] = df[auto_col].astype(str).str.strip().str.lower()

# Consider only rows with manual label present (non-empty)
manual_rows = df[df['manual_norm'] != '']
manual_total = len(manual_rows)

high_manual_yes = manual_rows[(manual_rows['auto_conf']=='high') & (manual_rows['manual_norm']=='yes')]
high_manual_no_or_none = manual_rows[(manual_rows['auto_conf']=='high') & (manual_rows['manual_norm']!='yes')]

# Agreement: auto_high==manual_yes OR auto_high!=manual_yes (i.e., equivalence between auto_high and manual_yes)
# For manual-labeled rows only
matches = manual_rows[((manual_rows['auto_conf']=='high') & (manual_rows['manual_norm']=='yes')) | ((manual_rows['auto_conf']!='high') & (manual_rows['manual_norm']!='yes'))]

print('Manual labeled rows:', manual_total)
print("Automated 'High' -> manual 'Yes':", len(high_manual_yes))
print("Automated 'High' -> manual 'Not Yes' (None/No/Other):", len(high_manual_no_or_none))
print('Agreement count:', len(matches), 'Agreement rate:', f"{(len(matches)/manual_total*100) if manual_total>0 else 0:.2f}%")

# Also print per-agent breakdown for manual rows
print('\nPer-agent breakdown (manual labeled rows):')
per_agent = manual_rows.groupby('agent').apply(lambda g: pd.Series({
    'manual_count': len(g),
    'high_and_yes': ((g['auto_conf']=='high') & (g['manual_norm']=='yes')).sum(),
    'high_and_not_yes': ((g['auto_conf']=='high') & (g['manual_norm']!='yes')).sum(),
    'agreement_count': (((g['auto_conf']=='high') & (g['manual_norm']=='yes')) | ((g['auto_conf']!='high') & (g['manual_norm']!='yes'))).sum()
}))
print(per_agent.to_string())
