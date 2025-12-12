# src/data_loader.py
import pandas as pd
import os
from datasets import load_dataset

def load_aidev(local_path="data/raw/aidata.csv", from_huggingface=False, config="all_pull_request", sample_size=None, use_full_dataset=True):
    """
    Load AIDev dataset containing AI-generated pull request data
    
    Args:
        local_path: Path to local CSV file (relative to project root)
        from_huggingface: If True, download from HuggingFace instead of using local file
        config: HuggingFace dataset configuration name
        sample_size: Number of rows to randomly sample (only used if use_full_dataset=False)
        use_full_dataset: If True, load the entire dataset (default behavior)
    
    Returns:
        pandas.DataFrame: Loaded dataset with columns like 'title', 'body', 'agent', etc.
    """
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
        
        if use_full_dataset:
            # Load entire dataset with optimized data types for memory efficiency
            print("Loading complete dataset (932,791 records)...")
            dtype_optimizations = {
                'agent': 'category',
                'state': 'category',
                'user': 'string',
                'title': 'string',
                'body': 'string'
            }
            try:
                df = pd.read_csv(local_path, low_memory=False, dtype=dtype_optimizations, encoding='utf-8')
            except UnicodeDecodeError:
                print("UTF-8 encoding failed, trying latin-1...")
                df = pd.read_csv(local_path, low_memory=False, dtype=dtype_optimizations, encoding='latin-1')
            print(f"Loaded full dataset: {len(df):,} rows")
            print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        elif sample_size:
            # Legacy sampling mode
            try:
                df_full = pd.read_csv(local_path, low_memory=False, encoding='utf-8')
            except UnicodeDecodeError:
                df_full = pd.read_csv(local_path, low_memory=False, encoding='latin-1')
            if len(df_full) <= sample_size:
                df = df_full
                print(f"Loaded full dataset: {len(df)} rows")
            else:
                df = df_full.sample(n=sample_size, random_state=42)
                print(f"Loaded random sample of {sample_size} rows from {len(df_full)} total")
        else:
            # Default full dataset load
            try:
                df = pd.read_csv(local_path, low_memory=False, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(local_path, low_memory=False, encoding='latin-1')
    
    return df

def load_data_efficiently(use_full_dataset=True):
    """
    Load the dataset efficiently for analysis
    
    Args:
        use_full_dataset: If True, load all records. If False, use smaller sample.
    
    Returns:
        pandas.DataFrame: Loaded and optimized dataset
    """
    return load_aidev(use_full_dataset=use_full_dataset)
