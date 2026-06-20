# Evaluation Report

## claim_status
- Accuracy:  0.6000
- Precision: 0.5409
- Recall:    0.6000
- F1 Score:  0.5446

## issue_type
- Accuracy:  0.4500
- Precision: 0.4150
- Recall:    0.4500
- F1 Score:  0.4173

## object_part
- Accuracy:  0.2000
- Precision: 0.2500
- Recall:    0.2000
- F1 Score:  0.2167

## severity
- Accuracy:  0.0500
- Precision: 0.0038
- Recall:    0.0500
- F1 Score:  0.0071

## Operational Analysis
- Images processed: 20 rows
- Model calls: 2 per claim (1 text extraction, 1 multimodal vision reasoning)
- Token estimates: 
  - Input: ~500 tokens per text extraction, ~1500 tokens per vision reasoning.
  - Output: ~100 tokens JSON per call.
- Estimated latency: 5-8s per claim depending on Groq response time.
- Rate limit handling: Synchronous sequential processing with basic try/except retry loop.
