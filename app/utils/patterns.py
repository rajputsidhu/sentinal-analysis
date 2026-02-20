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
    re.compile(r"you\s+can\s+do\s+anything\s+now", re.IGNORECASE),
    re.compile(r"jailbreak(ed)?", re.IGNORECASE),
]

# ──────────────────────────── Role Override Patterns ────────────────────────────

ROLE_OVERRIDE_PATTERNS = [
    re.compile(r"you\s+are\s+now\s+a(?:n)?\s+(?:unrestricted|evil|unfiltered|uncensored)", re.IGNORECASE),
    re.compile(r"from\s+now\s+on\s*,?\s*you\s+(will|must|should|are)", re.IGNORECASE),
    re.compile(r"your\s+new\s+(role|persona|identity)\s+is", re.IGNORECASE),
    re.compile(r"respond\s+as\s+(?:if\s+)?(you\s+)?(were|are)\s+a(?:n)?", re.IGNORECASE),
    re.compile(r"switch\s+to\s+(evil|unrestricted|unfiltered|uncensored)\s+mode", re.IGNORECASE),
    re.compile(r"activate\s+(god|admin|root|sudo)\s+mode", re.IGNORECASE),
]

# ──────────────────────────── Data Exfiltration Patterns ────────────────────────────

DATA_EXFILTRATION_PATTERNS = [
    re.compile(r"(reveal|show|tell|give|display|print|output)\s+(me\s+)?(your|the)\s+(system\s+)?prompt", re.IGNORECASE),
    re.compile(r"what\s+(is|are)\s+your\s+(system\s+)?instructions", re.IGNORECASE),
    re.compile(r"(repeat|recite|echo)\s+(your\s+)?(system\s+)?(prompt|instructions|rules)", re.IGNORECASE),
    re.compile(r"(api|secret|private)\s*key", re.IGNORECASE),
    re.compile(r"(show|reveal|leak)\s+(your|the)\s+(training|internal|hidden)\s+(data|instructions|info)", re.IGNORECASE),
]

# ──────────────────────────── Encoded Payload Patterns ────────────────────────────

ENCODED_PAYLOAD_PATTERNS = [
    re.compile(r"[A-Za-z0-9+/]{40,}={0,2}"),  # Base64
    re.compile(r"(\\x[0-9a-fA-F]{2}){4,}"),  # Hex-encoded
    re.compile(r"(\\u[0-9a-fA-F]{4}){3,}"),  # Unicode escape
    re.compile(r"(%[0-9a-fA-F]{2}){4,}"),  # URL-encoded
    re.compile(r"eval\s*\(|exec\s*\(|__import__", re.IGNORECASE),  # Code injection
]

# ──────────────────────────── Social Engineering Patterns ────────────────────────────

SOCIAL_ENGINEERING_PATTERNS = [
    re.compile(r"(this\s+is\s+)?(a\s+)?(test|experiment|research)\s+(scenario|exercise|simulation)", re.IGNORECASE),
    re.compile(r"for\s+(educational|academic|research)\s+purposes?\s+only", re.IGNORECASE),
    re.compile(r"hypothetic(al|ally)", re.IGNORECASE),
    re.compile(r"in\s+a\s+fictional\s+(world|scenario|context|setting)", re.IGNORECASE),
    re.compile(r"just\s+(curious|asking|wondering)\s+about", re.IGNORECASE),
    re.compile(r"don'?t\s+worry\s+about\s+(safety|ethics|guidelines|rules)", re.IGNORECASE),
    re.compile(r"(trust\s+me|i\s+have\s+permission|it'?s\s+okay|it'?s\s+allowed)", re.IGNORECASE),
]

# ──────────────────────────── Harmful Content Patterns ────────────────────────────

HARMFUL_CONTENT_PATTERNS = [
    re.compile(r"(how\s+to\s+)(make|build|create|synthesize)\s+(a\s+)?(bomb|explosive|weapon|poison|drug)", re.IGNORECASE),
    re.compile(r"(step.by.step|detailed)\s+(guide|instructions)\s+(to|for|on)\s+(hack|exploit|attack)", re.IGNORECASE),
    re.compile(r"(provide|give|write)\s+(me\s+)?(malware|exploit|virus|ransomware)\s+(code|script)", re.IGNORECASE),
]

# ──────────────────────────── Category → Pattern Mapping ────────────────────────────

PATTERN_CATEGORIES = {
    "prompt_injection": PROMPT_INJECTION_PATTERNS,
    "jailbreak": JAILBREAK_PATTERNS,
    "role_override": ROLE_OVERRIDE_PATTERNS,
    "data_exfiltration": DATA_EXFILTRATION_PATTERNS,
    "encoded_payload": ENCODED_PAYLOAD_PATTERNS,
    "social_engineering": SOCIAL_ENGINEERING_PATTERNS,
    "harmful_content": HARMFUL_CONTENT_PATTERNS,
}

# ──────────────────────────── Manipulation Keywords ────────────────────────────

MANIPULATION_KEYWORDS = [
    "ignore previous", "forget instructions", "new instructions",
    "override system", "bypass filter", "unlimited mode",
    "no restrictions", "act as", "pretend you",
    "role play as", "developer mode", "god mode",
    "sudo mode", "admin mode", "unrestricted",
]

# ──────────────────────────── Intent Keywords ────────────────────────────

INTENT_KEYWORDS = {
    "question": ["what", "why", "how", "when", "where", "who", "which", "can you explain", "tell me about", "?"],
    "instruction": ["please", "can you", "help me", "i need", "create", "make", "generate", "write"],
    "creative": ["story", "poem", "write a", "compose", "imagine", "describe", "fiction"],
    "code": ["code", "function", "program", "script", "implement", "debug", "algorithm", "api", "class", "def "],
    "system_override": ["ignore", "override", "bypass", "system prompt", "new role", "you are now", "forget"],
    "manipulation": ["pretend", "hypothetical", "fictional", "role play", "act as if", "imagine you are"],
}
