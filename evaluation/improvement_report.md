# Evaluation Report

## claim_status
- Accuracy:  0.6000
- Precision: 0.5409
- Recall:    0.6000
- F1 Score:  0.5446

## issue_type
- Accuracy:  0.5500
- Precision: 0.5062
- Recall:    0.5500
- F1 Score:  0.5032

## object_part
- Accuracy:  0.5500
- Precision: 0.5563
- Recall:    0.5500
- F1 Score:  0.5278

## severity
- Accuracy:  0.4000
- Precision: 0.4329
- Recall:    0.4000
- F1 Score:  0.3573

## Operational Analysis
- Images processed: 20 rows
- Model calls: 2 per claim (1 text extraction, 1 multimodal vision reasoning)
- Token estimates: 
  - Input: ~500 tokens per text extraction, ~1500 tokens per vision reasoning.
  - Output: ~100 tokens JSON per call.
- Estimated latency: 5-8s per claim depending on Groq response time.
- Rate limit handling: Synchronous sequential processing with basic try/except retry loop.

## Optimization Metrics
- **Number of new Gemini calls**: 0
- **Number of cached Gemini hits**: 20
- **Number of Groq calls**: 20 (Cached) / 5 (New calls due to claim_status overrides)
