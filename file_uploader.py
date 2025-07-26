import streamlit as st
from ai_module.pdf_rag import create_rag_db
import os
import uuid
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
load_dotenv(".env", override=False)
os.environ["GOOGLE_API_KEY"] = os.environ['GOOGLE_API_KEY']


if 'temp_dir' not in st.session_state:
    # Create a temporary directory to store uploaded files
    temp_dir = f"temp_uploads_{uuid.uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)
    st.session_state['temp_dir'] = temp_dir

if 'pdf_file' not in st.session_state:
    st.session_state['pdf_file'] = []

if 'rag_db' not in st.session_state:
    st.session_state['rag_db'] = None

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

state = st.session_state

def create_user_folder():
    if 'user_folder' not in state:
        user_folder = f"user_data_{uuid.uuid4()}"
        os.makedirs(user_folder, exist_ok=True)
        state.user_folder = user_folder
        st.success(f"User folder created: {user_folder}")
    return state.user_folder

def process_pdf_files(uploaded_files):
    all_chunks = []
    file_names = []
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, dir=state.temp_dir) as temp_file:
            temp_file.write(file.getvalue())
            temp_file_path = temp_file.name

        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()
        for doc in documents:
            doc.metadata['source'] = file.name
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        all_chunks.extend(docs)
        file_names.append(file.name)
        os.remove(temp_file_path)

    if all_chunks:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectordb = Chroma.from_documents(
            documents=all_chunks,
            embedding=embeddings,
            persist_directory=state.temp_dir
        )
        state.rag_db = vectordb
        st.success(f"Processed {len(all_chunks)} chunks from {len(uploaded_files)} files: {', '.join(file_names)}")
        return list(set(file_names))
    return []

files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
if files and st.button("Process PDFs"):
    with st.spinner("Processing PDFs..."):
        state.pdf_file = process_pdf_files(files)
        st.success("PDF files processed successfully.")

if state.rag_db:
    st.subheader("Query the RAG Database")

    for message in state.message_history:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if user_query := st.chat_input("Ask a question about the uploaded PDFs"):
        state.message_history.append({"role": "user", "content": user_query})

        with st.chat_message("assistant"):
            with st.spinner("Retrieving information..."):
                retriever = state.rag_db.as_retriever(search_kwargs={"k": 2})
                retrieved_docs = retriever.invoke(user_query)

                if retrieved_docs:
                    response = retrieved_docs[0].page_content
                    st.markdown(response)
                    state.message_history.append({"role": "assistant", "content": response})
                else:
                    st.markdown("No relevant information found.")
                    state.message_history.append({"role": "assistant", "content": "No relevant information found."})
    