import os
import argparse
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def evaluate(pred_file: str, true_file: str, report_file: str):
    if not os.path.exists(pred_file):
        print(f"Predictions file not found: {pred_file}")
        return
        
    pred_df = pd.read_csv(pred_file)
    true_df = pd.read_csv(true_file)
    
    merged = pd.merge(true_df, pred_df, on="user_id", suffixes=('_true', '_pred'))
    
    metrics_to_eval = ['claim_status', 'issue_type', 'object_part', 'severity']
    
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, 'w') as f:
        f.write("# Evaluation Report\n\n")
        
        for metric in metrics_to_eval:
            y_true = merged[f"{metric}_true"].astype(str).str.lower()
            y_pred = merged[f"{metric}_pred"].astype(str).str.lower()
            
            acc = accuracy_score(y_true, y_pred)
            p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
            
            f.write(f"## {metric}\n")
            f.write(f"- Accuracy:  {acc:.4f}\n")
            f.write(f"- Precision: {p:.4f}\n")
            f.write(f"- Recall:    {r:.4f}\n")
            f.write(f"- F1 Score:  {f1:.4f}\n\n")
            
        f.write("## Operational Analysis\n")
        f.write(f"- Images processed: {len(pred_df)} rows\n")
        f.write("- Model calls: 2 per claim (1 text extraction, 1 multimodal vision reasoning)\n")
        f.write("- Token estimates: \n")
        f.write("  - Input: ~500 tokens per text extraction, ~1500 tokens per vision reasoning.\n")
        f.write("  - Output: ~100 tokens JSON per call.\n")
        f.write("- Estimated latency: 5-8s per claim depending on Groq response time.\n")
        f.write("- Rate limit handling: Synchronous sequential processing with basic try/except retry loop.\n")
        
    print(f"Evaluation report generated at {report_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred", default="outputs/sample_output.csv")
    parser.add_argument("--true", default="dataset/sample_claims.csv")
    parser.add_argument("--report", default="code/evaluation/evaluation_report.md")
    args = parser.parse_args()
    
    evaluate(args.pred, args.true, args.report)
