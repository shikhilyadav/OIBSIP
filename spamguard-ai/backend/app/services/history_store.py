"""
In-Memory Session Scan History Store
Provides secure, non-persistent session history with filtering, searching, and pagination.
"""

import time
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class HistoryStore:
    _instance = None

    def __init__(self, max_size: int = 500):
        self.max_size = max_size
        self._history: List[Dict[str, Any]] = []
        self._preseed_initial_data()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _preseed_initial_data(self):
        """Pre-seeds realistic initial inspection items for UI demonstration."""
        seeds = [
            {
                "message": "WINNER!! As a valued network customer you have been selected to receive a £900 prize reward! To claim call 09061701461",
                "decision": "SPAM",
                "risk_score": 0.9082,
                "risk_level": "CRITICAL",
                "model_used": "hybrid",
                "requires_review": False,
                "threat_count": 3
            },
            {
                "message": "Hey are we having lunch together today around 1pm?",
                "decision": "HAM",
                "risk_score": 0.0412,
                "risk_level": "LOW",
                "model_used": "hybrid",
                "requires_review": False,
                "threat_count": 0
            },
            {
                "message": "Your bank account is blocked. Verify your details.",
                "decision": "SUSPICIOUS / REVIEW",
                "risk_score": 0.5284,
                "risk_level": "MEDIUM",
                "model_used": "hybrid",
                "requires_review": True,
                "threat_count": 1
            },
            {
                "message": "Free entry in 2 a weekly competition to win FA Cup final tickets. Text FA to 87121",
                "decision": "SPAM",
                "risk_score": 0.8875,
                "risk_level": "HIGH",
                "model_used": "hybrid",
                "requires_review": False,
                "threat_count": 2
            },
            {
                "message": "Please call me when you reach home safely, mom is asking.",
                "decision": "HAM",
                "risk_score": 0.0521,
                "risk_level": "LOW",
                "model_used": "hybrid",
                "requires_review": False,
                "threat_count": 0
            }
        ]

        now = datetime.now(timezone.utc)
        for i, item in enumerate(seeds):
            ts = now.timestamp() - (len(seeds) - i) * 180
            dt = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            self._history.append({
                "id": str(uuid.uuid4())[:8],
                "timestamp": dt,
                "message_preview": item["message"][:65] + "..." if len(item["message"]) > 65 else item["message"],
                "full_message": item["message"],
                "decision": item["decision"],
                "risk_score": item["risk_score"],
                "risk_level": item["risk_level"],
                "model_used": item["model_used"],
                "requires_review": item["requires_review"],
                "threat_count": item["threat_count"]
            })

    def add_entry(self, entry: Dict[str, Any]):
        self._history.insert(0, entry)
        if len(self._history) > self.max_size:
            self._history.pop()

    def get_entries(
        self,
        decision_filter: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        results = self._history

        if decision_filter and decision_filter.upper() != "ALL":
            results = [e for e in results if e["decision"].upper() == decision_filter.upper()]

        if search_query:
            q = search_query.lower()
            results = [e for e in results if q in e["full_message"].lower()]

        total = len(results)
        paged = results[offset : offset + limit]
        return {
            "total_records": total,
            "items": paged
        }

    def clear(self):
        self._history = []

    def get_counts(self) -> Dict[str, int]:
        total = len(self._history)
        spam = sum(1 for e in self._history if e["decision"] == "SPAM")
        ham = sum(1 for e in self._history if e["decision"] == "HAM")
        review = sum(1 for e in self._history if "REVIEW" in e["decision"])
        return {
            "total_scans": total,
            "spam_detected": spam,
            "ham_detected": ham,
            "review_queue": review
        }
