"""
AURA Bilingual Language & Intent Processor
Supports English, Urdu (اردو), and Roman Urdu for global enterprise IT & BPO environments.
"""

import re
from typing import Dict, Any, Tuple

# Common Roman Urdu & Urdu patterns mapped to Enterprise IT / BPO Concepts
ROMAN_URDU_PATTERNS = {
    "server_down": [
        r"server\s+(down|band|crash|chal\s*nahi\s*raha)",
        r"system\s+(chal\s*nahi\s*raha|hang\s*hai|down\s*hai)",
        r"production\s+(ruk\s*gyi|fat\s*gya|down)",
        r"سرور\s+(ڈاؤن|بند|خراب)"
    ],
    "payment_failure": [
        r"(payment|paisa|pese|transaction)\s+(nahi\s*ho\s*rahi|ruk\s*gyi|fail|reject)",
        r"(jazzcash|easypaisa|stripe|bank)\s+(masla|issue|fail|error)",
        r"ادائیگی\s+(مسئلہ|ناکام)"
    ],
    "ticket_creation": [
        r"(ticket|shikayat|complain|issue)\s+(banao|darj|karo|open\s*karo|create\s*karo)",
        r"(ticket|request)\s+(kholo|daalo)",
        r"ٹکٹ\s+(بنائیں|درج\s*کریں)"
    ],
    "urgent_escalation": [
        r"(urgent|fauri|jaldi|emergency|bohot\s*masla|shiddat)",
        r"(senior|lead|manager|cto|head)\s+(ko\s*bulao|se\s*baat\s*krao|inform\s*karo)",
        r"فوری\s+(ایمرجنسی|رابطہ|مدد)"
    ],
    "scope_estimation": [
        r"(estimate|scope|cost|qemat|budget|kharcha|timeline|waqt|quote)\s+(batao|chahiye|kya\s*hoga)",
        r"(project|app|website|software)\s+(banana\s*hai|shuru\s*karna\s*hai|banwana\s*hai)",
        r"پروجیکٹ\s+(تخمینہ|لاگت|بجٹ)"
    ],
    "meeting_schedule": [
        r"(meeting|call|sync|baat\s*cheet)\s+(rakho|schedule\s*karo|fix\s*karo|karni\s*hai)",
        r"(demo|discussion)\s+(time|slot)",
        r"میٹنگ\s+(شیڈول|وقت)"
    ]
}

# Bilingual response templates
BILINGUAL_PHRASES = {
    "greetings_en": "Welcome to AURA Enterprise Operations. How can I assist your technical support or project scoping needs today?",
    "greetings_ur": "السلام علیکم! اورا (AURA) انٹرپرائز آپریشنز میں خوش آمدید۔ بتائیے، میں آپ کی تکنیکی مدد یا پروجیکٹ اسکوپنگ میں کیسے رہنمائی کروں؟",
    "greetings_roman": "Assalam-o-Alaikum! AURA Enterprise Operations mein khushamdeed. Main technical support, project scoping, ya SLA escalation mein aapki kya madad kar sakta hoon?",
    
    "ticket_created_en": "SLA Priority ticket has been created and assigned to the primary engineering roster.",
    "ticket_created_ur": "ترجیحی SLA ٹکٹ بن گیا ہے اور انجینئرنگ ٹیم کو سونپ دیا گیا ہے۔",
    "ticket_created_roman": "SLA priority ticket generate ho gaya hai aur on-call engineering team ko assign kar diya gaya hai.",
    
    "escalated_en": "Incident has been escalated to Tier-2 Engineering Lead under SLA emergency protocol.",
    "escalated_ur": "واقعہ ایمرجنسی پروٹوکول کے تحت ٹائر-2 انجینئرنگ لیڈ کو آگے بھیج دیا گیا ہے۔",
    "escalated_roman": "Incident ko Tier-2 Tech Lead ko escalate kar diya gaya hai under emergency SLA."
}


class BilingualProcessor:
    """Detects dialect, analyzes urgency, and provides normalized intent for IT/BPO workflows."""

    @staticmethod
    def detect_language(text: str) -> str:
        """Detects whether input is English, Nastaliq Urdu, or Roman Urdu."""
        # Check for Arabic/Persian/Urdu Unicode range
        if re.search(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]", text):
            return "ur"  # Nastaliq Urdu
        
        # Check Roman Urdu indicators
        text_lower = text.lower()
        roman_urdu_markers = [
            "hai", "hain", "karo", "karna", "nahi", "raha", "rahi", "kaise",
            "masla", "shikayat", "batao", "chahiye", "bohot", "jaldi", "shukriya",
            "aap", "hum", "kya", "kyun", "kab", "kahan", "banao", "madad"
        ]
        words = set(re.findall(r"\b\w+\b", text_lower))
        matches = words.intersection(roman_urdu_markers)
        if len(matches) >= 2 or (len(words) <= 4 and len(matches) >= 1):
            return "roman_ur"
        
        return "en"

    @staticmethod
    def analyze_intent(text: str) -> Dict[str, Any]:
        """Classifies enterprise intent and urgency level."""
        text_lower = text.lower()
        detected_lang = BilingualProcessor.detect_language(text)
        
        intents = []
        for intent_name, patterns in ROMAN_URDU_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, text_lower, re.IGNORECASE):
                    intents.append(intent_name)
                    break

        # Urgency scoring (1 = Low to 4 = Critical Blocker)
        urgency = 2  # default normal
        severity_p = "P3"
        
        critical_keywords = [
            "production down", "critical", "crash", "outage", "data loss",
            "severely impacted", "emergency", "blocker", "fat gya", "down hai",
            "urgent", "fauri", "bohot shiddat", "zaruri"
        ]
        high_keywords = [
            "payment fail", "api timeout", "database lock", "major", "error 500",
            "nahi chal raha", "kaam ruk gya"
        ]

        if any(kw in text_lower for kw in critical_keywords):
            urgency = 4
            severity_p = "P1"
        elif any(kw in text_lower for kw in high_keywords):
            urgency = 3
            severity_p = "P2"
        elif "estimate" in text_lower or "quote" in text_lower or "budget" in text_lower:
            urgency = 1
            severity_p = "P4"

        primary_intent = intents[0] if intents else "general_inquiry"

        return {
            "language": detected_lang,
            "primary_intent": primary_intent,
            "detected_intents": intents,
            "urgency_score": urgency,
            "suggested_severity": severity_p
        }

    @staticmethod
    def get_localized_confirmation(key: str, lang: str) -> str:
        """Retrieves localized response template."""
        if lang == "ur":
            return BILINGUAL_PHRASES.get(f"{key}_ur", BILINGUAL_PHRASES.get(f"{key}_en", ""))
        elif lang == "roman_ur":
            return BILINGUAL_PHRASES.get(f"{key}_roman", BILINGUAL_PHRASES.get(f"{key}_en", ""))
        return BILINGUAL_PHRASES.get(f"{key}_en", "")
