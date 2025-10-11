# MSR 2026 Honours Project: Caution & Automated Agents

## Overview
This project investigates patterns in pull requests made by automated agents in open-source repositories, focusing on:
- Test contributions by automated agents
- Test-to-code churn ratio
- Consistency between PR descriptions and code changes
- Factors affecting PR quality
- Adoption patterns among newcomers and experienced developers

## Dataset
We use the **AIDev dataset** from Hugging Face (`hao-li/AIDev`) which contains comprehensive pull request data from AI-generated contributions across various GitHub repositories.

## Repository Structure
- `data/` — Datasets (raw, processed, samples)
  - `raw/aidata.csv` — AIDev dataset (753MB)
  - `processed/` — Cleaned and processed data
  - `samples/` — Sample datasets for development
- `notebooks/` — Research Question Analysis
  - `RQ1_Agent_Distribution.ipynb` — Agent distribution and test contribution analysis
  - `RQ2_Test_to_Code_Ratio.ipynb` — Test-to-code ratio analysis
  - `RQ3_Code_Change_Analysis.ipynb` — Code change analysis with GitHub API
  - `RQ4_Description_Consistency.ipynb` — NLP description consistency analysis
  - `RQ5_User_Adoption.ipynb` — User adoption pattern analysis
  - `ErrorAnalysis.ipynb` — Comprehensive error analysis and data quality assessment
  - `ReuseableCode.ipynb` — Enhanced reusable functions and utilities
- `src/` — Python source code
  - `data_loader.py` — Robust data loading with fallback mechanisms
  - `analysis.py` — Core analysis functions for all research questions
  - `plots.py` — Visualization utilities and research dashboards
- `outputs/` — Generated reports and figures
  - `reports/` — Analysis results and insights (JSON format)
  - `figures/` — Visualizations and charts
- `docs/` — Reference material and documentation
- **Automation Scripts:**
  - `run_all.bat` — Windows batch script for automated analysis
  - `run_all.py` — Cross-platform Python automation script
  - `Makefile` — Make-based automation with multiple targets

## Key Features

### 🔧 Robust Data Loading
- **Fallback mechanisms**: Automatic fallback from local files to Hugging Face download
- **Error handling**: Comprehensive try-catch blocks with meaningful error messages
- **Memory optimization**: Efficient loading with sample size options for development
- **Progress tracking**: Clear status indicators and logging

### 📊 Data Quality Analysis
- **Comprehensive error detection**: Missing values, duplicates, type inconsistencies
- **Automated reporting**: JSON and visual reports for data quality metrics
- **Health monitoring**: Real-time data completeness and consistency tracking
- **Validation utilities**: Reusable functions for data structure validation

### 🛠️ Reusable Components
- **DataQualityAnalyzer class**: Modular data quality assessment tool
- **Safe operation wrappers**: Error-safe function execution utilities
- **Validation functions**: Comprehensive data structure and content validation
- **Cleaning pipelines**: Automated data cleaning with configurable strategies

## Recent Improvements (October 2025)

### Error Resolution
- ✅ **FileNotFoundError**: Fixed missing local data file issue with intelligent fallback
- ✅ **Dataset Configuration**: Resolved Hugging Face dataset config requirements
- ✅ **Memory Management**: Optimized loading for large datasets (753MB)

### Enhanced Functionality
- 🔍 **Comprehensive Error Analysis**: Detailed detection and categorization of data issues
- 📈 **Visual Dashboards**: Interactive charts for data quality monitoring
- 🔧 **Reusable Functions**: Modular components for future projects
- 📋 **Automated Reporting**: JSON exports and markdown documentation

## Getting Started

### Prerequisites
```bash
# Install required packages
pip install -r requirements.txt
```

### Quick Start
```python
# Load data with robust error handling
from src.data_loader import load_aidev
import os

# Check if local file exists, download if needed
local_path = "data/raw/aidata.csv"
if os.path.exists(local_path):
    df = load_aidev(sample_size=1000)  # Load sample for development
else:
    df = load_aidev(from_huggingface=True, config="pull_request")
```

### 🚀 Automated Analysis Pipeline

#### Windows (Batch Script)
```cmd
# Run all research questions automatically
run_all.bat
```

#### Cross-Platform (Python)
```bash
# Run complete analysis pipeline
python run_all.py

# Or activate virtual environment first
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
python run_all.py
```

#### Make-based Automation
```bash
# Complete setup and analysis
make all

# Individual targets
make setup          # Setup environment
make test-small     # Test with 1k rows
make test-medium    # Test with 50k rows  
make test-full      # Run with full dataset
make clean          # Clean outputs

# Individual research questions
make rq1            # Agent Distribution
make rq2            # Test-to-Code Ratio
make rq3            # Code Change Analysis
make rq4            # Description Consistency
make rq5            # User Adoption
```

#### Manual Notebook Execution
1. **RQ1 - Agent Distribution**: `notebooks/RQ1_Agent_Distribution.ipynb`
2. **RQ2 - Test Ratios**: `notebooks/RQ2_Test_to_Code_Ratio.ipynb`
3. **RQ3 - Code Changes**: `notebooks/RQ3_Code_Change_Analysis.ipynb`
4. **RQ4 - Text Consistency**: `notebooks/RQ4_Description_Consistency.ipynb`
5. **RQ5 - User Adoption**: `notebooks/RQ5_User_Adoption.ipynb`

## Data Quality Metrics
- **Dataset Size**: 753MB (full dataset), 1000+ samples available
- **Completeness**: >95% data completeness across key columns
- **Structure**: 14 columns including PR metadata, timestamps, and agent information
- **Quality**: Comprehensive validation and error detection implemented

## Documentation
- 📊 Error analysis report: `outputs/error_analysis_report.json`
- 📝 Best practices: `outputs/recommendations.md`
- 🎯 Project summary: `outputs/final_analysis_summary.json`
- 📋 Analysis logs: `outputs/error_analysis.log`

## Contributing
This project follows best practices for data science workflows:
- ✅ Robust error handling and logging
- 🧪 Comprehensive data validation
- 📚 Extensive documentation
- 🔄 Reusable, modular components
