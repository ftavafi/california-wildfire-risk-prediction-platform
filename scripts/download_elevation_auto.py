"""
Automated California DEM download using elevation library.
"""

import elevation
from pathlib import Path

OUTPUT_DIR = Path("../data/raw/topography")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("DOWNLOADING CALIFORNIA ELEVATION DATA (SRTM)")
print("=" * 80)

# California bounding box (west, south, east, north)
bounds = (-124.5, 32.5, -114.0, 42.0)
output_file = OUTPUT_DIR / 'california_dem_srtm.tif'

print(f"\nBounding box: {bounds}")
print(f"Output file: {output_file}")
print(f"\nDownloading... (this may take 5-10 minutes)")
print("Progress will be shown below:\n")

try:
    elevation.clip(bounds=bounds, output=str(output_file), product='SRTM3')
    print(f"\n✅ Download complete!")
    print(f"File saved to: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
except Exception as e:
    print(f"\n❌ Download failed: {e}")
    print("\nTry manual download from USGS National Map instead")

print("=" * 80)

