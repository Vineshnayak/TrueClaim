# Code.zip Manifest

The following items must be strictly EXCLUDED from the final `code.zip` packaging:

## Exclusions
- `.env`: Contains sensitive API keys.
- `cache/`: Contains massive JSON outputs, images, and text blobs not meant for evaluation environments.
- `venv/`: Contains python library binaries (can be hundreds of megabytes).
- `dataset/`: Only the output logic is submitted, not the core test sets.
- `node_modules/`: (N/A but excluded by default)
- Any temporary or experimental output CSV files (e.g., `sample_output_experimental.csv`).
- Any debug scripts.
- `.DS_Store` or other OS-specific metadata files.

## Inclusions
- `code/`: Execution scripts (`main.py`).
- `src/`: Pipeline implementation code.
- `docs/`: Audits, summaries, and manifests.
- `evaluation/`: Scripts and metrics.
- `requirements.txt`: Environment dependencies.
- `README.md`: Execution instructions.
- `AGENTS.md`: Agent contract file.
