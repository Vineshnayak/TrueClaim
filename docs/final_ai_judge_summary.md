# AI Judge Package Summary

## Project Overview
TrueClaim resolves multi-modal evidence review using a sequential LLM+VLM pipeline integrated with a deterministic rule engine.

## Architecture
- **Claim Extraction:** Groq `llama3-8b-8192` parses the raw conversation log to identify the structured `issue` and `part`.
- **Image Analysis:** Google `gemini-2.5-flash` analyzes the visual evidence to determine `issue`, `part`, `severity`, and visual quality flags.
- **Evidence Validation:** Validates required angles and formats based on `evidence_requirements.csv`.
- **Risk Assessment:** Flags high-risk users based on `user_history.csv` metrics.
- **Decision Engine:** Deterministically reconciles discrepancies between the text claim and the visual evidence, enforcing strict precedence logic to avoid hallucination-based contradictions.

## Model Choices
- **Groq:** Chosen for pure speed, zero-cost text parsing, and latency reduction in the justification engine.
- **Gemini:** Chosen for robust multimodal context capacity.
- **Caching Decisions:** Disk-based SHA-256 caching was extensively used to preserve limited API quotas and rapidly iterate on downstream rules.

## Evaluation Progression

### Initial Baseline
- **claim_status:** 60%
- **issue_type:** 45%
- **object_part:** 20%
- **severity:** 5%

### Improved Stable Pipeline (Selected)
Achieved through deterministic part-normalization, physics-bounded severity calibration, and confidence-aware resolution prioritizing "Not Enough Information" over outright "Contradiction".
- **claim_status:** 75%
- **issue_type:** 70%
- **object_part:** 70%
- **severity:** 50%

### Experimental Vision Pipeline
Attempted complex Chain-of-Thought reasoning entirely within the vision prompt.
- **claim_status:** 65%
- **issue_type:** 65%
- **object_part:** 70%
- **severity:** 35%

**Selection Rationale:** The stable pipeline offloads complex logical conflict resolution to predictable Python code, whereas the experimental pipeline overloaded the VLM, causing it to regress. Therefore, the stable pipeline remains the highest-quality candidate.
