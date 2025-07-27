import streamlit as st
import streamlit.components.v1 as components

st.set_page_config("Sahayak", page_icon="⚡", layout="wide")

# st.title("Sahayak")
google_translate_code = """
<div id="google_translate_element"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement(
    {pageLanguage: 'en'}, 'google_translate_element'
  );
}
</script>
<script type="text/javascript"
  src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit">
</script>
"""

# components.html(google_translate_code, height=100)
with st.sidebar:
    st.title("Sahayak AI")
    st.caption("Version V1.0 (Beta)")
pg = st.navigation(
        pages=[
        st.Page(page="pages/dashboard.py", title="Dashboard", icon="🏠"),
        st.Page(page="pages/tutor.py", title="Sahayak AI", icon="⚡"),
        # st.Page(page="pages/classes.py", title="Classes"),
        # st.Page(page="pages/ai_agents.py", title="Ai Agents"),
        st.Page(page="pages/image_generation.py", title="Image Generation", icon="🎨"),
        st.Page(page="pages/multi_rag.py", title="Multi RAG", icon="📝"),
        st.Page(page="pages/OCR.py", title="OCR", icon="📸"),
        st.Page(page="pages/vision_ai.py", title="Vision AI", icon="👁️‍🗨️"),
        st.Page(page="pages/audio_assess.py", title="Audio Assessment", icon="🎤"),
        st.Page(page="pages/exam_agent.py", title="Exam Agent", icon="💯"),
        st.Page(page='pages/game_generator.py', title="Game Generator", icon="🎮"),
        st.Page(page="pages/story_teller.py", title="Story Teller", icon="🌝"),

    ]
)

pg.run()