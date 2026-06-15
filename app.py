import streamlit as st
from qr_logic import generate_qr_code, process_image_to_base64

# Page configuration
st.set_page_config(
    page_title="Enterprise QR Code Studio",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Enterprise QR Code Studio")
st.write("Generate highly optimized, clean QR codes for any data format instantly.")
st.write("---")

# Use columns to separate controls from the preview output
col_controls, col_preview = st.columns([1, 1], gap="large")

with col_controls:
    st.subheader("1. Configure Payload")
    data_type = st.selectbox(
        "Select Data Type",
        ["URL or Text", "Wi-Fi Network", "Image (Compressed Base64)"]
    )
    
    payload = ""
    
    if data_type == "URL or Text":
        payload = st.text_area("Enter Text or URL", placeholder="https://github.com/yourprofile")
        
    elif data_type == "Wi-Fi Network":
        ssid = st.text_input("Wi-Fi SSID (Network Name)")
        password = st.text_input("Password", type="password")
        encryption = st.selectbox("Encryption Type", ["WPA", "WEP", "nopass"])
        if ssid:
            # Formats according to standard Wi-Fi QR specifications
            payload = f"WIFI:S:{ssid};T:{encryption};P:{password};;"
            
    elif data_type == "Image (Compressed Base64)":
        st.warning("⚠️ High capacity QR codes (like images) require 'High' error correction and modern scanners.")
        uploaded_image = st.file_file = st.file_uploader("Upload Image (PNG/JPG)", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            with st.spinner("Compressing and encoding image..."):
                try:
                    payload = process_image_to_base64(uploaded_image)
                    st.success(f"Image successfully encoded! String size: {len(payload)} bytes")
                except Exception as e:
                    st.error(f"Error processing image: {e}")

    st.subheader("2. Visual Styling")
    # Expanding advanced options cleanly
    with st.expander("Custom Colors & Parameters", expanded=True):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fill_color = st.color_picker("Foreground Color", "#000000")
            error_corr = st.selectbox("Error Correction", ["Low (7%)", "Medium (15%)", "Quarter (25%)", "High (30%)"], index=1)
        with col_c2:
            back_color = st.color_picker("Background Color", "#FFFFFF")
            box_size = st.slider("Scale (Box Size)", min_value=5, max_value=25, value=10, step=1)

with col_preview:
    st.subheader("3. Live Production Preview")
    
    if payload:
        try:
            # Generate the QR Code dynamically based on configuration
            qr_bytes = generate_qr_code(
                data=payload,
                fill_color=fill_color,
                back_color=back_color,
                error_correction=error_corr,
                box_size=box_size
            )
            
            # Display centered preview image
            st.image(qr_bytes, width=380, caption="Scan with your smartphone camera")
            
            # Actionable Download Button referencing the raw byte array
            st.download_button(
                label="📥 Download Production-Ready PNG",
                data=qr_bytes,
                file_name="generated_qr_code.png",
                mime="image/png",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Failed to generate QR code. The payload might be too large for the selected parameters. Error: {e}")
    else:
        st.info("Provide data in the configuration panel to generate your QR live preview.")
