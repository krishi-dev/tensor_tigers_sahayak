import streamlit as st

st.subheader("AI Agents")

# List of your AI models
ai_models = [
    {"name": "AI Chat", "desc": "Conversational AI assistant."},
    {"name": "AI Summarizer", "desc": "Summarize long texts in seconds."},
    {"name": "AI Story Generator", "desc": "Generate creative stories with AI."},
    {"name": "AI Image Gen", "desc": "Create images from text prompts."},
    {"name": "AI OCR", "desc": "Extract text from images."},
    {"name": "AI Speech Agent", "desc": "Convert speech to text and vice versa."},
    {"name": "AI Exam Agent", "desc": "Answer exam questions using AI."},
    {"name": "AI Game Module", "desc": "Interactive AI-powered games."},
]

# Add CSS for card style
st.markdown("""
<style>
.card {
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(60,60,60,0.1);
    padding: 20px 16px 16px 16px;
    margin-bottom: 24px;
    height: 210px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.card-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #3046C5;
}
.card-desc {
    font-size: 0.96rem;
    color: #323a4d;
    margin-top: 8px;
    margin-bottom: 20px;
    flex-grow: 1;
}
.card-btn {
    display: block;
    width: 100%;
    background: #4361EE;
    color: #fff;
    border: none;
    padding: 10px 0;
    border-radius: 7px;
    font-size: 0.97rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.18s;
}
.card-btn:hover {
    background: #2746B3;
}
</style>
""", unsafe_allow_html=True)

# Display the cards in two rows of four columns
cols_per_row = 4
model_chunks = [ai_models[i:i + cols_per_row] for i in range(0, len(ai_models), cols_per_row)]

for models in model_chunks:
    cols = st.columns(cols_per_row)
    for col, model in zip(cols, models):
        with col:
            st.markdown(f"""
                <div class="card">
                  <div>
                    <div class="card-title">{model['name']}</div>
                    <div class="card-desc">{model['desc']}</div>
                  </div>
                  <form>
                      <button class="card-btn" type="submit">{'Try ' + model['name']}</button>
                  </form>
                </div>
                """, unsafe_allow_html=True)
