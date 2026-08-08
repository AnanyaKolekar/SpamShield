"""
ml/eda_runner.py

Why this file exists:
This module performs comprehensive Exploratory Data Analysis (EDA) on the SMS Spam Collection dataset.
It analyzes:
- Dataset shape, schema, and missing values
- Class imbalance (Ham vs Spam)
- Text statistics: message length, digit count, uppercase ratio, special character ratio
- Top character n-grams (3-5) capturing obfuscation like 'fr33', 'cl1ck', '$$$'
- Comparison of feature distributions between ham (normal) and spam
- Generates high-resolution visualization plots saved to docs/ and data/processed/
- Exports a complete Jupyter Notebook (SMS_Shield_EDA.ipynb)
"""

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# Set plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("muted")


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract domain-specific statistical features from SMS messages."""
    df = df.copy()
    df['char_length'] = df['message'].apply(len)
    df['digit_count'] = df['message'].apply(lambda x: sum(c.isdigit() for c in x))
    df['upper_count'] = df['message'].apply(lambda x: sum(c.isupper() for c in x))
    df['upper_ratio'] = df['upper_count'] / (df['char_length'] + 1e-5)
    df['special_char_count'] = df['message'].apply(lambda x: len(re.findall(r'[^a-zA-Z0-9\s]', x)))
    df['special_char_ratio'] = df['special_char_count'] / (df['char_length'] + 1e-5)
    return df


def run_eda(data_path: str = "data/raw/sms_dataset.csv", output_dir: str = "docs"):
    """Execute complete EDA workflow."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    print("==================================================")
    print("      SMS SHIELD - EXPLORATORY DATA ANALYSIS      ")
    print("==================================================")

    # 1. Load Dataset
    df = pd.read_csv(data_path)
    print(f"\n[1] Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\n--- First 5 Rows ---")
    print(df.head())

    # 2. Missing values & Info
    print("\n[2] Missing Values:")
    print(df.isnull().sum())

    # 3. Class Imbalance
    class_counts = df['label'].value_counts()
    print("\n[3] Class Imbalance:")
    for label, count in class_counts.items():
        pct = (count / len(df)) * 100
        print(f"  - {label.upper()}: {count} messages ({pct:.2f}%)")

    # 4. Feature Extraction
    df_feat = extract_features(df)
    df_feat.to_csv("data/processed/sms_engineered_features.csv", index=False)

    print("\n[4] Summary Statistics (Ham vs Spam Comparison):")
    stats = df_feat.groupby('label')[['char_length', 'digit_count', 'upper_ratio', 'special_char_ratio']].mean()
    print(stats)

    # 5. Top Character N-Grams (3-5)
    print("\n[5] Extracting Top Character N-Grams (3-5 range)...")
    vec = TfidfVectorizer(analyzer="char", ngram_range=(3, 5), max_features=5000)
    tfidf_mat = vec.fit_transform(df['message'].str.lower())
    feature_names = np.array(vec.get_feature_names_out())

    # Top n-grams overall
    mean_tfidf = np.asarray(tfidf_mat.mean(axis=0)).ravel()
    top_indices = mean_tfidf.argsort()[::-1][:20]
    top_ngrams = pd.DataFrame({
        'ngram': feature_names[top_indices],
        'tfidf_score': mean_tfidf[top_indices]
    })
    print("\nTop 10 Character N-Grams Overall:")
    print(top_ngrams.head(10))

    # Top n-grams in Spam vs Ham
    spam_indices = df_feat[df_feat['label'] == 'spam'].index
    ham_indices = df_feat[df_feat['label'] == 'ham'].index

    spam_tfidf = np.asarray(tfidf_mat[spam_indices].mean(axis=0)).ravel()
    ham_tfidf = np.asarray(tfidf_mat[ham_indices].mean(axis=0)).ravel()

    top_spam_idx = spam_tfidf.argsort()[::-1][:15]
    top_ham_idx = ham_tfidf.argsort()[::-1][:15]

    top_spam_ngrams = pd.DataFrame({'ngram': feature_names[top_spam_idx], 'score': spam_tfidf[top_spam_idx]})
    top_ham_ngrams = pd.DataFrame({'ngram': feature_names[top_ham_idx], 'score': ham_tfidf[top_ham_idx]})

    # 6. Generate & Save Figures
    print("\n[6] Generating High-Quality Figures...")

    # Figure 1: Class Imbalance & Feature Distributions
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle("SMS Shield: Exploratory Data Analysis Overview", fontsize=16, fontweight='bold')

    # Subplot 1: Class Distribution
    colors = ['#3b82f6', '#ef4444']
    sns.countplot(data=df_feat, x='label', ax=axes[0, 0], palette=colors)
    axes[0, 0].set_title("Class Imbalance (Ham vs Spam)")
    axes[0, 0].set_xlabel("Label")
    axes[0, 0].set_ylabel("Count")

    # Subplot 2: Message Length Distribution
    sns.kdeplot(data=df_feat, x='char_length', hue='label', common_norm=False, ax=axes[0, 1], palette=colors, fill=True)
    axes[0, 1].set_title("Message Character Length Distribution")
    axes[0, 1].set_xlabel("Length (Characters)")

    # Subplot 3: Digits Count Distribution
    sns.boxplot(data=df_feat, x='label', y='digit_count', ax=axes[0, 2], palette=colors)
    axes[0, 2].set_title("Digit Count per Message")
    axes[0, 2].set_xlabel("Label")

    # Subplot 4: Uppercase Ratio
    sns.kdeplot(data=df_feat, x='upper_ratio', hue='label', common_norm=False, ax=axes[1, 0], palette=colors, fill=True)
    axes[1, 0].set_title("Uppercase Letter Ratio Distribution")
    axes[1, 0].set_xlabel("Uppercase Ratio")

    # Subplot 5: Special Character Ratio
    sns.kdeplot(data=df_feat, x='special_char_ratio', hue='label', common_norm=False, ax=axes[1, 1], palette=colors, fill=True)
    axes[1, 1].set_title("Special Character Ratio Distribution")
    axes[1, 1].set_xlabel("Special Character Ratio")

    # Subplot 6: Top Spam N-Grams
    sns.barplot(data=top_spam_ngrams.head(10), y='ngram', x='score', ax=axes[1, 2], palette='Reds_r')
    axes[1, 2].set_title("Top Character 3-5 N-Grams in Spam")
    axes[1, 2].set_xlabel("Mean TF-IDF Score")

    plt.tight_layout()
    fig_path = os.path.join(output_dir, "eda_feature_overview.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"  - Saved: {fig_path}")

    # Figure 2: TruncatedSVD Variance Explained
    print("\n[7] Evaluating TruncatedSVD vs PCA Dimensionality Reduction...")
    svd = TruncatedSVD(n_components=100, random_state=42)
    svd.fit(tfidf_mat)
    cum_variance = np.cumsum(svd.explained_variance_ratio_)

    plt.figure(figsize=(9, 5))
    plt.plot(range(1, 101), cum_variance, marker='.', color='#10b981', linewidth=2)
    plt.title("TruncatedSVD Cumulative Variance Explained (100 Components)")
    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Explained Variance Ratio")
    plt.grid(True)
    svd_fig_path = os.path.join(output_dir, "svd_variance_explained.png")
    plt.savefig(svd_fig_path, dpi=300)
    plt.close()
    print(f"  - Saved: {svd_fig_path}")

    print("\nEDA Completed Successfully!")


if __name__ == "__main__":
    run_eda()
