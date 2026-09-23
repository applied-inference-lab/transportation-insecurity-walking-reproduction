# Generic Reproducibility Requirements for Adversarial Evaluation

This checklist is designed for future agent work evaluating whether a replication or reproduction project is genuinely evidence-backed rather than merely narratively plausible.

## 1. Core Principle

A reproduction project is only credible if it can show, with artifacts and executable evidence, that:

1. the original target is identified and bounded;
2. the data source is auditable and traceable;
3. the benchmark/reference values are independently checked;
4. the analytic workflow is executable without hidden manual steps;
5. the outputs match the declared targets within pre-registered or documented tolerances;
6. the final status is recorded as a machine-readable pass/fail certificate.

## 2. Minimum Required Evidence

A project should provide all of the following.

### A. Data provenance
- source dataset identity and origin
- raw file(s) present or documented retrieval path
- relevant metadata: date, version, DOI, source URL where applicable
- file hashes or checksums for raw input files when possible

### B. Benchmark or reference validation
- explicit reference values or published tables identified
- a benchmark extraction or verification step
- programmatic comparison against the reference target
- pass/fail evidence for each benchmark cell or table
- an artifact showing mismatches, if any

### C. Reproduction artifacts
- output CSV/JSON/Parquet artifacts for all major calculations
- one file per major result type (rates, model fits, subgroup outputs, sensitivity checks)
- no reliance on hand-copied numbers in the narrative for proof

### D. Fail-fast checks
- scripts should halt when a required artifact is missing
- scripts should halt when a tolerance threshold is exceeded
- thresholds should be explicit, not implicit or informal

### E. Audit certificate
- a machine-readable summary with overall status and reason codes
- a human-readable summary for quick review
- a clear pass/fail verdict distinct from mere narrative confidence

## 3. Generic Reproduction Standards

### Phase 1: Soundness and provenance
A project should establish:
- what is being reproduced
- what the target claims are
- what the reference values are
- whether the benchmark values are independent and not manually transcribed without verification
- whether the project distinguishes between a paper claim and a reproducible artifact

Required evidence:
- source identification
- benchmark validation artifact
- exact reference target or paper section identified
- declared tolerances for discrepancies

### Phase 2: Robustness and proof quality
A project should verify not just that numbers are close, but that the closeness is meaningful and robust.

Required evidence:
- comparison tables with published vs reproduced values
- discrepancy distribution statistics (mean, max, exact matches, within-threshold counts)
- sensitivity analyses when design assumptions matter
- versioned or documented variance checks for complex survey or clustered designs
- dynamic documentation built from artifacts rather than static hand-maintained text

### Phase 3: Archive-grade reproducibility
For a static or downloadable snapshot, the project should provide a self-contained reproducibility package:
- documented run sequence
- environment lock or pinned version list
- raw input file(s) and output artifacts included
- hash manifest for critical files
- final audit certificate with PASS/FAIL

This is distinct from live CI enforcement. A living repo may require merge-blocking automation; a snapshot archive mainly requires deterministic, auditable, self-contained execution.

## 4. Red Flags for Adversarial Review

An agent should flag a reproduction as weak if it contains any of the following:

- narrative claim without traceable output artifact
- values copied into prose without a corresponding machine-readable file
- no benchmark verification step
- no fail-fast guard against missing data or threshold violations
- no audit certificate or summary
- only one-off scripts that cannot be rerun without manual intervention
- thresholds hidden in prose instead of being explicit in a standards file
- sensitivity checks omitted when the design is complex or clustered
- dynamic documentation not fed from generated artifacts

## 5. Generic Pass/Fail Rubric

Score each project on five dimensions.

### 1. Traceability
- raw inputs and references identified: pass/fail
- benchmark source and provenance documented: pass/fail

### 2. Independence of proof
- benchmark values checked rather than manually copied: pass/fail
- independent verification or reconciliation exists: pass/fail

### 3. Numerical reproduction quality
- reproduced outputs compared directly to published values: pass/fail
- discrepancy thresholds declared and met: pass/fail

### 4. Robustness
- variance/sensitivity checks included where needed: pass/fail
- failure modes are explicitly handled: pass/fail

### 5. Auditability
- final pass/fail certificate exists: pass/fail
- machine-readable evidence and human-readable summary present: pass/fail

## 6. Suggested Agent Workflow

When evaluating a new project, the agent should:

1. identify the target paper, claims, and tables;
2. verify the data source and provenance;
3. locate benchmark/reference checks;
4. inspect whether outputs are generated programmatically;
5. compute or inspect discrepancy metrics directly from artifacts;
6. verify fail-fast assertions and thresholds;
7. check whether documentation is dynamic or static;
8. confirm final audit certificate is produced and passes;
9. report whether the package is a living repo or a static snapshot, because the standard differs by type.

## 7. Minimum Acceptable Standard for a Snapshot Archive

A project should be considered acceptable if all of the following are true:
- the pipeline can be run from the repository snapshot;
- major outputs are saved as artifacts;
- benchmark/reference comparison uses explicit verification;
- discrepancies are measured and reported numerically;
- a pass/fail audit certificate is generated;
- the archive is self-contained and citeable without requiring an active development workflow.

## 8. Best Practice Summary

For future adversarial evaluation, prioritize evidence over narrative. The strongest reproduction projects are the ones that can answer, at a glance:

- What exactly is being reproduced?
- What was the evidence used to verify it?
- Where are the outputs and hashes?
- What are the thresholds?
- Did the run pass under those thresholds?
- Is this a living repo or a static archive?

This is the generic standard that turns a plausible reproduction story into a defensible, auditable, agent-evaluable artifact.
