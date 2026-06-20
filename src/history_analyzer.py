import pandas as pd
from src.config.settings import RiskFlag

class HistoryAnalyzer:
    def __init__(self, user_history_df: pd.DataFrame):
        self.history_df = user_history_df.set_index("user_id")
        
    def get_user_risk_context(self, user_id: str) -> dict:
        if user_id not in self.history_df.index:
            return {"risk_flags": [], "summary": "New user with no prior claim history."}
        
        row = self.history_df.loc[user_id]
        flags_str = str(row.get("history_flags", "none"))
        flags = []
        if flags_str and flags_str.lower() != "none" and flags_str.lower() != "nan":
            flags = [f.strip() for f in flags_str.split(";")]
            
        summary = str(row.get("history_summary", ""))
        
        valid_flags = []
        for f in flags:
            try:
                valid_flags.append(RiskFlag(f))
            except ValueError:
                pass
                
        return {
            "risk_flags": valid_flags,
            "summary": summary
        }
