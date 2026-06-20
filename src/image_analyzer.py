import os
import json
import hashlib
from typing import List
from google import genai
from google.genai import types

from src.config.settings import ImageAnalysisResult, IssueType, Severity, RiskFlag

class ImageAnalyzer:
    def __init__(self):
        import os
        api_key = os.environ.get("FINAL_GEMINI")
        self.client = genai.Client(api_key=api_key) if api_key else genai.Client()
        self.cache_dir = "cache/vision"
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _hash_image_set(self, image_paths: List[str], requirements: str) -> str:
        hasher = hashlib.sha256()
        for path in sorted(image_paths):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    hasher.update(f.read())
        hasher.update(requirements.encode("utf-8"))
        return hasher.hexdigest()
        
    def analyze_images(self, image_paths: List[str], claim_object: str, extracted_claim: dict, requirements: str, image_ids: List[str]) -> ImageAnalysisResult:
        cache_key = self._hash_image_set(image_paths, requirements)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                return ImageAnalysisResult(**data)
            except Exception as e:
                pass
                
        prompt = f"""
        You are an expert multimodal damage assessor.
        The user claims this is a {claim_object}.
        The claimed issue is: {extracted_claim['claimed_damage']} on part {extracted_claim['claimed_object_part']}.
        
        Requirements for evidence:
        {requirements}
        
        The image IDs are: {', '.join(image_ids)}.
        
        Analyze all the images together. Determine the issue, object part, and severity. 
        Select the supporting image IDs that clearly show the damage. 
        If damage is not visible, set issue_type to 'none' and add 'damage_not_visible' to quality_observations.
        """
        
        contents = [prompt]
        for path in image_paths:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    image_bytes = f.read()
                # Guessing jpeg is fine for most sample images
                contents.append(
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                )
        
        # We manually construct the response format because pydantic enums can be tricky sometimes
        # But let's try the direct pydantic schema passing
        import time
        last_error = "Unknown error"
        for attempt in range(4):
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=ImageAnalysisResult,
                        temperature=0.0
                    )
                )
                data = json.loads(response.text)
                
                try:
                    data['issue_type'] = IssueType(data.get('issue_type', '').lower())
                except:
                    data['issue_type'] = IssueType.UNKNOWN
                try:
                    data['severity'] = Severity(data.get('severity', '').lower())
                except:
                    data['severity'] = Severity.UNKNOWN
                    
                if 'quality_observations' not in data:
                    data['quality_observations'] = []
                if 'supporting_image_ids' not in data:
                    data['supporting_image_ids'] = []
                
                clean_flags = []
                for f in data['quality_observations']:
                    try:
                        clean_flags.append(RiskFlag(f))
                    except:
                        pass
                data['quality_observations'] = clean_flags
                
                result = ImageAnalysisResult(**data)
                with open(cache_file, "w") as f:
                    json.dump(result.model_dump(), f)
                return result
                
            except Exception as e:
                err_str = str(e)
                last_error = err_str
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    print(f"Rate limited. Sleeping 65 seconds... (Attempt {attempt+1}/4)")
                    time.sleep(65)
                    continue
                else:
                    print(f"Gemini error: {e}")
                    break
        
        return ImageAnalysisResult(
                object_detected="error",
                object_part="error",
                issue_type=IssueType.UNKNOWN,
                severity=Severity.UNKNOWN,
                supporting_image_ids=[],
                quality_observations=[],
                confidence=0.0,
                reasoning=f"Error analyzing image: {last_error}"
            )
