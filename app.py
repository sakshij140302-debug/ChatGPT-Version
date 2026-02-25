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
# Clean Generated Poem
# ---------------------------
def contains_unethical_content(text):
    text = text.lower()
    for word in BANNED_WORDS:
        if re.search(rf"\b{word}\b", text):
            return True
    return False

# ---------------------------
# Generate Safe Poem
# ---------------------------
def generate_safe_poem(topic):
    prompt = f"""
    Write a positive, clean, and ethical English poem about {topic}.
    The poem must not include violence, hate, adult content, crime, or harmful themes.
    Keep it inspirational and pure.
    """
    
    for _ in range(3):  # Try 3 times if unsafe output generated
        result = generator(
            prompt,
            max_length=150,
            num_return_sequences=1,
            temperature=0.8,
            top_p=0.9,
            repetition_penalty=1.2
        )
        
        poem = result[0]['generated_text']
        
        if not contains_unethical_content(poem):
            return poem
    
    return None  # If still unsafe after retries

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Soft ChatGPT - Ethical Poem Generator")

st.title("🌸 Soft ChatGPT - Ethical Poem Generator")
st.write("This AI generates only positive and ethical poems.")
st.write("Unethical topics or harmful content are blocked automatically.")

topic = st.text_input("Topic :--", "")

if st.button("Generate Poem"):
    if topic.strip() == "":
        st.warning("Please enter a topic.")
    
    elif is_unethical(topic):
        st.error("❌ This topic is not allowed due to ethical guidelines.")
    
    else:
        with st.spinner("Generating your poem safely..."):
            poem = generate_safe_poem(topic)
            
            if poem:
                st.subheader("Output :--")
                st.write(poem)
            else:
                st.error("⚠️ Unable to generate a safe poem. Please try another topic.")