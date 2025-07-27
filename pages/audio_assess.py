import streamlit as st
from streamlit_mic_recorder import speech_to_text
from ai_module.ai_models import TeacherChatAgent


# --- Initialize LLM (reuse your earlier setup) ---
llm = TeacherChatAgent().llm

# --- Reference prompt (speech to memorize/read) ---
REFERENCE_SPEECH = """
Good morning everyone. My name is [Your Name], and today I will talk about the importance of education. 
Education helps people learn new things, solve problems, and achieve their goals. 
It opens doors to many opportunities and helps us grow as individuals. 
Thank you for listening to my speech.
"""

def get_evaluation_prompt(reference_text: str, speech_text: str) -> str:
    """Generate the evaluation prompt for the LLM based on reference and spoken text."""
    return f"""
You are an English teacher grading a 5th-grade student's speech performance.

This is the reference speech for them to read or memorize:
----
{reference_text}
----

Here is the student's actual spoken version:
----
{speech_text}
----

Please compare the student's speech to the reference. Consider:
- Accuracy (did they say the same words/ideas?)
- Content (did they include all main points?)
- Structure (was the order or structure kept?)
- Clarity and grammar
- Confidence and delivery

List differences (things missed, added, or changed) in a few bullet points.
Then, give a friendly, encouraging progress report for a 5th grader with praise and suggestions.
Finish with a total score out of 10.

Use clear, simple language.

also generete the score card in json format with all the evalution matrixs
"""

def evaluate_speech(reference_text: str, speech_text: str) -> str:
    """Call the LLM with evaluation prompt and return feedback text."""
    prompt = get_evaluation_prompt(reference_text, speech_text)
    response = llm.invoke(prompt)
    # st.write(response)
    return response.content.strip()

# --- Streamlit UI ---
st.title("🎤 Sabddha AI")
st.subheader("Speech to Text Evaluation")
# st.markdown("Practice your speech and get instant feedback!")

# Initialize chat history list in session_state
if 'text_received' not in st.session_state:
    st.session_state['text_received'] = []

st.write(REFERENCE_SPEECH)

# Speech-to-text input
spoken_text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

if spoken_text:
    st.session_state['text_received'].append(spoken_text)
    with st.spinner("Evaluating your speech..."):
        feedback = evaluate_speech(REFERENCE_SPEECH, spoken_text)
    st.subheader("Evaluation Result")
    st.markdown(feedback)
else:
    st.info("🎧 Please record your speech to get started.")

# Optionally show history
if st.session_state['text_received']:
    st.markdown("### Your Spoken Attempts History:")
    for i, t in enumerate(st.session_state['text_received'], 1):
        st.markdown(f"**Attempt {i}:** {t}")
