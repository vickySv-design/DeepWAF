# DeepWAF Browser Extension - Installation Guide

## Overview
This browser extension monitors ALL URLs you visit and checks them against DeepWAF's detection system in real-time.

## Installation Steps

### 1. Start DeepWAF Server
```bash
python app.py
```
Make sure DeepWAF is running on http://127.0.0.1:5000

### 2. Install Extension in Chrome/Edge

1. Open Chrome/Edge browser
2. Go to: `chrome://extensions/` (or `edge://extensions/`)
3. Enable "Developer mode" (toggle in top right)
4. Click "Load unpacked"
5. Select the `browser_extension` folder
6. Extension is now installed!

### 3. Test Protection

Try visiting these URLs in your browser:

**SAFE URL** (will load normally):
```
https://www.google.com
https://www.github.com
```

**ATTACK URL** (will be blocked):
```
http://example.com/search?q=' OR '1'='1
http://example.com/page?id=<script>alert(1)</script>
```

## How It Works

1. **URL Monitoring**: Extension intercepts all navigation requests
2. **DeepWAF Analysis**: Sends URL to DeepWAF API for analysis
3. **Real-Time Blocking**: If malicious, redirects to blocked page
4. **Logging**: All detections logged in DeepWAF dashboard

## Features

- ✅ Monitors ALL websites you visit
- ✅ Real-time threat detection
- ✅ Character-Level CNN analysis
- ✅ Signature-based filtering
- ✅ Visual blocked page
- ✅ No configuration needed

## Note

This is a demonstration extension for academic purposes. In production:
- Extension would need proper signing
- API would use HTTPS
- More sophisticated blocking mechanisms
- User whitelist/blacklist options
