# Pre-Run Cleanup Report

This document records the cleanup of temporary, partial, or stale artifacts before executing the experimental vision pipeline.

## Items Cleaned

| Path | Reason | Decision |
|---|---|---|
| `outputs/sample_output_experimental.csv` | Partial output generated from an interrupted run (process killed due to quota exhaustion). | **Removed**. |
| `cache/vision_experimental/*` | Stale cache entries from the interrupted run to ensure a fully isolated fresh execution using the new API key. | **Removed** (Directory cleared). |

## Items Preserved

- `outputs/sample_output_v4.csv` (Stable submission output)
- `cache/vision/*` (Stable vision caches)
- `cache/justification/*` (Stable justification caches)
- `evaluation/claim_status_final_report.md` (Stable evaluation report)
- `evaluation/baseline_metrics.md` (Stable baseline metrics)
- All files required for reproducibility, compliance audit, and AI judge evaluation.
