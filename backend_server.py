"""
Demo Backend Server - Protected by DeepWAF

This is a simple web application that will be protected by DeepWAF.
Run this on port 8080, and DeepWAF will proxy traffic to it.
"""

from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='backend_templates')

# Simple HTML template for the protected site
PROTECTED_SITE = """
<!DOCTYPE html>
<html>
<head>
    <title>Protected Website - Demo</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        .header { background: #27ae60; color: white; padding: 20px; border-radius: 5px; }
        .content { margin-top: 20px; padding: 20px; background: #ecf0f1; border-radius: 5px; }
        .info { background: #3498db; color: white; padding: 10px; margin: 10px 0; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Protected Website</h1>
        <p>This website is protected by DeepWAF</p>
    </div>
    <div class="content">
        <h2>Welcome to the Demo Backend</h2>
        <p>This is a sample web application protected by DeepWAF reverse proxy.</p>
        <p>All requests are automatically filtered before reaching this server.</p>
        
        <div class="info">
            <strong>Request Information:</strong><br>
            Method: {{ method }}<br>
            Path: {{ path }}<br>
            Query: {{ query }}
        </div>
        
        <h3>Test Links:</h3>
        <p><strong>✅ Safe Requests (Will Pass):</strong></p>
        <ul>
            <li><a href="/products?id=123">Normal Request</a></li>
            <li><a href="/search?q=laptop">Search Query</a></li>
            <li><a href="/api/users">API Endpoint</a></li>
        </ul>
        
        <p><strong>❌ Attack Attempts (Will Be Blocked):</strong></p>
        <ul style="color: #e74c3c;">
            <li><a href="/search?q=' OR '1'='1" style="color: #e74c3c;">SQL Injection Attack</a></li>
            <li><a href="/comment?text=<script>alert(1)</script>" style="color: #e74c3c;">XSS Attack</a></li>
            <li><a href="/search?q=%27%20OR%20%271%27%3D%271" style="color: #e74c3c;">Obfuscated SQLi</a></li>
        </ul>
        
        <p><em>Note: Malicious requests are blocked by DeepWAF and return 403 Forbidden with error details.</em></p>
    </div>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Handle all requests"""
    return render_template(
        'protected_site.html',
        method=request.method,
        path=request.path,
        query=request.query_string.decode()
    )

@app.route('/api/<endpoint>')
def api_handler(endpoint):
    """API endpoint handler"""
    return jsonify({
        "status": "success",
        "endpoint": endpoint,
        "message": "This API is protected by DeepWAF",
        "data": {"sample": "data"}
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Protected Backend Server Starting...")
    print("="*60)
    print("Running on: http://127.0.0.1:8080")
    print("Protected by: DeepWAF (running on port 5000)")
    print("="*60 + "\n")
    app.run(host='127.0.0.1', port=8080, debug=False)
