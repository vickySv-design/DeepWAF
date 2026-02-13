"""
DeepWAF - CNN Detection Test Script

Tests the Character-Level CNN model with various attack patterns
to verify detection accuracy.
"""

from src.hybrid_waf.utils.cnn_checker import check_cnn_prediction
from src.hybrid_waf.utils.signature_checker import check_signature

print("\n" + "="*60)
print("DeepWAF - Detection System Test")
print("="*60)

test_cases = [
    # Benign requests
    ("GET / HTTP/1.1", "Benign"),
    ("GET /products?category=electronics", "Benign"),
    ("POST /login HTTP/1.1", "Benign"),
    
    # SQL Injection (Signature)
    ("' OR '1'='1", "Malicious"),
    ("admin'--", "Malicious"),
    ("1' UNION SELECT * FROM users--", "Malicious"),
    
    # XSS (Signature)
    ("<script>alert('XSS')</script>", "Malicious"),
    ("<img src=x onerror=alert(1)>", "Malicious"),
    
    # Obfuscated (CNN)
    ("%27%20OR%20%271%27%3D%271", "Obfuscated"),
    ("\\x27\\x20OR\\x20\\x31\\x3D\\x31", "Obfuscated"),
    ("%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E", "Obfuscated"),
]

print("\nTesting Hybrid Detection System:\n")

correct = 0
total = len(test_cases)

for payload, expected in test_cases:
    # Step 1: Signature check
    sig_result = check_signature(payload)
    
    # Step 2: CNN check if obfuscated
    if sig_result == "obfuscated":
        cnn_result = check_cnn_prediction(payload)
        final_result = "Malicious" if cnn_result == 1 else "Benign"
        detection_method = "CNN"
    elif sig_result == "malicious":
        final_result = "Malicious"
        detection_method = "Signature"
    else:
        final_result = "Benign"
        detection_method = "Signature"
    
    # Check if correct
    is_correct = (
        (expected == "Benign" and final_result == "Benign") or
        (expected in ["Malicious", "Obfuscated"] and final_result == "Malicious")
    )
    
    if is_correct:
        correct += 1
        status = "[✓]"
    else:
        status = "[✗]"
    
    print(f"{status} {detection_method:<10} | Expected: {expected:<12} | Got: {final_result:<10} | {payload[:40]}")

print("\n" + "="*60)
print(f"Test Results: {correct}/{total} ({correct/total*100:.1f}% accuracy)")
print("="*60 + "\n")
