import io
import base64
import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q
from PIL import Image

# Map string keys to qrcode constants for clean API usage
ERROR_CORRECTION_MAP = {
    "Low (7%)": ERROR_CORRECT_L,
    "Medium (15%)": ERROR_CORRECT_M,
    "Quarter (25%)": ERROR_CORRECT_Q,
    "High (30%)": ERROR_CORRECT_H
}

def process_image_to_base64(uploaded_file, max_size_kb: int = 50) -> str:
    """
    Optimizes and compresses an uploaded image, converting it to a compact 
    Base64 Data URI suitable for QR code embedding.
    """
    img = Image.open(uploaded_file)
    
    # Convert RGBA to RGB if necessary
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    # Smart resizing loop to ensure it fits comfortably within QR payload limits
    quality = 85
    for scale in [1.0, 0.75, 0.5, 0.3]:
        buffer = io.BytesIO()
        width, height = img.size
        resized_img = img.resize((int(width * scale), int(height * scale)), Image.Resampling.LANCZOS)
        resized_img.save(buffer, format="JPEG", quality=quality)
        
        if buffer.tell() <= max_size_kb * 1024 or scale == 0.3:
            encoded_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{encoded_str}"
        quality -= 15
    
    return f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"

def generate_qr_code(data: str, fill_color: str, back_color: str, error_correction: str, box_size: int) -> bytes:
    """
    Generates a QR code completely in-memory and returns the raw bytes.
    """
    qr = qrcode.QRCode(
        version=None,  # Auto-fit data size
        error_correction=ERROR_CORRECTION_MAP.get(error_correction, ERROR_CORRECT_M),
        box_size=box_size,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create the Pillow image object
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Save to an in-memory buffer instead of writing to disk
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
