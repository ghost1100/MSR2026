# MSR2026 Research Project - Enhanced Test Detection Study

## 🎯 Research Overview

This repository contains a comprehensive study of AI-assisted development and test detection methodologies using the MSR 2026 dataset (932,791 pull requests).

### Key Contributions:
1. **Enhanced Multi-Language Test Detection System** - Framework-aware detection across 29+ programming languages
2. **Methodological Critique** - Analysis of behavioral inference limitations in AI development research
3. **Statistical Validation** - Wilson score interval sampling and bidirectional verification methodology

## 🚀 Complete Reproducibility

### Quick Start (One Command):
```bash
python run_complete_research.py
```

This single command runs the entire research pipeline and generates all outputs.

### Requirements:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

### Essential Files:
- `run_complete_research.py` - Master reproducibility script
- `data/` - Raw MSR 2026 dataset
- `src/` - Core analysis modules
- `outputs/` - All generated research outputs
- `submission_files/` - Final paper and materials

### Key Research Scripts:
- `honest_analysis.py` - Basic dataset verification
- `analyze_languages.py` - Multi-language programming analysis
- `create_enhanced_detection.py` - Enhanced test detection system
- `complete_filtering_analysis.py` - Statistical filtering study
- `comprehensive_full_analysis.py` - Complete analysis pipeline

## 📊 Research Pipeline

The master script executes these stages:

1. **Dataset Verification** - Basic statistics and data quality checks
2. **Language Analysis** - 29+ programming language detection and analysis
3. **Enhanced Detection** - Multi-language, framework-aware test detection
4. **Verification Sampling** - Wilson score interval sampling for manual verification
5. **Statistical Analysis** - Complete filtering study with Gini coefficients, Shannon entropy
6. **Final Results** - Research outputs and paper materials

## 📈 Expected Outputs

After running `python run_complete_research.py`, check `outputs/` for:

- `research_execution_summary.json` - Execution log and status
- Language analysis results and distributions
- Enhanced detection system evaluation
- Statistical filtering study results
- Verification samples and protocols

## 🔬 Manual Verification

For manual verification of enhanced detection:
1. Open `verification_enhanced_detected.csv` (64 PRs)
2. Follow `enhanced_verification_protocol.txt`
3. Focus on precision measurement of enhanced system

## 📚 Documentation

- `REPRODUCIBILITY_GUIDE.md` - Detailed reproduction instructions
- `docs/` - Research papers and technical documentation
- `notebooks/` - Jupyter analysis notebooks (if applicable)

## 🎯 Research Questions

1. Can enhanced detection improve test identification precision?
2. How does language diversity affect test detection accuracy?
3. What are the limitations of behavioral inference in AI development research?

## 🏆 Results Summary

- **Enhanced Detection**: 12.8% test detection rate (vs 60% keyword-based)
- **Language Coverage**: 29+ programming languages analyzed
- **Verification Sample**: 500 PRs with Wilson score interval sampling
- **Statistical Rigor**: 95% confidence interval, ±5% margin of error

## 💻 Technical Requirements

- Python 3.8+
- pandas, numpy, scipy
- matplotlib, seaborn (for visualizations)
- See `requirements.txt` for complete dependencies

## 🤝 Contributing

This research is submission-ready. For questions or collaboration:
- Author: [REDACTED AUTHOR] ([REDACTED EMAIL])
- Institution: [REDACTED INSTITUTION]
- Conference: MSR 2026

---

**🚀 Ready for reproduction! Run `python run_complete_research.py` to reproduce all research results.**
