#!/usr/bin/env python3
"""
Quick check of agent column values
"""

import pandas as pd

# Load and inspect
df = pd.read_csv('data/raw/aidata.csv')

print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nAgent column unique values:")
print(df['agent'].value_counts())

print("\nFirst few agent values:")
print(df['agent'].head(10))

print("\nUser column top values:")
print(df['user'].value_counts().head(10))