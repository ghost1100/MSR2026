# MSR Project Makefile
# Automated analysis pipeline for all research questions

.PHONY: all setup install clean test-small test-medium test-full help

# Default target
all: setup run-analysis

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up MSR project environment..."
	python -m venv .venv
	.venv\Scripts\activate && pip install -r requirements.txt

# Install additional dependencies
install:
	@echo "Installing dependencies..."
	.venv\Scripts\activate && pip install -r requirements.txt

# Run all research question analyses
run-analysis:
	@echo "Running complete MSR analysis pipeline..."
	.venv\Scripts\activate && python run_all.py

# Run analysis on small dataset (1k rows)
test-small:
	@echo "Running analysis on small dataset (1k rows)..."
	.venv\Scripts\activate && python -c "import os; os.environ['SAMPLE_SIZE']='1000'; exec(open('run_all.py').read())"

# Run analysis on medium dataset (50k rows)
test-medium:
	@echo "Running analysis on medium dataset (50k rows)..."
	.venv\Scripts\activate && python -c "import os; os.environ['SAMPLE_SIZE']='50000'; exec(open('run_all.py').read())"

# Run analysis on full dataset (~900k rows)
test-full:
	@echo "Running analysis on full dataset..."
	.venv\Scripts\activate && python run_all.py

# Clean output files
clean:
	@echo "Cleaning output files..."
	if exist outputs\figures rmdir /s /q outputs\figures
	if exist outputs\reports rmdir /s /q outputs\reports
	mkdir outputs\figures
	mkdir outputs\reports

# Run individual research questions
rq1:
	@echo "Running RQ1: Agent Distribution Analysis..."
	.venv\Scripts\activate && jupyter nbconvert --to notebook --execute notebooks/RQ1_Agent_Distribution.ipynb

rq2:
	@echo "Running RQ2: Test-to-Code Ratio Analysis..."
	.venv\Scripts\activate && jupyter nbconvert --to notebook --execute notebooks/RQ2_Test_to_Code_Ratio.ipynb

rq3:
	@echo "Running RQ3: Code Change Analysis..."
	.venv\Scripts\activate && jupyter nbconvert --to notebook --execute notebooks/RQ3_Code_Change_Analysis.ipynb

rq4:
	@echo "Running RQ4: Description Consistency Analysis..."
	.venv\Scripts\activate && jupyter nbconvert --to notebook --execute notebooks/RQ4_Description_Consistency.ipynb

rq5:
	@echo "Running RQ5: User Adoption Analysis..."
	.venv\Scripts\activate && jupyter nbconvert --to notebook --execute notebooks/RQ5_User_Adoption.ipynb

# Help target
help:
	@echo "MSR Project - Available Commands:"
	@echo "  make all         - Setup environment and run complete analysis"
	@echo "  make setup       - Setup virtual environment and install dependencies"
	@echo "  make install     - Install/update dependencies"
	@echo "  make run-analysis - Run all research questions"
	@echo "  make test-small  - Test with 1k rows"
	@echo "  make test-medium - Test with 50k rows" 
	@echo "  make test-full   - Run with full dataset"
	@echo "  make clean       - Clean output directories"
	@echo "  make rq1-rq5     - Run individual research questions"
	@echo "  make help        - Show this help"