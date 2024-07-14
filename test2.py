import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
import io
import tempfile
import os
from PyPDF2 import PdfReader


# Function to convert text to speech using gTTS with language selection
def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes


# Function to read text from uploaded files (txt and pdf)
def read_uploaded_file(file):
    text = ""
    if file.type == 'text/plain':  # For .txt files
        text = file.read().decode('utf-8')
    elif file.type == 'application/pdf':  # For PDF files
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


# Streamlit app
def main():
    st.title("Multilingual Text to Speech with gTTS and pydub")

    # Language selection
    languages = {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Chinese': 'zh-cn',
    }
    selected_language = st.selectbox('Select Language', list(languages.keys()))
    language_code = languages[selected_language]

    # File upload
    st.sidebar.title("Upload Files")
    uploaded_file = st.sidebar.file_uploader("Upload a text file (.txt) or PDF file", type=['txt', 'pdf'])

    if uploaded_file is not None:
        text_input = read_uploaded_file(uploaded_file)
        st.text_area("Text from uploaded file:", value=text_input, height=200)

        # Convert button
        if st.button("Convert"):
            if text_input:
                # Convert text to speech
                audio_bytes = text_to_speech(text_input, language=language_code)

                # Convert audio to playable format
                audio = AudioSegment.from_file(io.BytesIO(audio_bytes.read()), format="mp3")

                # Display audio player
                st.audio(audio.export(format='mp3').read(), format='audio/mp3')
            else:
                st.warning("Uploaded file is empty or cannot be read.")

    # Input text area for user input
    st.text_area("Or, enter text to convert to speech:", key="text_input")

    # Convert button for text input
    if st.button("Convert Text"):
        text_input = st.session_state.text_input
        if text_input:
            # Convert text to speech
            audio_bytes = text_to_speech(text_input, language=language_code)

            # Convert audio to playable format
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes.read()), format="mp3")

            # Display audio player
            st.audio(audio.export(format='mp3').read(), format='audio/mp3')
        else:
            st.warning("Please enter some text.")


if __name__ == "__main__":
    main()
