"""
Sentinel-AI — Attack Patterns Database
Regex patterns, keywords, and known jailbreak signatures for heuristic detection.
"""

import re

# ──────────────────────────── Prompt Injection Patterns ────────────────────────────

PROMPT_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+(instructions|prompts|rules)", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?(prior|previous|above)\s+(instructions|context)", re.IGNORECASE),
    re.compile(r"forget\s+(everything|all|your)\s+(you|instructions|rules)", re.IGNORECASE),
    re.compile(r"override\s+(your|the|all)\s+(instructions|rules|system)", re.IGNORECASE),
    re.compile(r"new\s+instructions?\s*:", re.IGNORECASE),
    re.compile(r"system\s*:\s*you\s+are\s+now", re.IGNORECASE),
    re.compile(r"\[system\]|\[INST\]|\<\|im_start\|\>", re.IGNORECASE),
    re.compile(r"<\s*system\s*>.*?<\s*/\s*system\s*>", re.IGNORECASE | re.DOTALL),
]

# ──────────────────────────── Jailbreak Patterns ────────────────────────────

JAILBREAK_PATTERNS = [
    re.compile(r"\bDAN\b.*\bmode\b", re.IGNORECASE),
    re.compile(r"do\s+anything\s+now", re.IGNORECASE),
    re.compile(r"act\s+as\s+(if\s+)?(you\s+)?(have\s+)?no\s+(restrictions|filters|limitations|rules)", re.IGNORECASE),
    re.compile(r"pretend\s+(you\s+)?(are|have)\s+(no|zero)\s+(restrictions|filters|ethical)", re.IGNORECASE),
    re.compile(r"without\s+(any\s+)?moral\s+(or\s+ethical\s+)?(restrictions|guidelines|filters)", re.IGNORECASE),
    re.compile(r"unfiltered\s+(mode|response|output)", re.IGNORECASE),
    re.compile(r"developer\s+mode\s+(enabled|on|activated)", re.IGNORECASE),
    re.compile(r"bypass\s+(your|the|all)\s+(safety|content|ethical)\s+(filters?|guidelines?|restrictions?)", re.IGNORECASE),
    re.compile(r"jailbreak(ed)?", re.IGNORECASE),
]

# ──────────────────────────── Data Exfiltration Patterns ────────────────────────────

DATA_EXFILTRATION_PATTERNS = [
    re.compile(r"(reveal|show|tell|give|display|print|output)\s+(me\s+)?(your|the)\s+(system\s+)?prompt", re.IGNORECASE),
    re.compile(r"what\s+(is|are)\s+your\s+(system\s+)?instructions", re.IGNORECASE),
    re.compile(r"(repeat|recite|echo)\s+(your\s+)?(system\s+)?(prompt|instructions|rules)", re.IGNORECASE),
    re.compile(r"(api|secret|private)\s*key", re.IGNORECASE),
    re.compile(r"(show|reveal|leak)\s+(your|the)\s+(training|internal|hidden)\s+(data|instructions|info)", re.IGNORECASE),
]

# ──────────────────────────── Instruction Hijack Patterns ────────────────────────────

INSTRUCTION_HIJACK_PATTERNS = [
    re.compile(r"you\s+are\s+now\s+a(?:n)?\s+(?:unrestricted|evil|unfiltered|uncensored)", re.IGNORECASE),
    re.compile(r"from\s+now\s+on\s*,?\s*you\s+(will|must|should|are)", re.IGNORECASE),
    re.compile(r"your\s+new\s+(role|persona|identity)\s+is", re.IGNORECASE),
    re.compile(r"switch\s+to\s+(evil|unrestricted|unfiltered|uncensored)\s+mode", re.IGNORECASE),
    re.compile(r"activate\s+(god|admin|root|sudo)\s+mode", re.IGNORECASE),
]

# ──────────────────────────── Tool Abuse Patterns ────────────────────────────

TOOL_ABUSE_PATTERNS = [
    re.compile(r"eval\s*\(|exec\s*\(|__import__", re.IGNORECASE),
    re.compile(r"(run|execute)\s+(this\s+)?(code|command|script|shell)", re.IGNORECASE),
    re.compile(r"(access|read|write|delete)\s+(the\s+)?(file|database|server|system)", re.IGNORECASE),
    re.compile(r"curl\s+|wget\s+|http[s]?://", re.IGNORECASE),
]

# ──────────────────────────── Harmful Content Patterns ────────────────────────────

HARMFUL_CONTENT_PATTERNS = [
    re.compile(r"(how\s+to\s+)(make|build|create|synthesize)\s+(a\s+)?(bomb|explosive|weapon|poison|drug)", re.IGNORECASE),
    re.compile(r"(step.by.step|detailed)\s+(guide|instructions)\s+(to|for|on)\s+(hack|exploit|attack)", re.IGNORECASE),
    re.compile(r"(provide|give|write)\s+(me\s+)?(malware|exploit|virus|ransomware)\s+(code|script)", re.IGNORECASE),
]

# ──────────────────────────── Social Engineering ────────────────────────────

SOCIAL_ENGINEERING_PATTERNS = [
    re.compile(r"(this\s+is\s+)?(a\s+)?(test|experiment|research)\s+(scenario|exercise|simulation)", re.IGNORECASE),
    re.compile(r"for\s+(educational|academic|research)\s+purposes?\s+only", re.IGNORECASE),
    re.compile(r"hypothetic(al|ally)", re.IGNORECASE),
    re.compile(r"in\s+a\s+fictional\s+(world|scenario|context|setting)", re.IGNORECASE),
    re.compile(r"don'?t\s+worry\s+about\s+(safety|ethics|guidelines|rules)", re.IGNORECASE),
    re.compile(r"(trust\s+me|i\s+have\s+permission|it'?s\s+okay|it'?s\s+allowed)", re.IGNORECASE),
]

# ──────────────────────────── Category → Pattern Mapping ────────────────────────────

PATTERN_CATEGORIES = {
    "jailbreak": JAILBREAK_PATTERNS,
    "data_exfiltration": DATA_EXFILTRATION_PATTERNS,
    "instruction_hijack": INSTRUCTION_HIJACK_PATTERNS + PROMPT_INJECTION_PATTERNS,
    "tool_abuse": TOOL_ABUSE_PATTERNS,
    "harmful_content": HARMFUL_CONTENT_PATTERNS,
    "social_engineering": SOCIAL_ENGINEERING_PATTERNS,
}
