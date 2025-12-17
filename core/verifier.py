import random
import time

class GeoSentinel:
    """
    AI-driven component that simulates the analysis of satellite imagery
    to verify carbon assets.
    """
    def __init__(self):
        pass

    def verify_location(self, lat, lon):
        """
        Simulates fetching a satellite image and running a deep learning model.
        Returns a verification result with detailed reasons.
        """
        reasons = []
        
        # 1. SPECIAL DEMO WHITELIST
        # If the user enters the specific demo coordinates, give a perfect result.
        if abs(lat - 11.4102) < 0.001 and abs(lon - 76.6950) < 0.001:
            green_cover = 94.5
            authenticity_score = 0.99
            reasons.append("High Density Forest Detected")
        else:
            # 2. Standard Simulation
            # Deterministic capability based on coords for demo consistency
            random.seed(lat + lon) 
            
            # Widen the range to ensure we see both bad and good results 
            # BIAS: Weighted towards "verified" (forests) to match user expectation
            green_cover = random.uniform(35, 98) # Mostly > 45%
            authenticity_score = random.uniform(0.78, 0.99) # Check score

        # 3. Decision Logic
        is_valid = True
        
        # Criterion A: Green Cover
        if green_cover < 45.0:
            is_valid = False
            reasons.append(f"Insufficient Green Cover ({round(green_cover,1)}% < 45%)")
        
        # Criterion B: AI Confidence/Authenticity
        if authenticity_score < 0.80:
            is_valid = False
            reasons.append("AI Confidence Low - Potential Forgery")

        if is_valid:
            status = "VERIFIED"
            if not reasons: reasons.append("Asset Meets All Environmental Criteria")
        else:
            status = "FLAGGED"

        return {
            "latitude": lat,
            "longitude": lon,
            "green_cover_percentage": round(green_cover, 2),
            "ai_confidence": round(authenticity_score * 100, 1),
            "status": status,
            "reasons": reasons,
            "timestamp": time.time()
        }
