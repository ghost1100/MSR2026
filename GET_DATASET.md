# Dataset Download Instructions

## Large Dataset File

Due to GitHub's file size limitations, the large dataset file `aidata.csv` (718.91 MB) is not included directly in the repository.

## How to Download the Dataset

### Option 1: Automatic Download (Recommended)
Run the provided download script:
```bash
python download_dataset.py
```

This script will:
- Download the AIDev dataset from HuggingFace
- Place it in the correct location (`data/raw/aidata.csv`)
- Verify the file integrity

### Option 2: Manual Download
1. Visit the HuggingFace dataset page: https://huggingface.co/datasets/AIDev/AIDev
2. Download the dataset file
3. Place it as `data/raw/aidata.csv` in the project root

### Verification
After downloading, verify the dataset is correctly placed:
- File location: `data/raw/aidata.csv`
- Expected size: ~719 MB
- Format: CSV with pull request data

### Note for Reviewers
This dataset is essential for reproducing the results in the MSR2026 paper. The download script ensures you get the exact same dataset version used in our analysis.