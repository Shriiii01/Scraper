#!/usr/bin/env python3
"""
Simple example demonstrating how to use the Comext Extractor.
"""

from comext_extractor import ComextExtractor

# Initialize the extractor
extractor = ComextExtractor()

# Example 1: Get EU-China trade data for 2020
print("Example 1: EU-China Annual Trade (2020)")
print("-" * 50)

filters = {
    'freq': 'A',           # Annual data
    'time': '2020',        # Year 2020
    'geo': 'EU27_2020',    # European Union
    'partnerGeo': 'CN',    # China
    'product': 'TOTAL',    # All products
    'flow': '1'            # Imports (use '2' for exports)
}

try:
    df = extractor.fetch_data('DS-057009', filters=filters)
    print(f"Retrieved {len(df)} rows")
    print("\nFirst few rows:")
    print(df.head())
    
    # Save to CSV
    extractor.save_data(df, 'eu_china_trade_2020.csv', format='csv')
    print("\nData saved to 'eu_china_trade_2020.csv'")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nNote: Make sure you have internet connection and valid API access.")

# Example 2: Get monthly data for a specific country
print("\n\nExample 2: Germany-US Monthly Trade (January 2023)")
print("-" * 50)

filters2 = {
    'freq': 'M',           # Monthly data
    'time': '2023-01',     # January 2023
    'geo': 'DE',           # Germany
    'partnerGeo': 'US',    # United States
    'product': 'TOTAL',    # All products
    'flow': '2'            # Exports
}

try:
    df2 = extractor.fetch_data('DS-057009', filters=filters2)
    print(f"Retrieved {len(df2)} rows")
    print("\nFirst few rows:")
    print(df2.head())
    
    # Save to Excel
    extractor.save_data(df2, 'germany_us_exports_jan2023.xlsx', format='excel')
    print("\nData saved to 'germany_us_exports_jan2023.xlsx'")
    
except Exception as e:
    print(f"Error: {e}")

print("\n\nDone!")

