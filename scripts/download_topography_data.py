"""
Download USGS Digital Elevation Model (DEM) data for California.

This script downloads elevation data (DEM) for California and calculates:
- Elevation (meters)
- Slope (steepness)
- Aspect (direction slope faces)

These topographic features are critical for fire prediction because:
- Fires spread faster uphill (slope effect)
- South-facing slopes get more sun (drier vegetation)
- Elevation affects temperature and vegetation type
"""

import urllib.request
import subprocess
from pathlib import Path
import os

print("=" * 80)
print("CALIFORNIA TOPOGRAPHY DATA DOWNLOAD")
print("=" * 80)

# Output directory
OUTPUT_DIR = Path("../data/raw/topography")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"\nOutput directory: {OUTPUT_DIR.absolute()}")
print(f"Data source: USGS 3D Elevation Program (3DEP)")

print("\n" + "=" * 80)
print("DOWNLOAD OPTIONS")
print("=" * 80)

print("""
California DEM data can be downloaded from:

1. **USGS National Map Viewer** (Recommended - Manual)
   URL: https://apps.nationalmap.gov/downloader/
   
   Steps:
   - Click "Find Products"
   - Extent: Draw box around California OR enter coordinates:
     * North: 42.0°
     * South: 32.5°
     * West: -124.5°
     * East: -114.0°
   - Datasets: Check "Elevation Products (3DEP)"
   - Select "1/3 arc-second DEM" (10-meter resolution)
   - Click "Find Products"
   - Download the tiles covering California
   - Save to: {output_dir}

2. **OpenTopography** (Alternative - Research Quality)
   URL: https://opentopography.org/
   - Higher resolution options available
   - Requires free account

3. **SRTM (Shuttle Radar Topography Mission)** (Global Coverage)
   - 30-meter resolution (lower than 3DEP but global)
   - Available via: Google Earth Engine, USGS EarthExplorer

4. **Pre-processed Kaggle Dataset** (Easiest)
   - Search Kaggle for "California DEM" or "California elevation"
   - Already cropped and ready to use

""".format(output_dir=OUTPUT_DIR.absolute()))

print("=" * 80)
print("AUTOMATED DOWNLOAD (Option - Requires elevation library)")
print("=" * 80)

print("""
To download automatically using Python:

1. Install elevation library:
   pip install elevation

2. Run this in Python:
   ```python
   import elevation
   
   # California bounding box
   bounds = (-124.5, 32.5, -114.0, 42.0)  # (west, south, east, north)
   
   # Download DEM
   output = 'california_dem.tif'
   elevation.clip(bounds=bounds, output=output, product='SRTM3')
   ```

3. This downloads and merges DEM tiles automatically

Note: First run will download ~500MB for California
""")

print("\n" + "=" * 80)
print("MANUAL DOWNLOAD RECOMMENDED FOR THIS PROJECT")
print("=" * 80)

print("""
For this project, I recommend manual download from USGS National Map:
- Better quality (10m resolution vs 30m)
- Official USGS source
- More control over data selection

After downloading, save files to:
{output_dir}

Then we'll process the DEM to calculate slope and aspect in a Jupyter notebook.
""".format(output_dir=OUTPUT_DIR.absolute()))

print("=" * 80)
print("📋 NEXT STEPS")
print("=" * 80)
print("\n1. Choose a download method above")
print("2. Download California DEM data")
print("3. Save to: " + str(OUTPUT_DIR.absolute()))
print("4. Run notebook: 03_topography_exploration.ipynb")
print("\n" + "=" * 80)

