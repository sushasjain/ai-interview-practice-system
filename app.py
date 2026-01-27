import streamlit as st
import random
import os
from groq import Groq

# -----------------------------
# Setup
# -----------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
        "Explain OOP concepts.",
        "What is REST API?",
        "Explain difference between list and tuple.",
        "What is DBMS?"
    ],
    "Managerial Interview": [
        "How do you handle conflict in a team?",
        "Describe a leadership experience.",
        "How do you prioritize tasks?"
    ]
}

# -----------------------------
# Session State
# -----------------------------
if "question" not in st.session_state:
    st.session_state.question = None

if "followup_question" not in st.session_state:
    st.session_state.followup_question = None

if "step" not in st.session_state:
    st.session_state.step = 0  # 0=not started, 1=first answer, 2=followup, 3=evaluation

# -----------------------------
# Interview Selection
# -----------------------------
interview_type = st.selectbox("Select Interview Type", list(INTERVIEW_QUESTIONS.keys()))

if st.button("Generate Interview Question"):
    st.session_state.question = random.choice(INTERVIEW_QUESTIONS[interview_type])
    st.session_state.followup_question = None
    st.session_state.step = 1

# -----------------------------
# Show Main Question
# -----------------------------
if st.session_state.question:
    st.subheader("Interview Question")
    st.write(st.session_state.question)

# -----------------------------
# First Answer
# -----------------------------
if st.session_state.step == 1:
    user_answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):
        if user_answer.strip() == "":
            st.warning("Please write an answer.")
        else:
            # Generate follow-up question using AI
            prompt = f"""
You are an interviewer.

Main Question:
{st.session_state.question}

Candidate Answer:
{user_answer}

Generate ONE relevant follow-up interview question.
Only output the question.
"""
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=100
            )

            st.session_state.followup_question = response.choices[0].message.content.strip()
            st.session_state.first_answer = user_answer
            st.session_state.step = 2

# -----------------------------
# Follow-up Question (Mandatory)
# -----------------------------
if st.session_state.step == 2:
    st.subheader("Follow-up Question")
    st.write(st.session_state.followup_question)

    followup_answer = st.text_area("Your Follow-up Answer")

    if st.button("Submit Follow-up Answer"):
        if followup_answer.strip() == "":
            st.warning("Please answer the follow-up question.")
        else:
            st.session_state.followup_answer = followup_answer
            st.session_state.step = 3

# -----------------------------
# Final AI Evaluation
# -----------------------------
if st.session_state.step == 3:
    st.subheader("⭐ AI Feedback")

    evaluation_prompt = f"""
You are an interview evaluator.

Question:
{st.session_state.question}

Candidate Answer:
{st.session_state.first_answer}

Follow-up Question:
{st.session_state.followup_question}

Follow-up Answer:
{st.session_state.followup_answer}

Provide:

1. Strengths (bullet points)
2. Improvements (bullet points)
3. Ideal Answer (short)
4. Score (0-10)

Format clearly with headings.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": evaluation_prompt}],
        temperature=0.5,
        max_tokens=500
    )

    feedback_text = response.choices[0].message.content

    st.markdown(feedback_text)

    if st.button("Start New Interview"):
        st.session_state.step = 0
        st.session_state.question = None
        st.session_state.followup_question = None
