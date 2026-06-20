from typing import List
from src.config.settings import ClaimOutputRow, RiskFlag, ClaimStatus, ImageAnalysisResult, ClaimInput, IssueType
from src.object_part_mapper import ObjectPartMapper
from src.severity_calibrator import SeverityCalibrator

class DecisionEngine:
    def make_decision(self, input_row: ClaimInput, image_result: ImageAnalysisResult, user_history_context: dict, image_ids: List[str]) -> ClaimOutputRow:
        flags = set()
        for f in image_result.quality_observations:
            try:
                flags.add(RiskFlag(f))
            except ValueError:
                pass
                
        flags.update(user_history_context['risk_flags'])
        
        # Apply Normalization
        mapped_part = ObjectPartMapper.map_part(image_result.object_part, input_row.claim_object.value)
        image_result.object_part = mapped_part
        
        # Apply Severity Calibration
        calibrated_severity = SeverityCalibrator.calibrate(image_result.issue_type, image_result.severity)
        image_result.severity = calibrated_severity
        
        # Consistency checks
        obj_lower = input_row.claim_object.value.lower()
        iss_type = image_result.issue_type
        
        if image_result.object_detected.lower() != obj_lower and image_result.object_detected.lower() != "unknown":
            flags.add(RiskFlag.WRONG_OBJECT)
            
        # Hard constraint checks
        if obj_lower == "laptop":
            if iss_type in [IssueType.CRUSHED_PACKAGING, IssueType.TORN_PACKAGING]:
                iss_type = IssueType.UNKNOWN
                image_result.issue_type = IssueType.UNKNOWN
                flags.add(RiskFlag.CLAIM_MISMATCH)
            if iss_type == IssueType.WATER_DAMAGE and "stain" in input_row.user_claim.lower():
                iss_type = IssueType.STAIN
                image_result.issue_type = IssueType.STAIN
        elif obj_lower == "package":
            if iss_type in [IssueType.GLASS_SHATTER]:
                iss_type = IssueType.UNKNOWN
                image_result.issue_type = IssueType.UNKNOWN
                flags.add(RiskFlag.CLAIM_MISMATCH)
        elif obj_lower == "car":
            if iss_type == IssueType.GLASS_SHATTER and image_result.object_part == "windshield":
                iss_type = IssueType.CRACK
                image_result.issue_type = IssueType.CRACK
            if iss_type == IssueType.GLASS_SHATTER and image_result.object_part == "side_mirror":
                iss_type = IssueType.BROKEN_PART
                image_result.issue_type = IssueType.BROKEN_PART
                
        # Determine status
        status = ClaimStatus.NOT_ENOUGH_INFORMATION
        
        # Determine if we have a valid issue detected
        valid_issue = iss_type not in [IssueType.NONE, IssueType.UNKNOWN]
        
        # Keyword matching to overrule Gemini's claim_mismatch if it hallucinated it
        # E.g. user_004 claims 'crack' and we detected 'crack'.
        if valid_issue and RiskFlag.CLAIM_MISMATCH in flags:
            if iss_type.value.replace("_", " ") in input_row.user_claim.lower():
                flags.remove(RiskFlag.CLAIM_MISMATCH)
        
        # Priority 1: Not enough info (Wrong object, damage not visible, etc.)
        if RiskFlag.WRONG_OBJECT in flags or RiskFlag.DAMAGE_NOT_VISIBLE in flags or RiskFlag.WRONG_ANGLE in flags or RiskFlag.CROPPED_OR_OBSTRUCTED in flags:
            status = ClaimStatus.NOT_ENOUGH_INFORMATION
        # Priority 2: Contradictions (Mismatched claim, or explicitly 'none' damage when claimed and visible)
        elif RiskFlag.CLAIM_MISMATCH in flags or iss_type == IssueType.NONE:
            status = ClaimStatus.CONTRADICTED
        # Priority 3: Blurry/Low Light without a valid issue
        elif (RiskFlag.BLURRY_IMAGE in flags or RiskFlag.LOW_LIGHT_OR_GLARE in flags) and not valid_issue:
            status = ClaimStatus.NOT_ENOUGH_INFORMATION
        # Priority 4: Supported
        else:
            status = ClaimStatus.SUPPORTED
            
        evidence_met = True
        evidence_reason = "The image set provides sufficient visual evidence."
        if status == ClaimStatus.NOT_ENOUGH_INFORMATION:
            evidence_met = False
            evidence_reason = image_result.reasoning
            
        supporting = "none"
        if status == ClaimStatus.SUPPORTED:
            supporting = ";".join(image_result.supporting_image_ids) if image_result.supporting_image_ids else "none"
            
        if RiskFlag.NONE in flags and len(flags) > 1:
            flags.remove(RiskFlag.NONE)
            
        flag_str = ";".join([f.value for f in flags]) if flags else "none"
        
        justification = image_result.reasoning if image_result.reasoning else "No justification provided."
        
        # Override issue and severity if wrong object or damage not visible
        final_issue = image_result.issue_type.value if type(image_result.issue_type) != str else image_result.issue_type
        if type(final_issue) != str:
            final_issue = final_issue.value
            
        final_part = image_result.object_part
        final_severity = image_result.severity.value if type(image_result.severity) != str else image_result.severity
        if type(final_severity) != str:
            final_severity = final_severity.value
        
        if RiskFlag.WRONG_OBJECT in flags or RiskFlag.DAMAGE_NOT_VISIBLE in flags:
            final_issue = "unknown"
            final_part = "unknown"
            final_severity = "unknown"
        
        return ClaimOutputRow(
            user_id=input_row.user_id,
            image_paths=input_row.image_paths,
            user_claim=input_row.user_claim,
            claim_object=input_row.claim_object.value,
            evidence_standard_met=evidence_met,
            evidence_standard_met_reason=evidence_reason,
            risk_flags=flag_str,
            issue_type=final_issue,
            object_part=final_part,
            claim_status=status.value,
            claim_status_justification=justification,
            supporting_image_ids=supporting,
            valid_image=RiskFlag.BLURRY_IMAGE not in flags and RiskFlag.DAMAGE_NOT_VISIBLE not in flags,
            severity=final_severity
        )
