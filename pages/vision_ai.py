import streamlit as st
from ai_module.ai_models import GeminiVisionQA

st.title("👁️‍🗨️ Netra")
st.subheader("The Vision AI")
qa = GeminiVisionQA()

cam_on = st.toggle("Use Camera", key="use_camera", value=False)
if cam_on:
    uploaded = st.camera_input("Take a picture of the image")
else:
    uploaded = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
prompt = st.chat_input("What do you want to ask about the image?")

if uploaded and prompt:
    img_bytes = uploaded.read()
    with st.spinner("Thinking..."):
        answer = qa.ask_about_image(image=img_bytes, prompt_text=prompt)
    st.write(answer)
