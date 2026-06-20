# Experimental Vision Pipeline Report

## Configuration
- **Prompt Version**: `experimental_v1`
- **Changes Made**:
  - Implemented single-call multi-pass reasoning (Chain of Thought instructions in prompt).
  - Defined explicit object-part vocabularies matching `settings.py` for strictly bounded output.
  - Implemented severity bounds mapped to physical characteristics directly in the LLM prompt.
  - Explicitly instructed the model on `wrong_object`, `claim_mismatch`, and `damage_not_visible` rules.
  - Switched cache directory to `cache/vision_experimental` to isolate from stable pipeline.

## Execution Metrics
- **Gemini Calls Used**: 20 requests
- **Cache Hits**: 0 (Full fresh run on the experimental prompt)
- **Runtime**: ~4.5 minutes (Includes one 503 retry block)
- **Failures**: 1 (Row 17 encountered a 503 UNAVAILABLE that did not recover after 4 retries)
- **Cost Impact**: Free Tier (Consumed 20 requests of daily quota)

## Commands to Run
To run the experiment once API quota is available:
```bash
source venv/bin/activate && PYTHONPATH=. python code/main.py --input sample_claims.csv --output outputs/sample_output_experimental.csv
```

To compare against the stable baseline:
```bash
PYTHONPATH=. python code/evaluation/compare_models.py
```
