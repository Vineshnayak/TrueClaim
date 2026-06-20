import pandas as pd
import os
from sklearn.metrics import accuracy_score

def compare_models():
    true_file = "dataset/sample_claims.csv"
    stable_file = "outputs/sample_output_v4.csv"
    exp_file = "outputs/sample_output_experimental.csv"
    
    if not os.path.exists(true_file) or not os.path.exists(stable_file):
        print("Missing base files. Run the stable pipeline first.")
        return
        
    if not os.path.exists(exp_file):
        print(f"Missing experimental output {exp_file}. Please run the experimental pipeline first.")
        return
        
    df_true = pd.read_csv(true_file)
    df_stable = pd.read_csv(stable_file)
    df_exp = pd.read_csv(exp_file)
    
    # Merge
    df_s = pd.merge(df_true, df_stable, on="user_id", suffixes=('_true', '_pred'))
    df_e = pd.merge(df_true, df_exp, on="user_id", suffixes=('_true', '_pred'))
    
    metrics = ["claim_status", "issue_type", "object_part", "severity"]
    
    report = ["# Stable vs Experimental Pipeline Comparison\n"]
    
    stable_accs = {}
    exp_accs = {}
    
    for m in metrics:
        s_true = df_s[f"{m}_true"].astype(str).str.lower().str.strip()
        s_pred = df_s[f"{m}_pred"].astype(str).str.lower().str.strip()
        stable_accs[m] = accuracy_score(s_true, s_pred)
        
        e_true = df_e[f"{m}_true"].astype(str).str.lower().str.strip()
        e_pred = df_e[f"{m}_pred"].astype(str).str.lower().str.strip()
        exp_accs[m] = accuracy_score(e_true, e_pred)
        
    report.append("| Metric | Stable Pipeline | Experimental Pipeline | Delta |")
    report.append("|--------|-----------------|-----------------------|-------|")
    
    for m in metrics:
        s_val = stable_accs[m]
        e_val = exp_accs[m]
        delta = e_val - s_val
        delta_str = f"+{delta*100:.1f}%" if delta > 0 else f"{delta*100:.1f}%"
        report.append(f"| **{m}** | {s_val*100:.1f}% | {e_val*100:.1f}% | {delta_str} |")
        
    report.append("\n## Final Recommendation")
    
    if exp_accs['claim_status'] > stable_accs['claim_status'] and \
       exp_accs['issue_type'] > stable_accs['issue_type'] and \
       exp_accs['object_part'] >= stable_accs['object_part'] and \
       exp_accs['severity'] >= stable_accs['severity']:
        report.append("**Result:** **Replace with experimental version.** The experimental pipeline improved both claim_status and issue_type without regressing object_part or severity.")
    else:
        report.append("**Result:** **Keep current submission candidate.** The experimental pipeline failed to strictly improve the target metrics without regression.")
        
    out_path = "evaluation/model_comparison.md"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(report))
        
    print(f"Comparison report written to {out_path}")

if __name__ == "__main__":
    compare_models()
