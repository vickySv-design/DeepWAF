"""
DeepWAF - CNN Inference Module

Loads trained Character-Level 1D-CNN model and performs
threat detection on HTTP requests.

Input: ASCII character sequences (max 500 chars)
Output: Binary classification (0=benign, 1=malicious)
"""

import torch
import torch.nn as nn
import numpy as np
import os

MAX_LEN = 500
VOCAB_SIZE = 256

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

MODEL_PATH = "src/hybrid_waf/models/cnn_model.pth"

# Load model
try:
    cnn_model = CharCNN()
    if os.path.exists(MODEL_PATH):
        cnn_model.load_state_dict(torch.load(MODEL_PATH, weights_only=True))
        cnn_model.eval()
        print("[OK] CNN model loaded successfully")
    else:
        print("[WARNING] Model file not found. Run train_cnn.py first")
        cnn_model = None
except Exception as e:
    print(f"[ERROR] Could not load CNN model: {e}")
    cnn_model = None

def text_to_sequence(text, max_len=MAX_LEN):
    """Convert text to character-level sequence"""
    sequence = [ord(c) if ord(c) < 256 else 0 for c in text[:max_len]]
    if len(sequence) < max_len:
        sequence += [0] * (max_len - len(sequence))
    return sequence

def check_cnn_prediction(user_input: str, threshold: float = 0.5) -> int:
    """
    Uses Character-Level CNN to detect malicious requests.
    Returns 1 for malicious, 0 for benign.
    """
    if cnn_model is None:
        print("[WARNING] CNN model not available")
        return 0
    
    sequence = text_to_sequence(user_input)
    X = torch.tensor([sequence], dtype=torch.long)
    
    with torch.no_grad():
        prediction = cnn_model(X).item()
    
    return 1 if prediction >= threshold else 0
