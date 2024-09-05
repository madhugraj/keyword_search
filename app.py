import os
import streamlit as st
import google.generativeai as genai
import re

# Configure the API key
GOOGLE_API_KEY = "AIzaSyAe8rheF4wv2ZHJB2YboUhyyVlM2y0vmlk"
genai.configure(api_key=GOOGLE_API_KEY)

# Configuration for generation
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 34,
    "max_output_tokens": 2000,
    "response_mime_type": "text/plain",
}

# Define the keywords list
keywords = [
    "BOTOX", "Nexplanon", "Nexplanon removal", "Nexplanon sp", "SIS KL", "SIS", 
    "Nexplanon insertion", "Nexplanon insert", "Botox `100U", "IUD", "Ultrasound", 
    "bedside", "Fluoroscopy", "ASCUS", "Nuchal", "HPV", "skin tag removal", 
    "Paragard", "Paraguard", "Mirena", "Kyleena", "Anti Coag/Urology", "EDD", 
    "ROB", "Pessary", "Neplanon"
]

def highlight_keywords(text, keywords):
    """
    Highlight keywords in the text by wrapping them in HTML <u> tags.
    """
    for keyword in keywords:
        # Use regex to find whole words case-insensitively
        text = re.sub(rf'\b{re.escape(keyword)}\b', f'<u>{keyword}</u>', text, flags=re.IGNORECASE)
    return text

def generate(user_input):
    # Initialize the GenerativeModel
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Combine keywords and user input in the prompt
    prompt_text = f"""Giving you a set of keywords:
OBGYN Keywords: {', '.join(keywords)}

Find if any of the above keywords are present in the following sentence:
If yes, show the sentence and underline all the keywords. Do not highlight the non-keyword.

{user_input}"""

    # Generate content using the model
    responses = model.generate_content(
        [prompt_text],
        generation_config=generation_config,
        stream=True,
    )

    # Return the generated response
    for response in responses:
        return response.text

# Streamlit App Layout
st.title("Keyword Highlighter with Generative AI")

# Input from the user
user_input = st.text_input("Enter a sentence to check for keywords:")

if user_input:
    # Generate the response
    output = generate(user_input)

    # Highlight the keywords in the output
    highlighted_output = highlight_keywords(output, keywords)
    
    # Display the output with highlighted keywords
    st.markdown("### Output with Highlighted Keywords")
    st.markdown(highlighted_output, unsafe_allow_html=True)
