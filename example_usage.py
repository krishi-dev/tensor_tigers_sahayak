import streamlit as st
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.class_display import display_classes_card_view, display_class_details
from db_utils import get_db_manager
from pages.exam_agent import generate_quiz

def main():
    st.set_page_config(
        page_title="Sahayak - Class & Exam System",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Sahayak - Class & Exam System")
    st.markdown("Integrated class viewing and exam generation system")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Classes", "Generate Exam", "Class Details"]
    )
    
    if page == "Classes":
        show_classes_page()
    elif page == "Generate Exam":
        show_exam_page()
    elif page == "Class Details":
        show_class_details_page()

def show_classes_page():
    """Display classes page"""
    st.header("📚 Available Classes")
    
    db_manager = get_db_manager()
    if not db_manager:
        st.error("❌ Unable to connect to database.")
        return
    
    try:
        classes = db_manager.fetch_classes()
        if classes:
            display_classes_card_view(classes, "All Classes")
        else:
            st.info("No classes available.")
    finally:
        db_manager.disconnect()

def show_exam_page():
    """Show exam generation page with class integration"""
    st.header("📝 Generate Exam")
    
    # Get classes for subject selection
    db_manager = get_db_manager()
    if not db_manager:
        st.error("❌ Unable to connect to database.")
        return
    
    try:
        classes = db_manager.fetch_classes()
        
        if classes:
            # Extract unique subjects from classes
            subjects = list(set([cls.get('subject', '') for cls in classes if cls.get('subject')]))
            grades = list(set([cls.get('grade', '') for cls in classes if cls.get('grade')]))
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                subject = st.selectbox("Select Subject", subjects) if subjects else st.text_input("Enter Subject", "Math")
            
            with col2:
                grade = st.selectbox("Select Grade", grades) if grades else st.selectbox("Select Grade", [str(i) for i in range(1, 13)], index=4)
            
            with col3:
                num_questions = st.slider("Number of Questions", min_value=1, max_value=20, value=5)
            
            if st.button("Generate Quiz"):
                with st.spinner("Generating quiz..."):
                    quiz = generate_quiz(subject, grade, num_questions)
                    if quiz:
                        st.session_state['quiz'] = quiz
                        st.session_state['answers'] = {}
                        st.rerun()
            
            # Display quiz if available
            if 'quiz' in st.session_state:
                st.header(f"Quiz: {subject} Grade {grade}")
                quiz = st.session_state['quiz']
                answers = st.session_state.get('answers', {})
                
                for i, q in enumerate(quiz):
                    st.write(f"**Q{i+1}. {q['question']}**")
                    options = q['options']
                    answers[i] = st.radio(
                        label=f"Select answer for question {i+1}",
                        options=['a', 'b', 'c', 'd'],
                        format_func=lambda x: f"{x}. {options[x]}",
                        key=f"q{i}"
                    )
                st.session_state['answers'] = answers
                
                if st.button("Submit Answers"):
                    score = 0
                    for i, q in enumerate(quiz):
                        if answers.get(i) == q['answer']:
                            score += 1
                    st.success(f"You scored {score} out of {len(quiz)}")
                    
                    st.subheader("Detailed Results")
                    for i, q in enumerate(quiz):
                        user_ans = answers.get(i)
                        correct = q['answer']
                        is_correct = user_ans == correct
                        st.write(f"**Q{i+1}:** {q['question']}")
                        st.write(f"Your answer: {user_ans} - {q['options'][user_ans]}")
                        st.write(f"Correct answer: {correct} - {q['options'][correct]}")
                        st.write("✅ Correct" if is_correct else "❌ Incorrect")
                        st.write("---")
        else:
            st.info("No classes available for exam generation.")
            
    finally:
        db_manager.disconnect()

def show_class_details_page():
    """Show class details page"""
    st.header("🔍 Class Details")
    
    db_manager = get_db_manager()
    if not db_manager:
        st.error("❌ Unable to connect to database.")
        return
    
    try:
        classes = db_manager.fetch_classes()
        if classes:
            selected_class = st.selectbox(
                "Select a class for details:",
                options=classes,
                format_func=lambda x: f"{x.get('name', 'Unknown')} - Grade {x.get('grade', 'N/A')} - {x.get('subject', 'N/A')}"
            )
            
            if selected_class:
                display_class_details(selected_class)
                
                # Add exam generation for this specific class
                st.markdown("---")
                st.subheader("Generate Exam for This Class")
                
                if st.button(f"Generate {selected_class.get('subject', 'Subject')} Quiz"):
                    subject = selected_class.get('subject', 'Math')
                    grade = selected_class.get('grade', '5')
                    
                    with st.spinner("Generating quiz..."):
                        quiz = generate_quiz(subject, grade, 5)
                        if quiz:
                            st.session_state['class_quiz'] = quiz
                            st.session_state['class_answers'] = {}
                            st.rerun()
                
                # Display class-specific quiz
                if 'class_quiz' in st.session_state:
                    st.subheader(f"Quiz for {selected_class.get('name', 'Class')}")
                    quiz = st.session_state['class_quiz']
                    answers = st.session_state.get('class_answers', {})
                    
                    for i, q in enumerate(quiz):
                        st.write(f"**Q{i+1}. {q['question']}**")
                        options = q['options']
                        answers[i] = st.radio(
                            label=f"Select answer for question {i+1}",
                            options=['a', 'b', 'c', 'd'],
                            format_func=lambda x: f"{x}. {options[x]}",
                            key=f"class_q{i}"
                        )
                    st.session_state['class_answers'] = answers
                    
                    if st.button("Submit Class Quiz"):
                        score = 0
                        for i, q in enumerate(quiz):
                            if answers.get(i) == q['answer']:
                                score += 1
                        st.success(f"You scored {score} out of {len(quiz)}")
        else:
            st.info("No classes available.")
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    main() 