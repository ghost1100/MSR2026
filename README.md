# MSR 2026 Honours Project: AI Agents in Software Development

## 🎯 Overview
This project investigates patterns in pull requests made by automated agents in open-source repositories. Through comprehensive analysis of the AIDev dataset, we address five key research questions about AI-driven software development practices.

### 🔬 Research Questions
1. **RQ1**: What is the distribution of AI agents and their test contribution patterns?
2. **RQ2**: What is the test-to-code churn ratio for different AI agents?
3. **RQ3**: How do agentic PRs change code (additions/deletions/modifications)?
4. **RQ4**: How consistent are PR descriptions with actual code changes?
5. **RQ5**: What are the adoption patterns among newcomers vs experienced developers?

## 📊 Dataset
We analyze the **AIDev dataset** from Hugging Face (`hao-li/AIDev`) containing ~900K pull request records (753MB) with comprehensive metadata about AI-generated contributions across GitHub repositories.

## 📁 Repository Structure
```
MSR/
├── 📊 data/                    # Datasets and samples
│   ├── raw/aidata.csv          # AIDev dataset (753MB, ~900K records)
│   ├── processed/              # Cleaned and processed data
│   └── samples/                # Development samples (1K, 50K subsets)
├── 📓 notebooks/               # Research Question Analysis
│   ├── RQ1_Agent_Distribution.ipynb      # Agent patterns & test contributions
│   ├── RQ2_Test_to_Code_Ratio.ipynb     # Test-to-code ratio analysis
│   ├── RQ3_Code_Change_Analysis.ipynb   # GitHub API & change patterns
│   ├── RQ4_Description_Consistency.ipynb # NLP text consistency analysis
│   ├── RQ5_User_Adoption.ipynb          # User behavior & adoption patterns
│   ├── ErrorAnalysis.ipynb              # Data quality assessment
│   └── ReuseableCode.ipynb              # Utility functions & examples
├── 🔧 src/                     # Core Python modules
│   ├── data_loader.py          # Robust data loading with fallbacks
│   ├── analysis.py             # Research question analysis functions
│   └── plots.py                # Visualization & dashboard utilities
├── 📈 outputs/                 # Generated results
│   ├── reports/                # Analysis results (JSON format)
│   └── figures/                # Visualizations and charts
├── 📚 docs/                    # Documentation and references
└── 🚀 Automation Scripts
    ├── run_all.bat             # Windows batch automation
    ├── run_all.py              # Cross-platform Python pipeline
    └── Makefile                # Make-based workflow automation
```

## ✨ Key Features

### 🎯 **Research Question Framework**
- **Structured Analysis**: Individual notebooks for each research question
- **Progressive Methodology**: Scalable from 1K → 50K → 900K records
- **Academic Standards**: Thesis-ready documentation and methodology
- **Reproducible Results**: Automated execution with detailed reporting

### 🔧 **Robust Infrastructure** 
- **Intelligent Data Loading**: Automatic fallback (local → Hugging Face → error handling)
- **Memory Optimization**: Efficient processing with configurable sample sizes
- **Error Recovery**: Comprehensive try-catch blocks with meaningful feedback
- **Progress Tracking**: Real-time status indicators and execution logging

### 📊 **Comprehensive Analysis Tools**
- **Data Quality Assessment**: Automated error detection and health monitoring
- **Multi-Agent Comparison**: Side-by-side analysis of AI agent behaviors  
- **Statistical Analysis**: Test-to-code ratios, consistency metrics, adoption patterns
- **Visualization Suite**: Professional charts and research dashboards

### 🤖 **AI-Specific Features**
- **Agent Pattern Recognition**: Behavior analysis across different AI agents
- **Test Contribution Tracking**: Automated detection of test-related changes
- **GitHub API Integration**: Real-time code change analysis (RQ3)
- **NLP Text Analysis**: Description consistency and quality scoring (RQ4)

### 🚀 **Professional Automation**
- **One-Click Execution**: Complete pipeline automation with single command
- **Multi-Platform Support**: Windows batch, Python scripts, Make workflows
- **Execution Reporting**: Detailed JSON reports with timing and success metrics
- **Development Testing**: Progressive scaling for optimization (1K→50K→900K)

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

## 🚀 Getting Started

### 📋 Prerequisites
```bash
# Setup virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### ⚡ Quick Start Options

#### **Option 1: One-Click Automation (Recommended)**
```bash
# Windows
run_all.bat

# Cross-platform
python run_all.py

# Make-based (Linux/Mac)
make all
```

#### **Option 2: Progressive Testing**
```bash
# Start small for development
make test-small     # 1K records
make test-medium    # 50K records  
make test-full      # Full 900K dataset
```

#### **Option 3: Individual Research Questions**
```bash
# Run specific research questions
make rq1            # Agent Distribution Analysis
make rq2            # Test-to-Code Ratio Analysis  
make rq3            # Code Change Analysis
make rq4            # Description Consistency Analysis
make rq5            # User Adoption Analysis
```

#### **Option 4: Manual Notebook Execution**
1. Open Jupyter: `jupyter notebook`
2. Navigate to `notebooks/` directory
3. Execute notebooks in order: RQ1 → RQ2 → RQ3 → RQ4 → RQ5

### 🔧 **Development Setup**
```python
# For custom analysis or development
from src.data_loader import load_aidev
from src.analysis import analyze_test_contributions
from src.plots import create_research_dashboard

# Load sample data
df = load_aidev(sample_size=1000)  # Start small

# Run analysis
df_analyzed, stats = analyze_test_contributions(df)

# Create visualizations
fig = create_research_dashboard(df_analyzed)
```

## 📊 **Current Status & Results**

### ✅ **Completed Infrastructure**
- **Data Pipeline**: Robust loading with fallback mechanisms (local → Hugging Face)
- **Research Framework**: 5 individual notebooks with structured analysis
- **Automation Suite**: 3 execution approaches (batch, Python, Make)
- **Quality Assessment**: Comprehensive error detection and health monitoring
- **Visualization Tools**: Professional charts and research dashboards

### 🎯 **Research Question Progress**
| Research Question | Status | Key Findings |
|------------------|--------|--------------|
| **RQ1**: Agent Distribution | ✅ Completed | ~15% test contribution rate identified |
| **RQ2**: Test-to-Code Ratio | 🟡 Framework Ready | Ratio calculation logic implemented |
| **RQ3**: Code Change Analysis | 🟡 API Integration Ready | GitHub API framework established |
| **RQ4**: Description Consistency | 🟡 NLP Framework Ready | Text analysis infrastructure complete |
| **RQ5**: User Adoption | 🟡 Classification Ready | User behavior models implemented |

### 📈 **Dataset Insights** (Sample Analysis)
- **Total Records**: ~900K pull requests (753MB dataset)
- **Agent Distribution**: Multiple AI agents with varying contribution patterns
- **Data Quality**: >95% completeness across key columns
- **Test Contributions**: ~15% of PRs contain test-related changes
- **State Distribution**: Majority of PRs are in 'closed' state

### 🚀 **Automation Capabilities**
```bash
# Available automation commands
make all          # Complete pipeline (setup → analysis → reporting)
make test-small   # Development testing (1K records)
make test-medium  # Validation testing (50K records) 
make test-full    # Production analysis (900K records)
make clean        # Reset outputs for fresh analysis
```

## 📚 **Documentation & Outputs**

### � **Generated Reports**
- `outputs/execution_report.json` — Automation pipeline results
- `outputs/error_analysis_report.json` — Data quality assessment
- `outputs/final_analysis_summary.json` — Comprehensive project summary
- `outputs/recommendations.md` — Best practices and guidelines

### 📊 **Research Outputs** 
- `outputs/figures/` — Professional visualizations and charts
- `outputs/reports/` — Research question results (JSON format)
- Individual notebook results with embedded analysis and insights

### 🔧 **Development Resources**
- `checkme.txt` — Pro tips and best practices checklist
- `src/` modules — Reusable functions for analysis and visualization
- Error logs and debugging information for troubleshooting

## Contributing
This project follows best practices for data science workflows:
- ✅ Robust error handling and logging
- 🧪 Comprehensive data validation
- 📚 Extensive documentation
- 🔄 Reusable, modular components
