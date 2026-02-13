from flask import Blueprint, request, jsonify
from src.hybrid_waf.utils.signature_checker import check_signature
from src.hybrid_waf.utils.cnn_checker import check_cnn_prediction
import logging
import requests

# Backend server configuration
BACKEND_URL = "http://127.0.0.1:8080"

# Create a dedicated logger for WAF detections
waf_logger = logging.getLogger('waf_detections')
waf_logger.setLevel(logging.INFO)

# Create file handler
fh = logging.FileHandler('logs/detections.log')
fh.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)

# Add the handler to the logger
waf_logger.addHandler(fh)

proxy_bp = Blueprint('proxy', __name__)

# Reverse Proxy Route - Intercepts ALL traffic
@proxy_bp.route('/protected', defaults={'path': ''})
@proxy_bp.route('/protected/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def reverse_proxy(path):
    """Reverse proxy that filters all requests through DeepWAF"""
    
    # Build full request URL
    full_path = request.full_path if request.query_string else request.path
    request_url = full_path.replace('/protected', '', 1)
    
    # Analyze request for threats (include query string in analysis)
    analysis_input = request_url
    if '?' not in analysis_input and request.query_string:
        analysis_input += f"?{request.query_string.decode()}"
    
    # Step 1: Signature check
    signature_result = check_signature(analysis_input)
    
    if signature_result == "malicious":
        waf_logger.info(f"{analysis_input} - BLOCKED(signature)")
        return jsonify({
            "error": "Access Denied",
            "message": "Malicious pattern detected by DeepWAF",
            "blocked_by": "Signature Filter"
        }), 403
    
    # Step 2: CNN check for obfuscated
    if signature_result == "obfuscated":
        prediction = check_cnn_prediction(analysis_input)
        if prediction == 1:
            waf_logger.info(f"{analysis_input} - BLOCKED(CNN)")
            return jsonify({
                "error": "Access Denied",
                "message": "Suspicious pattern detected by DeepWAF CNN",
                "blocked_by": "Character-Level CNN"
            }), 403
    
    # Request is safe - forward to backend
    waf_logger.info(f"{analysis_input} - ALLOWED")
    
    try:
        # Forward request to backend
        backend_url = f"{BACKEND_URL}{request_url}"
        
        if request.method == 'GET':
            resp = requests.get(backend_url, params=request.args, timeout=5)
        elif request.method == 'POST':
            resp = requests.post(backend_url, json=request.get_json(), timeout=5)
        else:
            resp = requests.request(request.method, backend_url, timeout=5)
        
        return resp.content, resp.status_code, dict(resp.headers)
    
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Backend Unavailable",
            "message": "Protected backend server is not running. Start backend_server.py first."
        }), 503
    except Exception as e:
        return jsonify({"error": "Proxy Error", "message": str(e)}), 500

# Manual Testing API (original functionality)
@proxy_bp.route('/check_request', methods=['POST'])
def check_request():
    data = request.get_json()
    
    user_input = data.get("user_request", "")
    uri = data.get("uri", user_input)
    get_data = data.get("get_data", "")
    post_data = data.get("post_data", "")
    
    # --- Step 1: Signature-Based Detection ---
    signature_result = check_signature(user_input)
    
    if signature_result == "valid":
        waf_logger.info(f"{user_input} - valid")
        return jsonify({
            "status": "valid",
            "message": "Request validated successfully. No threats detected."
        })

    if signature_result == "malicious":
        waf_logger.info(f"{user_input} - malicious(signature)")
        return jsonify({
            "status": "malicious",
            "message": "Malicious pattern detected. Request blocked by signature-based filter."
        })
    
    # --- Step 2: Character-Level CNN Detection (Only for obfuscated requests) ---
    if signature_result == "obfuscated":
        prediction = check_cnn_prediction(user_input)
        
        final_status = "malicious" if prediction == 1 else "valid"
        
        waf_logger.info(f"{user_input} - malicious(CNN)" if prediction == 1 else f"{user_input} - valid")
            
        return jsonify({
            "status": "obfuscated",
            "ml_verdict": (
                "Threat confirmed - Request blocked by CNN" 
                if final_status == "malicious" 
                else "CNN analysis complete - Request verified safe"
            ),
            "message": "Suspicious pattern detected - Character-Level CNN analysis performed",
            "detection_method": "Character-Level Convolutional Neural Network"
        })