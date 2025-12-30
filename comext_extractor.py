#!/usr/bin/env python3
"""
Eurostat Comext Data Extractor
Automates data downloads from the Eurostat Comext (International Trade in Goods) database.
"""

import requests
import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, Optional, List
import argparse
import sys


class ComextExtractor:
    """Class to extract data from Eurostat Comext database."""
    
    BASE_URL_SDMX = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/"
    BASE_URL_REST = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the Comext extractor.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'ComextExtractor/1.0'
        })
    
    def fetch_data(
        self,
        dataset_code: str,
        filters: Optional[Dict[str, str]] = None,
        format_type: str = 'csv'
    ) -> pd.DataFrame:
        """
        Fetch data from Eurostat Comext database.
        
        Args:
            dataset_code: The code of the dataset to retrieve (e.g., 'DS-057009')
            filters: Dictionary of filters (e.g., {'freq': 'A', 'time': '2020'})
            format_type: Output format ('json' or 'csv', default: 'csv')
            
        Returns:
            pandas DataFrame containing the retrieved data
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the response cannot be parsed
        """
        # Try REST API first (more reliable for Eurostat)
        url_rest = f"{self.BASE_URL_REST}{dataset_code}"
        
        params = {}
        if filters:
            # Convert filters to REST API format
            for key, value in filters.items():
                params[key] = value
        
        try:
            # Try REST API with JSON format (most reliable)
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'ComextExtractor/1.0'
            }
            
            response = self.session.get(url_rest, params=params, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                # Parse REST API JSON response
                data = response.json()
                return self._parse_rest_api_response(data)
            
            # If REST API fails, try SDMX endpoint
            if response.status_code in [404, 406]:
                url_sdmx = f"{self.BASE_URL_SDMX}{dataset_code}/"
                headers_csv = {
                    'Accept': 'text/csv',
                    'User-Agent': 'ComextExtractor/1.0'
                }
                response = self.session.get(url_sdmx, params=params, headers=headers_csv, timeout=self.timeout)
                
                if response.status_code == 200:
                    from io import StringIO
                    df = pd.read_csv(StringIO(response.text))
                    df.columns = df.columns.str.strip().str.upper()
                    return df
            
            response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to fetch data from Eurostat API: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f"\nResponse status: {e.response.status_code}"
                try:
                    error_msg += f"\nResponse: {e.response.text[:200]}"
                except:
                    pass
            raise requests.exceptions.RequestException(error_msg)
    
    def _parse_rest_api_response(self, json_data: Dict) -> pd.DataFrame:
        """
        Parse REST API JSON response from Eurostat into a pandas DataFrame.
        
        Args:
            json_data: JSON response from the REST API
            
        Returns:
            pandas DataFrame
        """
        try:
            # REST API format: {"value": {...}, "dimension": {...}, "status": "..."}
            if 'value' not in json_data:
                raise ValueError("Invalid REST API response format")
            
            values = json_data['value']
            dimensions = json_data.get('dimension', {})
            ids = json_data.get('id', [])
            
            # Build rows
            rows = []
            for key, value in values.items():
                # Parse key (e.g., "0:0:0:0:0" represents dimension indices)
                indices = [int(idx) for idx in key.split(':')]
                
                row = {}
                # Map indices to dimension values
                for i, dim_id in enumerate(ids):
                    if i < len(indices) and dim_id in dimensions:
                        dim_values = dimensions[dim_id].get('category', {}).get('index', {})
                        # Reverse lookup to get label
                        for label, idx in dim_values.items():
                            if idx == indices[i]:
                                row[dim_id.upper()] = label
                                break
                        else:
                            # Fallback: use index directly
                            row[dim_id.upper()] = str(indices[i])
                
                row['OBS_VALUE'] = value
                rows.append(row)
            
            if not rows:
                raise ValueError("No data found in response")
            
            return pd.DataFrame(rows)
            
        except Exception as e:
            raise ValueError(f"Failed to parse REST API response: {str(e)}")
    
    def _parse_json_response(self, json_data: Dict) -> pd.DataFrame:
        """
        Parse JSON response from Eurostat API into a pandas DataFrame.
        
        Args:
            json_data: JSON response from the API
            
        Returns:
            pandas DataFrame
        """
        try:
            # Parse SDMX-JSON format
            if 'dataSets' not in json_data:
                raise ValueError("Invalid response format: missing 'dataSets'")
            
            data_set = json_data['dataSets'][0]
            structure = json_data.get('structure', {})
            
            # Extract dimensions
            dims = structure.get('dimensions', {})
            if 'observation' in dims:
                dimensions = dims['observation']
            elif 'series' in dims:
                dimensions = dims['series']
            else:
                dimensions = []
            
            dimension_names = [dim['id'] for dim in dimensions]
            
            # Extract observations
            observations = data_set.get('observations', {})
            if not observations:
                observations = data_set.get('series', {})
            
            # Build DataFrame
            rows = []
            for obs_key, obs_value in observations.items():
                # Parse observation key (indices for dimensions)
                try:
                    indices = [int(idx) for idx in obs_key.split(':')]
                except ValueError:
                    continue
                
                # Get dimension values
                row = {}
                for i, dim_name in enumerate(dimension_names):
                    if i < len(indices) and i < len(dimensions):
                        dim_values = dimensions[i].get('values', [])
                        if indices[i] < len(dim_values):
                            row[dim_name] = dim_values[indices[i]].get('id', '')
                
                # Add observation value
                if isinstance(obs_value, list) and len(obs_value) > 0:
                    row['OBS_VALUE'] = obs_value[0]
                elif isinstance(obs_value, dict):
                    row['OBS_VALUE'] = obs_value.get('value', obs_value)
                else:
                    row['OBS_VALUE'] = obs_value
                
                rows.append(row)
            
            if not rows:
                raise ValueError("No observations found in response")
            
            df = pd.DataFrame(rows)
            return df
            
        except (KeyError, IndexError, ValueError) as e:
            # Fallback: try CSV format instead
            print(f"Warning: JSON parsing failed ({str(e)}). Trying CSV format...")
            raise ValueError(f"Failed to parse JSON response: {str(e)}. Try using format='csv' instead.")
    
    def list_available_datasets(self, search_term: Optional[str] = None) -> List[Dict]:
        """
        List available datasets from Comext database.
        Note: This requires accessing the Eurostat data browser API.
        
        Args:
            search_term: Optional search term to filter datasets
            
        Returns:
            List of dataset dictionaries
        """
        # This is a placeholder - actual implementation would query Eurostat's dataset list API
        print("Note: To find available datasets, visit:")
        print("https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/database")
        return []
    
    def save_data(self, df: pd.DataFrame, output_path: str, format: str = 'csv'):
        """
        Save DataFrame to file.
        
        Args:
            df: DataFrame to save
            output_path: Output file path
            format: Output format ('csv', 'excel', 'json', 'parquet')
        """
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        if format == 'csv':
            df.to_csv(output_path, index=False)
        elif format == 'excel':
            df.to_excel(output_path, index=False)
        elif format == 'json':
            df.to_json(output_path, orient='records', indent=2)
        elif format == 'parquet':
            df.to_parquet(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")


def load_config(config_path: str) -> Dict:
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    """Main function to run the extractor."""
    parser = argparse.ArgumentParser(
        description='Extract data from Eurostat Comext database'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    parser.add_argument(
        '--dataset',
        type=str,
        help='Dataset code (overrides config file)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (overrides config file)'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['csv', 'excel', 'json', 'parquet'],
        default='csv',
        help='Output format (default: csv)'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    if os.path.exists(args.config):
        config = load_config(args.config)
    else:
        print(f"Warning: Config file {args.config} not found. Using defaults.")
        config = {}
    
    # Get parameters
    dataset_code = args.dataset or config.get('dataset_code', 'DS-057009')
    filters = config.get('filters', {})
    output_path = args.output or config.get('output_path', 'comext_data.csv')
    output_format = args.format or config.get('output_format', 'csv')
    
    print(f"Extracting data from Eurostat Comext...")
    print(f"Dataset: {dataset_code}")
    print(f"Filters: {filters}")
    print(f"Output: {output_path}")
    print("-" * 50)
    
    # Create extractor and fetch data
    extractor = ComextExtractor()
    
    try:
        df = extractor.fetch_data(dataset_code, filters)
        
        if df.empty:
            print("Warning: No data returned from the API.")
            return
        
        print(f"Successfully retrieved {len(df)} rows")
        print("\nFirst few rows:")
        print(df.head())
        print("\nDataFrame info:")
        print(df.info())
        
        # Save data
        extractor.save_data(df, output_path, output_format)
        print(f"\nData saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

