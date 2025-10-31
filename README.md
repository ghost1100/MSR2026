# AI Agents in Software Development: Trust and Verification

## Project Overview

This research analyzes over 900,000 pull requests from AI coding agents to understand their impact on software development quality and safety. We examine whether AI-generated code can be trusted and where human oversight remains critical.

## Research Questions

**RQ1: Agent Distribution** - Which AI agents are most active and how do they compare?

**RQ2: Testing Behavior** - Do AI agents write tests for their code changes?

**RQ3: Code Changes** - What types of modifications do AI agents make?

**RQ4: Description Quality** - How well do PR descriptions match actual code changes?

**RQ5: Adoption Patterns** - Who uses AI agents and in what contexts?

## Key Findings

- OpenAI Codex dominates with 87.3% of all AI-generated PRs
- High testing discipline across agents with 93.6% test contribution rate
- Consistent quality patterns regardless of which AI agent is used
- Description-code alignment varies significantly by agent and PR complexity

## Dataset

We use the AIDev dataset containing approximately 900K pull request records (753MB) from GitHub repositories. This represents one of the largest known collections of AI-generated code contributions.

## Repository Structure

```
MSR/
├── data/                       # Datasets and processed results
│   ├── raw/                   # AIDev dataset (753MB, gitignored)
│   ├── processed/             # Analysis cache and results (gitignored)
│   └── samples/               # Development samples (gitignored)
├── notebooks/                 # Jupyter analysis notebooks (RQ1-RQ5)
│   ├── RQ1_Agent_Distribution.ipynb
│   ├── RQ2_Test_to_Code_Ratio.ipynb
│   ├── RQ3_Code_Change_Analysis.ipynb
│   ├── RQ4_Description_Consistency.ipynb
│   ├── RQ5_User_Adoption.ipynb
│   └── summary.ipynb
├── src/                       # Core analysis modules
│   ├── data_loader.py         # Data loading utilities
│   ├── analysis.py            # Research question analysis functions
│   ├── claude_analyzer.py     # Claude API integration
│   └── plots.py               # Visualization utilities
├── outputs/                   # Generated reports and visualizations
│   ├── reports/               # Analysis results (JSON format)
│   └── figures/               # Visualizations and charts
├── tests/                     # Testing and validation scripts
│   ├── test_*.py             # Unit and integration tests
│   ├── validate_agents.py    # Agent validation
│   └── verify_system.py      # System verification
├── docs/                      # Documentation
│   └── Log.md                # Development progress log
├── main.py                    # Main analysis entry point
├── run_*.py                   # Automation scripts
├── requirements.txt           # Python dependencies
├── CHECKME.md                # Technical operations manual
└── README.md                 # This file
```

## Technology Stack

- Python 3.12 with pandas, matplotlib, seaborn
- Claude API for intelligent PR classification
- Jupyter Notebooks for analysis and visualization
- Statistical Analysis using scikit-learn and numpy
│   ├── raw/aidata.csv          # AIDev dataset (753MB, ~900K records)
│   ├── processed/              # Cleaned and processed data
│   └── samples/                # Development samples (1K, 50K subsets)
├── notebooks/                  # Research Question Analysis
│   ├── RQ1_Agent_Distribution.ipynb      # Agent patterns & test contributions
│   ├── RQ2_Test_to_Code_Ratio.ipynb     # Test-to-code ratio analysis
│   ├── RQ3_Code_Change_Analysis.ipynb   # GitHub API & change patterns
│   ├── RQ4_Description_Consistency.ipynb # NLP text consistency analysis
│   ├── RQ5_User_Adoption.ipynb          # User behavior & adoption patterns
│   ├── ErrorAnalysis.ipynb              # Data quality assessment
│   └── ReuseableCode.ipynb              # Utility functions & examples
├── src/                        # Core Python modules
│   ├── data_loader.py          # Data loading with fallbacks
│   ├── analysis.py             # Research question analysis functions
│   └── plots.py                # Visualization utilities
├── outputs/                    # Generated results
│   ├── reports/                # Analysis results (JSON format)
│   └── figures/                # Visualizations and charts
├── docs/                       # Documentation and references
└── Automation Scripts
    ├── run_all.bat             # Windows batch automation
    ├── run_all.py              # Cross-platform Python pipeline
    └── Makefile                # Make-based workflow automation
```

## Research Methodology

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

### Usage

**Complete Analysis Pipeline**
```bash
python run_all.py
```

**Individual Analysis**
```bash
# Test with small sample
python test.bat 1000

# Complete analysis with larger sample
python test.bat 10000 complete
```

**Enhanced Analysis (Optional)**
```bash
# Add ANTHROPIC_API_KEY to .env file
python run_claude_analysis.py
```

## Outputs

The analysis generates:
- Statistical reports (JSON format)
- Visualizations (PNG, SVG, PDF formats)
- Interactive dashboards (HTML)
- Detailed agent comparison metrics

## Results

**Agent Distribution:**
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

## Documentation

- `checkme.txt` - Technical operations manual
- `docs/Log.md` - Development progress and notes
- Individual notebook documentation within each analysis file

## Contributing

This is an academic research project. For questions or collaboration opportunities, please refer to the project documentation or open an issue.

## License

Academic research project - see license file for details.
## Research Impact

This analysis provides evidence for:
- The dominance of specific AI coding tools in open source
- Generally good testing practices among AI agents
- The need for continued human oversight in AI-generated code
- Patterns that can inform AI tool development and usage guidelines
