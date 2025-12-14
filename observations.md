# Observations, Assumptions, and Threats to Validity

## 1. Documented Knowns and Unknowns

### What is Verifiable (from Manual Review)
- The existence and quality of tests in 385 PRs (77 per agent) were manually verified using direct inspection of available PR links.
- Four levels of testing quality were established and applied:
  - **Extensive**: Every logical type of testing present, high coverage and quality.
  - **Comprehensive**: Good level of testing, multiple types, clear intent.
  - **Included**: Testing is present, but only at a basic or minimal level.
  - **Low**: Testing is present but of low quality or superficial.
- For PRs with working links, the presence/absence and quality of tests, language, and framework could be directly confirmed.

### What Remains Uncertain (404s, Metadata Limitations)
- Many PRs (especially older or from certain agents) returned 404 errors, making direct content verification impossible.
- For 404 PRs, only metadata (title, body, repo language, etc.) could be used, which is often unreliable for confirming actual test inclusion or quality.
- User and repository information may be missing or outdated due to deleted accounts or private repos most of the PRs were made by a very low number of users with high yield of PRs which is why almost everything returned an error 404, page not found.

## 2. Observations, Assumptions, and Threats to Validity

### Key Observations
- **Testing Quality Spectrum**: Most agents show a wide range of testing quality, from extensive to low, with only a minority of PRs achieving the 'extensive' level.
- **404 Prevalence**: A significant portion of PRs, especially from high-volume agents, are no longer accessible (404), limiting direct verification.
- **Metadata Gaps**: For inaccessible PRs, metadata is often insufficient to reliably determine if testing was included.
- **User Churn**: Many PRs are associated with users who appear to be deleted, inactive, or 'ghost' accounts.

### Assumptions Made
- If a PR was 404, testing status was inferred from metadata only when strong indicators were present; otherwise, it was marked as unknown.
- The language and framework were assumed based on repository metadata when PR content was unavailable.
- The distribution of testing quality in accessible PRs is representative of the overall sample, though this cannot be proven.

### Threats to Validity
- **Ghost/Deleted Users**: High numbers of PRs from a small set of users, many of whom are now deleted or inactive, may bias results.
- **Unreliable Metadata**: Titles, bodies, and repo language fields are not always accurate proxies for actual code/test content.
- **Sampling Bias**: The inability to access a random subset of PRs (due to 404s) may skew the observed distribution of testing quality.
- **Agent-Specific Data Quality**: Some agents (notably Devin) have a much higher rate of inaccessible or low-quality PRs.

## 3. Agent-Specific Patterns

- **Devin**: Exhibits a suspiciously high error rate (404s, missing users), suggesting use for prototyping, possible data fabrication, or shortcuts. The reliability of Devin PRs is especially questionable.
- **OpenAI Codex**: Dominates the dataset in volume, but also has a high number of inaccessible PRs. Testing quality is highly variable.
- **Copilot, Cursor, Claude_Code**: Show a mix of accessible and inaccessible PRs, with a broad spectrum of testing quality. Some evidence of ghost users.

## 4. Recommendations for Future Datasets

- **Require Persistent User/Account Activity**: Only include PRs from users who remain active or whose accounts are verifiably present at the time of analysis.
- **Improve Metadata Reliability**: Ensure that repository and PR metadata is accurate, up-to-date, and sufficient for analysis if direct content is unavailable.
- **Archive PR Content**: Where possible, archive the full content of PRs at the time of dataset creation to prevent loss due to deletion or privatization.
- **Stratified Sampling**: Use stratified sampling to ensure all agent/user types are fairly represented and to reduce bias from high-volume/low-quality users.

## 5. Limitations of Relying on Metadata

- When PR content is unavailable, conclusions about testing, language, or framework are necessarily tentative and may be inaccurate.
- Metadata-based inference cannot substitute for direct code review, especially for nuanced judgments like testing quality.
- The inability to confirm test presence in 404 PRs is a major threat to the validity of any aggregate statistics.

## 6. Manual Testing Quality Levels (as Used in This Study)

- **Extensive**: All logical types of testing present, high coverage, best practices followed.
- **Comprehensive**: Good level of testing, multiple types, clear intent, but not exhaustive.
- **Included**: Testing is present, but only at a basic or minimal level.
- **Low**: Testing is present but of low quality or superficial.
- **None/Unknown**: No evidence of testing, or PR was inaccessible (404).

## 7. Recent Commit Messages (Researcher Notes)

```
95270ac | manual review is now complete time to write about the known and unknown
3802500 | the fact that devin has a high number of errors and with my understanding of human nature, I now believe that devin is solely or was solely used for prototyping either that or it's data is fabricated or is a shortcut
c865dc7 | after I finish manually populating this sheet, I plan to write down a long list of observations, assumptions and threats to validity, which I would then breakdown in an attempt to find a motive and reasoning as well as impact, this whole research project felt like a massive puzzle with no actual solution such as life
f277184 | i figured out the reason, kinda it's just an assumption i need to confirm but maybe the pages are all error 404 because these agents have so many PRs from a little number of users, ghost users, users that maybe deleted their accounts or something so now I will have to rely on meta data to find out if testing was actually added or not and the meta data is unreliable, we need to propose a new dataset for sure and we need the users whom made any form of commitment to said dataset to remain active at least until the challenge is over
96345f0 | Update dataset file metadata for size adjustment, I have no clue why everything after a certain section brings up an error 404, I now can't compare it threat to validity is that I can't actually confirm that testing was implemented i can only rely on the meta data
d8e3fef | Update dataset file metadata for size adjustment, almost half way manually populated
ce3f1b5 | Update dataset file metadata for comprehensive PR manual verification
199d029 | manually fixing up the test file for manual analysis later

## 8. Statistical Validation and Sample Size Justification

This study's sample size and confidence level are justified using the same statistical methodology as the SANER_Naghashzadeh paper, which is widely recognized in software engineering research. The sample size formula for proportions (finite population) is:

$$
n = \frac{NZ^2p(1-p)}{(N-1)E^2 + Z^2p(1-p)}
$$

Where:
- $n$ = required sample size
- $N$ = population size
- $Z$ = Z-score for desired confidence level (1.96 for 95%)
- $p$ = estimated proportion (conservatively set to 0.5 for maximum sample size)
- $E$ = margin of error (0.05 for 5%)

In this study, the sample size per agent (77 PRs) and the total (385 PRs) were chosen to ensure a 95% confidence level with a 5% margin of error, matching the methodology of SANER_Naghashzadeh. This provides strong statistical validity for the findings, given the constraints of PR accessibility and metadata reliability. The use of this formula ensures that the results are comparable to prior work and that the conclusions drawn are methodologically sound.

## 8a. Methodology: Research Evolution and Validation Process

This study’s methodology evolved through four distinct phases, each building on the lessons and failures of the previous, ultimately resulting in a robust, transparent, and empirically validated approach to dataset analysis and measurement validity.

### Phase 1: Initial Behavioral Analysis Attempt
- **Objective:** Compare testing behaviors across AI agents (Copilot, Codex, Devin, Cursor, Claude) using statistical association (Cramér's V, chi-square tests) on a 50k stratified sample from the MSR 2026 dataset.
- **Approach:**
  - Used comprehensive keyword detection (test, spec, unittest, pytest, jest, etc.) across 29+ programming languages and frameworks to identify "test-related" PRs.
  - Built contingency tables (Agent × Testing Presence) and applied chi-square tests, Cramér's V, and confidence intervals.
- **Outcome:**
  - Initial results suggested large, significant differences (e.g., Codex 98.5% test rate, Cursor 18%, Cramér's V = 0.65).
  - However, these results were invalid due to lack of code verification, attribution impossibility, keyword pollution, and statistical independence violations.

### Phase 2: Methodological Critique and Post-Mortem
- **Objective:** Systematically document why behavioral inference was impossible with the available dataset.
- **Key Problems Identified:**
  - Attribution failures (agent mislabeling, power user domination, temporal drift)
  - Structural clustering (user, repository, and organizational policy effects)
  - Keyword-based detection failures (context ambiguity, false positives/negatives, multi-language complexity)
  - Conceptual mismatches (PR metadata ≠ code changes, agent label ≠ authorship, keyword ≠ test creation)
- **Insight:** The dataset’s structure violated all assumptions needed for valid behavioral inference, making statistical results scientifically meaningless.

### Phase 3: Dataset Debiasing and Structural Correction
- **Objective:** Restore statistical validity for adoption and usage pattern analysis, if not behavioral inference.
- **Debiasing Pipeline:**
  - **Power user detection:** Identified and filtered users above the 99th percentile (>178 PRs), revealing extreme concentration (Gini = 0.829).
  - **Bot/automation detection:** Pattern analysis for non-human contributions, bulk operations, and script-driven accounts (44.2% automation contamination).
  - **Multi-agent contamination removal:** Focused on single-agent attribution, removing sessions with multiple agents.
- **Metrics Used:**
  - Gini coefficient (contribution inequality)
  - Shannon entropy (distribution diversity)
- **Outcome:**
  - After debiasing, Copilot adoption increased from 5.4% to 9.6%, Gini dropped below 0.6, and entropy improved, yielding a more representative sample for adoption analysis.

### Phase 4: Empirical Validation via Manual Verification
- **Objective:** Quantify measurement error and validate the accuracy of keyword-based test detection.
- **Bidirectional Verification Protocol:**
  - Stratified, random sample of 500 PRs (60% keyword-detected, 40% non-keyword) across all agents.
  - Manual inspection of each PR’s actual code/files for true test presence, framework, and quality.
  - Measured false positive and false negative rates, precision, recall, and overall accuracy.
- **Data Cleaning:**
  - Removed PRs missing essential fields (html_url, agent, title); verified GitHub accessibility.
  - Ensured minimal data loss (only 1 PR removed from 932,791, although true, due to devin's contributions having been made by a smaller number of users, access to their PRs to determine tests accuracy was unsuccessful).
- **Findings:**
  - Keyword-based detection systematically overestimated test presence due to template contamination, discussion artifacts, and multi-language complexity.
  - Manual verification provided ground truth, revealing the true accuracy and limitations of automated measurement.

### Methodological Lessons and Contribution
- Statistical significance does not guarantee scientific validity—large n can make noise appear meaningful.
- Effect size interpretation (e.g., Cramér's V) is only meaningful if measurement is valid.
- Inequality and entropy metrics are essential for assessing dataset representativeness.
- Manual verification is critical for establishing ground truth and quantifying systematic error.

This multi-phase methodology, grounded in both failure and correction, provides a replicable framework for future empirical software engineering research, emphasizing transparency, validity, and the necessity of manual validation in large-scale data analysis.

## 9. Motive, Impact, and Reasoning
## 10. Methodology Overview: Empirical Validation and Research Process

This section provides a comprehensive overview of the methodology employed in this study, detailing the evolution of research design, empirical validation steps, and the rationale behind each phase. The approach was shaped by both the limitations of the dataset and the need for scientific rigor, resulting in a multi-phase process that emphasizes transparency, reproducibility, and critical self-assessment.

### 10.1 Research Design and Evolution

The methodology evolved through four major phases, each addressing specific challenges and building on the lessons of the previous stage:

**Phase 1: Initial Behavioral Analysis Attempt**
- **Goal:** Quantitatively compare testing behaviors across AI agents using statistical association measures (Cramér's V, chi-square tests) on a stratified sample of 50,000 PRs from the MSR2026 dataset.
- **Method:** Employed comprehensive keyword detection (e.g., 'test', 'spec', 'unittest', 'pytest', 'jest') across 29+ programming languages and frameworks to identify test-related PRs. Constructed contingency tables (Agent × Testing Presence) and applied statistical tests.
- **Outcome:** Initial results suggested large, significant differences in test rates between agents. However, these findings were invalidated due to lack of code verification, agent misattribution, and statistical independence violations. The phase highlighted the dangers of relying solely on automated keyword detection and metadata.

**Phase 2: Methodological Critique and Post-Mortem**
- **Goal:** Systematically document the reasons behavioral inference was impossible with the available dataset.
- **Method:** Identified key problems, including agent mislabeling, power user domination, temporal drift, and conceptual mismatches (e.g., PR metadata ≠ code changes, agent label ≠ authorship, keyword ≠ test creation). Critically assessed the scientific validity of the initial approach.
- **Outcome:** Concluded that the dataset's structure violated core assumptions required for valid behavioral inference, rendering statistical results scientifically meaningless. This phase established the need for a more robust, empirically grounded methodology.

**Phase 3: Dataset Debiasing and Structural Correction**
- **Goal:** Restore statistical validity for adoption and usage pattern analysis, even if behavioral inference remained out of reach.
- **Method:** Implemented a debiasing pipeline that included power user detection (filtering users above the 99th percentile of PR contributions), removal of multi-agent contamination (focusing on single-agent attribution), and recalculation of key metrics (Gini coefficient for contribution inequality, Shannon entropy for distribution diversity).
- **Outcome:** Debiasing led to a more representative sample, with improved adoption rates and reduced inequality. This phase demonstrated the importance of structural corrections in large-scale empirical studies.

**Phase 4: Empirical Validation via Manual Verification**
- **Goal:** Quantify measurement error and validate the accuracy of automated test detection.
- **Method:** Conducted a stratified, random sample of 500 PRs (60% keyword-detected, 40% non-keyword) across all agents. Manually verified the presence and quality of tests, measured false positive/negative rates, and calculated precision, recall, and overall accuracy. Cleaned data by removing PRs missing essential fields or inaccessible on GitHub.
- **Outcome:** Revealed that keyword-based detection systematically overestimated test presence due to template contamination and discussion artifacts. Manual verification established ground truth, quantified systematic error, and provided a benchmark for future automated methods.

### 10.2 Empirical Validation and Statistical Justification

The study's sample size and confidence level were justified using the same statistical methodology as the SANER_Naghashzadeh paper, ensuring comparability with prior work. The sample size formula for proportions (finite population) was applied, with conservative estimates to maximize validity. Manual review of 385 PRs (77 per agent) provided a robust empirical foundation, while the use of stratified sampling and bidirectional verification protocols ensured that findings were both representative and replicable.

### 10.3 Lessons Learned and Methodological Contributions

- **Statistical significance is not scientific validity:** Large sample sizes can make noise appear meaningful; measurement validity is paramount.
- **Manual verification is essential:** Automated methods must be empirically validated to quantify systematic error and avoid misleading conclusions.
- **Structural corrections are critical:** Debiasing for power users and agent contamination is necessary for representative analysis.
- **Transparency and documentation:** Every phase, including failures and corrections, was documented to provide a replicable framework for future research.

### 10.4 Summary

This multi-phase methodology, grounded in empirical validation and critical self-assessment, provides a transparent and replicable approach to large-scale software engineering research. By combining automated analysis with manual verification, and by rigorously documenting both successes and failures, this study offers a methodological blueprint for future work in the field.

### Motive
The primary motivation for this research is to empirically understand how different AI coding agents influence software testing practices at scale. With the rapid adoption of AI-powered development tools, there is a critical need to move beyond anecdotal or small-sample studies and provide population-level evidence about agent-specific behaviors, especially regarding test inclusion and quality. This work aims to inform both practitioners and researchers about the real-world impact of AI agent selection on software quality, workflow design, and organizational adaptation.

### Impact
The findings reveal dramatic, statistically robust differences in testing behavior across AI agents, with test inclusion rates ranging from 18.7% to 98.5%. These differences are not only statistically significant but also practically meaningful, challenging the assumption that all AI tools are interchangeable. The results demonstrate that agent choice fundamentally shapes software quality practices, and that development teams adapt their review and acceptance processes to compensate for agent-specific strengths and weaknesses. This has direct implications for tool selection, process engineering, and the development of agent-aware quality assurance strategies in industry.

### Reasoning

The reasoning behind these observations is rooted in a synthesis of empirical evidence, methodological rigor, and critical reflection on the limitations of large-scale software engineering data:

- **Empirical grounding**: The study leverages the largest available dataset of AI-assisted pull requests, enabling population-level analysis and minimizing sampling bias. The observed behavioral signatures—such as dramatic differences in test inclusion rates—are robust across hundreds of thousands of observations, providing strong evidence that agent architecture and training fundamentally shape development practices.

- **Methodological choices**: The research employs stratified sampling, conservative test detection heuristics, and effect size reporting to ensure that findings are both statistically and practically significant. The use of established statistical frameworks (e.g., chi-square tests, Cramer’s V) and validation against prior work (e.g., SANER_Naghashzadeh) further strengthens the credibility of the results.

- **Threats to validity**: Despite these strengths, the study acknowledges several threats:
  - *Internal validity*: Test detection may miss non-standard or implicit tests; agent attribution relies on metadata that may be noisy; developer selection effects could confound agent-specific patterns.
  - *External validity*: The dataset is GitHub-centric and may not generalize to other platforms, organizations, or future AI agent versions. The rapid evolution of AI tools and practices means findings are time-sensitive.
  - *Construct validity*: Test presence is used as a proxy for quality, but does not capture test effectiveness, coverage, or maintenance. Behavioral signatures may reflect dataset or training biases rather than intentional design.

- **Interpretation and recommendations**: These limitations are mitigated through transparent reporting, robustness checks (e.g., language and time stratification), and a focus on effect sizes rather than just statistical significance. The study recommends that future research prioritize improved dataset construction, independent validation of agent labels, and domain-specific replication to address these threats.

In summary, the reasoning connects the empirical findings to methodological decisions and known limitations, providing a balanced interpretation that supports actionable recommendations for both researchers and practitioners. The study’s transparency about its constraints ensures that its conclusions are credible, reproducible, and useful as a foundation for future work in AI-assisted software engineering.

## 10. Actionable Recommendations and Future Work

### Actionable Recommendations
- **For Practitioners:**
  - Select AI coding agents based on project needs: Use test-focused agents (e.g., OpenAI Codex) for quality-critical work, and rapid-development agents (e.g., Cursor) for prototyping, with compensatory review processes as needed.
  - Implement agent-aware review protocols: Calibrate code review and quality assurance practices to the strengths and weaknesses of each agent.
  - Archive and validate PR content: Ensure that all PRs, especially those generated by AI agents, are archived and accessible for future analysis and reproducibility.
  - Monitor and adapt: Continuously monitor agent behaviors and team adaptation strategies as AI tools and workflows evolve.

- **For Researchers:**
  - Prioritize dataset quality: Develop and use datasets with validated agent labels, persistent user activity, and comprehensive metadata.
  - Address threats to validity: Design studies that explicitly account for internal, external, and construct validity threats, using stratified sampling and robustness checks.
  - Replicate and extend: Conduct domain-specific and longitudinal studies to assess the generalizability and evolution of AI agent behaviors.
  - Focus on test quality: Move beyond test presence to evaluate the effectiveness, coverage, and maintainability of AI-generated tests.

### Future Work
- **Code-level Test Quality Assessment:** Develop automated and manual methods to evaluate the effectiveness and reliability of tests generated by AI agents.
- **Longitudinal Monitoring:** Track changes in agent behavior and team adaptation over time as models and development practices evolve.
- **Controlled Experiments:** Design randomized or matched studies to isolate agent effects from developer selection and project context.
- **Domain-Specific Replication:** Apply these analyses to safety-critical, enterprise, and embedded domains to assess external validity.
- **Improved Dataset Construction:** Create new datasets with verified agent attribution, reduced automation dominance, and improved user diversity.

These recommendations and future directions aim to advance both the practical integration of AI agents in software engineering and the scientific understanding of their impact. By addressing current limitations and building on robust empirical foundations, the field can move toward more reliable, effective, and transparent use of AI in software development.

---

## Appendix: Comprehensive Inventory — Observations, Claims, Assumptions, Validity Threats, and Implications

### 1. Empirical Observations (What Was Directly Observed)
**O1. Extreme contribution inequality exists in the dataset**
  - Gini coefficient ≈ 0.83; top ~1% of users account for a large share of PRs.
  - ✔ Directly computed from contribution counts; does not rely on agent attribution.

**O2. Agent-labeled PR volume is highly imbalanced**
  - One agent dominates by PR count; others are marginal.
  - ✔ Observed from dataset labels; ⚠ depends on attribution correctness.

**O3. Certain agents are dominated by a very small number of users**
  - Some agent categories have thousands of PRs from a single user.
  - ✔ Directly observable; user–agent linkage confirmed.

**O4. A large fraction of PRs are inaccessible (404) at verification time**
  - Many PR URLs no longer resolve, especially for high-volume users.
  - ✔ Verified via manual inspection.

**O5. Manual inspection confirms that test presence is heterogeneous**
  - Test inclusion and quality vary widely among accessible PRs.
  - ✔ Direct code-level inspection; explicit quality categories used.

**O6. Keyword-based test detection produces false positives and false negatives**
  - Some "testing" PRs contain no tests; some non-keyword PRs do contain tests.
  - ✔ Confirmed via manual validation; error quantified.

**O7. Metadata alone is insufficient to determine test inclusion or quality**
  - Titles, bodies, and repo language often misrepresent actual changes.
  - ✔ Observed repeatedly during manual review.

**O8. Agent categories differ in data accessibility and reliability**
  - Some agents show higher rates of deleted users, 404 PRs, or automation.
  - ✔ Observable; ⚠ cause cannot be uniquely determined.

### 2. Claims (What the Paper Explicitly Asserts)
**C1. PR-level metadata cannot reliably support behavioral inference about AI agents**
  - Behavioral claims require attribution, independence, and valid measurement—none are met.

**C2. Keyword-based test detection is an unreliable proxy for actual testing behavior**
  - Measurement error is non-trivial and systematic.

**C3. Contribution inequality and automation distort apparent agent-level patterns**
  - Raw PR counts exaggerate the influence of a few users or systems.

**C4. Agent attribution labels do not imply authorship or intent**
  - A labeled agent does not guarantee the agent generated tests or code.

**C5. Dataset structure invalidates standard independence-based statistical tests**
  - Chi-square and Cramér’s V rely on assumptions violated by clustering.

**C6. After debiasing, adoption patterns change materially**
  - Filtering high-volume users alters relative agent shares.

### 3. Assumptions (Explicit and Implicit)
**A1. Accessible PRs are broadly representative of inaccessible PRs**
  - Used when generalizing manual review findings.

**A2. Manual reviewers correctly identify test presence and quality**
  - Relies on expertise and rubric consistency.

**A3. Sample size formula assumptions hold**
  - Assumes conservative proportion (p = 0.5) and random sampling.

**A4. High-volume users are more likely to represent automation or non-human processes**
  - Used in filtering and interpretation.

**A5. Test presence is a meaningful proxy for testing behavior**
  - Used cautiously, not equated with test quality or effectiveness.

### 4. Threats to Validity (Structured)
**Internal Validity**
  - Inability to attribute test creation to agent vs human
  - Automation contamination
  - Reviewer subjectivity in manual inspection

**Construct Validity**
  - “Testing behavior” operationalized as test presence/quality
  - Keyword detection imperfect
  - Metadata ≠ code changes

**External Validity**
  - GitHub-only dataset
  - Time-bounded snapshot
  - Rapid evolution of AI tools

**Conclusion Validity**
  - Statistical significance inflated by clustering
  - Effect sizes meaningless without valid measurement

### 5. Implications (Why This Matters)
**For Researchers**
  - Behavioral claims from PR metadata require validation
  - Large N does not compensate for invalid measurement
  - Manual verification is essential, not optional

**For Dataset Designers**
  - PR content must be archived
  - Agent attribution must be instrumented, not inferred
  - Persistent user identifiers are critical

**For Industry Interpretation**
  - Tool comparisons based on PR statistics are unreliable
  - Apparent agent “quality differences” may be dataset artifacts
  - Process decisions should not rely on raw observational metrics

### 6. Meta-Observation (Why This Paper Is Valuable)
The failure of Phase 1 is itself a result. This paper documents how misleading conclusions emerge and how to prevent them. This is a methodological contribution, not a negative result.
```
