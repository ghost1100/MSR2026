# MSR Project Main Entry Point
# Initial data loading and validation for AIDev dataset analysis
from src.data_loader import load_aidev
import os

# Intelligent data loading strategy - local first, then HuggingFace fallback
local_path = "data/raw/aidata.csv"
if os.path.exists(local_path):
    print("Loading sample of data from local file...")
    # Load subset for initial testing and validation
    df = load_aidev(sample_size=1000)  # First 1000 rows from local CSV
else:
    print("Local data file not found. Downloading subset from Hugging Face...")
    # Fallback to HuggingFace with smaller config for initial download
    df = load_aidev(from_huggingface=True, config="pull_request")

if df is not None:
    print(f"Dataset loaded successfully! Shape: {df.shape}")
    print("\nColumn names:")
    print(df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())
    print(f"\nDataset sample contains {len(df)} rows of pull request data.")
    
    # Display basic statistics for data validation
    print("\nBasic info about the dataset:")
    print(f"- States: {df['state'].value_counts().to_dict()}")
    print(f"- Agents: {df['agent'].value_counts().to_dict()}")
else:
    print("Failed to load dataset.")
