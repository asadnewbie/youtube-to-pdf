# youtube-to-pdf



# YouTube Audio to Text Converter

This Python script downloads audio from YouTube videos, converts it to text using Vosk speech recognition, and saves the transcript as a PDF file.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository

    Install dependencies:

    bash

    pip install pytube pydub vosk fpdf

    Download the Vosk model:
        Download the Vosk model from https://alphacephei.com/vosk/models and extract it into the project directory.

Usage

    Run the script:

    bash

    python3 ytpdf.py

    Enter the YouTube video URL when prompted.

    The script will download the audio, convert it to text, and save it as transcript.pdf in the output directory.

Contributing

Contributions are welcome! Here's how you can contribute:

    Submit bug reports or feature requests as issues.
    Fork the repository, create your branch, and submit a pull request.

License

This project is licensed under the MIT License - see the LICENSE file for details.




### Notes:
- Replace `yourusername` and `your-repository` with your actual GitHub username and repository name.
- Ensure the dependencies (`pytube`, `pydub`, `vosk`, `fpdf`) are correctly installed and the Vosk model is downloaded and placed in the project directory before running the script.
- Provide additional details as needed based on your project's specific requirements and functionalities.
- download the vosk model from the vosk website and extract the model to path same as your script path.
- you can change the path in the script.

