# MSR 2026 Honours Project: AI Agents in Software Development

## Project Overview

This research investigates patterns in pull requests made by automated agents across GitHub repositories, with a focus on when their contributions can be trusted and where developers must exercise caution. Through comprehensive analysis of 932,791 pull requests from the complete MSR 2026 Challenge dataset, we uncover the hidden dynamics of human-AI collaboration in software development, this research project also serves as an extention of The Rise of AI Teammates in Software Engineering (SE) 3.0: How Autonomous
Coding Agents Are Reshaping Software Engineering we are now accepting that AI teammates are here and they are here to stay so how can we minimize damage and boost productivity.

### Central Research Theme

This study reveals both the promises and perils of AI-driven development. We examine three critical challenge segments that determine whether AI agents enhance or endanger software quality:

1. **Testing Behavior** - Do AI agents verify their own work? to be completely honest from my own experiance they often times don't and once you correct them, they act like a know it all, they say something along the lines of: "your'e complety right!!!!, but that only happens due to this and that" then you find your self going down the wrong rabbit hole chasing a clue which didnt matter from the start just for it to end up being a depricated library, a mismatch in configuration files or ports, or even a small semi colon somewhere.
2. **Code Patch Characteristics** - Are changes explainable and safe? reading code is not that challenging once a person is familiar with the syntax however sometimes they do hallucinate and add random bits and pieces that make no sense by make no sense I mean extra added functionality that breaks KISS or SRP principles.
3. **Adoption Patterns** - Who trusts AI, and when does it work? once more from experiance it's junior developers due to academic preassure and wanting to live the student life so we do tend to try and find the path with least resistance although it is not always rightious but it does make life easier.

### Research Questions & Challenge Segments

#### Challenge Segment 1: Testing Behavior
"Do AI agents verify their own work?" - A core caution signal

- **RQ1a**: How frequently do coding agents contribute tests?
- **RQ1b**: What types of tests are most common (unit, integration, end-to-end)?
- **RQ2**: What is the test-to-code churn ratio for different AI agents?

**Caution Indicator**: Agents that don't test their code may produce unverified, potentially dangerous changes.

#### Challenge Segment 2: Code Patch Characteristics
"Understanding the risk surface - are changes small and explainable, or large and unpredictable?"

- **RQ3**: How do agentic PRs change code (additions, deletions, files touched)?
- **RQ4**: How consistent are PR descriptions with actual code changes?

**Risk Assessment**: Large, poorly documented changes signal higher caution requirements.

#### Challenge Segment 3: Adoption & Practices
"Identifying safer collaboration patterns and the possibility of true human-AI partnership"

- **RQ5a**: Who adopts coding agents (newcomers vs experienced developers)?
- **RQ5b**: What practices correlate with higher-quality PRs?

**Trust Framework**: Understanding which developer behaviors lead to safer AI collaboration.

### Dataset & Scale

We analyze the complete MSR 2026 Challenge dataset containing 932,791 pull request records (754MB) - representing the largest empirical analysis of AI-generated contributions across GitHub repositories.

## Repository Structure

```
MSR/
├── data/                           # Datasets and samples
│   ├── raw/aidata.csv             # Complete MSR dataset (754MB, 932,791 records)
│   ├── processed/                 # Cleaned and processed data
│   │   ├── processed_dataset.csv  # Main processed dataset
│   │   ├── executive_summary.json # Executive summary of findings
│   │   ├── rq1_agent_distribution.json # RQ1 analysis results
│   │   └── rq2_test_ratios.json   # RQ2 analysis results
│   └── samples/                   # Development samples (1K, 50K subsets)
├── notebooks/                     # Research Question Analysis
│   ├── RQ1_Agent_Distribution.ipynb      # Agent patterns & test contributions
│   ├── RQ2_Test_to_Code_Ratio.ipynb     # Test-to-code ratio analysis
│   ├── RQ3_Code_Change_Analysis.ipynb   # GitHub API & change patterns
│   ├── RQ4_Description_Consistency.ipynb # NLP text consistency analysis
│   ├── RQ5_User_Adoption.ipynb          # User behavior & adoption patterns
│   ├── summary.ipynb                    # Combined analysis summary
│   ├── MSR_Visualization_Recreation.ipynb # Comprehensive visualization suite
│   ├── ErrorAnalysis.ipynb              # Data quality assessment
│   └── ReuseableCode.ipynb              # Utility functions & examples
├── src/                           # Core Python modules
│   ├── data_loader.py            # Robust data loading with fallbacks
│   ├── analysis.py               # Research question analysis functions
│   ├── analysis_ext.py           # Extended analysis functions
│   ├── plots.py                  # Visualization & dashboard utilities
│   ├── claude_analyzer.py        # Claude API integration for analysis
│   └── cache_utils.py            # Caching utilities for performance
├── outputs/                      # Generated results
│   ├── reports/                  # Analysis results (JSON format)
│   │   ├── analysis_with_visuals_*.json # Complete analysis results
│   │   └── complete_analysis_*.json     # Comprehensive analysis outputs
│   └── figures/                  # Visualizations and charts
│       ├── interactive_executive_dashboard.html # Interactive dashboard
│       └── visualization_summary_report.json   # Visualization metadata
├── docs/                         # Documentation and references
│   ├── Log.md                    # Development progress log
│   └── MSR2026_COMPLETE.tex      # Academic paper (LaTeX)
└── Automation Scripts
    ├── run_all.bat               # Windows batch automation
    ├── run_all.py                # Cross-platform Python pipeline
    ├── comprehensive_full_analysis.py # Complete dataset analysis
    ├── complete_analysis.py      # Analysis with visualizations
    ├── analysis_with_visuals.py  # Visual analysis pipeline
    └── Makefile                  # Make-based workflow automation
```

## Research Methodology & Tools

### Classification & Analysis Strategy

Given the massive scale (932,791+ PRs), we employ comprehensive statistical analysis and automated classification to:
- Analyze behavioral patterns across all AI agents
- Calculate statistical significance with unprecedented power
- Measure consistency between PR descriptions and actual code changes
- Generate publication-ready visualizations and insights

### Technical Stack

| Category | Tools & Libraries | Purpose |
|----------|------------------|---------|
| **Data Processing** | pandas, numpy | Large-scale data manipulation and analysis |
| **Statistical Analysis** | scipy, statsmodels | Hypothesis testing and effect size calculation |
| **Visualization** | matplotlib, seaborn, plotly | Professional research dashboards and interactive plots |
| **Development** | VS Code, GitHub, Jupyter | Version control and analysis environment |
| **Text Processing** | nltk, scikit-learn | Description consistency verification |
| **Performance** | pyarrow, fastparquet | Efficient data caching and storage |

## Requirements and Installation

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended) especially with how windows 11 crashes these days the second you download a framework or test editor or perhaps it is just my system.
- 8GB+ RAM for full dataset processing
- ~2GB free disk space for data and outputs

### Required Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `pandas` - Data analysis and manipulation
- `matplotlib` - Plotting and visualization
- `seaborn` - Statistical data visualization
- `jupyter` - Interactive notebooks
- `numpy` - Numerical computations
- `scipy` - Statistical analysis
- `plotly` - Interactive graphing
- `kaleido` - Static plotly image export
- `pyarrow` - Fast columnar storage
- `fastparquet` - Parquet file support
- `nltk` - Natural language processing
- `scikit-learn` - Machine learning tools
- `datasets` - Hugging Face dataset access
- `requests` - HTTP requests
- `python-dotenv` - Environment variable management

### Optional Dependencies
- `anthropic` - Claude API integration (for extended analysis) due to replication purposes and claude API keys being a subscription based resource I decided to focus more on implementation without it as much as possible, and that's where free tier Artificial intelegance came in handy, assisting me in figuiring out better more robust work arounds to problems in ways I did not expect.
## Getting Started

### Quick Start Options

#### Option 1: Complete Analysis (Recommended)
```bash
# Setup environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run complete analysis
python comprehensive_full_analysis.py
```

#### Option 2: Cross-Platform Automation
```bash
# Windows
run_all.bat

# Cross-platform
python run_all.py
("Recommended because its the version I worked on the most so I can somewhat gurentee it's functionality")
# Make-based (Linux/Mac)
make all
```

#### Option 3: Progressive Testing
```bash
# Start small for development
make test-small     # 1K records
make test-medium    # 50K records
make test-full      # Full dataset
```

#### Option 4: Individual Research Questions
```bash
# Run specific research questions
make rq1            # Agent Distribution Analysis
make rq2            # Test-to-Code Ratio Analysis
make rq3            # Code Change Analysis
make rq4            # Description Consistency Analysis
make rq5            # User Adoption Analysis
```

#### Option 5: Manual Notebook Execution
1. Open Jupyter: `jupyter notebook`
2. Navigate to `notebooks/` directory
3. Execute notebooks in order: RQ1 → RQ2 → RQ3 → RQ4 → RQ5 → summary

### Development Setup

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

## Study Results & Key Findings

### Comprehensive Analysis Results

**Dataset Coverage**: Complete analysis of 932,791 pull requests across 5 AI agents
**Statistical Power**: Chi-square = 389,069, p < 0.001, Cramér's V = 0.646 (large effect) AI also came in handy for segemts such as these because It honestly made no sense to me I thought I was doing rocket science for a second ("more like a whole day I was stuck on tutorial hell trying to find out what this could've possibly meant")
**Unique Contributors**: 299,294 unique developers analyzed

### Agent Performance Metrics

| Agent | Total PRs | Test Inclusion Rate | Market Share | Unique Users |
|-------|-----------|-------------------|--------------|--------------|
| **OpenAI Codex** | 813,821 | 98.5% | 87.2% | 251,447 |
| **GitHub Copilot** | 51,289 | 81.3% | 5.5% | 22,485 |
| **Claude Code** | 5,737 | 79.8% | 0.6% | 2,341 |
| **Devin** | 29,317 | 68.4% | 3.1% | 10,127 |
| **Cursor** | 32,627 | 18.7% | 3.5% | 12,894 |

### Key Research Discoveries

#### Testing Behavior Analysis
- **Overall Test Rate**: 93.8% across all 932,791 pull requests
- **Range**: 79.8 percentage point difference between highest (98.5%) and lowest (18.7%) performers
- **Statistical Significance**: Unprecedented statistical power confirms genuine behavioral differences ("without having to conduct this research project this outcome could have been predicted due to how AI development takes place not all models are trained on the same data types and some models speacialise in certain fields unlike basic general purpose LLMs trained on wikipedia and reddit")

#### Behavioral Signatures
1. **Testing-Centric Architecture (OpenAI Codex)**: Near-universal test coverage indicates quality-first training
2. **Balanced Development (Copilot, Claude)**: Moderate testing rates (79-81%) show feature-test balance
3. **Rapid Development Optimization (Cursor)**: Low test inclusion optimizes for development velocity
4. **Adaptive Specialization (Devin)**: Intermediate behavior suggests context-aware adaptation
devin and cursor are both very suitable for context awareness and fast development but lack testing depths unlike their counteroparts, how ever that makes them an interesting team mate to work with due to their unpredictability I used curor to make a front end for a basic snake game once to gauge its capabilies and I gave it a basic prompt, (something along the lines of make me a basic classic snake game using html, css and js)

#### Quality Assurance Findings
- **Consistent Acceptance Rates**: 89.1% - 94.6% across all agents despite testing differences
- **Organizational Adaptation**: Teams successfully maintain quality standards through compensatory measures
- **Experience Effects**: Testing behavior varies significantly across developer experience levels

### Generated Outputs

#### Analysis Reports
- `outputs/reports/complete_analysis_*.json` - Comprehensive statistical analysis
- `outputs/reports/analysis_with_visuals_*.json` - Analysis with visualization metadata
- `data/processed/executive_summary.json` - Executive summary of key findings
- `data/processed/rq1_agent_distribution.json` - Detailed agent analysis
- `data/processed/rq2_test_ratios.json` - Test ratio calculations

#### Visualizations
- `outputs/figures/interactive_executive_dashboard.html` - Interactive Plotly dashboard
- `outputs/figures/visualization_summary_report.json` - Visualization metadata
- Individual research question visualizations (PNG, PDF, SVG formats)
- Comprehensive statistical analysis charts and correlation matrices

#### Academic Outputs
- `docs/MSR2026_COMPLETE.tex` - Complete academic paper in LaTeX format
- Publication-ready visualizations and statistical analysis
- Comprehensive methodology documentation

## Research Methodology

### Progressive Analysis Approach
1. **Development Phase**: Start with 1K records for rapid iteration
2. **Validation Phase**: Scale to 50K records for methodology validation  
3. **Production Phase**: Execute full 932,791 dataset analysis
4. **Optimization**: Refine based on performance and insights

### Academic Standards
- **Reproducible Research**: All analyses can be re-run with single commands
- **Comprehensive Documentation**: Each notebook includes methodology and insights
- **Professional Reporting**: JSON exports suitable for thesis integration
- **Version Control**: Git-based workflow with structured commits

### Statistical Rigor
- **Population-Level Analysis**: Complete dataset eliminates sampling bias
- **Effect Size Quantification**: Cramér's V measures practical significance
- **Multiple Comparison Correction**: Bonferroni adjustment maintains family-wise error rate
- **Robust Validation**: Cross-validation across multiple analytical perspectives

## Contributing & Development

### Development Workflow
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

### Code Quality Standards
- **Error Handling**: Comprehensive try-catch blocks with meaningful messages
- **Data Validation**: Automated quality checks and health monitoring  
- **Documentation**: Inline documentation and README maintenance
- **Modularity**: Reusable functions and components
- **Logging**: Detailed execution logs for debugging and monitoring

## Academic Impact & Contributions

### Research Innovation Points
- **First Population-Scale AI Behavior Analysis**: Comprehensive study of 932,791 AI-generated contributions
- **Novel Behavioral Framework**: Systematic approach to identifying AI collaboration patterns
- **Multi-Dimensional Analysis**: Testing behavior + code characteristics + adoption patterns
- **Evidence-Based Guidelines**: Actionable insights for safer human-AI collaboration

### Methodological Contributions
- **Reusable Framework**: Template for MSR studies on AI-human collaboration
- **Statistical Validation**: Unprecedented statistical power for behavioral analysis
- **Comprehensive Pipeline**: End-to-end automation for reproducible research
- **Academic Standards**: Professional research output suitable for publication

### Practical Implications
- **Strategic Tool Selection**: Evidence-based approach to AI agent adoption
- **Workflow Adaptation**: Agent-specific quality assurance recommendations
- **Risk Assessment**: Framework for evaluating AI collaboration safety
- **Training Guidelines**: Best practices for teams adopting AI tools

## Conclusions

This comprehensive empirical study reveals profound behavioral differences between AI coding agents that fundamentally challenge assumptions about tool interchangeability. Key findings include:

1. **Behavioral Architecture**: AI agents exhibit distinct, embedded testing philosophies
2. **Statistical Robustness**: Large effect sizes with unprecedented statistical power
3. **Organizational Adaptation**: Teams successfully maintain quality despite agent differences
4. **Strategic Implications**: Evidence-based tool selection becomes critical for software quality

The era of generic AI integration is over. Evidence-based, agent-aware software engineering represents the future of effective AI-human collaboration in software development.

**Research Status**: Production-ready automated analysis pipeline with comprehensive academic documentation

**Last Updated**: November 6, 2025 | **Dataset**: Complete MSR 2026 Challenge (932,791 records)
| **Proportions** | Pie Charts | Share of AI PRs by type (features/bugs/tests) |

## Chi-square & Cramér's V — what they are and how we use them

This project reports two closely related statistics when assessing categorical associations between AI agent identity and testing behavior: the Chi-square (χ²) test of independence and Cramér's V (an effect-size measure). Below is a concise, practical summary of each, why both are necessary, how we compute them here, and where to find the generated outputs in this repository.

- Chi-square (χ²) test of independence
    - What it is: A non-parametric test that evaluates whether two categorical variables are independent. It compares observed counts in a contingency table to the counts expected if the variables were independent.
    - Why we use it: It tells us whether there is a statistically significant relationship between an AI agent (which agent created the PR) and whether a PR is test-related. With very large samples (like our full dataset), p-values become very small for even minor differences — so the χ² tells us whether an association exists, not how important it is.
    - How we compute it here: we build a contingency table with pandas (pd.crosstab(df['agent'], df['is_test_pr'])) and call scipy.stats.chi2_contingency to obtain the χ² statistic, p-value, degrees of freedom, and expected counts.
    - Where the result is produced/saved: the main implementation is in `comprehensive_full_analysis.py` (see the statistical significance section). Running the full analysis writes the statistics into `outputs/comprehensive_full_dataset_analysis.json` under `statistical_analysis.chi_square` and `p_value`, and these figures are echoed in console output when the script runs.

- Cramér's V (effect size)
    - What it is: A normalized measure of association derived from χ² for contingency tables. It ranges from 0 (no association) to 1 (perfect association). For an r x c table, it is defined as

        V = sqrt(χ² / (n * (k - 1)))

        where n is the total sample size and k = min(number_of_rows, number_of_columns).
    - Why we use it: Because statistical significance alone is not enough with large samples — Cramér's V quantifies the practical magnitude of the association so readers can judge how meaningful the relationship is in real terms.
    - Interpretation (used in this repo): commonly used thresholds are shown as guidance (not absolute):
        - V < 0.10: negligible
        - 0.10 ≤ V < 0.30: small
        - 0.30 ≤ V < 0.50: medium
        - V ≥ 0.50: large
    - How we compute it here: after obtaining χ² (from scipy), we compute V as shown above. The computation and interpretation logic are implemented in `comprehensive_full_analysis.py` which also prints a short interpretation string (e.g., "negligible", "small", "medium", "large").
    - Where the result is produced/saved: the computed Cramér's V is saved to `outputs/comprehensive_full_dataset_analysis.json` under `statistical_analysis.cramers_v` (and also shown in console output). Other pipeline outputs that summarize results (for example `outputs/reports/complete_analysis_*.json`) can also include these statistics depending on which analysis pipeline was run.

Why both are reported together
- χ² (and its p-value) answers "Is there evidence of an association?". With large n, even very small differences can be statistically significant.
- Cramér's V answers "How big is that association in practice?". Reporting both avoids over-interpreting trivially significant results.

Files and places to look (quick reference)
- Implementation and primary runner: `comprehensive_full_analysis.py` — builds the contingency table, runs scipy.stats.chi2_contingency, computes Cramér's V, prints the results, and saves them.
- Smaller, modular helpers: `src/analysis.py` contains helper utilities used by smaller analyses (test-detection helpers and per-agent summaries). For the full-sample χ² and V we rely on the complete-analysis script.
- Notebooks: `notebooks/RQ1_Agent_Distribution.ipynb` and `notebooks/RQ2_Test_to_Code_Ratio.ipynb` display and visualize agent/test relationships and may replicate or visualize the same χ²/ V results for specific subsets.
- Outputs:
    - `outputs/comprehensive_full_dataset_analysis.json` — primary JSON that contains the `statistical_analysis` block with `chi_square`, `p_value`, `cramers_v`, `effect_size`, `degrees_of_freedom`, and `sample_size`.
    - `outputs/reports/complete_analysis_*.json` — other analysis/visualization report files generated by auxiliary pipelines; some runs export the same statistics here as well.

How to reproduce the numbers locally
```powershell
# Windows (from the repo root)
python comprehensive_full_analysis.py
# or run the cross-platform pipeline
python run_all.py
```

Notes & caveats
- Large sample sizes amplify statistical power — always examine effect sizes (Cramér's V) alongside p-values.
- For multi-way comparisons and many agent categories we also consider multiple-comparison corrections (Bonferroni) elsewhere in analysis where appropriate; χ² + V remain the primary pairwise/contingency diagnostics for categorical associations.
