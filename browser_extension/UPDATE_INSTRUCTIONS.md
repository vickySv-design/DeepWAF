# Browser Extension Update Instructions

## The extension has been updated to whitelist localhost URLs!

### What Changed:
- Added whitelist for localhost (http://localhost and http://127.0.0.1)
- DeepWAF web interface URLs are now excluded from scanning
- You can now access http://127.0.0.1:5000 without being blocked

### How to Apply the Update:

1. **Open Chrome/Edge Extensions Page**
   - Go to `chrome://extensions/` (Chrome) or `edge://extensions/` (Edge)

2. **Reload the Extension**
   - Find "DeepWAF" extension in the list
   - Click the circular reload icon (🔄) on the extension card
   - OR toggle it off and back on

3. **Verify Update**
   - Click the DeepWAF extension icon in toolbar
   - You should see "Whitelisted: localhost, 127.0.0.1, chrome://, file://"

4. **Access DeepWAF**
   - Now you can visit: http://127.0.0.1:5000
   - Or: http://localhost:5000
   - These URLs will NOT be blocked by the extension

### Whitelisted URLs:
- `http://localhost` (all ports)
- `http://127.0.0.1` (all ports)
- `chrome://` (browser internal pages)
- `chrome-extension://` (extension pages)
- `edge://` (Edge browser pages)
- `about:` (browser about pages)
- `file://` (local files)

### Testing:
1. Visit http://127.0.0.1:5000 - Should load normally
2. Visit http://127.0.0.1:5000/home - Should load normally
3. Visit http://127.0.0.1:5000/model - Should load normally
4. Try a malicious URL like: http://example.com/?id=1' OR '1'='1 - Should be blocked

The extension will now only scan external websites, not your local DeepWAF application!
