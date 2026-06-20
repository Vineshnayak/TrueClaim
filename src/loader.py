import pandas as pd

class DataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        
    def load_claims(self, file_name: str = "claims.csv") -> pd.DataFrame:
        return pd.read_csv(f"{self.data_dir}/{file_name}")

    def load_user_history(self) -> pd.DataFrame:
        return pd.read_csv(f"{self.data_dir}/user_history.csv")
        
    def load_evidence_requirements(self) -> pd.DataFrame:
        return pd.read_csv(f"{self.data_dir}/evidence_requirements.csv")
