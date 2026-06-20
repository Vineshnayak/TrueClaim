import pandas as pd
import os

def generate_error_analysis():
    pred_file = "outputs/sample_output.csv"
    true_file = "dataset/sample_claims.csv"
    
    if not os.path.exists(pred_file) or not os.path.exists(true_file):
        print("Missing files")
        return
        
    df_pred = pd.read_csv(pred_file)
    df_true = pd.read_csv(true_file)
    
    # Merge on user_id
    df = pd.merge(df_pred, df_true, on='user_id', suffixes=('_pred', '_true'))
    
    report = ["# Error Analysis\n"]
    
    categories = ['claim_status', 'issue_type', 'object_part', 'severity']
    
    error_counts = {c: 0 for c in categories}
    
    for _, row in df.iterrows():
        user_id = row['user_id']
        errors = []
        for cat in categories:
            pred_val = str(row[cat + '_pred']).lower().strip()
            true_val = str(row[cat + '_true']).lower().strip()
            if pred_val != true_val:
                errors.append({
                    'category': cat,
                    'pred': pred_val,
                    'true': true_val
                })
                error_counts[cat] += 1
                
        if errors:
            report.append(f"## Claim ID: {user_id}")
            for err in errors:
                report.append(f"- **{err['category']}**: True='{err['true']}' | Pred='{err['pred']}'")
            report.append("")
            
    report.insert(1, "## Summary Statistics")
    for cat in categories:
        report.insert(2, f"- **{cat} errors**: {error_counts[cat]}/{len(df)}")
    report.insert(2 + len(categories), "")
    
    out_path = "code/evaluation/error_analysis.md"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(report))
        
    print(f"Error analysis written to {out_path}")

if __name__ == "__main__":
    generate_error_analysis()
