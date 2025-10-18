# 🔥 California Wildfire Risk Prediction Platform

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: In Development](https://img.shields.io/badge/status-in%20development-orange.svg)]()

> A production-ready machine learning platform that predicts wildfire risk for any location in California based on weather patterns, vegetation conditions, topography, and historical fire data.

## 🎯 Project Overview

**Personal Motivation**: In January 2025, I was living in West Hollywood when the wildfire broke out in the Hollywood Hills. Half of my building received evacuation orders, and my family and I packed our car with essentials, ready to flee at any moment. It was terrifying—watching neighbors scrambling with whatever they could carry, children crying, elderly residents needing help to evacuate, not knowing if any of us would have homes to return to. The fire eventually damaged and destroyed several homes in the area, displacing families and even impacting major events like the Oscar nominations.

As a data scientist standing there with our car packed, I kept thinking: "We have all this data—weather patterns, historical fires, satellite imagery—why can't we predict this better? Why are we always reacting instead of preparing?" That experience drove me to build this platform. The idea is simple but critical: if communities had reliable 7-30 day wildfire risk predictions, families could prepare their properties, secure important documents, coordinate with vulnerable neighbors, and evacuate safely—not in panic, but with a plan.

California faces increasing wildfire threats due to climate change, with devastating consequences for communities, ecosystems, and infrastructure. This platform leverages machine learning and real-time data to predict wildfire risk 7-30 days in advance, enabling:

- **Early warning systems** for fire departments and emergency services
- **Risk assessment** for insurance companies and property developers  
- **Public safety tools** for California residents
- **Resource allocation optimization** for CAL FIRE

## ✨ Key Features

- **Predictive ML Models**: Random Forest and XGBoost models trained on 20+ years of historical fire data
- **Real-Time Predictions**: REST API serving wildfire risk scores for any California location
- **Interactive Map**: Streamlit dashboard displaying color-coded risk zones across California
- **Cloud Deployment**: Production ML pipeline deployed on AWS SageMaker
- **MLOps Pipeline**: Experiment tracking with MLflow, containerization with Docker, CI/CD with GitHub Actions
- **Geospatial Analysis**: Advanced feature engineering using NASA satellite data, NOAA weather, and USGS topography

## 🛠️ Technology Stack

### **Data & ML**

- **Languages**: Python 3.9+, SQL
- **ML Libraries**: Scikit-Learn, XGBoost, TensorFlow, PyTorch
- **Data Processing**: Pandas, NumPy, GeoPandas, Rasterio
- **Geospatial**: Folium, Shapely, PostGIS

### **MLOps & Deployment**

- **Cloud Platform**: AWS (SageMaker, S3, Lambda)
- **ML Tracking**: MLflow, DVC
- **API Framework**: FastAPI
- **Frontend**: Streamlit
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Database**: PostgreSQL with PostGIS

### **Visualization**

- Matplotlib, Seaborn, Plotly

## 📊 Data Sources

This project integrates multiple public datasets to build a comprehensive wildfire risk prediction model:

### **Datasets Collected ✅**

#### 1. **CAL FIRE Historical Fire Data** (2000-2025)

- **Source**: [CAL FIRE Fire and Resource Assessment Program (FRAP)](https://frap.fire.ca.gov/)
- **Coverage**: 20,000+ fire perimeters across California
- **Key Features**: Fire location, size (acres), year, cause, duration
- **Format**: Shapefile (GIS), converted to GeoJSON/CSV
- **Status**: ✅ Downloaded and ingested
- **Notebook**: `01_fire_data_ingestion.ipynb`

#### 2. **NOAA Climate Data** (2000-2025)

- **Source**: [NOAA Climate at a Glance - Statewide Time Series](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series)
- **Coverage**: Monthly climate data for California statewide
- **Key Features**: Temperature (avg/min/max), precipitation
- **Format**: CSV
- **Status**: ✅ Downloaded and ingested
- **Notebook**: `02_weather_data_ingestion.ipynb`

#### 3. **US Drought Monitor Data** (2000-2025)

- **Source**: [US Drought Monitor](https://droughtmonitor.unl.edu/)
- **Coverage**: Weekly drought severity classifications for California
- **Key Features**: Drought categories (D0-D4), population affected, area percentage
- **Format**: Shapefile → CSV
- **Status**: ✅ Downloaded and ingested
- **Notebook**: `03_drought_data_ingestion.ipynb`

#### 4. **California County Population Data** (2000-2025)

- **Source**: [CA Department of Finance - E-4 Population Estimates](https://dof.ca.gov/forecasting/demographics/estimates/)
- **Coverage**: All 58 California counties, annual estimates (2000-2025)
- **Key Features**: Total population by county and year
- **Format**: Excel (3 files) → Merged CSV
- **Data Files**:
  - E4_2000-2010_Report_Final_EOC_000.xlsx
  - E-4_2010-2020-Internet-Version.xlsx
  - E-4_2025_InternetVersion.xlsx
- **Status**: ✅ Downloaded, merged, and ingested
- **Notebook**: `04_population_data_processing.ipynb`

### **Datasets Planned 🔄**

#### 5. **SRTM Topography Data** (2000)

- **Source**: [OpenTopography - SRTM GL1 (30m)](https://portal.opentopography.org/raster?opentopoID=OTSRTM.082015.4326.1)
- **Coverage**: California (3 regions: Northern, Central, Southern)
- **Key Features**: Elevation (30m resolution), slope, aspect
- **Format**: GeoTIFF
- **Bounding Boxes**:
  - Northern CA: xmin=-124.5, xmax=-119.5, ymin=39.0, ymax=42.0
  - Central CA: xmin=-123.0, xmax=-118.0, ymin=35.5, ymax=39.0
  - Southern CA: xmin=-121.0, xmax=-114.0, ymin=32.5, ymax=35.5
- **Status**: ✅ Downloaded (awaiting rasterio installation for processing)
- **Notebook**: `05_topography_data_ingestion.ipynb`

#### 6. **NOAA Lightning Strike Data**

- **Source**: [NOAA GOES Geostationary Lightning Mapper](https://www.ncei.noaa.gov/products/goes-geostationary-lightning-mapper)
- **Coverage**: Lightning detection across California
- **Key Features**: Strike location, intensity, timestamp
- **Purpose**: Natural fire ignition sources
- **Status**: ⏳ Pending

### **Dataset Summary**

| Dataset | Years | Records | Size | Status |
|---------|-------|---------|------|--------|
| CAL FIRE Fires | 2000-2025 | 20,000+ | ~500 MB | ✅ Complete |
| NOAA Climate | 2000-2025 | 308 | <1 MB | ✅ Complete |
| Drought Monitor | 2000-2025 | 1,345 | ~2 GB | ✅ Complete |
| CA County Population | 2000-2025 | 1,566 | <1 MB | ✅ Complete |
| SRTM Topography | 2000 | 3 regions | ~1.2 GB | ✅ Downloaded |
| **Total Collected** | - | **22,000+** | **~3.7 GB** | **5/6 datasets** |

All data sources are publicly available and free to access.

### **Data Visualization & Exploration**

Each dataset has been thoroughly explored with comprehensive visualizations in Jupyter notebooks:

- **Fire Data (01)**: Fires per year, acres burned trends, size distribution, monthly patterns, top 10 largest fires, cause analysis
- **Weather Data (02)**: Seasonal temperature patterns, temp vs precipitation correlation, annual trends with trendlines, dry season analysis
- **Drought Data (03)**: Stacked area charts, severity heatmaps, category distributions, intensity scores, exceptional drought timelines
- **Population Data (04)**: County growth comparisons, fire-risk county trends, distribution analysis, fastest growing counties
- **Topography Data (05)**: Elevation maps and histograms (full processing pending rasterio installation)

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- AWS account (for deployment phase)
- 10GB+ free disk space (for datasets)

### Installation

```bash
# Clone the repository
git clone https://github.com/ftavafi/california-wildfire-risk-prediction-platform.git
cd california-wildfire-risk-prediction-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Quick Start

```bash
# Download initial datasets (Coming in Phase 1)
python scripts/download_data.py

# Run exploratory data analysis (Coming in Phase 1)
jupyter notebook notebooks/01_data_exploration.ipynb

# Train model (Coming in Phase 3)
python scripts/train_model.py

# Start API server (Coming in Phase 4)
uvicorn src.api.main:app --reload

# Launch Streamlit dashboard (Coming in Phase 6)
streamlit run streamlit_app/app.py
```

## 📁 Project Structure

```
california-wildfire-risk-prediction-platform/
│
├── data/                          # Data storage (gitignored)
│   ├── raw/                       # Original datasets
│   ├── processed/                 # Cleaned data
│   ├── features/                  # Engineered features
│   └── predictions/               # Model outputs
│
├── notebooks/                     # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_fire_analysis.ipynb
│   └── ...
│
├── src/                           # Source code
│   ├── data/                      # Data loading and processing
│   ├── features/                  # Feature engineering
│   ├── models/                    # Model training and evaluation
│   ├── api/                       # FastAPI application
│   ├── deployment/                # AWS SageMaker deployment
│   └── utils/                     # Utility functions
│
├── streamlit_app/                 # Web application
│   ├── app.py                     # Main Streamlit app
│   └── components/                # UI components
│
├── tests/                         # Unit and integration tests
├── scripts/                       # Utility scripts
├── docs/                          # Documentation
│
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container configuration
└── README.md                      # This file
```

## 🎯 Project Roadmap

### Phase 0: Setup ✅ (In Progress)

- [x] Project structure initialization
- [x] Git repository setup
- [ ] Documentation framework

### Phase 1: Data Collection & Exploration (Planned)

- [ ] Download historical fire data
- [ ] Collect weather and climate data
- [ ] Exploratory data analysis
- [ ] Data quality assessment

### Phase 2: Feature Engineering (Planned)

- [ ] Temporal features (seasonality, trends)
- [ ] Weather features (temperature, humidity, wind)
- [ ] Vegetation features (NDVI, land cover)
- [ ] Spatial features (elevation, distance metrics)

### Phase 3: Model Development (Planned)

- [ ] Baseline model creation
- [ ] Advanced model training (Random Forest, XGBoost)
- [ ] Hyperparameter tuning
- [ ] Model evaluation and selection

### Phase 4: API Development (Planned)

- [ ] FastAPI REST endpoints
- [ ] Input validation
- [ ] Error handling

### Phase 5: AWS Deployment (Planned)

- [ ] SageMaker model deployment
- [ ] Cloud endpoint configuration
- [ ] Performance monitoring

### Phase 6: Frontend Development (Planned)

- [ ] Interactive California map
- [ ] Location search functionality
- [ ] Risk visualization dashboard

### Phase 7: MLOps (Planned)

- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Automated testing

### Phase 8: Documentation & Launch (Planned)

- [ ] Comprehensive documentation
- [ ] Demo video creation
- [ ] Public release

## 📈 Expected Results

**Target Model Performance:**

- Accuracy: > 85%
- Precision: > 70%
- Recall: > 80%
- ROC-AUC: > 0.85
- API Latency: < 500ms

## 🤝 Contributing

This is a personal passion project born from experiencing the January 2025 Hollywood Hills fire evacuations firsthand. Standing with my car packed, watching neighbors evacuate, uncertain if we'd lose our homes—that experience showed me the urgent need for better wildfire prediction tools. As a data scientist, I'm committed to using my skills to ensure other families never have to experience that same fear and uncertainty without warning. While currently in active development, I'm exploring ways to make this tool freely accessible to California residents, emergency responders, and community organizations who need it most.

Contributions, suggestions, and collaboration opportunities are welcome!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Tara Tavafi**

- Email: <f.tavafi@gmail.com>
- LinkedIn: [linkedin.com/in/taratavafi](https://www.linkedin.com/in/taratavafi)
- GitHub: [@ftavafi](https://github.com/ftavafi)
- Location: Los Angeles, California

## 🙏 Acknowledgments

- CAL FIRE for providing comprehensive fire history data
- NOAA for weather and climate data access
- NASA for satellite imagery and vegetation indices
- USGS for topography and terrain data
- The open-source community for excellent ML tools and frameworks

## 📞 Contact

For questions, collaborations, or opportunities, please reach out via:

- Email: <f.tavafi@gmail.com>
- LinkedIn: [https://www.linkedin.com/in/taratavafi](https://www.linkedin.com/in/taratavafi)

---

**⚠️ Disclaimer**: This project is for educational and research purposes. Wildfire risk predictions should not be used as the sole basis for emergency decisions. Always follow official guidance from CAL FIRE and local authorities.

---

*Last Updated: January 2025*
