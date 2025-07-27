import streamlit as st
import tempfile
import asyncio
import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ai_module.ai_models import TeacherChatAgent, save_chat_history  # shared LLM + util
from ai_module.rag_utils import extract_text_from_pdf, create_vectorstore, get_custom_rag_chain

# Set up asyncio loop (Python 3.11 fix)
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Streamlit config
st.set_page_config(page_title="Local-Aware RAG with Gemini", layout="centered")
st.title("📄 RAGaBot AI")
# Shared embeddings and LLM from agent
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
chat_agent = TeacherChatAgent()  # initializes shared LLM
llm = chat_agent.llm

# Session state for chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Upload PDF
uploaded_pdf = st.file_uploader("📄 Upload a PDF (Telugu or Multilingual)", type=["pdf"])

if uploaded_pdf:
    with st.spinner("Extracting and indexing PDF..."):
        text = extract_text_from_pdf(uploaded_pdf)

        if not text.strip():
            st.error("No extractable text found.")
            st.stop()
        st.success("PDF text extracted successfully!")
        with tempfile.TemporaryDirectory() as tmpdir:
            vectordb = create_vectorstore(text, embeddings, tmpdir)
            rag_query_fn = get_custom_rag_chain(llm, vectordb)

            # Display previous messages
            for msg in st.session_state["messages"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            # User input
            if prompt := st.chat_input("Ask a question (Telugu/English/mixed)..."):
                st.session_state["messages"].append({"role": "user", "content": prompt})

                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        lc_history = save_chat_history(st.session_state["messages"])
                        response = rag_query_fn(prompt)
                        st.markdown(response)
                        st.session_state["messages"].append({"role": "assistant", "content": response})

