import pandas as pd
import os

def generate_claim_status_analysis():
    pred_file = "outputs/sample_output_v3.csv"
    true_file = "dataset/sample_claims.csv"
    
    if not os.path.exists(pred_file) or not os.path.exists(true_file):
        print("Missing files")
        return
        
    df_pred = pd.read_csv(pred_file)
    df_true = pd.read_csv(true_file)
    
    df = pd.merge(df_pred, df_true, on='user_id', suffixes=('_pred', '_true'))
    
    report = ["# Claim Status Error Analysis\n"]
    
    errors = []
    
    for _, row in df.iterrows():
        user_id = row['user_id']
        pred_status = str(row['claim_status_pred']).lower().strip()
        true_status = str(row['claim_status_true']).lower().strip()
        
        if pred_status != true_status:
            # Categorize
            category = f"{pred_status} predicted instead of {true_status}"
            
            errors.append({
                'user_id': user_id,
                'category': category,
                'true': true_status,
                'pred': pred_status,
                'issue_pred': row['issue_type_pred'],
                'issue_true': row['issue_type_true'],
                'part_pred': row['object_part_pred'],
                'part_true': row['object_part_true'],
                'flags': row['risk_flags_pred'],
                'evidence_met_pred': row['evidence_standard_met_pred'],
                'evidence_met_true': row['evidence_standard_met_true'],
                'user_claim': row['user_claim_true']
            })
            
    report.append(f"Total Errors: {len(errors)}/20\n")
    
    for err in errors:
        report.append(f"## Claim ID: {err['user_id']} ({err['category']})")
        report.append(f"- **True Status**: {err['true']}")
        report.append(f"- **Pred Status**: {err['pred']}")
        report.append(f"- **Evidence Met (True/Pred)**: {err['evidence_met_true']} / {err['evidence_met_pred']}")
        report.append(f"- **Flags Triggered**: {err['flags']}")
        report.append(f"- **Issue (True/Pred)**: {err['issue_true']} / {err['issue_pred']}")
        report.append(f"- **Part (True/Pred)**: {err['part_true']} / {err['part_pred']}")
        report.append(f"- **User Claim**: {err['user_claim']}\n")
        
    out_path = "evaluation/claim_status_error_analysis.md"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(report))
        
    print(f"Claim status analysis written to {out_path}")

if __name__ == "__main__":
    generate_claim_status_analysis()
