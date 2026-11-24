"""
Threat Intelligence Router (MITRE & Rule Heuristics Catalog)
"""
from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/threat-intel", tags=["Threat Intelligence"])

@router.get("")
def get_threat_intelligence() -> Dict[str, Any]:
    """Returns catalog of structural indicators, heuristic regex rules, and mitigation policies."""
    indicators = [
        {
            "id": "THREAT-001",
            "name": "Reverse Billing Premium Shortcodes",
            "category": "Financial Exfiltration",
            "severity": "CRITICAL",
            "pattern": r"(?:\b\d{5}\b|\b\d{6}\b|text\s+[a-z0-9]+\s+to\s+\d{4,6})",
            "mechanism": "Unsolicited 5-6 digit shortcodes designed to enroll victims into recurring carrier billing tariffs (£1.50 - £4.50/msg).",
            "remediation": "Immediate carrier quarantine; block shortcode responses at the SMS gateway."
        },
        {
            "id": "THREAT-002",
            "name": "Coercive Urgency & Account Suspension Bait",
            "category": "Social Engineering",
            "severity": "HIGH",
            "pattern": r"\b(urgent|immediately|within 24 hours|suspended|action required|verify account|account locked)\b",
            "mechanism": "Induces cognitive panic, compelling the victim to bypass standard validation protocols and click fraudulent verification links.",
            "remediation": "Flag panic-inducing rhetoric; cross-reference message domain against bank fraud advisories."
        },
        {
            "id": "THREAT-003",
            "name": "Lottery / Prize / Advance Fee Baiting",
            "category": "Advance Fee Fraud",
            "severity": "HIGH",
            "pattern": r"\b(winner|won|cash|prize|jackpot|claim|reward|free gift|congratulations)\b",
            "mechanism": "Promises fictitious high-value rewards conditioned on upfront administrative fees or personal identity disclosure.",
            "remediation": "Score token probability with BERT-Tiny; suppress links and quarantine message."
        },
        {
            "id": "THREAT-004",
            "name": "Direct Inbound Callback Trap (Vishing)",
            "category": "Vishing & Voice Social Engineering",
            "severity": "HIGH",
            "pattern": r"\b(?:call|ring|dial|contact)\s+(?:now|immediately|today)?\s*(?:on|at)?\s*(?:0[89]\d{8,9}|\+?44\d{10}|\+?1\d{10}|\b\d{10,11}\b)",
            "mechanism": "Prompts caller to ring premium-rate numbers (0906/0871) or connects to fraudulent call centers impersonating financial institutions.",
            "remediation": "Sanitize dialer links; present advisory warning against unsolicited incoming numbers."
        },
        {
            "id": "THREAT-005",
            "name": "Domain Masking & URL Shortener Redirection",
            "category": "Credential Harvesting",
            "severity": "CRITICAL",
            "pattern": r"(?:https?:\/\/)?(?:bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd|cutt\.ly|ow\.ly|rb\.gy)\/\S+",
            "mechanism": "Obfuscates malicious credential phishing landing pages behind benign URL shortener redirection chains.",
            "remediation": "Neutralize hyperlinks in safe-preview; perform automated sandbox link expansion."
        }
    ]

    mitre_techniques = [
        {"technique_id": "T1566.002", "name": "Phishing: Spearphishing Link", "tactic": "Initial Access"},
        {"technique_id": "T1566.003", "name": "Phishing: Spearphishing via Service", "tactic": "Initial Access"},
        {"technique_id": "T1204.001", "name": "User Execution: Malicious Link", "tactic": "Execution"},
        {"technique_id": "T1451", "name": "Sim Card Swap / SMS Redirection", "tactic": "Defense Evasion"}
    ]

    return {
        "status": "active",
        "engine": "SpamGuard ThreatIntelligence v2.0",
        "total_active_indicators": len(indicators),
        "threat_catalog": indicators,
        "mitre_alignment": mitre_techniques
    }
