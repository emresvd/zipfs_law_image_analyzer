import streamlit as st
from PIL import Image
from zipf_image_analyzer import analyze_zipf_from_image

st.set_page_config(page_title="Zipf Image Analyzer", layout="wide")

st.title("Zipf's Law Image Analyzer")
st.markdown("Upload an image to analyze its color distribution against Zipf's Law.")

# Sidebar controls
st.sidebar.header("Analysis Settings")
scale_factor = st.sidebar.slider("Scale Factor", min_value=0.1, max_value=1.0, value=1.0, step=0.1, help="Reduce image resolution to analyze at a different scale.")
bits_per_channel = st.sidebar.slider("Color Depth (Bits)", min_value=1, max_value=8, value=8, step=1, help="Reduce color depth to group similar colors together.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp", "bmp", "gif", "tiff"])

if uploaded_file is not None:
    # Read the image
    img = Image.open(uploaded_file).convert("RGB")
    
    # Display the input image
    st.subheader("Input Image")
    st.image(img, caption="Original Image", use_container_width=True)
    
    st.write("Analyzing...")
    
    # Run analysis
    try:
        fig, num_colors = analyze_zipf_from_image(img, scale_factor=scale_factor, bits_per_channel=bits_per_channel)
        
        st.subheader("Results")
        st.write(f"**Total Unique Colors (at this scale & depth):** {num_colors}")
        
        # Display plot
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error during analysis: {e}")
else:
    st.info("Please upload an image to begin.")
