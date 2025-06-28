import streamlit as st
from transformers import pipeline
import re

st.set_page_config(page_title="AI Quiz Generator", page_icon="🧠")
st.title("🧠 AI Quiz Generator (GPT2)")
st.markdown("Generate MCQs on any topic and difficulty using Hugging Face GPT2.")

# Load GPT2 model once
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

generator = load_model()

# Topic and Difficulty selection
topic = st.selectbox("Choose Topic", ["Python", "C++", "Java", "DBMS", "SQL", "OOP"])
difficulty = st.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Advanced"])

# Button to trigger quiz generation
if st.button("Generate Quiz"):
    with st.spinner("Generating quiz... please wait"):
        prompt = f"Generate 3 MCQs on the topic '{topic}' for {difficulty} level learners. Each question should have 4 options (a, b, c, d) and indicate the correct answer at the end."
        try:
            result = generator(prompt, max_new_tokens=300)[0]["generated_text"]
            output = result.replace(prompt, "").strip()

            # Parse the output to structured format
            questions = re.split(r'\d+\.', output)[1:]  # Split by question numbers
            quiz_data = []

            for q in questions:
                parts = re.split(r'[a-d]\)', q)
                if len(parts) < 5:
                    continue  # skip malformed
                question_text = parts[0].strip()
                options = [f"{chr(97+i)}) {opt.strip()}" for i, opt in enumerate(parts[1:5])]
                answer_match = re.search(r'Answer: ([a-dA-D])', q)
                answer_letter = answer_match.group(1).lower() if answer_match else "a"
                answer = options[ord(answer_letter) - ord('a')]
                quiz_data.append({
                    "question": question_text,
                    "options": options,
                    "answer": answer
                })

            if len(quiz_data) == 0:
                st.error("Failed to generate properly formatted questions. Try again.")
            else:
                st.success("Quiz Generated Successfully!")
                st.markdown("---")

                # Render quiz and allow user to answer
                user_answers = []
                for idx, q in enumerate(quiz_data):
                    st.subheader(f"Q{idx+1}: {q['question']}")
                    selected = st.radio("Select an option:", q["options"], key=f"q{idx}")
                    user_answers.append((selected, q["answer"]))
                    st.markdown("---")

                if st.button("Check My Answers"):
                    score = 0
                    for idx, (user_ans, correct_ans) in enumerate(user_answers):
                        if user_ans == correct_ans:
                            st.success(f"✅ Q{idx+1}: Correct!")
                            score += 1
                        else:
                            st.error(f"❌ Q{idx+1}: Wrong. Correct answer: {correct_ans}")
                    st.info(f"🎯 Your Score: {score}/{len(user_answers)}")

        except Exception as e:
            st.error(f"Error: {e}")
