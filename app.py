import streamlit as st
from transformers import pipeline

st.title("🧠 AI Quiz Generator (Free Version)")
st.markdown("Generate basic MCQs using a lightweight free model")

@st.cache_resource
def load_model():
    return pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

generator = load_model()

topic = st.text_input("Enter a topic (e.g., Python, History, Algebra)")
level = st.selectbox("Select difficulty level", ["Beginner", "Intermediate", "Advanced"])

if st.button("Generate Quiz"):
    with st.spinner("Generating..."):
        prompt = f"Create 3 MCQs on '{topic}' for {level} students. Each question must have 4 options and 1 correct answer."

        try:
            output = generator(prompt, max_new_tokens=200)[0]['generated_text']
            st.markdown("### 📄 Quiz")
            st.markdown(output[len(prompt):])  # trim the prompt
        except Exception as e:
            st.error(f"Error: {e}")
