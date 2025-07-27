# st_game.py
import streamlit as st
import subprocess
import sys
import os
from gamemodule.game_generator import generate_game_code

st.set_page_config(layout="wide")
st.title("🎮 Kreda AI")
st.markdown("Web-Ready 2D Game Generator")

st.write("Enter a context (e.g., 'waste management') to generate a playable 2D Game.")

context = st.text_input("Game Context", "waste management")

if st.button("Generate Game"):
    if context:
        code = generate_game_code(context)
        if code:
            st.session_state.game_code = code
            st.success("Game code generated successfully!")
        else:
            st.error("Failed to generate game code.")

# Show generated HTML game
if 'game_code' in st.session_state:
    # st.subheader("Generated Game Code (HTML + JavaScript)")
    # st.code(st.session_state.game_code, language='html')

    game_filename = f"{context.replace(' ', '_')}_game.html"
    game_folder = "web_game"
    os.makedirs(game_folder, exist_ok=True)
    game_path = os.path.join(game_folder, game_filename)

    # Save HTML game file
    with open(game_path, "w", encoding="utf-8") as f:
        f.write(st.session_state.game_code)

    # Provide download
    st.download_button(
        label="Download HTML Game",
        data=st.session_state.game_code,
        file_name=game_filename,
        mime="text/html"
    )

    # Render the game inside Streamlit
    st.markdown("### Live Preview")
    try:
        st.components.v1.html(st.session_state.game_code, height=600, scrolling=True)
    except Exception as e:
        st.error(f"Error rendering game: {e}")