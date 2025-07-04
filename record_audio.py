import sounddevice as sd
from scipy.io.wavfile import write

samplerate = 44100  # CD quality

def record_audio_dynamic(duration_sec=3600, channels=1):
    # Starts recording and returns the buffer and sample rate
    recording = sd.rec(int(duration_sec * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    return recording, samplerate

def save_audio(recording, samplerate, filename="meeting.wav", frames=None):
    # Saves the audio file with only the recorded frames if specified
    if frames is not None:
        write(filename, samplerate, recording[:frames])
    else:
        write(filename, samplerate, recording)
