import streamlit as st
from transformers import pipeline
import re

st.set_page_config(page_title="AI Quiz Generator", page_icon="🧠")
st.title("🧠 AI Quiz Generator (GPT2)")
st.markdown("Generate MCQs on any topic and difficulty using Hugging Face GPT2.")

@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

generator = load_model()

topic = st.selectbox("Choose Topic", ["Python", "C++", "Java", "DBMS", "SQL", "OOP"])
difficulty = st.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Advanced"])

if st.button("Generate Quiz"):
    with st.spinner("Generating quiz... please wait"):
        prompt = (
            f"Generate 3 multiple choice questions (MCQs) on the topic '{topic}' for {difficulty} level learners.\n"
            "Each question must follow this exact format:\n"
            "1. <Question text>\n"
            "a) <Option A>\n"
            "b) <Option B>\n"
            "c) <Option C>\n"
            "d) <Option D>\n"
            "Answer: <a/b/c/d>\n"
            "Repeat this format strictly for all 3 questions with no additional explanation.\n"
        )

        try:
            result = generator(prompt, max_new_tokens=300)[0]["generated_text"]
            output = result.replace(prompt, "").strip()

            # Extract 3 questions properly
            raw_questions = re.findall(
                r'\d+\.\s*(.*?)\s*a\)(.*?)\s*b\)(.*?)\s*c\)(.*?)\s*d\)(.*?)\s*Answer:\s*([a-dA-D])',
                output, re.DOTALL
            )

            quiz_data = []
            for i, match in enumerate(raw_questions):
                q_text = match[0].strip()
                options = [
                    f"a) {match[1].strip()}",
                    f"b) {match[2].strip()}",
                    f"c) {match[3].strip()}",
                    f"d) {match[4].strip()}",
                ]
                correct = match[5].strip().lower()
                answer = options[ord(correct) - ord('a')]
                quiz_data.append({
                    "question": q_text,
                    "options": options,
                    "answer": answer
                })

            if not quiz_data:
                st.error("❌ Failed to generate properly formatted questions. Try again.")
            else:
                st.success("✅ Quiz Generated Successfully!")
                st.markdown("---")

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
            st.error(f"❌ Error: {e}")
