import streamlit as st
from ai_module.ai_models import ImageSceneGenerator  # Adjust if filename is different
from PIL import Image
import io, os

# Initialize image generator once
if "img_gen" not in st.session_state:
    st.session_state.img_gen = ImageSceneGenerator()

st.title("🎨 AI Kala Vedhika")

st.markdown("""
This tool uses **Vertex AI Imagen** to turn scene prompts into beautiful images.
Write story scenes or topic descriptions below.
""")

# Prompt input
default_prompt = """
Scene: Explain about Newton's Third Law in a cartoon story way
Image Prompt: cartoon type, story depection
"""
s1, s2 = st.columns([0.7, 0.3])
with s1:
    prompt_input = st.text_area("📝 Describe your scene(s):", value=default_prompt, height=300)
with s2:
    num_images = st.slider("🖼️ Number of images", 1, 6, 1)
    aspect_ratio = st.selectbox("📐 Aspect ratio", ["1:1", "4:3", "16:9"])
generate_button = st.button("🚀 Generate Images")

if generate_button and prompt_input.strip():
    with st.spinner("Generating images..."):
        try:
            response = st.session_state.img_gen.generate_images(
            prompt=prompt_input,
            number_of_images=num_images,
            aspect_ratio=aspect_ratio
        )
            images = response.images  # list of GeneratedImage
            st.write(f"Generated {len(images)} images.")
            img_list = []
            for i, img in enumerate(images):
                img.save(f"scene_{i + 1}.png")
                image = Image.open(f"scene_{i + 1}.png")
                img_list.append(image)
            # Display images in a grid
            cols = st.columns(min(len(img_list), 3))
            for i, img in enumerate(img_list):
                with cols[i % len(cols)]:
                    st.image(img, caption=f"Image {i + 1}", use_container_width=False, width=400)

                    # Download button
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format="PNG")
                    st.download_button(
                        label="⬇️ Download",
                        data=img_bytes.getvalue(),
                        file_name=f"scene_{i + 1}.png",
                        mime="image/png"
                    )
                    os.remove(f"scene_{i + 1}.png")  # Clean up saved images after display
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
