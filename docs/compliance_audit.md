# Compliance Audit: TrueClaim

| Requirement | Implemented | Evidence | File Location | Pass/Fail |
|---|---|---|---|---|
| 1. Extract damage claim from conversation | Yes | `ClaimParser` uses Groq LLM (Llama 3.3 70B) to extract structured text. | `src/claim_parser.py` | Pass |
| 2. Inspect submitted images | Yes | `ImageAnalyzer` sends all images to Gemini 2.5 Flash in a single prompt. | `src/image_analyzer.py` | Pass |
| 3. Decide if evidence is sufficient | Yes | Deterministic logic in `decision_engine` merges outputs and checks validity flags. | `src/decision_engine.py` | Pass |
| 4. Identify visible issue type | Yes | Gemini correctly identifies `IssueType` explicitly from image payload. | `src/image_analyzer.py` | Pass |
| 5. Identify relevant object part | Yes | Gemini successfully segments the part mapping to expected enum strings. | `src/image_analyzer.py` | Pass |
| 6. Determine claim status | Yes | Rules derive `supported`, `contradicted`, or `not_enough_information` | `src/decision_engine.py` | Pass |
| 7. Select supporting image IDs | Yes | Gemini selects specific valid IDs supporting the claim from the input batch. | `src/image_analyzer.py` | Pass |
| 8. Detect image quality problems | Yes | Handled locally via OpenCV (blur, brightness) & Gemini (obstructions, angles). | `src/local_preprocessor.py` | Pass |
| 9. Detect object mismatches | Yes | Gemini identifies wrong objects vs claimed expectation. | `src/image_analyzer.py` | Pass |
| 10. Detect risk factors | Yes | Merged historical flags (e.g. `user_history_risk`) overlaid into flags list. | `src/history_analyzer.py` | Pass |
| 11. Estimate severity | Yes | Vision model maps severity scales (none, low, medium, high). | `src/image_analyzer.py` | Pass |
| 12. Produce concise image-grounded justification | Yes | Groq-powered `JustificationEngine` synthesizes vision explanations into concise text. | `src/justification_engine.py` | Pass |
| 13. Output exactly 14 columns | Yes | Validated exact schema matching target layout. | `src/output_formatter.py` | Pass |
| 14. Efficient Model APIs | Yes | Heavily cached, local filtering, one batched call per claim. No OpenAI usage. | `code/main.py` | Pass |
| 15. Provide evaluation framework | Yes | Scikit-learn outputs Accuracy/Precision/Recall/F1 dynamically. | `code/evaluate.py` | Pass |

**Audit Status: COMPLIANT AND SUBMISSION READY.**
