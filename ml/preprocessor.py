"""
ml/preprocessor.py

Why this file exists:
This module provides minimal preprocessing and domain-specific feature extraction for incoming SMS messages.
- Preprocessing: Minimal lowercasing to retain character-level obfuscation like 'fr33', 'cl1ck', '$$$', 'W1N'.
- Feature Extraction: Calculates message length, digit counts, uppercase letter ratios, and special character ratios.
"""

import re
from typing import Dict, Any, List
import pandas as pd
import numpy as np


class SMSPreprocessor:
    """Preprocesses raw SMS text and computes statistical text features."""

    def __init__(self):
        pass

    @staticmethod
    def clean_text(text: str) -> str:
        """Minimal preprocessing preserving obfuscations: lowercases and strips whitespace."""
        if not isinstance(text, str):
            return ""
        return text.lower().strip()

    @staticmethod
    def extract_single_features(text: str) -> Dict[str, float]:
        """Extract statistical features from a single text message."""
        if not isinstance(text, str):
            text = ""

        char_len = len(text)
        if char_len == 0:
            return {
                "char_length": 0.0,
                "digit_count": 0.0,
                "upper_ratio": 0.0,
                "special_char_ratio": 0.0
            }

        digit_count = float(sum(c.isdigit() for c in text))
        upper_count = float(sum(c.isupper() for c in text))
        upper_ratio = upper_count / float(char_len)
        
        # Count non-alphanumeric and non-whitespace characters
        special_count = float(len(re.findall(r'[^a-zA-Z0-9\s]', text)))
        special_char_ratio = special_count / float(char_len)

        return {
            "char_length": float(char_len),
            "digit_count": digit_count,
            "upper_ratio": upper_ratio,
            "special_char_ratio": special_char_ratio
        }

    def extract_batch_features(self, messages: List[str]) -> pd.DataFrame:
        """Extract statistical features for a list of SMS messages."""
        rows = [self.extract_single_features(msg) for msg in messages]
        return pd.DataFrame(rows)
