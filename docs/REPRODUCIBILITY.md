Reproducibility:
Below is a concise mapping of the repository artifacts to the computations they perform and the simplest commands to reproduce the results used in the paper.

- `comprehensive_full_analysis.py` — Full-dataset production analysis (computes population-level statistics: χ², Cramér's V, per-agent counts/percentages, generates publication figures and writes `outputs/comprehensive_full_dataset_analysis.json`). Recommended for reproducing the paper numbers.
- `notebooks/RQ1_Agent_Distribution.ipynb` — Sample-based EDA for RQ1 (computes `is_test_pr`, per-agent test percentages, visualizations). Useful for interactive exploration and re-running smaller analyses.
- `notebooks/summary.ipynb` — Aggregates cached results (loads JSON in `data/processed/`), builds the executive summary/dashboard and re-creates summary figures.
- `src/data_loader.py` — Data-loading utilities (sampling, caching, and a full-data loader used by the production script).
- `src/analysis.py` — Reusable analysis functions (e.g., `analyze_test_contributions`) called by notebooks and used during sample analyses.
- `run_all.py` / `run_all.bat` — Orchestration scripts that run the pipeline end-to-end (calls the production analysis and optional visualization steps).

Where outputs are written:
- `outputs/comprehensive_full_dataset_analysis.json` — Full-analysis JSON (contains `chi_square`, `cramers_v`, per-agent stats).
- `outputs/figures/` — PNG/HTML figures used in the paper (test rates, agent distribution, dashboard, etc.).
- `data/processed/` — Cached per-RQ JSONs used by notebooks (e.g., `rq1_agent_distribution.json`, `rq2_test_ratios.json`).

Quick reproduce commands (Windows `cmd.exe`):

```cmd
cd c:\MSR
# create and activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 1) Full production analysis (population-level statistics and figures)
python comprehensive_full_analysis.py

# 2) Or run the cross-platform pipeline (runs smaller steps or full pipeline depending on args)
python run_all.py

# 3) Interactive exploration via notebooks
jupyter notebook
# then open notebooks/RQ1_Agent_Distribution.ipynb or summary.ipynb and run cells
```

Notes and tips
- The full analysis loads the complete dataset (~754MB) and can require significant memory (8+ GB recommended). For development, run the notebooks with smaller `sample_size` values (1k–50k) or use the provided samples in `data/samples/`.
- If you only need to reproduce the χ² and Cramér's V in the paper, running `comprehensive_full_analysis.py` will compute them and save the result to `outputs/comprehensive_full_dataset_analysis.json`.
- If you prefer the notebooks to trigger the same full analysis, you can import and call the analysis entry point from a notebook (e.g., `from comprehensive_full_analysis import analyze_complete_dataset; analyze_complete_dataset()`), but running the script is the simplest approach for reproducibility.
