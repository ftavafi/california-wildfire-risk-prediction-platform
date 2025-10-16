"""
Download NOAA weather data for California weather stations.

This script downloads historical weather data from NOAA's Climate Data Online (CDO) API
for California weather stations from 2000-2025.

Data includes: Temperature, Precipitation, Wind Speed, etc.
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
NOAA_TOKEN = os.getenv('NOAA_API_TOKEN')

if not NOAA_TOKEN:
    raise ValueError("NOAA_API_TOKEN not found in .env file!")

# NOAA API configuration
BASE_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2"
HEADERS = {"token": NOAA_TOKEN}

# California bounding box
CA_EXTENT = {
    'min_lat': 32.5,
    'max_lat': 42.0,
    'min_lon': -124.5,
    'max_lon': -114.0
}

# Data output directory
OUTPUT_DIR = Path("../data/raw/weather")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("NOAA WEATHER DATA DOWNLOAD FOR CALIFORNIA")
print("=" * 80)
print(f"API Token: {'✅ Loaded' if NOAA_TOKEN else '❌ Missing'}")
print(f"Output directory: {OUTPUT_DIR.absolute()}")
print(f"Date range: 2000-01-01 to 2025-12-31")
print(f"Region: California ({CA_EXTENT['min_lat']}°N to {CA_EXTENT['max_lat']}°N)")
print("=" * 80)


def get_california_stations():
    """Get list of weather stations in California."""
    print("\n📍 Step 1: Finding California weather stations...")
    
    url = f"{BASE_URL}/stations"
    params = {
        'locationid': 'FIPS:06',  # California FIPS code
        'limit': 1000,
        'offset': 1
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'results' in data:
            stations = pd.DataFrame(data['results'])
            print(f"   ✅ Found {len(stations)} weather stations in California")
            
            # Save station list
            stations_file = OUTPUT_DIR / 'california_weather_stations.csv'
            stations.to_csv(stations_file, index=False)
            print(f"   💾 Saved station list to: {stations_file}")
            
            return stations
        else:
            print("   ⚠️  No stations found")
            return pd.DataFrame()
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error fetching stations: {e}")
        return pd.DataFrame()


def get_datasets():
    """Get available datasets."""
    print("\n📊 Step 2: Checking available datasets...")
    
    url = f"{BASE_URL}/datasets"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        if 'results' in data:
            datasets = pd.DataFrame(data['results'])
            print(f"   ✅ Found {len(datasets)} available datasets")
            
            # Show relevant datasets
            relevant = ['GHCND', 'GSOM', 'GSOY']  # Daily, Monthly, Yearly
            for ds in datasets[datasets['id'].isin(relevant)].itertuples():
                print(f"   - {ds.id}: {ds.name}")
            
            return datasets
        else:
            print("   ⚠️  No datasets found")
            return pd.DataFrame()
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error fetching datasets: {e}")
        return pd.DataFrame()


def download_weather_data_yearly(dataset_id='GHCND', start_year=2020, end_year=2024, station_id=None):
    """
    Download weather data for California in yearly chunks to avoid API limits.
    
    Args:
        dataset_id: GHCND (daily), GSOM (monthly), or GSOY (yearly)
        start_year: Start year
        end_year: End year
        station_id: Specific station ID (optional, None = all California)
    """
    print(f"\n🌦️  Step 3: Downloading weather data ({dataset_id})...")
    print(f"   Years: {start_year} to {end_year}")
    print(f"   Strategy: Downloading year-by-year to avoid API limits")
    
    url = f"{BASE_URL}/data"
    
    # Data types we want
    datatypes = [
        'TMAX',  # Maximum temperature
        'TMIN',  # Minimum temperature
        'PRCP',  # Precipitation
    ]
    
    all_data = []
    total_records = 0
    
    # Download year by year
    for year in range(start_year, end_year + 1):
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        print(f"\n   📅 Downloading {year}...")
        
        for datatype in datatypes:
            params = {
                'datasetid': dataset_id,
                'locationid': 'FIPS:06',  # California
                'datatypeid': datatype,
                'startdate': start_date,
                'enddate': end_date,
                'units': 'metric',
                'limit': 1000,
                'offset': 1
            }
            
            if station_id:
                params['stationid'] = station_id
            
            try:
                response = requests.get(url, headers=HEADERS, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'results' in data:
                        df = pd.DataFrame(data['results'])
                        all_data.append(df)
                        total_records += len(df)
                        print(f"      ✅ {datatype}: {len(df)} records")
                    else:
                        print(f"      ⚠️  {datatype}: No data")
                else:
                    print(f"      ⚠️  {datatype}: Status {response.status_code}")
                
                # Rate limiting - NOAA allows 5 requests per second
                time.sleep(0.3)
                
            except Exception as e:
                print(f"      ❌ {datatype}: {str(e)[:50]}")
                time.sleep(1)
                continue
        
        # Save yearly data as we go
        if len(all_data) > 0:
            yearly_df = pd.concat(all_data, ignore_index=True)
            yearly_file = OUTPUT_DIR / f'california_weather_{year}.csv'
            yearly_df.to_csv(yearly_file, index=False)
            print(f"      💾 Saved year {year} to file ({total_records} total records so far)")
    
    # Combine all years
    if all_data:
        weather_df = pd.concat(all_data, ignore_index=True)
        
        # Save combined file
        output_file = OUTPUT_DIR / f'california_weather_{start_year}_{end_year}_combined.csv'
        weather_df.to_csv(output_file, index=False)
        
        print(f"\n   ✅ Total records downloaded: {len(weather_df):,}")
        print(f"   💾 Saved combined file to: {output_file}")
        
        # Show summary
        if len(weather_df) > 0:
            print(f"\n   📊 Data Summary:")
            print(f"      Date range: {weather_df['date'].min()} to {weather_df['date'].max()}")
            print(f"      Data types: {weather_df['datatype'].unique().tolist()}")
            print(f"      Unique stations: {weather_df['station'].nunique()}")
        
        return weather_df
    else:
        print("   ⚠️  No weather data downloaded")
        return pd.DataFrame()


def main():
    """Main execution function."""
    
    print("\n" + "=" * 80)
    print("STARTING WEATHER DATA DOWNLOAD")
    print("=" * 80)
    
    # Step 1: Get California weather stations
    stations = get_california_stations()
    
    # Step 2: Get available datasets
    datasets = get_datasets()
    
    # Step 3: Download weather data year by year (2020-2025)
    print("\n" + "=" * 80)
    print("DOWNLOADING DATA (2020-2025) - YEAR BY YEAR")
    print("This approach downloads in yearly chunks to avoid API rate limits")
    print("=" * 80)
    
    weather_data = download_weather_data_yearly(
        dataset_id='GHCND',  # Daily data
        start_year=2020,
        end_year=2025
    )
    
    print("\n" + "=" * 80)
    print("✅ WEATHER DATA DOWNLOAD COMPLETE!")
    print("=" * 80)
    print(f"\nFiles saved to: {OUTPUT_DIR.absolute()}")
    print("\nNext steps:")
    print("1. Explore the data in a Jupyter notebook")
    print("2. Extend to full range (2000-2019) if needed")
    print("3. Match weather data with fire locations")
    print("=" * 80)


if __name__ == "__main__":
    main()

