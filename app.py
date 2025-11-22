import streamlit as st
import leafmap.foliumap as leafmap
import os
import tempfile

st.set_page_config(layout="wide")
st.title("Multi-Day Interactive Map Viewer (SAR / Optical / Fused Data)")

st.write("""
Upload one or more raster maps (GeoTIFF) such as:
- SAR Backscatter
- Optical Data  
- Fused Output  
- DL Segmentation Output (Deforestation / Non-Deforestation)
""")

uploaded_files = st.file_uploader(
    "Upload files here",
    type=["tif", "tiff", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded!")

    # Temporary folder for uploaded rasters
    temp_dir = tempfile.mkdtemp()

    m = leafmap.Map(center=[20.59, 78.96], zoom=4)

    for file in uploaded_files:
        temp_path = os.path.join(temp_dir, file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())

        # Auto-name the layer
        layer_name = os.path.splitext(file.name)[0]

        st.write(f"### Loaded Layer: {layer_name}")

        try:
            m.add_raster(temp_path, layer_name=layer_name)
        except Exception as e:
            st.error(f"Could not load {file.name}: {e}")

    st.subheader("🗺 Interactive Map")
    m.add_layer_control()
    m.to_streamlit(height=700)

else:
    st.info("Upload GeoTIFF files to begin.")

