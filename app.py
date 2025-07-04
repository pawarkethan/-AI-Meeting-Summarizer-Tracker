import streamlit as st
import os
import ffmpeg
import sounddevice as sd
import time
from record_audio import record_audio_dynamic, save_audio
from transcriber import transcribe_audio
from summarizer import summarize_text
from extractor import extract_action_items

st.set_page_config(page_title="Meeting Tracker", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 AI Meeting Summarizer</h1>", unsafe_allow_html=True)

st.markdown("This app records your voice, transcribes the audio, summarizes the content using an LLM, and extracts action items — ideal for team meetings, lectures, or personal notes.")
st.divider()

# Audio Input Selection
audio_source = st.radio("Choose audio input:", ["🎙️ Record now", "📂 Upload file(.mp3/.wav)"])

# Session state init
if "recording" not in st.session_state:
    st.session_state.recording = False
if "audio_buffer" not in st.session_state:
    st.session_state.audio_buffer = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "duration_sec" not in st.session_state:
    st.session_state.duration_sec = 0

# === RECORDING SECTION ===
if audio_source == "🎙️ Record now":
    if not st.session_state.recording:
        if st.button("🎙️ Start Recording"):
            st.session_state.recording = True
            st.session_state.audio_buffer, st.session_state.samplerate = record_audio_dynamic()
            st.session_state.start_time = time.time()
            st.success("🔴 Recording... Click again to stop")
    else:
        st.success("🔴 Recording Saved... Click the button below to transcribe.")
        if st.button("📝 Transcribe"):
            st.session_state.recording = False
            sd.stop()
            end_time = time.time()
            st.session_state.duration_sec = int(end_time - st.session_state.start_time)

            save_audio(
                st.session_state.audio_buffer,
                st.session_state.samplerate,
                filename="meeting.wav",
                frames=st.session_state.duration_sec * st.session_state.samplerate
            )

            st.success(f"✅ Recording saved! Duration: {st.session_state.duration_sec} sec")

            # 🔊 Play recorded audio
            st.subheader("🔊 Play Audio")
            with open("meeting.wav", "rb") as f:
                st.audio(f.read(), format="audio/wav")

            # 🔁 Transcription and NLP pipeline
            st.info("📝 Transcribing audio...")
            transcript, lang = transcribe_audio("meeting.wav")
            st.subheader("📄 Transcript")
            st.write(transcript)
            st.download_button("📥 Download Transcript", transcript, file_name="transcript.txt")

            col1, col2 = st.columns(2)
            col1.metric("🕒 Duration", f"{st.session_state.duration_sec} sec")
            col2.metric("📢 Language", lang.upper())

            st.info("🧠 Summarizing transcript...")
            summary = summarize_text(transcript)
            st.subheader("📝 Summary")
            st.write(summary)

            st.info("📌 Extracting action items...")
            actions = extract_action_items(summary)
            st.subheader("✅ Action Items")
            if actions:
                for item in actions:
                    st.markdown(f"• {item}")
            else:
                st.warning("No actionable items found.")

# === UPLOAD SECTION ===
elif audio_source == "📂 Upload file(.mp3/.wav)":
    uploaded_file = st.file_uploader("Upload a .wav or .mp3 file", type=["wav", "mp3"])
    audio_file = None

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        file_path = f"uploaded.{file_extension}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        if file_extension == "mp3":
            st.info("🎧 Converting MP3 to WAV...")
            wav_path = "converted.wav"
            try:
                ffmpeg.input(file_path).output(wav_path).run(overwrite_output=True, quiet=True)
                audio_file = wav_path
                st.success("✅ MP3 converted to WAV successfully.")
            except Exception as e:
                st.error("❌ MP3 to WAV conversion failed.")
                st.code(str(e))
        else:
            audio_file = file_path

        if audio_file:
            st.success("✅ File ready for transcription.")

            # 🔊 Play uploaded audio
            st.subheader("🔊 Play Audio")
            with open(audio_file, "rb") as f:
                st.audio(f.read(), format="audio/wav")

            # 🔁 Transcription and NLP pipeline
            st.info("📝 Transcribing audio...")
            transcript, lang = transcribe_audio(audio_file)
            st.subheader("📄 Transcript")
            st.write(transcript)
            st.download_button("📥 Download Transcript", transcript, file_name="transcript.txt")

            col1, col2 = st.columns(2)
            col1.metric("🕒 Duration", "Unknown")  # Could extract via librosa/pydub if needed
            col2.metric("📢 Language", lang.upper())

            st.info("🧠 Summarizing transcript...")
            summary = summarize_text(transcript)
            st.subheader("📝 Summary")
            st.write(summary)

            st.info("📌 Extracting action items...")
            actions = extract_action_items(summary)
            st.subheader("✅ Action Items")
            if actions:
                for item in actions:
                    st.markdown(f"• {item}")
            else:
                st.warning("No actionable items found.")
