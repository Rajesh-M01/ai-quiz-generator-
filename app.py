import streamlit as st
from transformers import pipeline
import re

# Set page configuration
st.set_page_config(page_title="AI Quiz Generator", page_icon="🧠")
st.title("🧠 AI Quiz Generator (GPT2)")
st.markdown("Generate MCQs on any topic and difficulty using Hugging Face GPT2.")

# Load the GPT2 model once and cache
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
        prompt = (
            f"Generate 3 multiple choice questions (MCQs) on the topic '{topic}' for {difficulty} level learners. "
            "Each question must have:\n"
            "- One question line\n"
            "- Exactly 4 options: a), b), c), d)\n"
            "- State the correct option clearly like: Answer: a\n"
            "Make sure options start with exactly: a), b), c), d) and no repetition or extra answers.\n"
            "Example:\n"
            "1. What is a database?\n"
            "a) A website\nb) A place to store data\nc) A server\nd) A protocol\n"
            "Answer: b\n"
            "Now generate 3 such MCQs.\n"
        )

        try:
            result = generator(prompt, max_new_tokens=300)[0]["generated_text"]
            output = result.replace(prompt, "").strip()

            # Parse into questions
            questions = re.split(r'\d+\.', output)[1:]
            quiz_data = []

            for q in questions:
                question_text = q.split('a)')[0].strip()

                # Extract 4 options only
                options_match = re.findall(r'([a-d]\)\s?.*?)(?=\s+[a-d]\)|\s+Answer:|$)', q, re.DOTALL)

                if len(options_match) == 4:
                    answer_match = re.search(r'Answer:\s*([a-dA-D])', q)
                    answer_letter = answer_match.group(1).lower() if answer_match else "a"
                    answer = options_match[ord(answer_letter) - ord('a')]
                    quiz_data.append({
                        "question": question_text,
                        "options": options_match,
                        "answer": answer.strip()
                    })

            if len(quiz_data) == 0:
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
                        if user_ans.strip() == correct_ans.strip():
                            st.success(f"✅ Q{idx+1}: Correct!")
                            score += 1
                        else:
                            st.error(f"❌ Q{idx+1}: Wrong. Correct answer: {correct_ans}")
                    st.info(f"🎯 Your Score: {score}/{len(user_answers)}")

        except Exception as e:
            st.error(f"❌ Error generating quiz: {e}")
