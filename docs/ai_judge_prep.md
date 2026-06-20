# TrueClaim: AI Judge Preparation

## Architecture
TrueClaim is structured as a deterministic, modular 10-stage pipeline that strictly isolates multimodal vision tasks from language reasoning tasks. 
- **Stage 1 (Load):** Ingests claims, user histories, and evidence standards using pandas.
- **Stage 2 (Local Preprocessing):** Uses OpenCV to perform computationally cheap checks (blur detection via Laplacian variance, brightness/glare detection via pixel thresholds).
- **Stage 3 (Vision Analysis):** Uses Gemini 2.5 Flash to process all submitted images for a claim in a single batch request, ensuring contextual understanding.
- **Stage 4 (Claim Extraction):** Uses Groq (Llama 3.3 70B) to parse conversational transcripts into structured JSON payloads (extracted issue, object part, severity hints).
- **Stage 5 (Evidence Validation):** A deterministic Python layer that matches extracted findings against `evidence_requirements.csv`.
- **Stages 6-8 (Risk & Decision Engines):** Combines image flags, local preprocessing flags, and user history into a final `supported`, `contradicted`, or `not_enough_information` state.
- **Stages 9-10 (Justification & Output):** Uses Groq to synthesize a concise, image-grounded explanation and validates the final schema before writing `output.csv`.

## Model Choices & Tradeoffs
- **Gemini 2.5 Flash for Vision:** Chosen over OpenAI and Groq (which recently decommissioned their vision models) due to its exceptional cost-efficiency, speed, and strong multimodal capabilities. Sending a single batch of images per claim to Gemini significantly reduces prompt overhead compared to per-image calls.
- **Groq (Llama 3.3 70B) for Text Reasoning:** Chosen for its lightning-fast inference speed and reliable structured JSON output. Groq is restricted to text-only tasks where it excels, avoiding the high cost and latency of using multimodal models for pure text extraction.

## Cost Strategy
1. **Local Preprocessing:** Rejecting corrupted or extremely blurry images via OpenCV before hitting any API saves direct LLM costs.
2. **Caching:** A cryptographic SHA-256 hash of the image bytes and prompts is used to cache Gemini outputs in `cache/vision` and Groq outputs in `cache/claims`. Identical inputs are never processed twice.
3. **Batching:** We perform exactly 1 Gemini request per claim (encompassing all images for that claim), drastically reducing the token overhead of repeated system instructions.
4. **Model Tiering:** We use the `flash` variant of Gemini and the open-source Llama model on Groq, avoiding premium models like `gpt-4o` or `gemini-1.5-pro` entirely.

## Evaluation Methodology
- **Scikit-learn Framework:** The pipeline is continuously evaluated against a hold-out `sample_claims.csv` dataset.
- **Metrics Calculated:** Accuracy, Precision, Recall, and F1-score are tracked for `claim_status`, `issue_type`, `object_part`, and `severity`.
- **Iterative Improvement:** The structured JSON schemas for both Gemini and Groq were iteratively tightened to ensure their outputs strictly aligned with the allowed domain strings.

## Risk Handling & Evidence Validation Logic
- **No Hallucinations:** The system aggressively flags `damage_not_visible` if the model cannot confidently identify the issue. 
- **Conflict Resolution:** If the text transcript claims "hood scratch" but the image shows "front bumper dent", the system flags `claim_mismatch` and outputs `contradicted`.
- **User History Overlays:** `user_history.csv` is checked. If a user has a history of rejected claims or severity exaggeration, `user_history_risk` is appended. However, history never overrides clear physical evidence (a valid photo of a broken hinge will be `supported` regardless of user history).

## Future Improvements
- **Parallel Processing:** Introduce `asyncio` to run the Groq claim extraction and Gemini vision analysis concurrently for each claim.
- **Advanced Local Filtering:** Implement perceptual hashing (pHash) to detect exact duplicate images across different claims, preventing fraud.
- **Fallback Models:** Add a retry mechanism that falls back to Gemini 1.5 Pro if Flash's confidence score drops below a specific threshold.
