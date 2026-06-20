import pandas as pd
from typing import List
from src.config.settings import ClaimOutputRow

class OutputFormatter:
    def write_output(self, rows: List[ClaimOutputRow], filepath: str):
        data = [r.model_dump() for r in rows]
        df = pd.DataFrame(data)
        columns = [
            "user_id", "image_paths", "user_claim", "claim_object", 
            "evidence_standard_met", "evidence_standard_met_reason",
            "risk_flags", "issue_type", "object_part", "claim_status",
            "claim_status_justification", "supporting_image_ids",
            "valid_image", "severity"
        ]
        df = df[columns]
        df.to_csv(filepath, index=False)
