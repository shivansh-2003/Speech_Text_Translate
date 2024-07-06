# Speech To Text Translate Summarize(STTS)

## Main working

### 1.File Upload:
Users can upload an audio file in MP3 format.
The uploaded file is saved temporarily for processing.

### 2.Transcription:
Users click the "Transcribe" button to transcribe the audio file.
The app uses AssemblyAI to transcribe the audio into text.
The transcription result is displayed on the page.

### 3.Summarization:
After transcription, users can click the "Summarize" button to summarize the transcribed text.
The app uses a summarization model to generate a concise summary of the transcribed text.
The summary result is displayed on the page.

### 4.Translation of Transcript:
Users can select a target language from a dropdown menu to translate the transcribed text.
After selecting the language, they click the "Translate Transcript" button.
The app translates the transcribed text into the selected language.
The translated transcript is displayed on the page.

### 5.Translation of Summary:
After summarizing, users can select a target language from a dropdown menu to translate the summary text.
After selecting the language, they click the "Translate Summary" button.
The app translates the summarized text into the selected language.
The translated summary is displayed on the page.

## Running on System
```angular2html
 pip install -r requirement.txt
```
```angular2html
 streamlit run test.py
 streamlit run "file_name"
```
#### Please replace YOUR_API_KEY in base.py and test.py file with your assemblyai api. 

## Model And Api used :-

### Assembly.ai
```angular2html
https://www.assemblyai.com/
```
##### please register your id in assembly.ai and get api key from there
This Api can convert Speech-to-Text very efficiently.

### Summarizer

##### Model Name:- sshleifer/distilbart-cnn-12-6
##### Functionality:-
It Summarizes the transcript .

### Translation

##### Model Name:-facebook/nllb-200-distilled-600M

It translates the summarized text or Transcript
