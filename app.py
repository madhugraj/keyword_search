import streamlit as st
import google.generativeai as genai
import re  # Import the regex library

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
    Only highlight whole words.
    """
    highlighted_text = text
    keyword_found = False  # Flag to check if any keyword is found

    for keyword in keywords:
        # Use regex to match whole words only (case insensitive)
        pattern = rf'\b{re.escape(keyword)}\b'
        if re.search(pattern, highlighted_text, flags=re.IGNORECASE):
            # If a keyword is found, replace it with highlighted text
            highlighted_text = re.sub(
                pattern,
                f'<mark style="background-color: yellow;">{keyword}</mark>',
                highlighted_text,
                flags=re.IGNORECASE
            )
            keyword_found = True  # Set the flag to True if any keyword is found

    if not keyword_found:
        return "No keywords found."
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

Find if any of the keywords are present in the input sentence : 
If yes show the sentence. Do not highlight the non keyword. Remember the keyword should be whole word.

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
st.title("Keyword Highlighter")

# Input from the user with a unique key
user_input = st.text_area("Enter a sentence to check for keywords:", key="unique_text_area_key")

if st.button("Generate"):
    if user_input.strip():
        # Generate the response (if you want to use the model's output for some reason)
        generated_response = generate(user_input)

        # Highlight the keywords in the user's input
        highlighted_input = highlight_keywords(user_input, all_keywords)

        # Display the output with highlighted keywords or "No keywords found"
        st.markdown("### Output with Highlighted Keywords")
        st.markdown(highlighted_input, unsafe_allow_html=True)
        
        # Display the model's generated response (if needed)
        # st.markdown("### Model's Response")
        # st.write(generated_response)
    else:
        st.warning("Please enter a sentence to check for keywords.")
