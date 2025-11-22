import streamlit as st
import leafmap.foliumap as leafmap
import rasterio
import numpy as np
from rasterio.plot import reshape_as_image
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

st.set_page_config(layout="wide")
st.title("Deforestation Segmentation Map Viewer")
st.write("Upload your fused / segmentation GeoTIFF to visualize it on an interactive map.")

uploaded_file = st.file_uploader("Upload GeoTIFF map", type=["tif", "tiff"])

if uploaded_file:
    temp_filename = f"temp_{uploaded_file.name}"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    # Load raster
    with rasterio.open(temp_filename) as src:
        profile = src.profile
        bounds = src.bounds
        data = src.read()

    # Normalize bands for display
    if data.shape[0] == 1:  # single band segmentation
        arr = data[0]
        classes = np.unique(arr)

        # Create a categorical color map
        cmap = {
            0: (0, 150, 0),     # Non-deforestation (green)
            1: (200, 0, 0),     # Deforestation (red)
        }

        rgb = np.zeros((arr.shape[0], arr.shape[1], 3), dtype=np.uint8)
        for cls, color in cmap.items():
            rgb[arr == cls] = color

    else:  # Multi-band TIFF (RGB)
        rgb = reshape_as_image(data)
        rgb = (255 * (rgb - rgb.min()) / (rgb.max() - rgb.min())).astype(np.uint8)

    # save PNG preview
    preview_png = "preview.png"
    Image.fromarray(rgb).save(preview_png)

    # Show preview
    st.subheader("Raster Preview (Computed Colormap Applied)")
    st.image(preview_png, use_container_width=True)

    # Map bounding box conversion
    map_bounds = [
        [bounds.bottom, bounds.left],   # south, west
        [bounds.top, bounds.right]      # north, east
    ]

    st.subheader("Interactive Georeferenced Map")
    m = leafmap.Map(center=[(bounds.top + bounds.bottom) / 2,
                            (bounds.left + bounds.right) / 2],
                    zoom=8)

    # Add PNG layer with exact geospatial bounds
    m.add_image(preview_png, bounds=map_bounds, opacity=0.8, layer_name="Segmentation Map")
    m.to_streamlit(height=700)

    # Add legend
    st.subheader("Legend")
    st.markdown("""
        <div style="display:flex; align-items:center;">
            <div style="width:20px;height:20px;background-color:rgb(0,150,0);margin-right:10px;"></div>
            Non-Deforestation
        </div>
        <div style="display:flex; align-items:center;margin-top:10px;">
            <div style="width:20px;height:20px;background-color:rgb(200,0,0);margin-right:10px;"></div>
            Deforestation
        </div>
    """, unsafe_allow_html=True)
