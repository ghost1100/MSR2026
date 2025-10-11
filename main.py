from src.data_loader import load_aidev
import os

# Check if data file exists locally first
local_path = "data/raw/aidata.csv"
if os.path.exists(local_path):
    print("Loading sample of data from local file...")
    # Load just a sample first to test
    df = load_aidev(sample_size=1000)  # loads first 1000 rows from local CSV
else:
    print("Local data file not found. Downloading a smaller subset from Hugging Face...")
    # Try a smaller config first - 'pull_request' instead of 'all_pull_request'
    df = load_aidev(from_huggingface=True, config="pull_request")  # downloads from Hugging Face and saves locally

if df is not None:
    print(f"Dataset loaded successfully! Shape: {df.shape}")
    print("\nColumn names:")
    print(df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())
    print(f"\nDataset sample contains {len(df)} rows of pull request data.")
    
    # Show basic statistics
    print("\nBasic info about the dataset:")
    print(f"- States: {df['state'].value_counts().to_dict()}")
    print(f"- Agents: {df['agent'].value_counts().to_dict()}")
else:
    print("Failed to load dataset.")
