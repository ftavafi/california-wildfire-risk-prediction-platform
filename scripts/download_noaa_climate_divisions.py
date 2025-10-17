#!/usr/bin/env python3
"""
Download and process NOAA Climate Divisional Data for California
Source: https://www.ncei.noaa.gov/pub/data/cirs/climdiv/
"""

import os
import requests
import pandas as pd
from pathlib import Path
import time

def download_file(url, filename, data_dir):
    """Download a file from URL to specified directory"""
    filepath = data_dir / filename
    
    print(f"Downloading {filename}...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded {filename} ({filepath.stat().st_size / 1024:.1f} KB)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading {filename}: {e}")
        return False

def process_climate_file(filepath, data_type):
    """Process a single climate division file"""
    print(f"Processing {data_type} data...")
    
    data = []
    
    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if len(line) < 68:  # Skip incomplete lines
                    continue
                
                # Extract division code, year, and monthly values
                division_code = line[:4].strip()
                year = int(line[4:8])
                monthly_values = []
                
                # Extract 12 monthly values (5 characters each)
                for i in range(8, 68, 5):
                    value_str = line[i:i+5].strip()
                    if value_str and value_str != '-9999':
                        try:
                            value = float(value_str) / 100.0  # Convert to proper units
                            monthly_values.append(value)
                        except ValueError:
                            monthly_values.append(None)
                    else:
                        monthly_values.append(None)
                
                # Create records for each month
                for month, value in enumerate(monthly_values, 1):
                    data.append({
                        'division_code': division_code,
                        'year': year,
                        'month': month,
                        data_type.lower(): value
                    })
    
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return None
    
    return pd.DataFrame(data)

def main():
    """Main function to download and process climate data"""
    
    # Set up directories
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data" / "noaa_climate_divisions"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # NOAA Climate Divisional Data URLs
    base_url = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/"
    
    files_to_download = {
        'precipitation': 'climdiv-ca-pcpncy-v1.0.0-20250905.txt',
        'max_temperature': 'climdiv-ca-tmaxcy-v1.0.0-20250905.txt',
        'min_temperature': 'climdiv-ca-tmincy-v1.0.0-20250905.txt',
        'readme': 'climdiv-inv-readme.txt'
    }
    
    print("🌦️  Downloading NOAA Climate Divisional Data for California")
    print("=" * 60)
    
    # Download files
    downloaded_files = {}
    for data_type, filename in files_to_download.items():
        url = base_url + filename
        if download_file(url, filename, data_dir):
            downloaded_files[data_type] = data_dir / filename
        time.sleep(1)  # Be respectful to the server
    
    print("\n📊 Processing climate data...")
    print("=" * 60)
    
    # Process climate data files
    processed_dfs = []
    
    for data_type, filepath in downloaded_files.items():
        if data_type == 'readme':
            continue
            
        df = process_climate_file(filepath, data_type)
        if df is not None:
            processed_dfs.append(df)
            print(f"✅ Processed {data_type}: {len(df)} records")
    
    # Merge all data
    if processed_dfs:
        print("\n🔄 Merging climate data...")
        merged_df = processed_dfs[0]
        
        for df in processed_dfs[1:]:
            merged_df = pd.merge(merged_df, df, on=['division_code', 'year', 'month'], how='outer')
        
        # Filter to 2000-2025 range
        merged_df = merged_df[(merged_df['year'] >= 2000) & (merged_df['year'] <= 2025)]
        
        # Add date column
        merged_df['date'] = pd.to_datetime(merged_df[['year', 'month']].assign(day=1))
        
        # Save processed data
        output_file = data_dir / "california_climate_data_processed.csv"
        merged_df.to_csv(output_file, index=False)
        
        print(f"✅ Saved processed data: {output_file}")
        print(f"📈 Records: {len(merged_df):,}")
        print(f"📅 Date range: {merged_df['year'].min()}-{merged_df['year'].max()}")
        print(f"🌍 Climate divisions: {merged_df['division_code'].nunique()}")
        
        # Display sample
        print("\n📋 Sample data:")
        print(merged_df.head())
        
    else:
        print("❌ No data files were successfully processed")

if __name__ == "__main__":
    main()
