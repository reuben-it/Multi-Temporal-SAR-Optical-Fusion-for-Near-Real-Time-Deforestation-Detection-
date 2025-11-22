import streamlit as st
import leafmap.foliumap as leafmap
import os
import tempfile
import rasterio
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("Multi-Day Interactive Map Viewer (SAR / Optical / Fused Data)")
st.title("Interactive Map Viewer (SAR / Optical / Fused Data)")
st.write("Upload a GeoTIFF map to visualize (segmentation/fusion maps).")

st.write("""
Upload one or more raster maps (GeoTIFF) such as:
- SAR Backscatter
- Optical Data  
- Fused Output  
- DL Segmentation Output (Deforestation / Non-Deforestation)
""")
uploaded_file = st.file_uploader("Upload GeoTIFF", type=["tif", "tiff"])

uploaded_files = st.file_uploader(
    "Upload files here",
    type=["tif", "tiff", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)
if uploaded_file:
    temp_filename = f"temp_{uploaded_file.name}"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded!")
    st.success("File uploaded successfully!")

    # Temporary folder for uploaded rasters
    temp_dir = tempfile.mkdtemp()
    st.subheader("Raster Preview")

    m = leafmap.Map(center=[20.59, 78.96], zoom=4)

    for file in uploaded_files:
        temp_path = os.path.join(temp_dir, file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
    # Read the raster
    with rasterio.open(temp_filename) as src:
        arr = src.read(1)  # first band
        arr_norm = (arr - arr.min()) / (arr.max() - arr.min())  # normalize 0-1
        arr_uint8 = (arr_norm * 255).astype(np.uint8)
        
        img = Image.fromarray(arr_uint8, mode="L")
        preview_png = "preview.png"
        img.save(preview_png)

        # Auto-name the layer
        layer_name = os.path.splitext(file.name)[0]
    st.image(preview_png, caption="Raster Preview", use_container_width=True)

        st.write(f"### Loaded Layer: {layer_name}")
    st.subheader("Interactive Map")
    m = leafmap.Map(center=[20.59, 78.96], zoom=4)

        try:
            m.add_raster(temp_path, layer_name=layer_name)
        except Exception as e:
            st.error(f"Could not load {file.name}: {e}")
    try:
        m.add_image(preview_png, bounds=[[-10, 60], [40, 100]], opacity=0.8)
    except Exception as e:
        st.error(f"Could not load raster: {e}")

    st.subheader("🗺 Interactive Map")
    m.add_layer_control()
m.to_streamlit(height=700)

else:
    st.info("Upload GeoTIFF files to begin.")
