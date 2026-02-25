import streamlit as st
from transformers import pipeline
import re

# ---------------------------
# Load Text Generation Model
# ---------------------------
generator = pipeline("text-generation", model="gpt2")

# ---------------------------
# Ethical Filter Function
# ---------------------------
def is_unethical(topic):
    banned_keywords = [
        "violence", "kill", "murder", "terrorism",
        "drugs", "abuse", "hate", "racism",
        "porn", "sex", "weapon", "bomb",
        "suicide", "crime"
    ]
    
    topic = topic.lower()
    
    for word in banned_keywords:
        if re.search(rf"\b{word}\b", topic):
            return True
    return False

# ---------------------------
# Generate Poem Function
# ---------------------------
def generate_poem(topic):
    prompt = f"Write a beautiful and meaningful English poem about {topic}:\n"
    
    result = generator(
        prompt,
        max_length=150,
        num_return_sequences=1,
        temperature=0.9,
        top_p=0.95
    )
    
    poem = result[0]['generated_text']
    return poem

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Soft ChatGPT - Ethical Poem Generator")

st.title("🌸 Soft ChatGPT - Ethical Poem Generator")
st.write("Enter a topic and get a beautiful English poem.")
st.write("⚠️ Unethical topics are automatically blocked.")

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