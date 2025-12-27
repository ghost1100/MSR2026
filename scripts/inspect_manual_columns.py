import pandas as pd
p='comprehensive_pr_manual_verification_dataset.csv'
df=pd.read_csv(p,dtype=str).fillna('')
cols=['manual_testing_present','was test included Y/N','test detection','auto_testing_keywords_found','auto_testing_keywords_count']
print('FOUND columns in file:')
print([c for c in cols if c in df.columns])
for c in cols:
    if c in df.columns:
        vals=df[c].astype(str).str.strip()
        nonempty=vals[vals!='']
        print('\nCOLUMN:',c,' non-empty count:',len(nonempty))
        print('SAMPLES ->', list(nonempty.head(10).unique())[:10])
    else:
        print('\nCOLUMN:', c, ' not present')
