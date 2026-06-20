import os
import argparse
import sys

# Add project root to path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from src.loader import DataLoader
from src.history_analyzer import HistoryAnalyzer
from src.evidence_checker import EvidenceChecker
from src.claim_parser import ClaimParser
from src.image_analyzer import ImageAnalyzer
from src.decision_engine import DecisionEngine
from src.output_formatter import OutputFormatter
from src.local_preprocessor import LocalPreprocessor
from src.justification_engine import JustificationEngine
from src.config.settings import ClaimInput, ObjectType, RiskFlag

def run_pipeline(data_dir: str, input_file: str, output_file: str):
    load_dotenv()
    
    missing_keys = []
    if not os.environ.get("GEMINI_API_KEY"):
        missing_keys.append("GEMINI_API_KEY")
    if not os.environ.get("GROQ_API_KEY"):
        missing_keys.append("GROQ_API_KEY")
        
    if missing_keys:
        print(f"Missing API keys: {', '.join(missing_keys)}")
        sys.exit(1)
        
    loader = DataLoader(data_dir)
    claims_df = loader.load_claims(input_file)
    history_df = loader.load_user_history()
    evidence_df = loader.load_evidence_requirements()
    
    history_analyzer = HistoryAnalyzer(history_df)
    evidence_checker = EvidenceChecker(evidence_df)
    
    local_preprocessor = LocalPreprocessor()
    claim_parser = ClaimParser()
    image_analyzer = ImageAnalyzer()
    decision_engine = DecisionEngine()
    justification_engine = JustificationEngine()
    output_formatter = OutputFormatter()
    
    results = []
    
    for idx, row in claims_df.iterrows():
        print(f"Processing row {idx+1}/{len(claims_df)}: {row['user_id']}")
        
        input_row = ClaimInput(
            user_id=row['user_id'],
            image_paths=row['image_paths'],
            user_claim=row['user_claim'],
            claim_object=ObjectType(row['claim_object'])
        )
        
        image_paths = [p.strip() for p in input_row.image_paths.split(";")]
        image_ids = [os.path.splitext(os.path.basename(p))[0] for p in image_paths]
        
        full_image_paths = [os.path.join(data_dir, p) for p in image_paths]
        
        # Local preprocessing
        valid_local, local_flags = local_preprocessor.process_images(full_image_paths)
        
        user_context = history_analyzer.get_user_risk_context(input_row.user_id)
        
        extracted_claim = claim_parser.parse_claim(input_row.user_claim, input_row.claim_object.value)
        
        reqs = evidence_checker.get_requirements(input_row.claim_object.value, extracted_claim.issue_family)
        
        image_result = image_analyzer.analyze_images(full_image_paths, input_row.claim_object.value, extracted_claim.model_dump(), reqs, image_ids)
        
        # Merge local flags into image_result
        image_result.quality_observations.extend(local_flags)
        
        final_row = decision_engine.make_decision(input_row, image_result, user_context, image_ids)
        
        # Call justification engine
        final_justification = justification_engine.generate_justification(
            claim_status=final_row.claim_status,
            vision_reasoning=image_result.reasoning,
            user_claim=input_row.user_claim,
            image_ids=final_row.supporting_image_ids
        )
        final_row.claim_status_justification = final_justification
        
        results.append(final_row)
        
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        output_formatter.write_output(results, output_file)
        
    print(f"Finished processing. Output written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="dataset", help="Path to dataset directory")
    parser.add_argument("--input", default="claims.csv", help="Input filename inside data_dir")
    parser.add_argument("--output", default="output.csv", help="Output filename")
    args = parser.parse_args()
    
    run_pipeline(args.data_dir, args.input, args.output)
