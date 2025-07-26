import streamlit as st
from ai_module.ai_models import TeacherChatAgent
import re
import json

llm = TeacherChatAgent().llm
def generate_quiz(subject: str, grade: str, num_questions: int):
    prompt = (
        f"Create a multiple choice quiz with {num_questions} questions for grade {grade} on the subject {subject}. "
        "Each question should have 4 options labeled a, b, c, d, and one correct answer. "
        "Format the output as a JSON array of questions with fields: 'question', 'options' (a dict), and 'answer' (the correct option letter)."
    )
    
    response = llm.invoke(input=prompt)
    response = response.to_json()

    json_match = re.search(r"```json\s*(\[\s*[\s\S]*\s*\])\s*```", response['kwargs']['content'])
    if not json_match:
        st.error("Could not find JSON data in the response.")
        return []
    
    json_str = json_match.group(1)
    try:
        quiz_data = json.loads(json_str)
        return quiz_data
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse quiz JSON: {e}")
        return []

def main():
    st.title("Pariksha")
    st.subheader("The Exam Agent")

    subject = st.text_input("Enter Subject (e.g. Math, History)", "Math")
    grade = st.selectbox("Select Grade", [str(i) for i in range(1, 13)], index=4)
    num_questions = st.slider("Number of Questions", min_value=1, max_value=20, value=5)

    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            quiz = generate_quiz(subject, grade, num_questions)
            if quiz:
                st.session_state['quiz'] = quiz
                st.session_state['answers'] = {}
                st.rerun()

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

if __name__ == "__main__":
    main()