# MSR Project Development Log

This document records daily iterations and sessions spent working on the MSR 2026 Honours Project: "AI Agents in Software Development - A Cautionary Tale of Trust and Verification", excluding time spent on external courses such as:

- [Claude Anthropic API Key Usage Course](https://anthropic.skilljar.com/claude-with-the-anthropic-api)
- [ChatGPT Prompt Engineering](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)
- [The Data Science Course: Complete Data Science Bootcamp (Udemy)](https://www.udemy.com/course/the-data-science-course-complete-data-science-bootcamp/?couponCode=25BBPMXINACTIVE)

## 📺 **Reference Video**

- [Jupyter Notebook In 10 Minutes(Colt Steele)](https://youtu.be/H9Iu49E6Mxs?si=luL7kHgePlwM7C7t)

## **AI Usage Policy & Acknowledgment Framework**

**Transparency Commitment**: All AI assistance used in this project is fully documented for academic integrity and reproducibility.

**Standard AI Usage Documentation Format:**
- **AI Tool Used**: [Specific AI system and version]
- **Tasks Assisted**: [Clear description of AI-supported activities]
- **Human Oversight**: [Validation and review processes applied]
- **Limitations**: [Acknowledged boundaries of AI contributions]
- **Original Work**: [Human-led research design and decision-making]

**Academic Integrity Standards:**
- All AI-generated code is reviewed, tested, and validated
- Research methodology and insights remain fully human-driven
- AI serves as a development tool, not a research collaborator
- Transparent documentation ensures reproducible research practices

---

## [Date: 2025-10-12] - Project Foundation & Infrastructure Development

**Summary of work performed today:**

### 🚀 **Initial Setup & Problem Resolution**
- **Issue Encountered**: FileNotFoundError when attempting to load AIDev dataset locally
- **Root Cause**: Missing local data file (data/raw/aidata.csv) with no fallback mechanism
- **Resolution**: Implemented robust data loading with intelligent fallback (local → Hugging Face → error handling)
- **Configuration Fix**: Resolved Hugging Face dataset config requirements (specified "pull_request" config)

### 📊 **Data Infrastructure Development**
- Created comprehensive data loading system (`src/data_loader.py`)
- Implemented memory-efficient sample loading for development (1K → 50K → 900K progression)
- Established error handling with meaningful user feedback
- Built data quality assessment framework with automated health monitoring

### 🔧 **Analysis Framework Creation**
- Developed core analysis functions (`src/analysis.py`) with research question focus:
  - `analyze_test_contributions()` - Test behavior analysis for RQ1/RQ2
  - `calculate_test_code_ratios()` - Test-to-code ratio calculations
  - `analyze_text_consistency()` - NLP consistency analysis for RQ4
  - `classify_users()` - User adoption pattern analysis for RQ5
- Created visualization suite (`src/plots.py`) with professional research dashboards
- Built reusable utilities for data validation and error detection

### 📓 **Research Question Structure Implementation**
**Completed Notebooks:**
1. **ErrorAnalysis.ipynb** - Comprehensive data quality assessment and error documentation
2. **ReuseableCode.ipynb** - Enhanced utility functions and development patterns
3. **RQ1_Agent_Distribution.ipynb** (renamed from exploration.ipynb) - Agent distribution and test contribution analysis

**Framework Notebooks Created:**
4. **RQ2_Test_to_Code_Ratio.ipynb** - Test-to-code ratio analysis with statistical framework
5. **RQ3_Code_Change_Analysis.ipynb** - GitHub API integration for code change analysis
6. **RQ4_Description_Consistency.ipynb** - NLP text analysis for PR description consistency
7. **RQ5_User_Adoption.ipynb** - User classification and adoption pattern analysis

### 🤖 **Professional Automation Pipeline**
**Created Three Automation Approaches:**
1. **Windows Batch Script** (`run_all.bat`) - Simple execution with progress tracking
2. **Cross-Platform Python Script** (`run_all.py`) - Advanced automation with JSON reporting
3. **Makefile** (`Makefile`) - Professional workflow with multiple targets:
   - `make test-small` (1K records), `make test-medium` (50K records), `make test-full` (900K records)
   - Individual research question execution (`make rq1-rq5`)
   - Environment setup and cleanup utilities

### 📚 **Documentation & Project Standards**
- **README.md**: Complete rewrite with cautionary tale narrative integration
  - Professional academic presentation with engaging storytelling
  - Comprehensive methodology documentation
  - Research question restructuring around challenge segments
  - Tool stack and visualization strategy documentation
- **requirements.txt**: Enhanced with NLP dependencies (nltk, scikit-learn, numpy)
- **Project Structure**: Organized with clear separation of concerns

### 🎯 **Research Progress Achieved**
- **RQ1 (Agent Distribution)**: ✅ Completed - ~15% test contribution rate identified
- **RQ2-RQ5**: 🟡 Frameworks ready for execution with established methodologies
- **Data Quality**: >95% completeness validated across 753MB dataset (~900K records)
- **Infrastructure**: Fully automated, reproducible pipeline established

**Key Insights Discovered:**
- Only ~15% of AI-generated PRs include test contributions (potential caution signal)
- Multiple AI agents with varying contribution patterns identified
- Robust data loading essential for large-scale MSR analysis
- Progressive scaling approach (1K→50K→900K) optimal for development

**Technical Achievements:**
- Error-resilient data pipeline with comprehensive fallback mechanisms
- Professional automation suitable for thesis-level reproducibility
- Modular analysis framework reusable for future MSR projects
- Academic-standard documentation with narrative engagement

**Next Session Goals:**
- Execute RQ2 test-to-code ratio analysis on larger dataset
- Configure GitHub API integration for RQ3 implementation
- Install and configure NLP libraries for RQ4 text analysis
- Begin user classification analysis for RQ5 adoption patterns
- Scale analysis from development samples to production dataset
- achive actual replicatable results and begin documentation
- begin researching material for dissertation
- begin gathering data/answering questions and creating presentable visualizations

**Time Investment**: ~27 hours of focused development and analysis work
**Lines of Code**: ~2000+ across notebooks, source modules, and automation scripts
**Files Created/Modified**: 15+ files including notebooks, source code, documentation, and automation scripts

###  **AI Usage Acknowledgment & Transparency**

**AI Assistant Used**: Claude 3.5 Sonnet (Anthropic) via VS Code Extension
**Role**: Development/Debuging assistance, documentation structure, and problem-solving support

#### **Key AI-Assisted Tasks:**
1. **Data Loading Infrastructure** - Generated robust fallback mechanisms and error handling
2. **Analysis Functions** - Created comprehensive research question analysis modules
3. **Automation Scripts** - Built cross-platform automation pipeline (batch, Python, Make)
4. **Documentation** - Enhanced README with narrative integration and technical documentation

#### **Representative Prompts Used:**
- *"Help me create a robust data loading function with fallback mechanisms for the AIDev dataset"*
- *"Create individual research question notebooks following academic standards"*
- *"Build a comprehensive automation pipeline with error handling and reporting"*
- *"Update the README to integrate the cautionary tale narrative professionally"*
- *"Generate comprehensive error analysis and data quality assessment functions"*

#### **Human Contributions:**
- **Research Design**: All research questions, methodology, and academic framework
- **Problem Identification**: Recognition of data loading issues and infrastructure needs
- **Quality Assurance**: Review, testing, and validation of all AI-generated code
- **Academic Integration**: Narrative theme development and thesis structure planning
- **Domain Expertise**: MSR methodology application and research question formulation

#### **AI Limitations Acknowledged:**
- AI provided implementation assistance but did not design the research approach
- All code was reviewed, tested, and validated by human researcher
- Research insights and academic conclusions remain fully human-driven
- AI served as a sophisticated development tool, not a research collaborator

#### **Ethical Use Declaration:**
- AI usage was transparent and documented throughout the development process
- All AI-generated content was reviewed for accuracy and appropriateness
- Academic integrity maintained through clear delineation of AI vs human contributions
- No AI-generated content was used without human oversight and validation

---

*This session established the complete foundation for a professional MSR thesis project with automated workflows, comprehensive analysis capabilities, and engaging academic presentation.*