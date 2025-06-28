import streamlit as st
from transformers import pipeline

st.title("🧠 AI Quiz Generator – Hugging Face Version (Free)")
st.markdown("Generate MCQs based on any topic and level using open models.")

# Load model only once
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", tokenizer="mistralai/Mistral-7B-Instruct-v0.1")

generator = load_model()

topic = st.text_input("Enter a topic (e.g., Python, Algebra, WW2)")
level = st.selectbox("Select difficulty level", ["Beginner", "Intermediate", "Advanced"])

if st.button("Generate Quiz"):
    with st.spinner("Generating questions..."):
        prompt = f"Generate 3 multiple choice questions on the topic '{topic}' for a {level} level learner. Each question should have 4 options and indicate the correct answer."

        try:
            result = generator(prompt, max_new_tokens=250, do_sample=True, temperature=0.7)[0]["generated_text"]
            st.markdown("### 📄 Quiz")
            st.markdown(result.split(prompt)[-1])
        except Exception as e:
            st.error(f"Error generating quiz: {e}")
