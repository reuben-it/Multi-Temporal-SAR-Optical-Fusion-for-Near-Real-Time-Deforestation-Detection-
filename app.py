import streamlit as st
import leafmap.foliumap as leafmap
import rasterio
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("Interactive Map Viewer (SAR / Optical / Fused Data)")
st.write("Upload a GeoTIFF map to visualize (segmentation/fusion maps).")

uploaded_file = st.file_uploader("Upload GeoTIFF", type=["tif", "tiff"])

if uploaded_file:
    temp_filename = f"temp_{uploaded_file.name}"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    st.subheader("Raster Preview")

    # Read the raster
    with rasterio.open(temp_filename) as src:
        arr = src.read(1)  # first band
        arr_norm = (arr - arr.min()) / (arr.max() - arr.min())  # normalize 0-1
        arr_uint8 = (arr_norm * 255).astype(np.uint8)
        
        img = Image.fromarray(arr_uint8, mode="L")
        preview_png = "preview.png"
        img.save(preview_png)

    st.image(preview_png, caption="Raster Preview", use_container_width=True)

    st.subheader("Interactive Map")
    m = leafmap.Map(center=[20.59, 78.96], zoom=4)

    try:
        m.add_image(preview_png, bounds=[[-10, 60], [40, 100]], opacity=0.8)
    except Exception as e:
        st.error(f"Could not load raster: {e}")

    m.to_streamlit(height=700)
