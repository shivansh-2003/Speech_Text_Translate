import streamlit as st
from gtts import gTTS
from transformers import pipeline
import assemblyai as aai
import os
import io
from pydub import AudioSegment

# For adding custom HTML and JavaScript
def inject_custom_css():
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.1);
        background-color: #ff7b7b;
    }
    .header-text {
        font-family: 'Courier New', Courier, monospace;
        color: #1f77b4;
    }
    .animated-element {
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

def inject_javascript_animation():
    st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var textWrapper = document.querySelector('.ml9 .letters');
            textWrapper.innerHTML = textWrapper.textContent.replace(/([^\x00-\x80]|\w)/g, "<span class='letter'>$&</span>");

            anime.timeline({loop: true})
            .add({
                targets: '.ml9 .letter',
                scale: [0, 1],
                duration: 1500,
                elasticity: 600,
                delay: (el, i) => 45 * (i+1)
            }).add({
                targets: '.ml9',
                opacity: 0,
                duration: 1000,
                easing: "easeOutExpo",
                delay: 1000
            });
        });
    </script>
    """, unsafe_allow_html=True)

# Set AssemblyAI API key
aai.settings.api_key = "639595d69b8645fd9adfad1224f8907c"

# Initialize the summarizer pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def transcribe_audio(file_path):
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
        return transcript.text
    except Exception as e:
        st.error(f"Error in transcription: {e}")
        return None


def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes


def summarize_text(text):
    try:
        chunks = split_text(text)
        summaries = [summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text'] for chunk in
                     chunks]
        bullet_points = "\n".join([f"- {summary}" for summary in summaries])
        return bullet_points
    except Exception as e:
        st.error(f"Error in summarization: {e}")
        return "Summary could not be generated."


def split_text(text, max_length=1000):
    """Splits text into chunks of a specified maximum length."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_chunk.append(word)
            current_length += len(word) + 1
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def main():
    # Set page config for title and icon
    st.set_page_config(page_title="Speech and Text App", page_icon="🔊", layout="centered")

    # Inject custom CSS and JS
    inject_custom_css()
    inject_javascript_animation()

    st.markdown("<h1 class='header-text'>🔊 Speech-to-Text and Text-to-Speech</h1>", unsafe_allow_html=True)

    # Create tabs for a more modern UI
    tab1, tab2 = st.tabs(["🎙️ Speech-to-Text", "🗣️ Text-to-Speech"])

    with tab1:
        st.header("🎙️ Speech-to-Text")

        # Use columns to structure layout better
        col1, col2 = st.columns(2)

        with col1:
            st.info("Upload an audio file for transcription")
            uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "mp4", "wav", "m4a"])

        with col2:
            st.image("https://via.placeholder.com/150", caption="Upload Audio", use_column_width=True)

        if uploaded_file is not None:
            file_path = os.path.join("/tmp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            if st.button("Transcribe"):
                with st.spinner('Transcribing audio...'):
                    transcript_text = transcribe_audio(file_path)
                    if transcript_text:
                        st.success("Transcription complete!")
                        st.write("Transcript:")
                        st.write(transcript_text)

                        # Summarize the transcript
                        st.subheader("Summary:")
                        summary = summarize_text(transcript_text)
                        st.write(summary)
                    else:
                        st.error("Transcription failed. Please try again.")

    with tab2:
        st.header("🗣️ Text-to-Speech")

        # Use container for better organization
        with st.container():
            text_input = st.text_area("Enter text to convert to speech:")

            languages = {
                'English': 'en',
                'Spanish': 'es',
                'French': 'fr',
                'German': 'de',
                'Chinese': 'zh-cn',
            }
            selected_language = st.selectbox('Select Language', list(languages.keys()))
            language_code = languages[selected_language]

            # Add progress bar for better UX during conversion
            if st.button("Convert"):
                if text_input:
                    with st.spinner('Converting text to speech...'):
                        audio_bytes = text_to_speech(text_input, language=language_code)
                        st.success("Conversion complete!")

                        # Audio playback with a progress bar
                        st.audio(audio_bytes, format='audio/mp3')
                else:
                    st.warning("Please enter some text.")

    # Use sidebar to add additional options or instructions
    with st.sidebar:
        st.subheader("About the App")
        st.write("""
        This app allows you to:
        - Convert speech to text using AssemblyAI
        - Summarize large text inputs using transformers
        - Convert text to speech in multiple languages using GTTS.
        """)


if __name__ == "__main__":
    main()
