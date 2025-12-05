import pandas as pd
import sys
path='data/raw/aidata.csv'
try:
    df=pd.read_csv(path, nrows=5)
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
print('Columns:', list(df.columns))
print(df.to_string(index=False))
