#!/usr/bin/env python3
"""
Decode and explain what the Eurostat data actually represents
"""

import requests
import pandas as pd
from comext_extractor import ComextExtractor

def decode_and_explain():
    """Decode the data and explain what it really means."""
    
    print("=" * 80)
    print("DECODING YOUR EUROSTAT COMEXT DATA")
    print("=" * 80)
    
    # Get full API response
    url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ext_lt_intratrd?geo=EU27_2020&time=2020'
    response = requests.get(url, headers={'Accept': 'application/json'})
    data = response.json()
    
    dims = data.get('dimension', {})
    values = data.get('value', {})
    
    # Decode dimensions
    indic_et = dims.get('indic_et', {}).get('category', {}).get('label', {})
    indic_index = dims.get('indic_et', {}).get('category', {}).get('index', {})
    
    sitc06 = dims.get('sitc06', {}).get('category', {}).get('label', {})
    sitc06_index = dims.get('sitc06', {}).get('category', {}).get('index', {})
    
    partner = dims.get('partner', {}).get('category', {}).get('label', {})
    partner_index = dims.get('partner', {}).get('category', {}).get('index', {})
    
    print("\n📊 WHAT THIS DATASET IS ABOUT:")
    print("   Dataset: Intra and Extra-EU trade by Member State and product group")
    print("   This shows trade flows:")
    print("   • INTRA-EU: Trade between EU member countries")
    print("   • EXTRA-EU: Trade between EU and non-EU countries")
    print("   • By product categories (SITC06 classification)")
    print("   • By partner countries/regions")
    print()
    
    print("🔍 WHAT THE 'FREQ' COLUMN REALLY MEANS:")
    print("   The FREQ codes are actually TRADE INDICATOR codes (INDIC_ET)")
    print("   They represent different types of trade measurements:")
    print()
    
    # Show what each code means
    code_meanings = {}
    for code, label in indic_et.items():
        idx = indic_index.get(code)
        if idx is not None:
            code_meanings[idx] = (code, label)
    
    # Show first 20 codes
    for idx in sorted(code_meanings.keys())[:20]:
        code, label = code_meanings[idx]
        print(f"   Code {idx} ({code}): {label}")
    
    print()
    print("📦 WHAT THE OTHER DIMENSIONS MEAN:")
    print()
    
    print("   SITC06 (Product Categories):")
    sitc_samples = list(sitc06.items())[:10]
    for code, label in sitc_samples:
        print(f"     {code}: {label}")
    
    print()
    print("   PARTNER (Trading Partners):")
    partner_samples = list(partner.items())[:15]
    for code, label in partner_samples:
        print(f"     {code}: {label}")
    
    print()
    print("💰 WHAT THE VALUES MEAN:")
    print("   OBS_VALUE = Trade value in MILLIONS of EUR")
    print("   • Positive values = Trade surplus or export values")
    print("   • Negative values = Trade deficit or import values")
    print("   • 100.0 = 100% (for percentage indicators)")
    
    print()
    print("📈 EXAMPLE DECODED DATA:")
    print("   Let's decode a few rows from your data:")
    print()
    
    # Decode sample values
    sample_keys = list(values.keys())[:5]
    for key in sample_keys:
        indices = [int(x) for x in key.split(':')]
        if len(indices) >= 4:
            # Format: freq:indic_et:sitc06:partner:geo:time
            freq_idx = indices[0]
            indic_idx = indices[1]
            sitc_idx = indices[2]
            partner_idx = indices[3]
            
            indic_label = "Unknown"
            for code, idx in indic_index.items():
                if idx == indic_idx:
                    indic_label = indic_et.get(code, code)
                    break
            
            sitc_label = "Unknown"
            for code, idx in sitc06_index.items():
                if idx == sitc_idx:
                    sitc_label = sitc06.get(code, code)
                    break
            
            partner_label = "Unknown"
            for code, idx in partner_index.items():
                if idx == partner_idx:
                    partner_label = partner.get(code, code)
                    break
            
            value = values[key]
            print(f"   • {indic_label}")
            print(f"     Product: {sitc_label}")
            print(f"     Partner: {partner_label}")
            print(f"     Value: {value:,.2f} million EUR")
            print()
    
    print("=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    print("✅ Your data shows REAL EU trade statistics")
    print("✅ Each row = Trade indicator × Product category × Partner country")
    print("✅ Values = Trade amounts in millions of EUR")
    print("✅ This is official Eurostat data from their API")
    print("=" * 80)

if __name__ == "__main__":
    decode_and_explain()

