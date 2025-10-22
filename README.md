# 🛰️ Multi-Temporal SAR–Optical Fusion
### Preprocessing and Data Cube Construction for Near-Real-Time Deforestation Detection

---

## 📖 Overview
This repository contains the **data engineering and preprocessing pipeline** developed by **Reuben Moses** for the collaborative project:

> *“Multi-Temporal SAR–Optical Fusion for Near-Real-Time Deforestation Detection in Cloud-Prone Tropical Regions.”*

The repository focuses on the **acquisition, correction, alignment, and fusion-ready preparation** of **Sentinel-1 (SAR)** and **Sentinel-2 (Optical)** imagery over the **Amazon biome (Brazil)**.  
The processed outputs form multi-temporal data cubes used for deep learning–based deforestation detection with <48-hour latency targets.

---

## 🎯 Key Objectives
- Automate the **download and organization** of Sentinel-1 and Sentinel-2 imagery.
- Perform **radiometric calibration**, **terrain correction**, and **speckle filtering** for SAR data.
- Apply **atmospheric correction** and **cloud masking/imputation** for optical data.
- Implement **cross-sensor geometric co-registration** between SAR and optical imagery.
- Construct **multi-temporal data cubes (4D tensors)** aligned spatially and temporally.
- Export preprocessed datasets in **HDF5/Zarr** formats for model ingestion.

---

## 🗂️ Repository Structure
```
/data/
 ├── sentinel1/        → Raw and calibrated Sentinel-1 SAR scenes
 ├── sentinel2/        → Atmospheric-corrected Sentinel-2 optical scenes
 ├── dem/              → Copernicus DEM tiles for terrain correction
 ├── labels/           → PRODES deforestation polygons and derived masks
 ├── metadata/         → AOI definitions, logs, metadata CSVs
/scripts/
 ├── create_aoi.py     → Generates AOI GeoJSON for target region
 ├── download_s1.py    → Automated Sentinel-1 acquisition via API
 ├── download_s2.py    → Sentinel-2 acquisition and filtering
 ├── preprocess_sar.py → Calibration, terrain correction, speckle filtering
 ├── preprocess_opt.py → Optical correction, co-registration, cloud handling
 ├── build_cube.py     → Constructs and validates 4D data cubes
 └── upload_to_cloud.py→ Uploads processed data to cloud storage
/outputs/
 ├── data_cubes/       → HDF5/Zarr multi-temporal tensors
 ├── reports/          → Quality assurance and preprocessing logs
 └── visualization/    → Sample plots and footprint maps
```

---

## ⚙️ Technologies & Tools
- **Languages:** Python, Bash  
- **Libraries:** `sentinelsat`, `rasterio`, `gdal`, `geopandas`, `xarray`, `opencv`, `torch`, `pyrosar`  
- **Platforms:** Copernicus Open Access Hub, Google Cloud Storage, ESA SNAP, INPE PRODES  
- **Formats:** GeoTIFF, HDF5, Zarr, GeoJSON  

---

## 🔄 Workflow Summary
1. Define **AOI** using PRODES polygons (Rondônia region).  
2. Download Sentinel-1 GRD and Sentinel-2 L2A data within target temporal range.  
3. Apply SAR calibration, terrain correction, and filtering.  
4. Perform optical preprocessing and co-registration to SAR geometry.  
5. Handle persistent cloud cover using **pix2pix GAN-based** imputation.  
6. Construct and validate **multi-temporal 4D data cubes** ready for model input.  
7. Upload outputs to shared cloud storage for model training (Vasist) and validation (Suhruth).

---

## 📦 Deliverables
- `aoi.geojson` — spatial footprint of the Amazon study region.  
- Preprocessed **SAR & Optical datasets** aligned in space and time.  
- Multi-temporal **data cubes** (HDF5/Zarr format).  
- Documentation: preprocessing parameters, metadata logs, QA reports.

---

## 👥 Team Collaboration
| Role | Member | Responsibility |
|------|---------|----------------|
| **Reuben** | *(You)* | Data acquisition, preprocessing, and cube generation |
| **Vasist** | Model architecture, fusion, and deployment |
| **Suhruth** | Model validation and benchmarking |
| **Sirivennela** | Label engineering and methodology documentation |

