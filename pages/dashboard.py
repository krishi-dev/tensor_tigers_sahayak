import streamlit as st

if "username" not in st.session_state:
    st.session_state.username = "Pavan"

st.title(f"Welcome {st.session_state.username}")

main_cols = st.columns([0.7, 0.3])
with main_cols[0]:
    st.subheader("Your Classes")
    subjects = ["Math", "Science", "History"]
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"Class {i + 1}")
                st.markdown(f"Subject: {subjects[i]}")
                st.button("View Class", key=f"join_class_{i + 1}", type="primary")
    
with main_cols[1]:
    st.subheader("Your History")