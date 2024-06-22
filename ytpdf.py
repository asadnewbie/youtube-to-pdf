import os
import yt_dlp
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from fpdf import FPDF
import wave
import json
from vosk import Model, KaldiRecognizer

# Function to download YouTube audio using yt-dlp and convert to WAV
def download_and_convert_audio(video_url, output_path):
    try:
        print(f"Fetching YouTube video: {video_url}")

        # Create yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        }

        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_title = info.get('title', None)

            # Find the audio file (assuming it's in webm or m4a format)
            audio_file = None
            for file in os.listdir(output_path):
                if file.endswith('.webm') or file.endswith('.m4a'):
                    audio_file = os.path.join(output_path, file)
                    break

            if not audio_file:
                raise ValueError("No audio file found for the YouTube video.")

            # Convert to WAV using pydub (adjust as needed)
            audio = AudioSegment.from_file(audio_file)
            
            # Ensure the audio is in the correct format for Vosk
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio = audio.set_sample_width(2)  # Set sample width to 16-bit (2 bytes) for PCM
            
            audio_file_wav = os.path.join(output_path, "audio.wav")
            audio.export(audio_file_wav, format="wav")

            print(f"Audio saved as: {audio_file_wav}")
            return audio_file_wav

    except CouldntDecodeError:
        raise ValueError("Could not decode audio file. Ensure the audio stream is valid.")

    except Exception as e:
        raise ValueError(f"Error occurred while downloading and converting audio: {str(e)}")

# Function to recognize audio to text using Vosk
def recognize_audio(audio_file, model_path):
    try:
        # Load Vosk model
        if not os.path.exists(model_path):
            raise ValueError(f"Model path '{model_path}' does not exist")
        model = Model(model_path)

        # Initialize recognizer
        wf = wave.open(audio_file, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("Audio file must be WAV format mono PCM with a sample rate of 16000 Hz.")

        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)

        # Process audio file
        recognized_text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                recognized_text += result.get("text", "") + " "

        final_result = json.loads(recognizer.FinalResult())
        recognized_text += final_result.get("text", "")

        return recognized_text.strip()

    except Exception as e:
        raise ValueError(f"Error occurred during recognition with Vosk: {str(e)}")

# Function to save text as PDF using fpdf
def save_text_as_pdf(text, output_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, txt=text, align="L")
    pdf.output(output_pdf)

# Example usage
if __name__ == "__main__":
    try:
        # Ask user for YouTube video URL
        video_url = input("Enter the YouTube video URL: ")

        # Get current working directory
        current_directory = os.getcwd()
        output_directory = os.path.join(current_directory, "output")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Download and convert audio from YouTube
        audio_file_wav = download_and_convert_audio(video_url, output_directory)
        print(f"Audio file saved as: {audio_file_wav}")

        # Path to Vosk model (assuming it's in the same directory as the script)
        model_path = os.path.join(current_directory, "vosk-model-small-en-us-0.15")

        # Recognize audio to text using Vosk
        recognized_text = recognize_audio(audio_file_wav, model_path)
        print(f"Recognized Text: {recognized_text}")

        # Save text as PDF in current directory
        pdf_file = os.path.join(output_directory, "transcript.pdf")
        save_text_as_pdf(recognized_text, pdf_file)
        print(f"Text saved as PDF: {pdf_file}")

    except ValueError as ve:
        print(f"Error: {ve}")

    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        
