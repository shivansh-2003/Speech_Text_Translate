import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import assemblyai as aai
import os

# Set AssemblyAI API key
aai.settings.api_key ="YOUR_API_KEY"

# Initialize the summarizer pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Load the tokenizer and model for translation
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")


# Supported languages and their codes
language_options = {
    "English": "eng_Latn",
    "Spanish": "spa_Latn",
    "German": "deu_Latn",
    "French": "fra_Latn",
    "Chinese": "zho_Hans",
    "Hindi": "hin_Deva"
}

def transcribe_audio(file_path):
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
        return transcript.text
    except Exception as e:
        st.error(f"Error in transcription: {e}")
        return None

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

def summarize_text(text):
    try:
        chunks = split_text(text)
        summaries = [summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
        bullet_points = "\n".join([f"- {summary}" for summary in summaries])
        return bullet_points
    except Exception as e:
        st.error(f"Error in summarization: {e}")
        return "Summary could not be generated."

def translate_text(text, target_language):
    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_language])
        translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translated_text
    except Exception as e:
        st.error(f"Error in translation: {e}")
        return "Translation could not be generated."

def main():
    st.title("Audio Transcription, Translation, and Summarization")

    # File upload
    uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3"])

    if 'transcript_text' not in st.session_state:
        st.session_state.transcript_text = ""
    if 'summary_text' not in st.session_state:
        st.session_state.summary_text = ""
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = ""

    if uploaded_file is not None:
        file_path = os.path.join("/tmp", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Transcribe"):
            with st.spinner('Transcribing audio...'):
                st.session_state.transcript_text = transcribe_audio(file_path)
                if st.session_state.transcript_text:
                    st.write("Transcript:")
                    st.write(st.session_state.transcript_text)
                else:
                    st.error("Transcription failed. Please try again.")

    if st.session_state.transcript_text:
        st.write("Transcript:")
        st.write(st.session_state.transcript_text)

        if st.button("Summarize"):
            with st.spinner('Summarizing text...'):
                st.session_state.summary_text = summarize_text(st.session_state.transcript_text)
                st.write("Summary:")
                st.markdown(st.session_state.summary_text)

        target_language = st.selectbox("Translate Transcript to:", list(language_options.keys()))
        if st.button("Translate Transcript"):
            with st.spinner('Translating text...'):
                st.session_state.translated_text = translate_text(st.session_state.transcript_text, language_options[target_language])
                st.write(f"Translated Text ({target_language}):")
                st.write(st.session_state.translated_text)

    if st.session_state.summary_text:
        st.write("Summary:")
        st.markdown(st.session_state.summary_text)

        target_language_summary = st.selectbox("Translate Summary to:", list(language_options.keys()))
        if st.button("Translate Summary"):
            with st.spinner('Translating summary...'):
                st.session_state.translated_summary_text = translate_text(st.session_state.summary_text, language_options[target_language_summary])
                st.write(f"Translated Summary ({target_language_summary}):")
                st.write(st.session_state.translated_summary_text)

if __name__ == "__main__":
    main()
