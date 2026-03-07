import streamlit as st
import random
import os
import google.generativeai as genai

# -----------------------------
# Configure Gemini API
# -----------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="AI Interview Practice System", layout="centered")

st.title("🎤 AI Interview Practice System")
st.write("Practice HR, Technical, and Managerial interviews using AI.")

# -----------------------------
# Question Bank
# -----------------------------
INTERVIEW_QUESTIONS = {
    "HR Interview": [
        "Tell me about yourself.",
        "Why should we hire you?",
        "Where do you see yourself in 5 years?",
        "What are your strengths and weaknesses?"
    ],
    "Technical Interview": [
        "Explain Object-Oriented Programming principles.",
        "What is the difference between a process and a thread?",
        "Explain REST API.",
        "What is a database index?"
    ],
    "Managerial Interview": [
        "How do you prioritize tasks?",
        "Describe a time you resolved a team conflict.",
        "How do you manage tight deadlines?",
        "How do you motivate team members?"
    ]
}

# -----------------------------
# AI Function
# -----------------------------
def ask_ai(prompt):
    response = model.generate_content(prompt)
    return response.text


# -----------------------------
# Interview Type
# -----------------------------
interview_type = st.selectbox(
    "Select Interview Type",
    list(INTERVIEW_QUESTIONS.keys())
)

# -----------------------------
# Generate Question
# -----------------------------
if st.button("Generate Interview Question"):
    question = random.choice(INTERVIEW_QUESTIONS[interview_type])
    st.session_state["question"] = question

# -----------------------------
# Show Question
# -----------------------------
if "question" in st.session_state:
    st.subheader("Interview Question")
    st.write(st.session_state["question"])

# -----------------------------
# User Answer
# -----------------------------
user_answer = st.text_area("Your Answer")

# -----------------------------
# Submit Answer
# -----------------------------
if st.button("Submit Answer"):

    if user_answer and "question" in st.session_state:

        question = st.session_state["question"]

        # -------- AI Evaluation Prompt --------
        feedback_prompt = f"""
        Interview Question: {question}

        Candidate Answer: {user_answer}

        Evaluate this interview answer professionally.

        Provide:

        Strengths:
        Improvements:
        Score out of 10:
        """

        feedback = ask_ai(feedback_prompt)

        st.subheader("⭐ AI Feedback")
        st.write(feedback)

        # -------- Follow-up Question --------
        followup_prompt = f"""
        Based on the interview question:

        {question}

        and the candidate answer:

        {user_answer}

        Generate a realistic follow-up interview question.
        """

        followup = ask_ai(followup_prompt)

        st.subheader("Follow-up Question")
        st.write(followup)