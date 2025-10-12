# src/data_loader.py
import pandas as pd
import os
from datasets import load_dataset

def load_aidev(local_path="data/raw/aidata.csv", from_huggingface=False, config="all_pull_request", sample_size=None):
    # Handle relative path from notebooks directory
    if not os.path.exists(local_path) and os.path.exists(f"../{local_path}"):
        local_path = f"../{local_path}"
    
    if from_huggingface:
        print(f"Loading dataset from Hugging Face with config '{config}'...")
        ds = load_dataset("hao-li/AIDev", config)
        print(f"Dataset loaded. Converting to pandas DataFrame...")
        df = ds['train'].to_pandas()
        print(f"DataFrame created with shape: {df.shape}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"Saving to {local_path}...")
        df.to_csv(local_path, index=False)
        print("Dataset saved successfully!")
    else:
        if not os.path.exists(local_path):
            print(f"Local file {local_path} not found. Use from_huggingface=True to download it first.")
            return None
        print(f"Loading dataset from local file: {local_path}")
        # For large files, load with low_memory=False to avoid mixed type warnings
        if sample_size:
            # Load full dataset first, then sample randomly to preserve agent distribution
            df_full = pd.read_csv(local_path, low_memory=False)
            if len(df_full) <= sample_size:
                df = df_full
                print(f"Loaded full dataset: {len(df)} rows")
            else:
                df = df_full.sample(n=sample_size, random_state=42)
                print(f"Loaded random sample of {sample_size} rows from {len(df_full)} total")
        else:
            df = pd.read_csv(local_path, low_memory=False)
    return df
