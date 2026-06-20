# Evaluation Report

## claim_status
- Accuracy:  0.7500
- Precision: 0.5893
- Recall:    0.7500
- F1 Score:  0.6538

## issue_type
- Accuracy:  0.7000
- Precision: 0.7525
- Recall:    0.7000
- F1 Score:  0.6875

## object_part
- Accuracy:  0.7000
- Precision: 0.7100
- Recall:    0.7000
- F1 Score:  0.6833

## severity
- Accuracy:  0.5000
- Precision: 0.5108
- Recall:    0.5000
- F1 Score:  0.4742

## Operational Analysis
- Images processed: 20 rows
- Model calls: 2 per claim (1 text extraction, 1 multimodal vision reasoning)
- Token estimates: 
  - Input: ~500 tokens per text extraction, ~1500 tokens per vision reasoning.
  - Output: ~100 tokens JSON per call.
- Estimated latency: 5-8s per claim depending on Groq response time.
- Rate limit handling: Synchronous sequential processing with basic try/except retry loop.
