import os
import json
import hashlib
from groq import Groq

class JustificationEngine:
    def __init__(self):
        self.client = Groq()
        self.cache_dir = "cache/justification"
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _hash_context(self, context: dict) -> str:
        hasher = hashlib.sha256()
        hasher.update(json.dumps(context, sort_keys=True).encode("utf-8"))
        return hasher.hexdigest()
        
    def generate_justification(self, claim_status: str, vision_reasoning: str, user_claim: str, image_ids: str) -> str:
        context = {
            "status": claim_status,
            "vision": vision_reasoning,
            "claim": user_claim,
            "images": image_ids
        }
        
        cache_key = self._hash_context(context)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.txt")
        
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                return f.read()
                
        prompt = f"""
        You are a justification engine for an insurance claim system.
        The final decision is: {claim_status}.
        The vision model reported: {vision_reasoning}.
        The user claimed: {user_claim}.
        Supporting images: {image_ids}.
        
        Write a concise (1-2 sentences), image-grounded justification for the decision. 
        Reference image ids if appropriate. Avoid hallucinations. Do not add any conversational filler.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            justification = response.choices[0].message.content.strip()
            with open(cache_file, "w") as f:
                f.write(justification)
            return justification
        except Exception as e:
            return vision_reasoning
