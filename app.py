import streamlit as st
import google.generativeai as genai

# Retrieve the API key from secrets
api_key = st.secrets["api_key"]  # Ensure you've set this in Streamlit Secrets
genai.configure(api_key=api_key)

# Configuration for generation
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 34,
    "max_output_tokens": 2000,
    "response_mime_type": "text/plain",
}

# List of keywords for checking
obgyn_keywords = [
    "BOTOX", "Nexplanon", "Nexplanon removal", "Nexplanon sp", "SIS KL", "SIS",
    "Nexplanon insertion", "Nexplanon insert", "Botox `100U", "IUD", "Ultrasound",
    "bedside", "Fluoroscopy", "ASCUS", "Nuchal", "HPV", "skin tag removal",
    "Paragard", "Paraguard", "Mirena", "Kyleena", "Anti Coag/Urology", "EDD",
    "ROB", "Pessary", "Neplanon"
]

cardiology_keywords = [
    "Plain Treadmill", "Carotid Doppler", "Submax stress", "Exnuke", "Nuc",
    "Lexi", "Echo", "Stress Echo", "RTM", "ETT"
]

# Combine both lists into one
all_keywords = obgyn_keywords + cardiology_keywords

def highlight_keywords(text, keywords):
    """
    Highlight keywords in the text by wrapping them in HTML <mark> tags with yellow background.  
    """
    # Ensure the keywords are highlighted correctly by checking for word boundaries
    highlighted_text = text
    for keyword in keywords:
        keyword_lower = keyword.lower()
        text_lower = highlighted_text.lower()
        
        # Find all occurrences of the keyword in the text (case insensitive)
        start_idx = text_lower.find(keyword_lower)
        while start_idx != -1:
            # Calculate the end index of the keyword
            end_idx = start_idx + len(keyword)
            
            # Highlight the keyword by wrapping it in HTML <mark> tags
            highlighted_text = (
                highlighted_text[:start_idx] +
                f'<mark style="background-color: yellow;">{highlighted_text[start_idx:end_idx]}</mark>' +
                highlighted_text[end_idx:]
            )
            
            # Update text_lower to match highlighted_text for accurate search
            text_lower = highlighted_text.lower()
            
            # Find the next occurrence of the keyword
            start_idx = text_lower.find(keyword_lower, end_idx + len('<mark style="background-color: yellow;"></mark>'))
            
    return highlighted_text

def generate(user_input):
    # Initialize the GenerativeModel
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Combine keywords and user input in the prompt
    prompt_text = f"""Given a set of keywords:
OBGYN Keywords: {', '.join(obgyn_keywords)}
Cardiology Keywords: {', '.join(cardiology_keywords)}

Find if any of the following keywords are present as whole words in the given sentence. If yes, show the sentence and mention the found keywords.

Sentence: {user_input}"""

    # Generate content using the model
    responses = model.generate_content(
        [prompt_text],
        generation_config=generation_config,
        stream=True,
    )

    # Return the generated response
    output = ""
    for response in responses:
        output += response.text
    return output

# Streamlit App Layout
st.title("Keyword Highlighter with Generative AI")

# Input from the user with a unique key
user_input = st.text_area("Enter a sentence to check for keywords:", key="unique_text_area_key")

if st.button("Generate"):
    if user_input.strip():
        # Generate the response (if you want to use the model's output for some reason)
        generated_response = generate(user_input)

        # Highlight the keywords in the user's input
        highlighted_input = highlight_keywords(user_input, all_keywords)

        # Display the output with highlighted keywords
        st.markdown("### Output with Highlighted Keywords")
        st.markdown(highlighted_input, unsafe_allow_html=True)
        
        # Display the model's generated response (if needed)
        #st.markdown("### Model's Response")
        #st.write(generated_response)
    else:
        st.warning("Please enter a sentence to check for keywords.")
