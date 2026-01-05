
from colony_detection import DetectColony
import cv2
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# Initialize detectors

colony_detect = DetectColony()

# Colony classes
classes = [
    'B.subtilis',
    'P.aeruginosa',
    'E.coli',
    'S.aureus',
    'C.albicans',
    'Contamination',
    'Defect'
]

# Page configuration
st.set_page_config(
    page_title="Colony Detection Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🔬 Real-Time Colony Detection Dashboard</div>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.header("⚙️ Controls")
    
    # File upload option
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
    
    # Or use default path
    use_default = st.checkbox("Use default image path", value=True)
    if use_default:
        default_path = st.text_input(
            "Image path:", 
            value="/home/muneer/Data/Centerofaicompetetion/system/sp01_img04.jpg"
        )
    
    # Detection button
    detect_button = st.button("🔍 Detect Colonies", type="primary")
    
    st.divider()
    
    # Display settings
    st.subheader("Display Settings")
    show_confidence = st.checkbox("Show confidence scores", value=True)
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
    
    st.divider()
    
    # Info section
    st.subheader("📋 Colony Types")
    for i, colony in enumerate(classes, 1):
        st.text(f"{i}. {colony}")

# Main content area
if detect_button or 'results' in st.session_state:
    
    # Load image
    if uploaded_file is not None:
        # Read uploaded file
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    elif use_default:
        img = cv2.imread(default_path)
    else:
        st.error("Please upload an image or use the default path.")
        st.stop()
    
    if img is None:
        st.error("Failed to load image. Please check the file path or upload.")
        st.stop()
    
    # Run detection
    with st.spinner('🔄 Detecting colonies...'):
        results = colony_detect.detect_colonies(img)
        counts = colony_detect.count_per_class()
        processed_img = colony_detect.post_process(img)
    
    # Store results in session state
    st.session_state['results'] = results
    st.session_state['counts'] = counts
    st.session_state['processed_img'] = processed_img
    st.session_state['original_img'] = img
    
    # Create two columns for layout
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.subheader("🖼️ Detection Results")
        
        # Display tabs for original and processed images
        tab1, tab2 = st.tabs(["Processed Image", "Original Image"])
        
        with tab1:
            # Convert BGR to RGB for display
            processed_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
            st.image(processed_rgb, width='stretch', caption="Detected Colonies")
            
            # Download button
            result_pil = Image.fromarray(processed_rgb)
            st.download_button(
                label="📥 Download Result",
                data=cv2.imencode('.jpg', processed_img)[1].tobytes(),
                file_name="colony_detection_result.jpg",
                mime="image/jpeg"
            )
        
        with tab2:
            original_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            st.image(original_rgb, width='stretch', caption="Original Image")
    
    with col2:
        st.subheader("📊 Colony Count Analysis")
        
        # Create DataFrame
        df = pd.DataFrame(
            list(counts.items()),
            columns=["Colony Type", "Count"]
        )
        
        # Display total count metric
        total_colonies = df['Count'].sum()
        st.metric(
            label="Total Colonies Detected",
            value=total_colonies,
            delta=None
        )
        
        st.divider()
        
        # Bar chart
        st.bar_chart(df.set_index("Colony Type"), height=400, color="#1f77b4")
        
        st.divider()
        
        # Detailed count table
        st.subheader("📋 Detailed Counts")
        
        # Add percentage column
        df['Percentage'] = (df['Count'] / total_colonies * 100).round(1) if total_colonies > 0 else 0
        df['Percentage'] = df['Percentage'].astype(str) + '%'
        
        st.dataframe(
            df,
            width='stretch',
            hide_index=True,
            column_config={
                "Colony Type": st.column_config.TextColumn("Colony Type", width="medium"),
                "Count": st.column_config.NumberColumn("Count", format="%d"),
                "Percentage": st.column_config.TextColumn("Percentage", width="small")
            }
        )
        
        # Export data option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📊 Export Data (CSV)",
            data=csv,
            file_name="colony_counts.csv",
            mime="text/csv"
        )

else:
    # Initial state - show instructions
    st.info("👆 Click 'Detect Colonies' in the sidebar to start analysis")
    
    # Display placeholder
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.subheader("🖼️ Detection Results")
        st.empty()
        st.markdown("*Detected image will appear here*")
    
    with col2:
        st.subheader("📊 Colony Count Analysis")
        st.empty()
        st.markdown("*Bar chart will appear here*")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
    <small>Colony Detection System | Real-time Analysis Dashboard</small>
    </div>
    """,
    unsafe_allow_html=True
)