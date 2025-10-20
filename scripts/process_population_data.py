"""
Process California Population Data (2000-2025)
Combines 3 Excel files from CA Dept of Finance into one dataset
"""

import pandas as pd
from pathlib import Path

def process_population_data():
    """
    Process and combine population data from 3 Excel files:
    - E4_2000-2010_Report_Final_EOC_000 (1).xlsx
    - E-4_2010-2020-Internet-Version.xlsx
    - E-4_2025_InternetVersion.xlsx
    """
    
    data_dir = Path('../data/raw/population')
    output_dir = Path('../data/raw/population')
    
    # File paths
    file_2000_2010 = data_dir / 'E4_2000-2010_Report_Final_EOC_000 (1).xlsx'
    file_2010_2020 = data_dir / 'E-4_2010-2020-Internet-Version.xlsx'
    file_2020_2025 = data_dir / 'E-4_2025_InternetVersion.xlsx'
    
    print("=" * 80)
    print("PROCESSING CALIFORNIA POPULATION DATA (2000-2025)")
    print("=" * 80)
    
    # Read each file's "Table 1 County State" sheet
    print("\nReading 2000-2010 data...")
    df_2000_2010 = pd.read_excel(file_2000_2010, sheet_name='Table 1 County State')
    print(f"✅ Loaded {len(df_2000_2010)} rows")
    print(f"   Columns: {df_2000_2010.columns.tolist()}")
    
    print("\nReading 2010-2020 data...")
    df_2010_2020 = pd.read_excel(file_2010_2020, sheet_name='Table 1 County State')
    print(f"✅ Loaded {len(df_2010_2020)} rows")
    print(f"   Columns: {df_2010_2020.columns.tolist()}")
    
    print("\nReading 2020-2025 data...")
    df_2020_2025 = pd.read_excel(file_2020_2025, sheet_name='Table 1 County State')
    print(f"✅ Loaded {len(df_2020_2025)} rows")
    print(f"   Columns: {df_2020_2025.columns.tolist()}")
    
    # Display first few rows to understand structure
    print("\n" + "=" * 80)
    print("SAMPLE DATA - 2000-2010:")
    print("=" * 80)
    print(df_2000_2010.head(10))
    
    print("\n" + "=" * 80)
    print("SAMPLE DATA - 2010-2020:")
    print("=" * 80)
    print(df_2010_2020.head(10))
    
    print("\n" + "=" * 80)
    print("SAMPLE DATA - 2020-2025:")
    print("=" * 80)
    print(df_2020_2025.head(10))
    
    print("\n" + "=" * 80)
    print("DATA INSPECTION COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Identify county name column")
    print("2. Identify year columns")
    print("3. Reshape data to long format (County, Year, Population)")
    print("4. Combine all three datasets")
    print("5. Save as california_population_2000_2025.csv")

if __name__ == "__main__":
    process_population_data()


