#!/usr/bin/env python3
"""
Download California Population Data from US Census API
====================================================

This script downloads population data for California counties from the US Census API.
The data includes population counts, density, and demographics for years 2000-2024.

Data Source: US Census Bureau API
API Documentation: https://www.census.gov/data/developers/data-sets.html

Author: Tara Tavafi
Date: January 2025
"""

import requests
import pandas as pd
import json
import os
from pathlib import Path
import time

def setup_directories():
    """Create necessary directories for population data"""
    data_dir = Path("data/raw/population")
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_california_counties():
    """Get list of California county FIPS codes"""
    # California state FIPS code is 06
    # We'll get all counties in California
    california_counties = {
        'Alameda': '001', 'Alpine': '003', 'Amador': '005', 'Butte': '007',
        'Calaveras': '009', 'Colusa': '011', 'Contra Costa': '013', 'Del Norte': '015',
        'El Dorado': '017', 'Fresno': '019', 'Glenn': '021', 'Humboldt': '023',
        'Imperial': '025', 'Inyo': '027', 'Kern': '029', 'Kings': '031',
        'Lake': '033', 'Lassen': '035', 'Los Angeles': '037', 'Madera': '039',
        'Marin': '041', 'Mariposa': '043', 'Mendocino': '045', 'Merced': '047',
        'Modoc': '049', 'Mono': '051', 'Monterey': '053', 'Napa': '055',
        'Nevada': '057', 'Orange': '059', 'Placer': '061', 'Plumas': '063',
        'Riverside': '065', 'Sacramento': '067', 'San Benito': '069', 'San Bernardino': '071',
        'San Diego': '073', 'San Francisco': '075', 'San Joaquin': '077', 'San Luis Obispo': '079',
        'San Mateo': '081', 'Santa Barbara': '083', 'Santa Clara': '085', 'Santa Cruz': '087',
        'Shasta': '089', 'Sierra': '091', 'Siskiyou': '093', 'Solano': '095',
        'Sonoma': '097', 'Stanislaus': '099', 'Sutter': '101', 'Tehama': '103',
        'Trinity': '105', 'Tulare': '107', 'Tuolumne': '109', 'Ventura': '111',
        'Yolo': '113', 'Yuba': '115'
    }
    return california_counties

def download_census_data(year, data_dir):
    """Download population data for a specific year"""
    print(f"Downloading population data for {year}...")
    
    # Census API endpoint for population data
    # Using American Community Survey (ACS) 5-Year estimates for more recent years
    if year >= 2010:
        # Use ACS 5-Year estimates for 2010+
        base_url = "https://api.census.gov/data/2022/acs/acs5"
        variables = "B01003_001E,B01001_002E,B01001_026E"  # Total population, Male, Female
        dataset = "acs/acs5"
    else:
        # Use Decennial Census for 2000 and 2010
        base_url = f"https://api.census.gov/data/{year}/dec/pl"
        variables = "P001001,P002002,P002026"  # Total population, Male, Female
        dataset = f"{year}/dec/pl"
    
    # Build the API request
    url = f"{base_url}"
    
    params = {
        'get': variables,
        'for': 'county:*',
        'in': 'state:06',  # California state FIPS code
        'key': os.getenv('CENSUS_API_KEY', '')  # Optional API key
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Convert to DataFrame
        if year >= 2010:
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df.rename(columns={
                'B01003_001E': 'total_population',
                'B01001_002E': 'male_population', 
                'B01001_026E': 'female_population',
                'state': 'state_fips',
                'county': 'county_fips'
            })
        else:
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df.rename(columns={
                'P001001': 'total_population',
                'P002002': 'male_population',
                'P002026': 'female_population',
                'state': 'state_fips',
                'county': 'county_fips'
            })
        
        # Add year column
        df['year'] = year
        
        # Convert population columns to numeric
        population_cols = ['total_population', 'male_population', 'female_population']
        for col in population_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Add county names
        california_counties = get_california_counties()
        df['county_name'] = df['county_fips'].map({v: k for k, v in california_counties.items()})
        
        # Save to CSV
        filename = data_dir / f"california_population_{year}.csv"
        df.to_csv(filename, index=False)
        
        print(f"✅ Saved {len(df)} counties to {filename}")
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading data for {year}: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error for {year}: {e}")
        return None

def download_all_population_data():
    """Download population data for all years 2000-2024"""
    print("🌍 Downloading California Population Data from US Census API")
    print("=" * 60)
    
    # Setup directories
    data_dir = setup_directories()
    
    # Years to download (focusing on key years to avoid rate limits)
    years = [2000, 2010, 2015, 2020, 2022, 2024]
    
    all_data = []
    
    for year in years:
        df = download_census_data(year, data_dir)
        if df is not None:
            all_data.append(df)
        
        # Be respectful to the API
        time.sleep(1)
    
    # Combine all years into one dataset
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Save combined dataset
        combined_filename = data_dir / "california_population_combined.csv"
        combined_df.to_csv(combined_filename, index=False)
        
        print(f"\n✅ Combined dataset saved: {combined_filename}")
        print(f"📊 Total records: {len(combined_df)}")
        print(f"📅 Years covered: {sorted(combined_df['year'].unique())}")
        print(f"🏛️ Counties: {combined_df['county_name'].nunique()}")
        
        return combined_df
    else:
        print("❌ No data was successfully downloaded")
        return None

if __name__ == "__main__":
    # Check if we have a Census API key (optional but recommended)
    api_key = os.getenv('CENSUS_API_KEY')
    if not api_key:
        print("⚠️  No Census API key found. Using public access (rate limited).")
        print("   Get a free API key at: https://api.census.gov/data/key_signup.html")
        print("   Set it as: export CENSUS_API_KEY=your_key_here")
        print()
    
    # Download the data
    population_data = download_all_population_data()
    
    if population_data is not None:
        print("\n🎉 Population data download complete!")
        print("\nNext steps:")
        print("1. Review the data in notebooks/04_population_data_ingestion.ipynb")
        print("2. Add population features to your ML model")
    else:
        print("\n❌ Download failed. Check your internet connection and try again.")
