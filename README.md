# 🤖 AI Meeting Summarizer

A smart Streamlit-based app that uses powerful AI models to transcribe, summarize, and extract key action items from meetings. Upload or record your meeting audio, and let the app do the rest.

## 🚀 Features
- 🎙️ **Record Meetings**  
  Record audio directly in the app (up to 1 hour).

- 📁 **Upload Audio Files**  
  Supports `.mp3` and `.wav` formats for easy file uploads.

- 🔁 **Audio Playback**  
  Play back recorded or uploaded meetings inside the app.

- 📝 **Smart Transcription**  
  Accurate transcription powered by OpenAI's Whisper model.

- 📄 **Meeting Summaries**  
  Generate concise summaries using the T5 transformer model.

- ✅ **Action Item Extraction**  
  Extract key tasks and follow-up actions automatically.

---

## 📦 Requirements

Install the required packages with:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- streamlit  
- sounddevice  
- scipy  
- transformers  
- torch  
- openai  
- ffmpeg-python

---
