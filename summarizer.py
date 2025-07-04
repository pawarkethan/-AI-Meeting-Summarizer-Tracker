from transformers import pipeline
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)  # Optional: suppress warnings

summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

def summarize_text(text):
    input_text = "summarize: " + text

    # Handle very short transcripts
    if len(text.split()) < 10:
        return "Transcript too short for summarization."

    # Dynamically adjust summary length
    input_length = len(input_text.split())
    max_len = min(100, int(input_length * 1.5))
    min_len = max(10, int(input_length * 0.5))

    summary = summarizer(input_text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]['summary_text']
