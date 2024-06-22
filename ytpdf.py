import os
import wave
import json
from vosk import Model, KaldiRecognizer
from pytube import YouTube
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from fpdf import FPDF

# Function to download YouTube audio using pytube and convert to WAV
def download_and_convert_audio(url, output_path):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(output_path=output_path)
    
    # Convert MP4 to WAV using pydub
    try:
        audio = AudioSegment.from_file(audio_file)
    except CouldntDecodeError:
        raise ValueError("Could not decode audio file. Ensure the audio stream is valid.")

    audio = audio.set_frame_rate(16000).set_channels(1)
    audio_file_wav = os.path.join(output_path, "audio.wav")
    audio.export(audio_file_wav, format="wav")
    
    return audio_file_wav

# Function to convert audio to text using Vosk
def audio_to_text(audio_file, model_path):
    # Load Vosk model
    if not os.path.exists(model_path):
        raise ValueError(f"Model path '{model_path}' does not exist")
    model = Model(model_path)
    
    # Convert audio to text
    wf = wave.open(audio_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("Audio file must be WAV format mono PCM with a sample rate of 16000 Hz.")
    
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    text = ""
    
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text += result.get("text", "") + " "
    
    final_result = json.loads(rec.FinalResult())
    text += final_result.get("text", "")
    
    return text

# Function to save text as PDF using fpdf
def save_text_as_pdf(text, output_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, txt=text, align="L")
    pdf.output(output_pdf)

# Example usage
if __name__ == "__main__":
    # Ask user for YouTube video URL
    video_url = input("Enter the YouTube video URL: ")

    # Get current working directory
    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, "output")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Download and convert audio from YouTube
    audio_file_wav = download_and_convert_audio(video_url, output_directory)

    # Path to Vosk model (assuming it's in the same directory as the script)
    model_path = os.path.join(current_directory, "vosk-model-small-en-us-0.15")

    # Convert audio to text
    recognized_text = audio_to_text(audio_file_wav, model_path)
    if recognized_text:
        print("Recognized Text:")
        print(recognized_text)

        # Save text as PDF in current directory
        pdf_file = os.path.join(output_directory, "transcript.pdf")
        save_text_as_pdf(recognized_text, pdf_file)
        print(f"Text saved as PDF: {pdf_file}")
    else:
        print("No text recognized or error occurred during recognition.")
