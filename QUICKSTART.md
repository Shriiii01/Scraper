# Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

### Option 1: Using the configuration file

1. Edit `config.json` with your desired parameters
2. Run:
```bash
python comext_extractor.py
```

### Option 2: Using command-line arguments

```bash
python comext_extractor.py --dataset DS-057009 --output my_data.csv
```

### Option 3: Using Python code

```python
from comext_extractor import ComextExtractor

extractor = ComextExtractor()
filters = {
    'freq': 'A',
    'time': '2020',
    'geo': 'EU27_2020',
    'partnerGeo': 'CN',
    'product': 'TOTAL',
    'flow': '1'
}

df = extractor.fetch_data('DS-057009', filters=filters)
extractor.save_data(df, 'output.csv')
```

## Common Filter Values

### Frequency (freq)
- `A` - Annual
- `M` - Monthly  
- `Q` - Quarterly

### Countries (geo, partnerGeo)
- `EU27_2020` - European Union (27 countries)
- `DE` - Germany
- `FR` - France
- `IT` - Italy
- `CN` - China
- `US` - United States
- `JP` - Japan
- `TOTAL` - All countries

### Trade Flow (flow)
- `1` - Imports
- `2` - Exports
- `3` - Net trade

### Products (product)
- `TOTAL` - All products
- HS codes: `01`, `02`, etc.
- CN codes: `0101`, `0102`, etc.

## Example Configurations

### Annual EU-China Trade
```json
{
  "dataset_code": "DS-057009",
  "filters": {
    "freq": "A",
    "time": "2020",
    "geo": "EU27_2020",
    "partnerGeo": "CN",
    "product": "TOTAL",
    "flow": "1"
  }
}
```

### Monthly Country Exports
```json
{
  "dataset_code": "DS-057009",
  "filters": {
    "freq": "M",
    "time": "2023-01",
    "geo": "DE",
    "partnerGeo": "US",
    "product": "TOTAL",
    "flow": "2"
  }
}
```

## Output Formats

Supported formats:
- `csv` - CSV file (default)
- `excel` - Excel file (.xlsx)
- `json` - JSON file
- `parquet` - Parquet file

Example:
```bash
python comext_extractor.py --format excel --output data.xlsx
```

## Troubleshooting

**No data returned?**
- Check if filters are too restrictive
- Verify dataset code is correct
- Try removing some filters

**API errors?**
- Check internet connection
- Verify API endpoint is accessible
- Try using CSV format: `format_type='csv'`

**Need help finding dataset codes?**
Visit: https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/database

