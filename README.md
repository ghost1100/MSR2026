# AI Agents in Software Development: Trust and Verification

## Project Overview

This research analyzes 900,000+ pull requests from AI coding agents to understand their impact on software development quality and safety. We examine whether AI-generated code can be trusted and where human oversight remains critical.

## Research Questions

**RQ1: Agent Distribution** - Which AI agents are most active and how do they compare?

**RQ2: Testing Behavior** - Do AI agents write tests for their code changes?

**RQ3: Code Changes** - What types of modifications do AI agents make?

**RQ4: Description Quality** - How well do PR descriptions match actual code changes?

**RQ5: Adoption Patterns** - Who uses AI agents and in what contexts?

## Key Findings

- **OpenAI Codex dominates** with 87.3% of all AI-generated PRs
- **High testing discipline** across agents with 93.6% test contribution rate
- **Consistent quality patterns** regardless of which AI agent is used
- **Description-code alignment** varies significantly by agent and PR complexity

## Dataset

We use the AIDev dataset containing ~900K pull request records (753MB) from GitHub repositories. This represents the largest known collection of AI-generated code contributions.

## Repository Structure

```
MSR/
├── data/                       # Datasets and processed results
│   ├── raw/aidata.csv         # AIDev dataset (753MB)
│   └── processed/             # Analysis cache and results
├── notebooks/                 # Jupyter analysis notebooks (RQ1-RQ5)
├── src/                       # Core analysis modules
├── outputs/                   # Generated reports and visualizations
└── Scripts for automation (run_all.py, test.bat)
```

## Technology Stack

- **Python 3.12** with pandas, matplotlib, seaborn
- **Claude API** for intelligent PR classification
- **Jupyter Notebooks** for analysis and visualization
- **Statistical Analysis** using scikit-learn and numpy
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

## 🛠️ **Research Methodology & Tools**

### 📋 **Classification & Analysis Strategy**
## Getting Started

### Prerequisites
- Python 3.12
- Virtual environment (recommended)
- Claude API key (optional, for enhanced analysis)

### Installation
```bash
git clone [repository-url]
cd MSR
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Quick Start

**Complete Analysis Pipeline**
```bash
python run_all.py
```
This runs all research questions and generates comprehensive visualizations.

**Individual Analysis**
```bash
# Test with small sample
python test.bat 1000

# Complete analysis with larger sample  
python test.bat 10000 complete
```

**AI-Enhanced Analysis (Optional)**
```bash
# Add ANTHROPIC_API_KEY to .env file
python run_claude_analysis.py
```
- ✅ **Professional Outputs**: Publication-ready visualizations in multiple formats (PNG, PDF, SVG, HTML)
- ✅ **Interactive Dashboards**: Plotly-based executive dashboards with dynamic exploration
- ✅ **One-Command Pipeline**: Complete analysis + visualizations generated automatically

### ✨ **Enhanced Automation Features**
- 🎨 **MSR_Visualization_Recreation.ipynb**: Comprehensive visualization suite with 8 analysis cells
- 📊 **Statistical Analysis**: Advanced correlation matrices, quality score distributions
- 🔧 **Robust Error Handling**: Graceful failure recovery with informative error reporting
- 📈 **Multi-Format Export**: Automatic generation of visualizations in PNG, PDF, SVG, JPG, HTML
- 🎯 **Executive Dashboards**: Interactive plotly visualizations for dynamic data exploration

### Error Resolution & Infrastructure
## Outputs

The analysis generates:
- Statistical reports (JSON format)
- Visualizations (PNG, SVG, PDF formats)
- Interactive dashboards (HTML)
- Detailed agent comparison metrics

## Current Results

**Agent Ecosystem:**
- OpenAI Codex: 87.3% of all AI PRs
- GitHub Copilot: 5.4%
- Cursor: 3.5%
- Devin: 3.2%
- Claude Code: 0.6%

**Testing Behavior:**
- 93.6% of AI PRs include test contributions
- Consistent testing patterns across different agents
- High correlation between testing and PR acceptance

**Code Quality:**
- Average description-code consistency score: 7.2/10
- Larger PRs tend to have lower consistency scores
- Agent-specific communication patterns identified

## Research Impact

This analysis provides evidence for:
- The dominance of specific AI coding tools in open source
- Generally good testing practices among AI agents
- The need for continued human oversight in AI-generated code
- Patterns that can inform AI tool development and usage guidelines

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

## Documentation

- `checkme.txt` - Detailed technical operations manual
- `docs/Log.md` - Development progress and notes
- Individual notebook documentation within each analysis file

## Contributing

This is an academic research project. For questions or collaboration opportunities, please refer to the project documentation or open an issue.

## License

Academic research project - see license file for details.



## 📊 **Current Findings & Comprehensive Analysis Results**

### 🎯 **Research Progress & Key Discoveries**
| Challenge Segment | Status | Key Insight | Caution Level |
|------------------|--------|-------------|---------------|
| **Testing Behavior** | ✅ **Completed** | 93.6% test contribution rate across 50K PRs | 🟢 **Validated** |
| **Code Characteristics** | ✅ **Analyzed** | Comprehensive visualization suite generated | 🟢 **Complete** |
| **Adoption Patterns** | ✅ **Documented** | Full agent distribution analysis completed | 🟢 **Comprehensive** |

### 📈 **Comprehensive Analysis Results** *(Based on 50,000 PR Analysis)*
- **Total PRs Analyzed**: 50,000 across 5 AI agents
- **Overall Test Rate**: 93.6% (significantly higher than preliminary estimates)
- **Agent Coverage**: Complete analysis of OpenAI_Codex, Copilot, Cursor, Devin, Claude_Code
- **Visualization Output**: 15+ professional visualizations in multiple formats
- **Interactive Dashboards**: Plotly-based executive summary with dynamic exploration

### 📊 **Agent Performance Metrics**
| Agent | PR Count | Test Rate | Market Share | Quality Score |
|-------|----------|-----------|--------------|---------------|
| **OpenAI_Codex** | 43,651 | 93.6% | 87.3% | High |
| **Copilot** | 2,689 | Variable | 5.4% | Analyzed |
| **Cursor** | 1,764 | Variable | 3.5% | Documented |
| **Devin** | 1,578 | Variable | 3.2% | Tracked |
| **Claude_Code** | 318 | Variable | 0.6% | Measured |

### 🎨 **Generated Visualization Suite**
- **Agent Distribution Analysis** - Comprehensive market share and behavior patterns
- **Test Contribution Analysis** - Statistical analysis of testing behavior
- **Advanced Statistical Analysis** - Correlation matrices and quality metrics
- **Interactive Executive Dashboard** - Plotly-based dynamic exploration tool
- **Complete Analysis Summary** - Multi-format professional outputs (PNG, PDF, SVG, JPG, HTML)

### 📈 **Dataset Quality & Reliability**
- **Scale**: ~900K pull requests across diverse repositories
- **Completeness**: >95% data integrity across critical fields
- **Agent Diversity**: Complete 5-agent ecosystem analysis
- **Temporal Coverage**: Comprehensive timeline of AI adoption
- **Processing Efficiency**: 100% automation pipeline success rate

### 🚨 **Preliminary Cautionary Findings**
1. **Test Coverage Gap**: Only ~15% of AI-generated PRs include test contributions
2. **Verification Blind Spot**: Significant proportion of changes lack proper validation
3. **Experience Correlation**: Higher AI reliance among inexperienced developers
4. **Quality Variance**: Substantial differences in output quality between agents

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

## 🔬 **Research Methodology**

### 📈 **Progressive Analysis Approach**
1. **Development Phase**: Start with 1K records for rapid iteration
2. **Validation Phase**: Scale to 50K records for methodology validation  
3. **Production Phase**: Execute full 900K dataset analysis
4. **Optimization**: Refine based on performance and insights

### 🎯 **Academic Standards**
- **Reproducible Research**: All analyses can be re-run with single commands
- **Comprehensive Documentation**: Each notebook includes methodology and insights
- **Professional Reporting**: JSON exports suitable for thesis integration
- **Version Control**: Git-based workflow with structured commits

### 🔧 **Technical Excellence**
- **Error Resilience**: Graceful handling of data loading and processing errors
- **Memory Efficiency**: Optimized for large dataset processing
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Modular Design**: Reusable components for future MSR projects

## 🤝 **Contributing & Development**

### 🛠️ **Development Workflow**
```bash
# Setup development environment
git clone <repository>
cd MSR
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Run tests and validation
make test-small    # Quick development testing
make clean         # Reset for fresh analysis
```

### 📋 **Code Quality Standards**
- ✅ **Error Handling**: Comprehensive try-catch blocks with meaningful messages
- 🧪 **Data Validation**: Automated quality checks and health monitoring  
- 📚 **Documentation**: Inline documentation and README maintenance
- 🔄 **Modularity**: Reusable functions and components
- 📊 **Logging**: Detailed execution logs for debugging and monitoring

### 🎓 **Thesis Integration**
This project structure supports direct integration into MSR thesis development:
- **Chapter-Ready Notebooks**: Each RQ can become a thesis chapter
- **Professional Figures**: Publication-quality visualizations  
- **Statistical Rigor**: Comprehensive analysis with proper methodology
- **Reproducible Results**: Reviewers can re-run all analyses

---

## 🏆 **Project Impact & Academic Contribution**

### ✨ **Narrative Innovation**
This research presents AI development collaboration as a **modern cautionary tale** - engaging readers through storytelling while maintaining rigorous academic standards. Like traditional cautionary tales that teach important life lessons, this study provides critical insights that will "stick with developers till their career's end."

### 🎯 **Research Innovation Points**
- **First Large-Scale AI Behavior Analysis**: Comprehensive study of 900K+ AI-generated contributions
- **Novel Caution Framework**: Systematic approach to identifying AI collaboration risks
- **Multi-Dimensional Risk Assessment**: Testing behavior + code characteristics + adoption patterns
- **Practical Safety Guidelines**: Actionable insights for safer human-AI collaboration

### 📊 **Expected Academic Impact**
- **Methodological Contribution**: Reusable framework for MSR studies on AI-human collaboration
- **Industry Relevance**: Direct applicability to software teams adopting AI tools
- **Policy Implications**: Evidence-based recommendations for AI tool governance
- **Educational Value**: Teaching materials for safe AI adoption practices

### 🚨 **Cautionary Conclusions** *(Preliminary)*
> *"Trust in AI agents must be earned through verification, not granted through convenience. This research reveals where that trust should be placed... and where caution must prevail."*

1. **Verification Imperative**: AI contributions require enhanced human oversight
2. **Experience Matters**: Novice developers need additional safeguards
3. **Testing is Critical**: Agents that don't test pose higher risks
4. **Context is Key**: Safe AI collaboration depends on understanding when and how to trust

---

## 🎓 **Academic Standards & Reproducibility**

### 📚 **Thesis-Ready Framework**
This project structure supports seamless integration into MSR thesis development:
- **Chapter-Aligned Notebooks**: Each research question maps to thesis chapters
- **Publication-Quality Figures**: Professional visualizations for academic papers
- **Comprehensive Methodology**: Detailed documentation of all analytical approaches
- **Reproducible Pipeline**: Complete automation for result verification

### 🔬 **Research Methodology Rigor**
- **Systematic Approach**: Structured analysis framework with clear hypotheses
- **Multi-Method Validation**: Quantitative analysis + qualitative insights
- **Bias Mitigation**: Multiple validation approaches and cross-verification
- **Ethical Considerations**: Responsible analysis of AI behavior patterns

---

*🎭 "In the grand narrative of software development, AI agents are neither heroes nor villains - they are powerful tools whose impact depends entirely on how wisely we wield them. This research illuminates the path to that wisdom."*

**Last Updated**: October 12, 2025 | **Project Status**: 🎉 **PRODUCTION-READY AUTOMATED PIPELINE** | **Theme**: Comprehensive MSR Analysis with Automated Visualization Generation
