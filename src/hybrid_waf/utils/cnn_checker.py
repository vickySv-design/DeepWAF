"""
DeepWAF - CNN Inference Module (Cloud-Compatible)

Simplified version for cloud deployment without PyTorch.
Falls back to signature-only detection.
"""

import os

def check_cnn(user_input: str) -> dict:
    """
    Simplified CNN checker for cloud deployment.
    Returns signature-only detection result.
    """
    # In cloud deployment without PyTorch, return benign
    # Signature checker will handle actual detection
    return {
        'is_malicious': False,
        'confidence': 0.0,
        'method': 'Signature-Only (Cloud Mode)'
    }

def check_cnn_prediction(user_input: str, threshold: float = 0.5) -> int:
    """
    Compatibility function for cloud deployment.
    Returns 0 (benign) - signature checker handles detection.
    """
    return 0
