#!/usr/bin/env python3
"""
Simple example demonstrating how to use the Comext Extractor.
"""

from comext_extractor import ComextExtractor

# Initialize the extractor
extractor = ComextExtractor()

# Example 1: Get EU trade data for 2020
print("Example 1: EU Intra/Extra Trade (2020)")
print("-" * 50)

filters = {
    'geo': 'EU27_2020',    # European Union
    'time': '2020'         # Year 2020
}

try:
    df = extractor.fetch_data('ext_lt_intratrd', filters=filters)
    print(f"Retrieved {len(df)} rows")
    print("\nFirst few rows:")
    print(df.head())
    
    # Save to CSV
    extractor.save_data(df, 'eu_trade_2020.csv', format='csv')
    print("\nData saved to 'eu_trade_2020.csv'")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nNote: Make sure you have internet connection and valid API access.")

# Example 2: Get trade data for a specific country
print("\n\nExample 2: Germany Trade Data (2021)")
print("-" * 50)

filters2 = {
    'geo': 'DE',           # Germany
    'time': '2021'         # Year 2021
}

try:
    df2 = extractor.fetch_data('ext_lt_intratrd', filters=filters2)
    print(f"Retrieved {len(df2)} rows")
    print("\nFirst few rows:")
    print(df2.head())
    
    # Save to Excel
    extractor.save_data(df2, 'germany_trade_2021.xlsx', format='excel')
    print("\nData saved to 'germany_trade_2021.xlsx'")
    
except Exception as e:
    print(f"Error: {e}")

print("\n\nDone!")

