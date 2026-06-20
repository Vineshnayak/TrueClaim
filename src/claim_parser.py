import os
import json
import time
import hashlib
from groq import Groq
from src.config.settings import ClaimExtraction

class ClaimParser:
    def __init__(self):
        self.client = Groq()
        self.cache_dir = "cache/claims"
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _hash_claim(self, user_claim: str, claim_object: str) -> str:
        hasher = hashlib.sha256()
        hasher.update(user_claim.encode("utf-8"))
        hasher.update(claim_object.encode("utf-8"))
        return hasher.hexdigest()
        
    def parse_claim(self, user_claim: str, claim_object: str) -> ClaimExtraction:
        cache_key = self._hash_claim(user_claim, claim_object)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                return ClaimExtraction(**data)
            except:
                pass
                
        system_prompt = (
            "You are a strict JSON data extractor. "
            f"Extract the damage claim for a '{claim_object}' from the conversation. "
            "Return JSON with EXACTLY these keys: "
            "'claimed_damage' (what is damaged?), "
            "'claimed_object_part' (which part?), "
            "'issue_family' (short category like 'dent', 'scratch', 'broken', etc.), "
            "'severity_hints' (any hint of severity or 'none'). "
        )
        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_claim}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0
                )
                data = json.loads(response.choices[0].message.content)
                result = ClaimExtraction(**data)
                with open(cache_file, "w") as f:
                    json.dump(result.model_dump(), f)
                return result
            except Exception as e:
                time.sleep(2)
        # fallback
        return ClaimExtraction(
            claimed_damage="unknown", 
            claimed_object_part="unknown", 
            issue_family="unknown", 
            severity_hints="none"
        )
