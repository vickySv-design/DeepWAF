// DeepWAF Browser Extension - Background Script
const DEEPWAF_API = 'http://127.0.0.1:5000/check_request';

console.log('[DeepWAF] Extension loaded');

// Whitelist for localhost and DeepWAF URLs
function isWhitelisted(url) {
  const whitelistPatterns = [
    'http://localhost',
    'http://127.0.0.1',
    'chrome://',
    'chrome-extension://',
    'edge://',
    'about:',
    'file://'
  ];
  
  return whitelistPatterns.some(pattern => url.startsWith(pattern));
}

// Monitor all navigation requests
if (chrome.webNavigation) {
  chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
    if (details.frameId === 0) { // Main frame only
      const url = details.url;
      
      // Skip whitelisted URLs (localhost, chrome://, etc.)
      if (isWhitelisted(url)) {
        console.log('[DeepWAF] Whitelisted URL (skipped):', url);
        return;
      }
      
      console.log('[DeepWAF] Checking URL:', url);
      
      // Check URL with DeepWAF
      try {
        const response = await fetch(DEEPWAF_API, {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({user_request: url})
        });
        
        const result = await response.json();
        
        // Determine if should block
        let shouldBlock = false;
        let detectionMethod = 'Signature Analysis';
        let threatType = 'Unknown';
        
        if (result.status === 'malicious') {
          shouldBlock = true;
          detectionMethod = 'Signature-Based Filter';
          threatType = 'SQL Injection / XSS Attack';
        } else if (result.status === 'obfuscated') {
          if (result.ml_verdict && result.ml_verdict.includes('Blocked')) {
            shouldBlock = true;
            detectionMethod = 'Character-Level CNN';
            threatType = 'Obfuscated Attack Pattern';
          }
        }
        
        if (shouldBlock) {
          // Block the request with detailed info
          const blockedUrl = chrome.runtime.getURL('blocked.html') + 
            '?url=' + encodeURIComponent(url) +
            '&method=' + encodeURIComponent(detectionMethod) +
            '&type=' + encodeURIComponent(threatType);
          
          chrome.tabs.update(details.tabId, { url: blockedUrl });
          
          console.log('[DeepWAF] BLOCKED:', url, '| Method:', detectionMethod);
        } else {
          console.log('[DeepWAF] ALLOWED:', url);
        }
      } catch (error) {
        console.error('[DeepWAF] Error checking URL:', error);
      }
    }
  });
  
  console.log('[DeepWAF] Browser protection active - Monitoring all URLs (localhost whitelisted)');
} else {
  console.error('[DeepWAF] webNavigation API not available');
}
