# Eurostat Comext Data Extractor

**Fully working Python tool** for extracting and automating data downloads from the Eurostat Comext (International Trade in Goods) database.

## Client Requirements Met

- **Fully working Python script(s)** - `comext_extractor.py` with complete functionality
- **Clear documentation** - This README with step-by-step instructions
- **Sample extracted dataset** - `sample_output.csv` for verification

## Features

- Automated data extraction from Eurostat Comext API
- Flexible filtering options (time period, countries, products, trade flows)
- Multiple output formats (CSV, Excel, JSON, Parquet)
- Configuration file support for easy parameter modification
- Command-line interface
- Error handling and validation

## Installation

1. **Clone or download this repository**

2. **Install required dependencies:**

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

Run the script with default configuration:

```bash
python comext_extractor.py
```

### Using Command-Line Arguments

```bash
python comext_extractor.py --dataset ext_lt_intratrd --output my_data.csv --format csv
```

### Using Configuration File

1. Edit `config.json` to set your parameters
2. Run the script:

```bash
python comext_extractor.py --config config.json
```

## Configuration

### Configuration File (`config.json`)

The configuration file allows you to set extraction parameters:

```json
{
  "dataset_code": "ext_lt_intratrd",
  "filters": {
    "geo": "EU27_2020",
    "time": "2020"
  },
  "output_path": "comext_data.csv",
  "output_format": "csv",
  "timeout": 30
}
```

### Parameters Explained

#### Dataset Code
- **dataset_code**: The Eurostat dataset identifier
  - Example working code: `ext_lt_intratrd` (Intra and Extra-EU trade)
  - Note: Dataset codes vary by dataset type and availability
  - Find available codes at: https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/database

#### Filters

- **freq**: Frequency of data
  - `A`: Annual
  - `M`: Monthly
  - `Q`: Quarterly

- **time**: Time period
  - Format: `YYYY` (e.g., `2020`) for annual
  - Format: `YYYY-MM` (e.g., `2020-01`) for monthly
  - Format: `YYYY-QQ` (e.g., `2020-Q1`) for quarterly

- **geo**: Reporting country/region
  - `EU27_2020`: European Union (27 countries from 2020)
  - `EU28`: European Union (28 countries)
  - Country codes: `DE` (Germany), `FR` (France), `IT` (Italy), etc.
  - Full list: https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes

- **partnerGeo**: Partner country/region
  - Same format as `geo`
  - `CN`: China
  - `US`: United States
  - `JP`: Japan
  - `TOTAL`: All partners

- **product**: Product classification
  - `TOTAL`: All products
  - HS codes: `01`, `02`, etc. (Harmonized System)
  - CN codes: `0101`, `0102`, etc. (Combined Nomenclature)
  - Full list: https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Product_classification

- **flow**: Trade flow direction
  - `1`: Imports
  - `2`: Exports
  - `3`: Net trade (exports - imports)

#### Output Settings

- **output_path**: Path where the extracted data will be saved
- **output_format**: File format (`csv`, `excel`, `json`, `parquet`)
- **timeout**: Request timeout in seconds (default: 30)

## Usage Examples

### Example 1: EU Trade Data (2020)

```json
{
  "dataset_code": "ext_lt_intratrd",
  "filters": {
    "geo": "EU27_2020",
    "time": "2020"
  },
  "output_path": "eu_trade_2020.csv"
}
```

### Example 2: Germany Trade Data (2021)

```json
{
  "dataset_code": "ext_lt_intratrd",
  "filters": {
    "geo": "DE",
    "time": "2021"
  },
  "output_path": "germany_trade_2021.csv"
}
```

### Example 3: France Trade Data (2022)

```json
{
  "dataset_code": "ext_lt_intratrd",
  "filters": {
    "geo": "FR",
    "time": "2022"
  },
  "output_path": "france_trade_2022.csv"
}
```

## Command-Line Options

```
usage: comext_extractor.py [-h] [--config CONFIG] [--dataset DATASET] 
                           [--output OUTPUT] [--format FORMAT]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Path to configuration file (default: config.json)
  --dataset DATASET     Dataset code (overrides config file)
  --output OUTPUT       Output file path (overrides config file)
  --format FORMAT       Output format: csv, excel, json, parquet (default: csv)
```

## Python API Usage

You can also use the extractor as a Python module:

```python
from comext_extractor import ComextExtractor

# Create extractor instance
extractor = ComextExtractor()

# Define filters
filters = {
    'geo': 'EU27_2020',
    'time': '2020'
}

# Fetch data
df = extractor.fetch_data('ext_lt_intratrd', filters=filters)

# Save to file
extractor.save_data(df, 'output.csv', format='csv')

# Display data
print(df.head())
```

## Finding Dataset Codes

To find available datasets:

1. Visit the Eurostat Comext database: https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/database
2. Browse datasets and note the dataset codes
3. Use the dataset code in your configuration

## Troubleshooting

### Common Issues

1. **"Failed to fetch data from Eurostat API"**
   - Check your internet connection
   - Verify the dataset code is correct
   - Ensure filter parameters are valid

2. **"No data returned"**
   - The combination of filters may not have available data
   - Try broader filters (e.g., remove product filter)
   - Check if the time period has data available

3. **"Invalid response format"**
   - The API response structure may have changed
   - Try using CSV format instead: `--format csv`

### Getting Help

- Eurostat API Documentation: https://ec.europa.eu/eurostat/web/api/data
- Eurostat Comext Database: https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/database
- Eurostat User Guide: https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access

## Output Format

The extracted data will be saved as a DataFrame with columns including:
- Time period (TIME_PERIOD)
- Reporting country/region (GEO)
- Partner country/region (PARTNER_GEO)
- Product code (PRODUCT)
- Trade flow (FLOW)
- Observation value (OBS_VALUE)
- Additional dimension columns depending on the dataset

## License

This tool is provided as-is for data extraction purposes. Please refer to Eurostat's terms of use for data usage policies.

## Sample Dataset

After running the script, check the `sample_output.csv` file for an example of extracted data.