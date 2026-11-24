import urllib.request
import json

messages = [
    "Hey, are we meeting tomorrow?",
    "Congratulations! You have won a free prize. Claim now!",
    "Your bank account is blocked. Verify your details.",
    "Please call me when you reach home.",
    "Free entry in a weekly competition. Text WIN to 87121."
]

print("=" * 60)
print("SPAMGUARD AI - PHASE 4 REAL INFERENCE VERIFICATION")
print("=" * 60)

for idx, msg in enumerate(messages, 1):
    payload = json.dumps({"message": msg, "model_preference": "hybrid"}).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/analyze",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"\n[{idx}] Message: \"{msg}\"")
        print(f"    • Hybrid Decision:  {res['hybrid_decision']}")
        print(f"    • Composite Score:  {res['risk_score'] * 100:.2f}%")
        print(f"    • Risk Level:       {res['risk_level']}")
        print(f"    • Requires Review:  {res['requires_review']}")
        print(f"    • Structural Flags: {len(res['threat_signals'])}")
        print(f"    • Preprocessed:     \"{res['preprocessed_tokens']}\"")
        print(f"    • Multi-Model Predictions:")
        for k, m in res['model_predictions'].items():
            print(f"        - {m['display_name']:<28}: {m['predicted_label']:<4} (p_spam={m['spam_probability']:.4f}, latency={m['latency_ms']}ms)")
