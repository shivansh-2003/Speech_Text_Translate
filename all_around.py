import streamlit as st
from gtts import gTTS
from transformers import pipeline
import assemblyai as aai
import os
import io
from pydub import AudioSegment

# Set AssemblyAI API key
aai.settings.api_key = "your api key"

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
    st.title("Speech-to-Text and Text-to-Speech")

    # Select page
    page = st.sidebar.selectbox("Select a page", ["Speech-to-Text", "Text-to-Speech"])

    if page == "Speech-to-Text":
        # Speech-to-Text page
        st.header("Speech-to-Text")

        # File upload for audio
        uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "mp4", "wav", "m4a"])

        if uploaded_file is not None:
            file_path = os.path.join("/tmp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            if st.button("Transcribe"):
                with st.spinner('Transcribing audio...'):
                    transcript_text = transcribe_audio(file_path)
                    if transcript_text:
                        st.write("Transcript:")
                        st.write(transcript_text)

                        # Summarize the transcript
                        st.subheader("Summary:")
                        summary = summarize_text(transcript_text)
                        st.write(summary)
                    else:
                        st.error("Transcription failed. Please try again.")

    elif page == "Text-to-Speech":
        # Text-to-Speech page
        st.header("Text-to-Speech")

        # Text input for TTS
        text_input = st.text_area("Enter text to convert to speech:")

        # Language selection for TTS
        languages = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Chinese': 'zh-cn',
        }
        selected_language = st.selectbox('Select Language', list(languages.keys()))
        language_code = languages[selected_language]

        if st.button("Convert"):
            if text_input:
                with st.spinner('Converting text to speech...'):
                    audio_bytes = text_to_speech(text_input, language=language_code)

                    # Convert audio to playable format
                    audio = AudioSegment.from_file(io.BytesIO(audio_bytes.read()), format="mp3")

                    # Display audio player
                    st.audio(audio.export(format='mp3').read(), format='audio/mp3')
            else:
                st.warning("Please enter some text.")


if __name__ == "__main__":
    main()
