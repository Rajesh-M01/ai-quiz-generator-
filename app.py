import streamlit as st
from transformers import pipeline

st.title("🧠 AI Quiz Generator (GPT2)")
st.markdown("Generate simple MCQs for any topic using GPT2 from Hugging Face.")

@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

generator = load_model()

topic = st.text_input("Enter a topic (e.g., Python, World War II)")
level = st.selectbox("Select difficulty level", ["Beginner", "Intermediate", "Advanced"])

if st.button("Generate Quiz"):
    with st.spinner("Generating..."):
        prompt = f"Create 3 MCQs on the topic '{topic}' for {level} level students. Each question should have 4 options and a correct answer."

        try:
            output = generator(prompt, max_new_tokens=150)[0]["generated_text"]
            st.markdown("### 📄 Quiz Output")
            st.text(output[len(prompt):].strip())  # remove prompt from output
        except Exception as e:
            st.error(f"Error: {e}")
