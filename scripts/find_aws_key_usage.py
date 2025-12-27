import pandas as pd
import sys
#inside one of the PRs I am investigating, I suspect an AWS key is present
# stubled upon it randomly while parsing data manually and github actually sent me an email for it as a warning to rotate all keys, what is confusing me is that the repo is still active 
CSV='comprehensive_pr_manual_verification_dataset.csv'
KEY='ASIAT64VHFT7ZHEMM3FK'
try:
    df=pd.read_csv(CSV,dtype=str).fillna('')
except Exception as e:
    print('Error reading CSV:',e)
    sys.exit(1)

mask = df.apply(lambda row: row.astype(str).str.contains(KEY).any(), axis=1)
found = df[mask]
if found.empty:
    print('No occurrences found')
else:
    for idx,row in found.iterrows():
        print('pr_id:', row.get('pr_id','(missing)'), 'agent:', row.get('agent',''), 'pr_title:', (row.get('pr_title','')[:120].replace('\n',' ')))
        # print the columns that contain the key
        for col in df.columns:
            val=str(row.get(col,''))
            if KEY in val:
                print('  column:',col)
                print('   snippet:', val[val.find(KEY)-40:val.find(KEY)+120])
    print('\nTotal rows with key:', len(found))
