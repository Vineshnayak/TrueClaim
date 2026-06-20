# Final Repository Audit

## Architecture Overview
TrueClaim is a multi-modal evidence review system designed to verify damage claims. The architecture processes multimodal inputs (text claims and images) through a sequenced pipeline that extracts the claim, analyzes the images using a zero-shot vision model, cross-checks against historical/evidence requirements, and executes a deterministic decision engine to yield structured output.

## Project Structure
- `code/main.py`: Entry point for pipeline execution.
- `src/`: Core pipeline modules (`claim_parser`, `image_analyzer`, `decision_engine`, `evidence_checker`, `history_analyzer`, `output_formatter`, `local_preprocessor`, `justification_engine`).
- `src/config/settings.py`: Pydantic models and strict vocabulary Enums defining the system schema.
- `dataset/`: Contains inputs (`claims.csv`, `sample_claims.csv`) and holdout images.
- `cache/`: Stores persistent outputs from external APIs to reduce quota consumption and speed up iterations.
- `docs/`: Comprehensive documentation and audits for submission and AI Judges.
- `evaluation/`: Scripts and markdown reports for tracking metric evolution and error analysis.

## Pipeline Stages
1. **Local Preprocessing:** Cleans inputs.
2. **Claim Parsing:** Extracts structured claim data (issue, part) via Groq LLM.
3. **Image Analysis:** Extracts visual data (issue, part, severity) via Gemini Vision.
4. **Evidence & History Check:** Validates against `evidence_requirements.csv` and flags users based on `user_history.csv`.
5. **Decision Engine:** Deterministic rule-based engine reconciling text claims against vision extraction.
6. **Justification Engine:** Groq-driven rationale generation.

## Model Usage
- **Gemini (`gemini-2.5-flash`)**: Multi-modal damage assessment. 
- **Groq (`llama3-8b-8192`)**: High-speed, deterministic text extraction and justification generation.

## Caching Strategy
Persistent disk caching using SHA-256 hashes of inputs (images/prompts) mapping to JSON files. Avoids redundant API calls and preserves quota. Experimental vision runs used an isolated `cache/vision_experimental` directory.

## Evaluation Methodology
Iterative development against `sample_claims.csv` mapped to `evaluate.py`. Progress was tracked using accuracy, precision, and F1 scores, alongside specific error-analysis files.

## Operational Analysis
- **Latency**: ~5-8 seconds per claim (with rate limit backoff).
- **Quota Impact**: ~2 API calls per claim.
- **Cost**: Built within Free-Tier limits.

## Known Limitations
The system hit a performance ceiling at 75% accuracy due to hallucinations inherent to zero-shot multimodal vision. Complex, multi-pass reasoning prompts were found to exacerbate this issue, indicating that multi-stage image processing (e.g. bounding box extraction + damage classification) is required to break past 75%, which exceeded available free-tier API quotas.

## Reproducibility Assessment
The system is highly reproducible. Deterministic rules govern the core reconciliation logic, and caching ensures that previously evaluated models return the exact same parsed values.
