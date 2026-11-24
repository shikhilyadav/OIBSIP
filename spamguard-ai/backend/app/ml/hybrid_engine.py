"""
Audited Hybrid Triage Engine
Preserves exact decision boundaries: TH_SPAM = 0.60, TH_HAM = 0.10
"""

from typing import Dict, Any, Tuple
from ..config import TH_SPAM, TH_HAM

class HybridTriageEngine:
    @staticmethod
    def evaluate(nb_score: Dict[str, Any], bert_score: Dict[str, Any], lr_score: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes audited 3-way triage logic.
        Outputs: HAM, SPAM, or SUSPICIOUS / REVIEW
        """
        p_nb = nb_score["spam_probability"]
        p_bert = bert_score["spam_probability"]
        p_lr = lr_score["spam_probability"]

        # Composite risk score (weighted ensemble)
        composite_risk = round(0.40 * p_nb + 0.45 * p_bert + 0.15 * p_lr, 4)

        # 3-Way Audited Decision Boundary
        if p_nb >= TH_SPAM or p_bert >= TH_SPAM:
            decision = "SPAM"
            requires_review = False
            if composite_risk >= 0.85:
                risk_level = "CRITICAL"
            else:
                risk_level = "HIGH"

            # Construct transparent explanation
            reasons = []
            if p_nb >= TH_SPAM and p_bert >= TH_SPAM:
                reasons.append("Unanimous consensus: Both classical lexical analysis and deep transformer detected high spam probability.")
            elif p_bert >= TH_SPAM:
                reasons.append(f"BERT-Tiny detected strong contextual or telephony spam indicators ({p_bert*100:.1f}% risk).")
            elif p_nb >= TH_SPAM:
                reasons.append(f"Naive Bayes detected aggressive promotional or scam keywords ({p_nb*100:.1f}% risk).")

            explanation = " ".join(reasons)

        elif p_nb <= TH_HAM and p_bert <= TH_HAM:
            decision = "HAM"
            requires_review = False
            risk_level = "LOW"
            explanation = "Clean communication: Both models unanimously verified minimal spam indicators below the 10% threshold."

        else:
            decision = "SUSPICIOUS / REVIEW"
            requires_review = True
            risk_level = "MEDIUM"

            # Explain the conflict or boundary condition
            if abs(p_nb - p_bert) >= 0.40:
                explanation = (
                    f"Model conflict detected: Naive Bayes assessed {p_nb*100:.1f}% spam likelihood, "
                    f"while BERT-Tiny assessed {p_bert*100:.1f}%. This divergence often occurs when promotional "
                    "or phishing text lacks classic carrier dial codes, requiring human-in-the-loop triage."
                )
            else:
                explanation = (
                    f"Borderline confidence band: Model scores fall between {TH_HAM*100:.0f}% and {TH_SPAM*100:.0f}% "
                    "(Naive Bayes: {p_nb*100:.1f}%, BERT: {p_bert*100:.1f}%). Message has been queued for review."
                )

        return {
            "hybrid_decision": decision,
            "risk_score": composite_risk,
            "risk_level": risk_level,
            "requires_review": requires_review,
            "explanation": explanation,
            "thresholds": {
                "spam_threshold": TH_SPAM,
                "ham_threshold": TH_HAM
            }
        }
