import streamlit as st
import openai

# Use secret key in Streamlit Cloud (don’t expose here!)
openai.api_key = st.secrets["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"]

st.title("🧠 AI Quiz Generator")
st.markdown("Generate AI-powered MCQ quizzes. Just enter a topic and difficulty level.")

topic = st.text_input("Enter a topic (e.g., Python, WWII, Algebra)")
level = st.selectbox("Choose difficulty level", ["Beginner", "Intermediate", "Advanced"])

if st.button("Generate Quiz"):
    with st.spinner("Generating quiz..."):
        prompt = (
            f"Generate 3 MCQs on '{topic}' for a {level} level learner. "
            "Each question should have 4 options and one correct answer."
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            quiz = response['choices'][0]['message']['content']
            st.markdown("### 📄 Quiz")
            st.markdown(quiz)
        except Exception as e:
            st.error("Something went wrong. Check your API key or try again.")
