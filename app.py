import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.title("Interactive Map Viewer (SAR / Optical / Fused Data)")

st.write("Upload a map file to visualize (GeoTIFF, PNG, JPG).")

uploaded_file = st.file_uploader("Upload file", type=["tif", "tiff", "png", "jpg", "jpeg"])

if uploaded_file:
    # Save file temporarily
    temp_filename = f"temp_{uploaded_file.name}"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Create map object
    m = leafmap.Map(center=[20.59, 78.96], zoom=4)

    try:
        m.add_raster(temp_filename, layer_name="Uploaded Map")
    except Exception as e:
        st.error(f"Could not load raster: {e}")

    st.subheader("Interactive Map")
    m.to_streamlit(height=700)
