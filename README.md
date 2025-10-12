# 🔥 California Wildfire Risk Prediction Platform

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: In Development](https://img.shields.io/badge/status-in%20development-orange.svg)]()

> A production-ready machine learning platform that predicts wildfire risk for any location in California based on weather patterns, vegetation conditions, topography, and historical fire data.

## 🎯 Project Overview

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

This project integrates multiple public datasets:

- **Historical Fires**: [CAL FIRE](https://frap.fire.ca.gov/) - Fire perimeters and incidents (2000-2024)
- **Weather Data**: [NOAA API](https://www.weather.gov/documentation/services-web-api) - Temperature, humidity, wind, precipitation
- **Vegetation**: [NASA MODIS](https://earthdata.nasa.gov/) - Vegetation indices (NDVI)
- **Topography**: [USGS](https://www.usgs.gov/) - Elevation, slope, terrain data

All data sources are publicly available and free to access.

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

This is currently a portfolio project in active development. Contributions, suggestions, and feedback are welcome!

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

*Last Updated: October 2025*
