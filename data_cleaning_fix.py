"""
Quick fix script to test improved pipeline cleaning/standardization.

Run: cd backend && fraud_env\\Scripts\\activate && python data_cleaning_fix.py
"""

import pandas as pd
import numpy as np
from pipeline import clean_data, engineer_features, rule_based_detection, train_and_predict, add_fraud_type

# Load user CSV (replace with your file)
df = pd.read_csv('sample_transactions.csv')  # or your CSV

print("Raw data shape:", df.shape)
print("Amount col sample:", df['transaction_amount'].dtype if 'transaction_amount' in df else 'not found')

# Test improved logic (preserve amount numeric)
amount_candidates = ['transaction_amount', 'amount', 'amt']
amount_col = next((col for col in amount_candidates if col in df.columns), None)

if amount_col:
    df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')
    print(f"Preserved {amount_col} as numeric: {df[amount_col].dtype}")

# Run pipeline
clean_df, amount_col = clean_data(df.copy())
feat_df = engineer_features(clean_df, df.copy(), amount_col)
rule_df = rule_based_detection(feat_df)
ml_df, metrics = train_and_predict(rule_df)
final_df = add_fraud_type(ml_df)

print("\nPipeline Results:")
print(f"Total frauds: { (final_df['rule_flag'] == 1).sum() }")
print(f"ML F1: {metrics['f1_score']}")
print("\nFirst 5 frauds:")
print(final_df[final_df['rule_flag'] == 1][['transaction_id', amount_col, 'rule_flag', 'fraud_type']].head())

print("\nTest complete. Ready for production fix in pipeline.py?")

