import streamlit as st
import cv2  # OpenCV - Video aur image processing ke liye
import tempfile # Temporary file banane ke liye
import numpy as np
from PIL import Image

# Setup Page - Layout ko "wide" karenge taaki dashboard jaisa feel aaye
st.set_page_config(page_title="Kisan Sahayak", page_icon="🌾", layout="wide")

# ---- SIDEBAR NAVIGATION ----
st.sidebar.title("🌾 Kisan Sahayak")
st.sidebar.write("Aapka Digital Krishi Mitra")
st.sidebar.divider()
app_mode = st.sidebar.radio("Navigation", ["🌿 Plant Disease Detector", "🐄 Dairy Farm Manager"])

# ---- MAIN AREA: PLANT DISEASE DETECTOR ----
if app_mode == "🌿 Plant Disease Detector":
    st.title("🌿 Plant Disease Detector")
    st.write("Fasal ki bimari pehchanein aur upay payein.")
    
    # Do columns banayenge: Left me upload, Right me result
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Photo/Video Daalein")
        uploaded_file = st.file_uploader("Yahan patte ki photo ya video upload karein", type=["jpg", "png", "mp4", "mov"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension in ['mp4', 'mov']:
            with col1:
                st.video(uploaded_file)
            
            with col2:
                st.subheader("2. AI Analysis Result")
                if st.button("Video Analyze Karein", use_container_width=True):
                    with st.spinner("Video analyze ho raha hai... kripya rukiye."):
                        tfile = tempfile.NamedTemporaryFile(delete=False) 
                        tfile.write(uploaded_file.read())
                        cap = cv2.VideoCapture(tfile.name)
                        frame_count = 0
                        
                        while cap.isOpened():
                            ret, frame = cap.read()
                            if not ret: break
                            frame_count += 1
                            
                            if frame_count % 30 == 0:
                                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                img = Image.fromarray(rgb_frame)
                                # Yahan model prediction code aayega
                        cap.release()
                        
                    # UI mein result dikhane ka accha tareeqa (Metrics aur Success box)
                    st.success("✅ Analysis Poori Hui!")
                    
                    # 3 columns for metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Bimari ka Naam", "Early Blight")
                    m2.metric("Confidence", "94.7%")
                    m3.metric("Khatra", "High", delta="- Action Needed", delta_color="inverse")
                    
                    st.info("💡 **Ilaaj (Organic):**\n1. Neem oil ka spray karein.\n2. Sankramit patto ko turant hata dein.")
                    
                    st.warning("⚠️ **Kisan Bhaiyon ke liye Sandesh:** Yeh AI ki jankari hai. Kripya **KVK (Krishi Vigyan Kendra)** se zaroor verify karein.")
        else:
            with col1:
                st.image(uploaded_file, use_container_width=True, caption="Uploaded Image")
            with col2:
                st.info("Image aane par prediction UI yahan chalega.")

# ---- MAIN AREA: DAIRY FARM MANAGER ----
elif app_mode == "🐄 Dairy Farm Manager":
    st.title("🐄 Dairy Farm Manager")
    
    # Dairy dashboard UI metrics
    st.subheader("Aaj ka Dashboard")
    d_col1, d_col2, d_col3 = st.columns(3)
    d_col1.metric("Total Doodh (Liters)", "145 L", "5 L (kal se zyada)")
    d_col2.metric("Aaj ki Kamai", "₹ 5,800", "₹ 200 (kal se zyada)")
    d_col3.metric("Bimar Pashu", "0", "Sab swasth hain!")
    
    st.divider()
    st.write("Agla hissa jaldi jodenge...")
