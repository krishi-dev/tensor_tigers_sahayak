import os
import uuid
import time
import datetime
import streamlit as st
from ai_module.ai_models import TeacherChatAgent

if "history" not in st.session_state:
    st.session_state.history = []

if 'username' not in st.session_state:
    st.session_state.username = "Pavan"

def create_user_folder():
    base_dir = 'user_sessions'
    
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    t = datetime.datetime.now().strftime("%d-%m-%Y_%I-%M")
    user_id = f"{st.session_state.username}{str(uuid.uuid4())[:8]}{t}"
    user_folder = os.path.join(base_dir, user_id)
    os.makedirs(user_folder)
    
    return user_folder

if 'user_folder' not in st.session_state:
        st.session_state.user_folder = create_user_folder()

def save_chat_to_file(user_folder, chat_history):
    file_path = os.path.join(user_folder, 'chat_history.txt')
    with open(file_path, 'w') as f:
        for message in chat_history:
            if message['role'] == "user":
                f.write(f"{message['role']}: {message['content']}\n")
            elif message['role'] == "assistant":
                f.write(f"{message['role']}: {message['content']}")



def generate_response(query):
    llm = TeacherChatAgent()
    response = llm.chat(user_input=query, history=st.session_state.history[-5::])    
    return response       

st.title("⚡ Sahayak")
st.markdown("Ask Sahayak Anything..")
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        if isinstance(message['content'], dict) and 'output' in message['content']:
            st.write(message['content']['output'])
        else:
            st.write(message['content'])

if query := st.chat_input("Ask something"):
    st.session_state.history.append({"role": "user", "content": query})
    
    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Processing ..."):
        st_time = time.time()
        try:
            response = generate_response(query)
        except Exception as e:
            response = {'output':f'Error generating response, please try again {e}'}
        st.toast(f"Response in {(time.time() - st_time):.2f} seconds")

    st.session_state.history.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
            
        st.write(response['output'])
        response_time = f"{(time.time() - st_time):.2f}"
        st.markdown(f"<p style='font-size:10px;'> Response in {response_time} seconds </p>" , unsafe_allow_html= True)
        save_chat_to_file(st.session_state.user_folder, st.session_state.history)