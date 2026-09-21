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

st.sidebar.header("Plot Settings")
log_scale_x = st.sidebar.checkbox("X-Axis Log Scale", value=True)
log_scale_y = st.sidebar.checkbox("Y-Axis Log Scale", value=True)
show_ref_line = st.sidebar.checkbox("Show Zipf Reference Line", value=True)
show_grid = st.sidebar.checkbox("Show Grid", value=True)
marker_style = st.sidebar.selectbox("Marker Style", options=['o', '.', 'x', '+', '*', 'None'], index=0)
top_n = st.sidebar.number_input("Limit Top N Colors (0 for all)", min_value=0, value=0, step=100)

uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png", "webp", "bmp", "gif", "tiff"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown(f"---")
        st.markdown(f"### {uploaded_file.name}")
        
        # Read the image
        img = Image.open(uploaded_file).convert("RGB")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Display the input image
            st.subheader("Input Image")
            st.image(img, use_container_width=True)
        
        with col2:
            st.subheader("Results")
            # Run analysis
            with st.spinner("Analyzing..."):
                try:
                    fig, num_colors = analyze_zipf_from_image(
                        img, 
                        scale_factor=scale_factor, 
                        bits_per_channel=bits_per_channel,
                        log_scale_x=log_scale_x,
                        log_scale_y=log_scale_y,
                        show_ref_line=show_ref_line,
                        show_grid=show_grid,
                        marker_style=marker_style,
                        top_n=top_n
                    )
                    
                    st.write(f"**Total Unique Colors (at this scale & depth):** {num_colors}")
                    
                    # Display plot
                    st.pyplot(fig)
                    
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
else:
    st.info("Please upload one or more images to begin.")
