import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

st.title("🧠 AI Quiz Generator – Free (Hugging Face)")
st.markdown("Generate MCQs using a free small model via Hugging Face.")

@st.cache_resource
def load_model():
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

generator = load_model()

topic = st.text_input("Enter a topic (e.g., Python, WW2, Algebra)")
level = st.selectbox("Choose difficulty", ["Beginner", "Intermediate", "Advanced"])

if st.button("Generate Quiz"):
    with st.spinner("Generating..."):
        prompt = f"Create 3 MCQs with 4 options and correct answers on '{topic}' for {level} students."
        try:
            result = generator(prompt, max_new_tokens=200)[0]['generated_text']
            st.markdown("### 📄 Quiz")
            st.markdown(result[len(prompt):])  # Clean the prompt from output
        except Exception as e:
            st.error(f"Error: {e}")
