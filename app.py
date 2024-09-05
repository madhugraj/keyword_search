import os
import streamlit as st
import google.generativeai as genai

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

# Define the keywords text
keywords_text = """Giving you set of keywords:
OBGYN:
 1. BOTOX
2. Nexplanon
3. Nexplanon removal
4. Nexplanon sp
5. SIS KL
6. SIS
7. Nexplanon insertion
8. Nexplanon insert
9. Botox `100U
10. IUD
11. Nexplanon
12. Botox
13. Nexaplenon
14. Nexplenon
15. Ultrasound
16. bedside
17. Fluoroscopy
18. ASCUS
19. Nuchal
20. HPV
21. skin tag removal
22. Paragard
23. Paraguard
24. Mirena
25. Kyleena
26 Anti Coag/Urology
27. EDD
28. ROB
29. Pessary
30. Neplanon
"""

def generate(user_input):
    # Initialize the GenerativeModel
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Combine keywords and user input in the prompt
    prompt_text = f"""{keywords_text}
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

    # Highlight the keywords using Streamlit's Markdown support
    st.markdown("### Output with Highlighted Keywords")
    st.markdown(output, unsafe_allow_html=True)
