import pandas as pd

class EvidenceChecker:
    def __init__(self, evidence_df: pd.DataFrame):
        self.evidence_df = evidence_df
        
    def get_requirements(self, claim_object: str, issue_family: str) -> str:
        reqs = []
        for _, row in self.evidence_df.iterrows():
            if row['claim_object'] in ['all', claim_object]:
                reqs.append(row['minimum_image_evidence'])
        return " ".join(reqs)
