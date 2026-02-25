import streamlit as st
from transformers import pipeline
import re

# ---------------------------
# Load Model
# ---------------------------
generator = pipeline("text-generation", model="distilgpt2")

# ---------------------------
# Ethical Word List
# ---------------------------
BANNED_WORDS = [
    "violence", "kill", "murder", "terrorism",
    "drugs", "abuse", "hate", "racism",
    "porn", "sex", "weapon", "bomb",
    "suicide", "crime", "blood", "attack"
]

# ---------------------------
# Check unethical topic
# ---------------------------
def is_unethical(text):
    text = text.lower()
    for word in BANNED_WORDS:
        if re.search(rf"\b{word}\b", text):
            return True
    return False

# ---------------------------
# Clean Poem Output
# ---------------------------
def clean_poem(text):
    for word in BANNED_WORDS:
        pattern = rf"\b{word}\b"
        text = re.sub(pattern, "***", text, flags=re.IGNORECASE)
    return text

# ---------------------------
# Generate Poem
# ---------------------------
def generate_poem(topic):
    prompt = f"""
    Write a beautiful, positive, and inspirational English poem about {topic}.
    The poem must be clean and suitable for all ages.
    """
    
    result = generator(
        prompt,
        max_length=120,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9
    )
    
    poem = result[0]['generated_text']
    return clean_poem(poem)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Soft ChatGPT - Ethical Poem Generator")

st.title("🌸 Soft ChatGPT - Ethical Poem Generator")
st.write("This AI generates only positive and ethical poems.")
st.write("Unethical topics are blocked automatically.")

topic = st.text_input("Topic :--", "")

if st.button("Generate Poem"):
    if topic.strip() == "":
        st.warning("Please enter a topic.")
    
    elif is_unethical(topic):
        st.error("❌ This topic is not allowed due to ethical guidelines.")
    
    else:
        with st.spinner("Generating your poem..."):
            poem = generate_poem(topic)
            st.subheader("Output :--")
            st.write(poem)