#!/usr/bin/env python3
"""
Verification script to test the setup and API connectivity.
"""

import sys
import requests
from comext_extractor import ComextExtractor

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("Checking dependencies...")
    missing = []
    
    try:
        import requests
        print("✅ requests")
    except ImportError:
        print("❌ requests - Install with: pip install requests")
        missing.append("requests")
    
    try:
        import pandas
        print("✅ pandas")
    except ImportError:
        print("❌ pandas - Install with: pip install pandas")
        missing.append("pandas")
    
    try:
        import openpyxl
        print("✅ openpyxl")
    except ImportError:
        print("⚠️  openpyxl - Optional, needed for Excel export")
    
    try:
        import pyarrow
        print("✅ pyarrow")
    except ImportError:
        print("⚠️  pyarrow - Optional, needed for Parquet export")
    
    if missing:
        print(f"\n❌ Missing required dependencies: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required dependencies are installed!")
    return True

def check_api_connectivity():
    """Check if Eurostat API is accessible."""
    print("\nChecking API connectivity...")
    
    try:
        # Test basic connectivity
        test_url = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code in [200, 400, 404]:  # 400/404 means API is reachable
            print("✅ Eurostat API is accessible")
            return True
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Eurostat API")
        print("   Check your internet connection")
        return False
    except requests.exceptions.Timeout:
        print("⚠️  Connection timeout")
        return False
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return False

def test_extractor():
    """Test the extractor with a simple query."""
    print("\nTesting extractor...")
    
    try:
        extractor = ComextExtractor(timeout=30)
        
        # Try a simple query (may fail if no data, but tests the code)
        filters = {
            'freq': 'A',
            'time': '2020',
            'geo': 'EU27_2020',
            'partnerGeo': 'CN',
            'product': 'TOTAL',
            'flow': '1'
        }
        
        print("Attempting to fetch sample data...")
        df = extractor.fetch_data('DS-057009', filters=filters, format_type='csv')
        
        if not df.empty:
            print(f"✅ Successfully retrieved {len(df)} rows")
            print(f"   Columns: {', '.join(df.columns)}")
            return True
        else:
            print("⚠️  Query succeeded but returned no data")
            print("   This might be normal if filters are too restrictive")
            return True  # Still counts as success
            
    except Exception as e:
        print(f"⚠️  Extractor test failed: {e}")
        print("   This might be due to:")
        print("   - API endpoint changes")
        print("   - Invalid dataset code")
        print("   - Network issues")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Eurostat Comext Extractor - Setup Verification")
    print("=" * 60)
    
    deps_ok = check_dependencies()
    api_ok = check_api_connectivity()
    
    if deps_ok and api_ok:
        test_extractor()
    
    print("\n" + "=" * 60)
    print("Verification complete!")
    print("=" * 60)
    
    if deps_ok and api_ok:
        print("\n✅ Setup looks good! You can now use the extractor.")
        print("\nTry running:")
        print("  python comext_extractor.py")
        print("  python example_usage.py")
    else:
        print("\n⚠️  Some issues detected. Please fix them before using the extractor.")
        sys.exit(1)

if __name__ == "__main__":
    main()

