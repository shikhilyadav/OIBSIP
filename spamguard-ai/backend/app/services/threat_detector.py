"""
Threat Intelligence & Structural Pattern Extractor
Extracts explainable lexical, numerical, and structural spam indicators.
"""

import re
from typing import List, Dict, Any

class ThreatDetector:
    # Telephony patterns
    PHONE_REGEX = re.compile(r"\b(0906\d{7}|0800\d{6,7}|0845\d{6,7}|0871\d{6,7}|\+?\d{10,12})\b", re.I)
    SHORTCODE_REGEX = re.compile(r"\b(87121|82242|86688|50300|69698|8007|78088|85023)\b")
    
    # URL patterns
    URL_REGEX = re.compile(r"https?://\S+|www\.\S+|\b\w+\.(xyz|top|club|ru|tk|cc|cn|info|live)\b", re.I)
    SUSPICIOUS_PATH_REGEX = re.compile(r"(login|auth|verify|secure|update|banking|account|signin)", re.I)
    
    # Financial & Prize keywords
    PRIZE_REGEX = re.compile(r"\b(congratulations|winner|won|free prize|cash reward|award|selected to receive|jackpot|£\d+|\$\d+)\b", re.I)
    
    # Urgency & Threat keywords
    URGENCY_REGEX = re.compile(r"\b(urgent|immediate|suspended|blocked|locked|verify your details|action required|expires? (today|soon)|unauthorized)\b", re.I)
    
    # Reverse billing SMS keywords
    REVERSE_BILL_REGEX = re.compile(r"\b(stop|reply to stop|txt\b|std txt rate|ppm|tone|subscrip)\b", re.I)

    @classmethod
    def analyze(cls, text: str) -> List[Dict[str, str]]:
        signals = []
        
        # 1. Phone number detection
        phone_matches = cls.PHONE_REGEX.findall(text)
        if phone_matches:
            signals.append({
                "signal_type": "telephony_premium_number",
                "indicator": f"Phone: {phone_matches[0]}",
                "severity": "high",
                "description": "Actionable toll or premium rate dial code detected (classic reverse-billing monetization mechanism)."
            })
            
        # 2. Shortcode detection
        shortcode_matches = cls.SHORTCODE_REGEX.findall(text)
        if shortcode_matches:
            signals.append({
                "signal_type": "telephony_shortcode",
                "indicator": f"Shortcode: {shortcode_matches[0]}",
                "severity": "high",
                "description": "5-digit commercial SMS shortcode identified (frequently utilized in mass unprompted mobile marketing)."
            })
            
        # 3. URL detection
        url_matches = cls.URL_REGEX.findall(text)
        if url_matches:
            has_auth_path = bool(cls.SUSPICIOUS_PATH_REGEX.search(text))
            signals.append({
                "signal_type": "suspicious_url",
                "indicator": f"Link: {url_matches[0][:30]}...",
                "severity": "critical" if has_auth_path else "medium",
                "description": "Embedded external web hyperlink identified; carries potential credential harvesting or phishing risk."
            })
            
        # 4. Prize & Financial bait
        prize_matches = cls.PRIZE_REGEX.findall(text)
        if prize_matches:
            signals.append({
                "signal_type": "promotional_prize_lure",
                "indicator": f"Bait: {prize_matches[0]}",
                "severity": "medium",
                "description": "Unprompted reward, prize claim, or cash incentive terminology identified."
            })
            
        # 5. Account threat & urgency
        urgency_matches = cls.URGENCY_REGEX.findall(text)
        if urgency_matches:
            signals.append({
                "signal_type": "urgency_account_threat",
                "indicator": f"Urgency: {urgency_matches[0]}",
                "severity": "high",
                "description": "High-urgency coercive language mimicking security, banking, or account suspension notices."
            })

        # 6. Reverse billing / opt-out
        rev_matches = cls.REVERSE_BILL_REGEX.findall(text)
        if rev_matches:
            signals.append({
                "signal_type": "carrier_rate_disclaimer",
                "indicator": f"Carrier: {rev_matches[0]}",
                "severity": "medium",
                "description": "Reverse-billed SMS disclaimer or mandatory opt-out prompt ('Reply STOP')."
            })

        return signals
