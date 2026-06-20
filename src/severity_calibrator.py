from src.config.settings import IssueType, Severity

class SeverityCalibrator:
    @staticmethod
    def calibrate(issue_type: IssueType, raw_severity: Severity) -> Severity:
        if issue_type in [IssueType.NONE, IssueType.UNKNOWN]:
            return Severity.NONE if issue_type == IssueType.NONE else Severity.UNKNOWN
            
        # Hard physics-based mappings where severity is intrinsically tied to issue type
        if issue_type in [IssueType.SCRATCH, IssueType.STAIN]:
            return Severity.LOW
            
        if issue_type in [IssueType.GLASS_SHATTER, IssueType.BROKEN_PART]:
            return Severity.HIGH
            
        # For DENT, CRACK, WATER_DAMAGE, torn/crushed packaging, fall back to what Gemini predicted,
        # but bound it to at least medium if Gemini underestimated, or cap it at medium if Gemini overestimated
        # For our baseline, let's just default these to medium unless Gemini specifically said HIGH and it's a major dent.
        if issue_type in [IssueType.DENT, IssueType.CRACK, IssueType.WATER_DAMAGE, IssueType.CRUSHED_PACKAGING, IssueType.TORN_PACKAGING]:
            # Gemini often over-predicts dent/crack as high. Let's default them to medium for most parts.
            return Severity.MEDIUM
            
        return raw_severity
