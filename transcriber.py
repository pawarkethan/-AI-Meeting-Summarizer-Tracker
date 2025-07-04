import whisper

model = whisper.load_model("base")

def transcribe_audio(file_path):
    result = model.transcribe(file_path, language="en")
    print("📝 Transcription result:", result)
    return result["text"], result["language"]

