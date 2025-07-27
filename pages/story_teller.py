import streamlit as st
from ai_module.gcloud_services import GoogleTTS
from ai_module.ai_models import TeacherChatAgent

# Initialize agents
llm = TeacherChatAgent()
tts = GoogleTTS()

# Function to generate a story based on user input
def generate_story(query: str) -> str:
    """Generates a story based on the user query."""
    try:
        # Check if query is not empty
        if not query.strip():
            raise ValueError("Query cannot be empty!")
        
        story = llm.chat("Generate a Story on the query: " + query)
        return story
    except Exception as e:
        st.error(f"❌ Error generating story: {str(e)}")
        return None

# Function to handle text-to-speech synthesis
def synthesize_speech(text: str, language_code: str = "te") -> bytes:
    """Generates speech for a given text."""
    try:
        audio_data = tts.synthesize(text, language_code=language_code)
        return audio_data
    except Exception as e:
        st.error(f"❌ TTS Error: {str(e)}")
        return None

# Main interaction UI
def main():

    st.title("Chandamama AI")

    # Initialize session state variables if they don't exist
    if 'story' not in st.session_state:
        st.session_state['story'] = None
    if 'audio_data' not in st.session_state:
        st.session_state['audio_data'] = None
    if 'user_query' not in st.session_state:
        st.session_state['user_query'] = None

    # User input
    query = st.chat_input("Ask about a story")

    # If query is provided
    if query:
        # Store the query in session state
        st.session_state['user_query'] = query
        st.write(f"**Your Query**: {st.session_state['user_query']}")
        
        # Generate story
        story = generate_story(query)
        
        if story:
            # Store the generated story in session state
            st.session_state['story'] = story

            # Convert story to bytes for download
            text_bytes = story.encode('utf-8')

            # Store audio data in session state
            audio_data = synthesize_speech(story)
            if audio_data:
                st.session_state['audio_data'] = audio_data

            # Display the user's query and the generated story
            st.write(f"**Generated Story**:\n{st.session_state['story']}")

            # Create columns for download and audio playback
            col_dl, col_audio = st.columns([1, 1])

            # Provide download option for the story text
            with col_dl:
                st.download_button(
                    label="📥 Download Text",
                    data=text_bytes,
                    file_name="generated_story.txt",
                    mime="text/plain"
                )

            # Provide audio playback option
            with col_audio:
                st.audio(st.session_state['audio_data'], format="audio/mp3")
                # if st.button("🔊 Read Aloud"):
                #     if st.session_state['audio_data']:
                #         st.audio(st.session_state['audio_data'], format="audio/mp3")

if __name__ == "__main__":
    main()
