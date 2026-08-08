"""
ml/feature_engineering.py

Why this file exists:
This module handles feature engineering for the unsupervised SMS drift monitoring pipeline.
- Uses Character N-Gram TF-IDF (analyzer="char", ngram_range=(3,5), max_features=5000)
- Applies TruncatedSVD (n_components=100) instead of PCA to operate efficiently on sparse matrices
- Combines reduced SVD features with scaled statistical features (length, digits count, uppercase ratio, special char ratio)
"""

from typing import Tuple, List, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from ml.preprocessor import SMSPreprocessor


class SMSFeaturePipeline:
    """Feature engineering pipeline combining Character TF-IDF, TruncatedSVD, and statistical metrics."""

    def __init__(
        self,
        ngram_range: Tuple[int, int] = (3, 5),
        max_features: int = 5000,
        n_components: int = 100,
        random_state: int = 42
    ):
        self.ngram_range = ngram_range
        self.max_features = max_features
        self.n_components = n_components
        self.random_state = random_state

        self.preprocessor = SMSPreprocessor()
        self.vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=self.ngram_range,
            max_features=self.max_features
        )
        self.svd = TruncatedSVD(
            n_components=self.n_components,
            random_state=self.random_state
        )
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit(self, raw_messages: List[str]) -> "SMSFeaturePipeline":
        """Fit TF-IDF vectorizer, TruncatedSVD, and StandardScaler on baseline normal traffic."""
        cleaned = [self.preprocessor.clean_text(msg) for msg in raw_messages]
        tfidf_mat = self.vectorizer.fit_transform(cleaned)
        
        # Fit TruncatedSVD on sparse TF-IDF matrix
        svd_mat = self.svd.fit_transform(tfidf_mat)

        # Extract and fit scaler on numerical statistical features
        stat_df = self.preprocessor.extract_batch_features(raw_messages)
        self.scaler.fit(stat_df.values)

        self.is_fitted = True
        return self

    def transform(self, raw_messages: List[str]) -> np.ndarray:
        """Transform raw messages into combined dense feature matrix."""
        if not self.is_fitted:
            raise ValueError("SMSFeaturePipeline is not fitted yet! Call fit() first.")

        cleaned = [self.preprocessor.clean_text(msg) for msg in raw_messages]
        tfidf_mat = self.vectorizer.transform(cleaned)
        svd_mat = self.svd.transform(tfidf_mat)

        stat_df = self.preprocessor.extract_batch_features(raw_messages)
        scaled_stat = self.scaler.transform(stat_df.values)

        # Concatenate SVD features and scaled statistical domain features
        combined = np.hstack([svd_mat, scaled_stat])
        return combined

    def fit_transform(self, raw_messages: List[str]) -> np.ndarray:
        """Fit pipeline and return transformed feature matrix."""
        self.fit(raw_messages)
        return self.transform(raw_messages)
