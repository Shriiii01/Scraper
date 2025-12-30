#!/usr/bin/env python3
"""
Test script for Comext Extractor
Demonstrates usage and creates sample output.
"""

from comext_extractor import ComextExtractor
import json

def test_basic_extraction():
    """Test basic data extraction."""
    print("=" * 60)
    print("Testing Eurostat Comext Data Extractor")
    print("=" * 60)
    
    extractor = ComextExtractor(timeout=60)
    
    # Test configuration
    test_configs = [
        {
            "name": "EU-China Annual Trade 2020",
            "dataset_code": "DS-057009",
            "filters": {
                "freq": "A",
                "time": "2020",
                "geo": "EU27_2020",
                "partnerGeo": "CN",
                "product": "TOTAL",
                "flow": "1"
            },
            "output": "sample_eu_china_2020.csv"
        },
        {
            "name": "Germany-US Monthly Trade (Jan 2023)",
            "dataset_code": "DS-057009",
            "filters": {
                "freq": "M",
                "time": "2023-01",
                "geo": "DE",
                "partnerGeo": "US",
                "product": "TOTAL",
                "flow": "2"
            },
            "output": "sample_germany_us_jan2023.csv"
        }
    ]
    
    for config in test_configs:
        print(f"\n{'='*60}")
        print(f"Test: {config['name']}")
        print(f"{'='*60}")
        print(f"Dataset: {config['dataset_code']}")
        print(f"Filters: {json.dumps(config['filters'], indent=2)}")
        
        try:
            df = extractor.fetch_data(
                config['dataset_code'],
                filters=config['filters'],
                format_type='csv'
            )
            
            if df.empty:
                print("⚠️  Warning: No data returned")
                continue
            
            print(f"\n✅ Successfully retrieved {len(df)} rows")
            print(f"\nColumn names: {list(df.columns)}")
            print(f"\nFirst 5 rows:")
            print(df.head().to_string())
            print(f"\nDataFrame shape: {df.shape}")
            
            # Save sample
            extractor.save_data(df, config['output'], format='csv')
            print(f"\n💾 Saved to: {config['output']}")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("\nNote: This might be due to:")
            print("  - API endpoint changes")
            print("  - Network connectivity issues")
            print("  - Invalid dataset code or filters")
            print("  - No data available for the specified filters")
            continue
    
    print(f"\n{'='*60}")
    print("Test completed!")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_basic_extraction()

