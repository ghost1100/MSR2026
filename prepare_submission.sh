#!/bin/bash
# MSR2026 Submission Setup Script
# Creates a clean submission branch with only essential files

echo "Setting up MSR2026 submission branch..."

# Create essential directories
mkdir -p submission_files/paper
mkdir -p submission_files/code
mkdir -p submission_files/data
mkdir -p submission_files/figures
mkdir -p submission_files/notebooks

# Copy paper files
cp docs/MSR2026_4p.tex submission_files/paper/
cp docs/MSR2026_4p.pdf submission_files/paper/
cp docs/MSR2026_COMPLETE.tex submission_files/paper/
cp docs/MSR2026_COMPLETE.pdf submission_files/paper/

# Copy essential code
cp src/*.py submission_files/code/
cp *.py submission_files/code/
cp requirements.txt submission_files/

# Copy key data files
cp outputs/test_rates_from_csv.json submission_files/data/
cp outputs/comprehensive_full_dataset_analysis.json submission_files/data/

# Copy figures
cp -r outputs/figures/* submission_files/figures/

# Copy essential notebooks
cp notebooks/summary.ipynb submission_files/notebooks/
cp notebooks/RQ*.ipynb submission_files/notebooks/

echo "Submission files prepared in submission_files/ directory"