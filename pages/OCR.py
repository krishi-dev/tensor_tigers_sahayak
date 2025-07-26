import streamlit as st
import os
import tempfile
from PIL import Image
import io
from ai_module.gcloud_services import GoogleOCR, GoogleTTS  # <-- Replace with your actual import path

# Streamlit page configuration
st.set_page_config(
    page_title="OCR Text Extractor",
    page_icon="📷",
    layout="wide"
)

# Initialize Google Cloud services
ocr = GoogleOCR()
tts = GoogleTTS()

# Title and description
st.title("📷 Akshara")
st.subheader("OCR Text Extractor")
st.markdown("Upload an image or take a picture to extract text using Google Cloud Vision API and convert to audio using TTS.")

# UI: Image input section
col1, col2 = st.columns([1, 1])

with col1:
    use_camera = st.toggle("📸 Use Camera")
    if use_camera:
        uploaded_file = st.camera_input("Take a picture of text")
    else:
        st.subheader("📤 Upload an Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
            help="Upload an image containing text to extract"
        )

    if uploaded_file:
        # Display the uploaded image
        st.subheader("📷 Preview")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # File info
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.info(f"File size: {file_size_mb:.2f} MB")

with col2:
    st.subheader("📝 OCR Results")

    if uploaded_file:
        with st.spinner("🔍 Extracting text using Google Vision..."):
            try:
                # Save uploaded image temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_image_path = tmp_file.name

                result = ocr.extract_text(temp_image_path)
                extracted_text = result.get("text", "")
                annotations = result.get("raw_response").text_annotations
                os.remove(temp_image_path)

                if extracted_text:
                    detected_lang = annotations[0].locale if annotations else "en-US"
                    st.success("✅ Text extracted successfully!")
                    st.caption(f"Detected Language: `{detected_lang}`")

                    # Display extracted text
                    st.text_area(
                        label="Extracted Text",
                        value=extracted_text,
                        height=300,
                        help="You can copy or download this text"
                    )

                    # Download + Audio options
                    text_bytes = extracted_text.encode('utf-8')
                    col_dl, col_audio = st.columns([1, 1])
                    with col_dl:
                        st.download_button(
                            label="📥 Download Text",
                            data=text_bytes,
                            file_name="extracted_text.txt",
                            mime="text/plain"
                        )

                    with col_audio:
                        if st.button("🔊 Read Aloud"):
                            try:
                                audio_data = tts.synthesize(extracted_text, language_code=detected_lang)
                                st.audio(audio_data, format="audio/mp3")
                            except Exception as e:
                                st.error(f"❌ TTS Error: {str(e)}")

                    # Stats
                    st.metric("📄 Words", len(extracted_text.split()))
                    st.metric("🔠 Characters", len(extracted_text))

                else:
                    st.warning("⚠️ No text detected in the image.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Ensure your Google Cloud credentials are configured.")
    else:
        st.info("👆 Upload or capture an image to get started.")
