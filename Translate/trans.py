import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")


# Function to translate text
def translate_text(text, target_language):
    # Prepare the text for the model
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    # Generate translation
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_language])

    # Decode the translated tokens
    translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

    return translated_text


# Supported languages and their codes
language_options = {
    "English": "eng_Latn",
    "Spanish": "spa_Latn",
    "German": "deu_Latn",
    "French": "fra_Latn",
    "Chinese": "zho_Hans",
    "Hindi": "hin_Deva"
}

# Streamlit UI
st.title("Multilingual Translator")
st.write("Enter text in any language and select the target language to translate.")

# Text area for input
input_text = st.text_area("Enter text:", "")

# Drop-down menus for selecting languages
target_language = st.selectbox("Target Language:", list(language_options.keys()))

# Translate button
if st.button("Translate"):
    if input_text.strip() == "":
        st.write("Please enter text to translate.")
    else:
        translated_text = translate_text(input_text, language_options[target_language])
        st.write(f"Translated Text ({target_language}):")
        st.write(translated_text)
