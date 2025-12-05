# AIDev Dataset: Data Dependencies and Project Data Flow

This short guide explains how the AIDev dataset is used in this repo, how files depend on each other, and what each section is responsible for. It’s intended as a quick reference for reproducibility and onboarding.

## Source and Scope
- Source: Hugging Face dataset `hao-li/AIDev`
- Configuration used here: `all_pull_request`
- Local raw export: `data/raw/aidata.csv`
- Population size used in this project: `932,791` pull requests (PRs)

Note: The AIDev dataset may offer additional configurations/splits. This repository analyzes only the PR-level configuration (`all_pull_request`). Refer to the dataset page for other configs when needed.

## Raw Data Schema (columns)
From `data/raw/aidata.csv` (peeked from file):
- `id`: Numeric PR identifier (global)
- `number`: PR number (repository-local ID)
- `title`: PR title string (used in test-detection and communication metrics)
- `user`: GitHub username of PR author (used for unique-user counts)
- `user_id`: Numeric GitHub user ID
- `state`: PR state (`open`, `closed`, `merged` encoded via timestamps)
- `created_at`: ISO timestamp PR was opened
- `closed_at`: ISO timestamp PR was closed (if applicable)
- `merged_at`: ISO timestamp PR was merged (if applicable)
- `repo_url`: API URL for the repository
- `repo_id`: Numeric repository ID
- `html_url`: Web URL for the PR
- `body`: PR description/body text (used in test-detection and documentation signals)
- `agent`: AI agent label inferred by original dataset authors (categorical): `OpenAI_Codex`, `Copilot`, `Claude_Code`, `Devin`, `Cursor`

## What Each Field Is Used For (analysis responsibilities)
- Testing behavior: `title`, `body` (keyword detection), plus file-level/context when available
- Acceptance/merge status: `state`, `merged_at`, `closed_at`
- Agent attribution: `agent`
- Adoption metrics: `user`, `user_id` (unique users per agent)
- Temporal analyses: `created_at`
- Repository-level linking: `repo_id`, `repo_url`, `html_url`

## Repository Data Flow (end-to-end)
1) Raw dataset
- `data/raw/aidata.csv`  ⟵ exported from `hao-li/AIDev` (`all_pull_request`)

2) Loading/utilities
- `src/data_loader.py`: loads CSV (or downloads via Hugging Face if requested) and applies dtype optimizations
- `scripts/peek_csv_header.py`: quick header preview of the CSV
- `scripts/check_unique_users.py`: recompute unique-user counts per agent directly from raw CSV

3) Core analysis and metrics
- `src/analysis.py`: test detection helpers and summarization logic
- `comprehensive_full_analysis.py` (and `run_all.py`): orchestrate full computations
- Outputs written to `outputs/comprehensive_full_dataset_analysis.json`:
  - `dataset_info`: sizes, unique agents/users, memory footprint, analysis date
  - `agent_distribution`: per-agent counts and percentages
  - `test_behavior`: per-agent and overall test rates, test PR counts
  - `statistical_analysis`: chi-square, degrees of freedom, Cramér’s V, sample size

4) Figures and visuals
- `regenerate_all_figures.py`: generates publication figures from JSON metrics and/or CSV
- Figures saved to `outputs/figures/` (e.g.,
  - `complete_dataset_test_contribution_rates.png`
  - `complete_dataset_agent_distribution.png`
  - `complete_dataset_comprehensive_analysis.png`
  - `advanced_statistical_analysis.png`
  - `summary_dashboard.png`
  - `msr_complete_analysis.png`)

5) Manuscript
- `docs/MSR2026_COMPLETE.tex`: references figures in `outputs/figures/` and cites key numbers from `outputs/comprehensive_full_dataset_analysis.json`
- PDF compiled via `pdflatex` from `docs/`

## Minimal Repro Commands (Windows cmd)
- Peek CSV header/columns
```
python scripts\peek_csv_header.py
```
- Unique users per agent (directly from raw CSV)
```
python scripts\check_unique_users.py
```
- Recompute key stats (chi-square, V) with and without Devin (from JSON metrics)
```
python scripts\recompute_stats.py
```
- Regenerate figures
```
python regenerate_all_figures.py
```
- Compile paper (from `docs/`)
```
pdflatex -interaction=nonstopmode MSR2026_COMPLETE.tex
```

## Dependency Graph (conceptual)
```
hao-li/AIDev (all_pull_request)
          │
          ▼
 data/raw/aidata.csv
          │
          ├── src/data_loader.py → in-memory DataFrame
          │
          ├── src/analysis.py + comprehensive_full_analysis.py / run_all.py
          │             │
          │             └── outputs/comprehensive_full_dataset_analysis.json
          │
          ├── regenerate_all_figures.py
          │             └── outputs/figures/*.png|.svg|.pdf
          │
          └── docs/MSR2026_COMPLETE.tex → MSR2026_COMPLETE.pdf
```

## Notes and Limitations
- Agent labels come from dataset metadata/heuristics; attribution noise is possible.
- Test detection (keyword-based in titles/bodies/paths) is a proxy and may have false positives/negatives.
- The project’s primary analysis uses the complete PR-level configuration; other dataset configs (if any) are out of scope here.

## Provenance and Versioning
- Dataset: `hao-li/AIDev`, configuration `all_pull_request`
- Project’s metrics file: `outputs/comprehensive_full_dataset_analysis.json` includes `analysis_date` for when results were last computed.

This document aims to make the data dependencies transparent so others can reproduce, audit, or extend the analysis with confidence.
