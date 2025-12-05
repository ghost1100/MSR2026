# MSR 2026 Submission: AI Coding Agents Testing Behavior Analysis

## Paper Submission Files

### Main Paper (Conference Submission)
- **MSR2026_4p.tex** - LaTeX source (4-page limit)
- **MSR2026_4p.pdf** - Compiled PDF for submission

### Extended Version 
- **MSR2026_COMPLETE.tex** - Full paper with detailed analysis
- **MSR2026_COMPLETE.pdf** - Complete version (10 pages)

## Reproducibility Package

### Essential Code
- `comprehensive_full_analysis.py` - Main analysis script
- `download_dataset.py` - Dataset retrieval script
- `regenerate_all_figures.py` - Figure generation script
- `src/` - Core analysis modules
  - `analysis.py` - Statistical analysis functions
  - `data_loader.py` - Data loading utilities
  - `test_detection.py` - Test detection logic
  - `plots.py` - Visualization functions

### Key Data Files
- `test_rates_from_csv.json` - Per-agent test rates (ground truth)
- `comprehensive_full_dataset_analysis.json` - Full analysis results
- `execution_report.json` - Analysis execution log

### Generated Figures
- `complete_dataset_test_contribution_rates.png` - Main results chart
- `complete_dataset_agent_distribution.png` - Agent distribution
- `msr_complete_analysis.png` - Executive summary dashboard
- Additional figures in `figures/` directory

### Analysis Notebooks
- `summary.ipynb` - Overview of key findings
- `RQ1_Agent_Distribution.ipynb` - Agent usage patterns
- `RQ2_Test_to_Code_Ratio.ipynb` - Testing behavior analysis
- `RQ3_Code_Change_Analysis.ipynb` - Code change characteristics
- `RQ4_Description_Consistency.ipynb` - PR description analysis
- `RQ5_User_Adoption.ipynb` - User adoption patterns

## Data Dependencies

### External Dataset
- **Source**: AIDev dataset from HuggingFace (`hao-li/AIDev`)
- **Configuration**: `all_pull_request`
- **Size**: 932,791 pull requests
- **Access**: `download_dataset.py` script

### System Requirements
- Python 3.8+
- Dependencies in `requirements.txt`
- LaTeX distribution for paper compilation

## Reproduction Instructions

### 1. Setup Environment
```bash
pip install -r requirements.txt
```

### 2. Download Data
```bash
python download_dataset.py
```

### 3. Run Analysis
```bash
python comprehensive_full_analysis.py
```

### 4. Generate Figures
```bash
python regenerate_all_figures.py
```

### 5. Compile Papers
```bash
cd paper/
pdflatex MSR2026_4p.tex
pdflatex MSR2026_COMPLETE.tex
```

## Important Validity Notes

**This study identifies fundamental limitations in observational AI tool research:**

1. **Agent labels are unreliable** (metadata/self-reports with unknown accuracy)
2. **Statistical tests invalid** due to clustering violations  
3. **Severe confounding** by developer selection and project characteristics
4. **Results may reflect dataset artifacts** rather than genuine agent behavior

The paper serves as a **methodological warning** about challenges in AI tool evaluation using convenience datasets.

## Contact Information

**Author**: Ahmed Mursal  
**Institution**: Edinburgh Napier University  
**Email**: 40646515@live.napier.ac.uk  
**Repository**: https://github.com/ghost1100/MSR2026

## Acknowledgments

- H. Li et al. for the AIDev dataset
- Dr. Ashkan Sami (supervisor)
- Edinburgh Napier University for computational resources