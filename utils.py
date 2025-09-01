# utils.py
import pandas as pd
from config import BRANDS

def save_csv(data, filepath):
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"✅ Saved {len(df)} rows to {filepath}")

def detect_brands(text):
    text_lower = text.lower()
    detected = {brand: (brand.lower() in text_lower) for brand in BRANDS}
    return detected
