import cv2
import numpy as np
import os
from typing import List, Tuple
from src.config.settings import RiskFlag

class LocalPreprocessor:
    def process_images(self, image_paths: List[str]) -> Tuple[bool, List[RiskFlag]]:
        valid = False
        flags = set()
        
        for path in image_paths:
            if not os.path.exists(path):
                continue
                
            img = cv2.imread(path)
            if img is None:
                continue
                
            valid = True
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            if laplacian_var < 50.0:
                flags.add(RiskFlag.BLURRY_IMAGE)
                
            mean_brightness = np.mean(gray)
            if mean_brightness < 40 or mean_brightness > 220:
                flags.add(RiskFlag.LOW_LIGHT_OR_GLARE)
                
        return valid, list(flags)
