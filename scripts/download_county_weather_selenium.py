#!/usr/bin/env python3
"""
Download County-Level Weather Data using Selenium Web Scraping
==============================================================

This script uses Selenium to interact with NOAA's Climate at a Glance web interface
to download weather data for all counties in our fire dataset.

Data Source: https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/county/time-series
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
from pathlib import Path

# Configuration
BASE_URL = "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/county/time-series"
OUTPUT_DIR = Path("../data/raw/weather/county")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Parameters to download
PARAMETERS = {
    'Average Temperature': 'tavg',
    'Maximum Temperature': 'tmax', 
    'Minimum Temperature': 'tmin',
    'Precipitation': 'pcp'
}

# Time period
START_YEAR = 2000
END_YEAR = 2025

# California counties from our fire dataset (subset for testing)
CALIFORNIA_COUNTIES = [
    'Alameda', 'Los Angeles', 'Orange', 'Riverside', 'San Bernardino', 'San Diego',
    'Fresno', 'Kern', 'Sacramento', 'Contra Costa', 'Santa Clara', 'Ventura',
    'San Francisco', 'San Joaquin', 'Stanislaus', 'Tulare', 'Sonoma', 'Solano'
]

def setup_driver():
    """Setup Chrome driver with options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Error setting up Chrome driver: {e}")
        print("Please make sure ChromeDriver is installed and in PATH")
        return None

def download_county_parameter(driver, county, parameter, start_year, end_year):
    """
    Download weather data for a specific county and parameter using Selenium.
    """
    try:
        print(f"  Downloading {parameter} for {county} County...")
        
        # Navigate to the page
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)
        
        # Wait for page to load
        time.sleep(2)
        
        # Select California state (should already be selected)
        state_select = wait.until(EC.presence_of_element_located((By.ID, "state")))
        state_dropdown = Select(state_select)
        state_dropdown.select_by_value("CA")
        
        # Select county
        county_select = wait.until(EC.presence_of_element_located((By.ID, "county")))
        county_dropdown = Select(county_select)
        county_dropdown.select_by_visible_text(f"{county} County")
        
        # Select parameter
        param_select = wait.until(EC.presence_of_element_located((By.ID, "parameter")))
        param_dropdown = Select(param_select)
        param_dropdown.select_by_visible_text(parameter)
        
        # Set time scale to Monthly
        timescale_select = wait.until(EC.presence_of_element_located((By.ID, "timescale")))
        timescale_dropdown = Select(timescale_select)
        timescale_dropdown.select_by_value("mly")
        
        # Set start year
        start_year_input = wait.until(EC.presence_of_element_located((By.ID, "startYear")))
        start_year_input.clear()
        start_year_input.send_keys(str(start_year))
        
        # Set end year
        end_year_input = wait.until(EC.presence_of_element_located((By.ID, "endYear")))
        end_year_input.clear()
        end_year_input.send_keys(str(end_year))
        
        # Click Plot button
        plot_button = wait.until(EC.element_to_be_clickable((By.ID, "plot")))
        plot_button.click()
        
        # Wait for data to load
        time.sleep(5)
        
        # Look for download link or data table
        try:
            # Try to find CSV download link
            download_link = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "CSV")))
            download_url = download_link.get_attribute("href")
            
            # Download the CSV file
            import requests
            response = requests.get(download_url)
            
            if response.status_code == 200:
                # Save to file
                param_code = PARAMETERS[parameter]
                filename = f"{county.replace(' ', '_').lower()}_{param_code}_{start_year}_{end_year}.csv"
                filepath = OUTPUT_DIR / filename
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"    ✅ Downloaded {len(response.content)} bytes to {filename}")
                return True
            else:
                print(f"    ❌ Failed to download CSV: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"    ❌ Could not find download link: {e}")
            return False
            
    except Exception as e:
        print(f"    ❌ Error downloading {parameter} for {county}: {e}")
        return False

def main():
    """
    Main function to download all county weather data using Selenium.
    """
    print("="*80)
    print("DOWNLOADING COUNTY-LEVEL WEATHER DATA USING SELENIUM")
    print("="*80)
    print(f"Source: {BASE_URL}")
    print(f"Counties: {len(CALIFORNIA_COUNTIES)}")
    print(f"Parameters: {list(PARAMETERS.keys())}")
    print(f"Time period: {START_YEAR}-{END_YEAR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*80)
    
    # Setup driver
    driver = setup_driver()
    if not driver:
        return
    
    try:
        total_downloads = len(CALIFORNIA_COUNTIES) * len(PARAMETERS)
        completed_downloads = 0
        successful_downloads = 0
        
        for county in CALIFORNIA_COUNTIES:
            print(f"\n🏛️  Processing {county} County...")
            
            for parameter in PARAMETERS.keys():
                success = download_county_parameter(driver, county, parameter, START_YEAR, END_YEAR)
                
                if success:
                    successful_downloads += 1
                
                completed_downloads += 1
                
                # Add delay between downloads
                time.sleep(3)
        
        print("\n" + "="*80)
        print("DOWNLOAD SUMMARY")
        print("="*80)
        print(f"Total downloads attempted: {total_downloads}")
        print(f"Successful downloads: {successful_downloads}")
        print(f"Failed downloads: {total_downloads - successful_downloads}")
        print(f"Success rate: {successful_downloads/total_downloads*100:.1f}%")
        print(f"Files saved to: {OUTPUT_DIR}")
        
        if successful_downloads > 0:
            print(f"\n📁 Files created:")
            for file in sorted(OUTPUT_DIR.glob("*.csv")):
                print(f"   {file.name}")
        
    finally:
        driver.quit()
        print("\n🔚 Browser session closed")

if __name__ == "__main__":
    main()
