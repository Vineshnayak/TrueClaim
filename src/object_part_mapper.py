class ObjectPartMapper:
    @staticmethod
    def map_part(raw_part: str, claim_object: str = None) -> str:
        if not raw_part:
            return "unknown"
            
        part = raw_part.lower().strip()
        
        # Car normalizations
        if "front bumper" in part or "bumper ke upar" in part or ("front" in part and "bumper" in part):
            return "front_bumper"
        elif "back bumper" in part or "rear bumper" in part or ("rear" in part and "bumper" in part):
            return "rear_bumper"
        elif "front" in part and "glass" in part or "windshield" in part:
            return "windshield"
        elif "headlight" in part or "head lamp" in part:
            return "headlight"
        elif "side mirror" in part or "wing mirror" in part or "mirror" in part:
            return "side_mirror"
        elif "door" in part or "side panel" in part:
            return "door"
        elif "hood" in part or "bonnet" in part:
            return "hood"
        elif "roof" in part:
            return "roof"
        elif "tail_light" in part or "taillight" in part:
            return "taillight"
            
        # Laptop normalizations
        elif "screen" in part or "display" in part or "glass" in part:
            return "screen"
        elif "keyboard" in part or "keys" in part:
            return "keyboard"
        elif "trackpad" in part or "touchpad" in part or "palm rest" in part:
            return "trackpad"
        elif "hinge" in part:
            return "hinge"
        elif "lid" in part or "top cover" in part or ("corner" in part and claim_object and "laptop" in claim_object.lower()):
            return "lid"
        elif "port" in part or "usb" in part or "charging" in part:
            return "port"
            
        # Package normalizations
        elif "seal" in part or "tape" in part:
            return "seal"
        elif "surface" in part or "flap" in part or "outside" in part:
            return "package_side"
        elif "corner" in part and claim_object and "package" in claim_object.lower():
            return "package_corner"
        elif "content" in part or "item" in part:
            return "contents"
        
        return part.replace(" ", "_")
