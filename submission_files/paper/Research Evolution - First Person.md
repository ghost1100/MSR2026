# My Research Journey: From Failed Behavioral Analysis to Valid Methodological Contribution

## 🔵 Phase 1 — Initial Behavioural Comparison Using Cramér's V

**My Goal:** I wanted to determine whether different AI agents (Copilot, Codex, Devin, Cursor, Claude) exhibited different testing behaviours.

### What I Did:

I took a 50k stratified sample from the MSR 2026 dataset to make analysis computationally feasible while maintaining representativeness.

I identified "test-related PRs" using comprehensive keyword detection across multiple frameworks:
- Core terms: test, spec, unittest, pytest, jest, karma, mocha, cypress
- Framework-specific: junit, testng, rspec, phpunit, nunit, xunit
- Context terms: testing, validation, verification

I built rigorous contingency tables of Agent × Testing Presence.

I applied multiple statistical methods:
- Chi-square tests for independence
- Cramér's V (effect size measurement) 
- 95% confidence intervals using Wilson score intervals
- Bootstrap validation of results
- Effect size interpretation using Cohen's guidelines

### What It Initially Appeared to Show:

**Stunning results that seemed too good to be true:**
- Codex dominated "test-related PRs" at 98.5% (43,997/44,668 PRs)
- Copilot showed 80.0% testing rate (2,200/2,751 PRs)  
- Cursor and Devin showed much lower rates (18% and similar)
- Cramér's V = 0.65 suggested "large, practically meaningful differences" between agents
- Statistical significance was overwhelming (p < 0.001, n = 50,000)
- Effect sizes suggested this was not just statistical noise but genuine behavioral differences

I was initially thrilled—this looked like a major empirical finding about AI tool capabilities.

### The Catastrophic Collapse:

**My supervisor's question:**
*"How do you know these are real tests? Did you verify the actual files?"*

**The brutal realization cascade:**

1. **No Code Verification Possible:** The MSR dataset contains only PR metadata (titles, descriptions, timestamps)—no file diffs, no actual code changes, no way to verify that "test-related" PRs actually contain tests.

2. **Attribution Impossibility:** PR content inevitably mixes human and AI contributions. Even if labeled as "Codex-generated," I cannot separate what the AI wrote from subsequent human editing, repository policies, or collaborative development.

3. **Systematic Keyword Pollution:** My keyword detection was capturing:
   - Mandatory PR templates requiring "test" in all descriptions
   - Discussions about existing test failures (not new test creation)
   - References to deployment testing, configuration testing, load testing
   - Repository-specific automation mentioning testing frameworks
   - Documentation updates about testing procedures

4. **Statistical Independence Violations:** Any statistical test was invalid because PRs cluster by user, repository, and project—violating the independence assumptions required for χ² and Cramér's V.

**The crushing personal realization:** I had spent weeks producing mathematically rigorous analysis of fundamentally meaningless data. My "significant differences" reflected dataset artifacts and measurement failures, not AI capabilities.

### Outcome:

Phase 1 failed completely. The behavioral differences suggested by Cramér's V were not defensible research claims—they depended on unverified assumptions and invalid measurement techniques. Rather than producing a behavioral comparison, I had created an elaborate statistical analysis of noise.

This methodological collapse forced me into Phase 2, where failure became the foundation for genuine contribution.

---

## 🔵 Phase 2 — Methodological Critique and Post-Mortem Analysis

**My New Goal:** Rather than hiding the failure, I decided to systematically document why behavioral inference was impossible. This became my methodological paper.

### Problems I Systematically Identified:

#### 1. Attribution Failures
- **Copilot Impossibility:** Dataset showed only 379 Copilot users—clearly impossible given millions of actual users
- **Power User Domination:** Devin category dominated by a single user with ~30,000 PRs
- **Inconsistent Labeling:** Agents mislabeled, inconsistently detected across repositories
- **Temporal Drift:** Attribution methods changed over time within the same dataset

#### 2. Structural Clustering Violations
I discovered that PRs cluster by:
- **Developer identity** (same users contribute repeatedly)
- **Repository policies** (template-driven content)  
- **Project phases** (testing surges during release cycles)
- **Organizational practices** (company-specific workflows)

This completely violates independence assumptions required for χ² tests and Cramér's V calculations.

#### 3. Keyword-Based Detection Systematic Failures
- **Context Ambiguity:** Same keywords mean different things in different contexts
- **False Positives:** Template requirements, discussion references, configuration mentions
- **False Negatives:** Implicit testing, framework-specific terminology, non-English keywords
- **Framework Bias:** Different testing conventions across languages and ecosystems
- **Template Contamination:** Repository policies artificially inflating keyword frequencies

#### 4. Fundamental Conceptual Mismatches
- **PR metadata ≠ testing behavior:** Descriptions don't reflect actual code changes
- **Agent label ≠ agent authorship:** Labels indicate session tools, not content creators
- **Keyword presence ≠ test creation:** Mentions don't equal implementation
- **Statistical significance ≠ practical validity:** Large n can make noise significant

### Key Insight Gained:

The MSR dataset is fundamentally unsuitable for behavioral inference because its structure violates every assumption needed for attribution, measurement, and statistical inference. This wasn't a fixable analysis problem—it was an unfixable dataset limitation.

### The Academic Value Discovery:

Rather than hide this methodological failure, I realized it had genuine academic value:
- A systematic "post-mortem" documenting why the approach fails
- A warning to the software engineering research community
- A validity framework for future researchers attempting similar analyses
- Demonstration of scientific integrity by prioritizing validity over exciting claims

This methodological honesty became the foundation for legitimate research contribution and set up Phase 3.

---

## 🔵 Phase 3 — Dataset Debiasing: Gini Coefficient and Shannon Entropy Analysis

**My Final Goal:** If the dataset cannot answer behavioral questions, could I at least make it statistically valid for adoption and usage pattern analysis?

This became my constructive contribution—moving from critique to solution.

### Stage 1 — Systematic Bias Detection and Removal

I developed a three-stage debiasing pipeline:

**Power User Detection:**
- Identified users with >178 PRs (99th percentile threshold)
- Discovered extreme concentration: single user contributed 200k+ PRs (21.4% of entire dataset)
- Created volume-based filtering to remove statistical outliers

**Bot and Automation Detection:**
- Pattern analysis for non-human contribution signatures
- Bulk operation detection (identical timestamps, templated content)
- Script-driven account identification
- Combined multiple heuristics to identify 44.2% automation contamination

**Multi-Agent Contamination Removal:**
- Focused on Copilot as meta-tool (often used alongside other agents)
- Removed cases where multiple agents appeared in same development sessions
- Created clean, single-agent attribution subsets

### Stage 2 — Inequality Quantification with Gini Coefficient

I applied the Gini coefficient (borrowed from economics) to measure contribution inequality:

**Shocking Results:**
- **Raw dataset Gini = 0.829** (extreme inequality, approaching maximum of 1.0)
- **Top 1% of users produced 43.6% of all PRs**
- **Top 10% of users produced 79.7% of all PRs**  
- **Bottom 50% of users produced only 5.1% of PRs**

**Mathematical Proof:** This quantitatively demonstrated what Phase 2 had identified qualitatively—the dataset does not represent typical developer behavior and any "agent comparisons" reflect the idiosyncratic practices of a tiny number of power users.

### Stage 3 — Distribution Analysis with Shannon Entropy

I measured information content and diversity using Shannon entropy:

**Agent Distribution Entropy:**
- Low entropy in raw data → high concentration in few agents (Codex dominance)
- Entropy increased after Copilot removal → more balanced, informative distribution
- Quantified the "information loss" from power user concentration

**User Participation Entropy:**
- Extremely low entropy → activity concentrated in few users
- After filtering: substantial entropy improvement → more representative participation patterns

**Repository Activity Entropy:**
- Repository-level analysis showed similar concentration effects
- Post-debiasing: more even distribution across project types

### The Constructive Outcome:

**Before Debiasing:**
- Copilot: 5.4% apparent adoption
- Extreme user inequality (Gini = 0.829)
- 44.2% automation contamination
- Statistically invalid for any inference

**After Debiasing:**
- Copilot: 9.6% actual adoption (78% increase when properly measured)
- Reduced inequality (Gini < 0.6)
- Clean, representative user sample
- Statistically valid for adoption analysis (though still not behavioral inference)

---

## 🎯 The Complete Research Arc: From Failure to Contribution

### What I Actually Accomplished:

**Phase 1:** I attempted legitimate empirical methodology (Cramér's V on behavioral categories) but discovered my inferences were unverifiable due to dataset limitations.

**Phase 2:** I pivoted to methodological critique, systematically documenting why inference was impossible and grounding everything in validity theory.

**Phase 3:** I developed a constructive solution—a debiasing and representation correction framework using Gini coefficient and Shannon entropy to restore structural validity.

### The Final Research Portfolio:

1. **Methodological Paper (MSR2026_COMPLETE.tex):** "Why Testing Behavior Cannot Be Inferred from AI-Generated Pull Requests" - A systematic post-mortem and validity framework

2. **Debiasing Paper:** Dataset correction methodology using inequality metrics and information theory

3. **Comprehensive Study:** Complete documentation of the research journey and lessons learned

### Why This Matters:

- **Complete research narrative** showing intellectual honesty and methodological rigor
- **Genuine methodological contribution** that advances empirical software engineering  
- **Replicable framework** for other researchers facing similar dataset validity challenges
- **Academic integrity demonstration** by prioritizing validity over exciting but unsupported claims

### Personal Research Growth:

I learned that **failed analysis can become successful methodology research** when approached with scientific integrity. The willingness to document and systematize failure transformed a collapsed behavioral study into a valuable contribution to research methods in software engineering.

This journey demonstrates that methodological rigor and honest self-reflection can turn research setbacks into genuine academic contributions—exactly the kind of mature research approach expected at the graduate level.

**this is a short polished summery of how i reached the results I had and why my research objectives kept changing**
