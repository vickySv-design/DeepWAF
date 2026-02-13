import numpy as np

MAX_LEN = 500
CHAR_DICT = {chr(i): i for i in range(256)}

def text_to_sequence(text: str, max_len: int = MAX_LEN) -> np.ndarray:
    """Convert text to character-level integer sequence"""
    sequence = [CHAR_DICT.get(c, 0) for c in text[:max_len]]
    if len(sequence) < max_len:
        sequence += [0] * (max_len - len(sequence))
    return np.array(sequence, dtype=np.int32)

def preprocess_request(user_input: str) -> np.ndarray:
    """Preprocess HTTP request for CNN model"""
    return text_to_sequence(user_input).reshape(1, -1)
