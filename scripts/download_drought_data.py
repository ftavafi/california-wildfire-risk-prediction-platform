"""
Download US Drought Monitor data for California.

The US Drought Monitor provides weekly drought classifications:
- D0: Abnormally Dry
- D1: Moderate Drought
- D2: Severe Drought
- D3: Extreme Drought
- D4: Exceptional Drought

These classifications are critical for wildfire prediction because drought 
conditions indicate dry fuels and elevated fire risk.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

# Output directory
OUTPUT_DIR = Path("../data/raw/drought")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("US DROUGHT MONITOR DATA DOWNLOAD FOR CALIFORNIA")
print("=" * 80)
print(f"Output directory: {OUTPUT_DIR.absolute()}")
print(f"Source: US Drought Monitor (droughtmonitor.unl.edu)")
print("=" * 80)

def download_drought_data(start_year=2020, end_year=2025):
    """
    Download drought data for California from US Drought Monitor.
    
    Data is available as weekly time series showing drought severity levels.
    """
    print(f"\n📊 Downloading drought data ({start_year}-{end_year})...")
    
    # US Drought Monitor data API
    base_url = "https://droughtmonitor.unl.edu/DmData/DataDownload/ComprehensiveStatistics.aspx"
    
    # Parameters for California
    params = {
        'mode': 'table',
        'aoi': '06',  # California FIPS code
        'startdate': f'{start_year}0101',
        'enddate': f'{end_year}1231',
        'statstype': '1'  # County statistics
    }
    
    print(f"\n   Requesting data from US Drought Monitor API...")
    print(f"   State: California (FIPS: 06)")
    print(f"   Date range: {start_year}-01-01 to {end_year}-12-31")
    
    try:
        response = requests.get(base_url, params=params, timeout=60)
        
        if response.status_code == 200:
            # Save raw response
            output_file = OUTPUT_DIR / f'california_drought_{start_year}_{end_year}.csv'
            
            with open(output_file, 'w') as f:
                f.write(response.text)
            
            print(f"\n   ✅ Downloaded drought data successfully!")
            print(f"   💾 Saved to: {output_file}")
            
            # Try to parse as CSV
            try:
                drought_df = pd.read_csv(output_file)
                print(f"\n   📊 Data Summary:")
                print(f"      Records: {len(drought_df):,}")
                print(f"      Columns: {drought_df.columns.tolist()}")
                
                if 'ValidStart' in drought_df.columns:
                    print(f"      Date range: {drought_df['ValidStart'].min()} to {drought_df['ValidStart'].max()}")
                
                return drought_df
            except Exception as e:
                print(f"   ⚠️  Could not parse CSV: {e}")
                print(f"   Raw data saved - check file manually")
                return None
        else:
            print(f"   ❌ Error: HTTP {response.status_code}")
            print(f"   Message: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error downloading drought data: {e}")
        return None


def download_alternative():
    """
    Alternative download instructions if API doesn't work.
    """
    print("\n" + "=" * 80)
    print("ALTERNATIVE: MANUAL DOWNLOAD")
    print("=" * 80)
    
    print("""
If the API download doesn't work, you can download manually:

1. Go to: https://droughtmonitor.unl.edu/DmData/DataDownload.aspx

2. Select options:
   - **Area**: California (or select specific counties)
   - **Time Period**: Custom → 2020-01-01 to 2025-12-31
   - **Output Format**: Tabular Data (CSV)
   - **Statistics Type**: Comprehensive Statistics

3. Click "Get Data"

4. Download the CSV file

5. Save to: {output_dir}
   Name it: california_drought_2020_2025.csv

The data will include weekly drought classifications (D0-D4) for California counties.
""".format(output_dir=OUTPUT_DIR.absolute()))


def main():
    """Main execution."""
    
    print("\n" + "=" * 80)
    print("STARTING DROUGHT DATA DOWNLOAD")
    print("=" * 80)
    
    # Try API download
    drought_data = download_drought_data(start_year=2020, end_year=2025)
    
    if drought_data is None:
        # Show manual download instructions
        download_alternative()
    else:
        print("\n" + "=" * 80)
        print("✅ DROUGHT DATA DOWNLOAD COMPLETE!")
        print("=" * 80)
        print(f"\nFiles saved to: {OUTPUT_DIR.absolute()}")
        print("\nNext steps:")
        print("1. Explore drought data in Jupyter notebook")
        print("2. Match drought levels with fire occurrence")
        print("3. Create drought-based features for ML model")
        print("=" * 80)


if __name__ == "__main__":
    main()

