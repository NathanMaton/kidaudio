import os
from transformers import AutoProcessor, AutoModel
import scipy.io.wavfile as wavfile
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the Hugging Face API key
os.environ["HUGGING_FACE_API_KEY"] = os.getenv("HUGGING_FACE_API_KEY")

# Initialize the Bark model and processor
processor = AutoProcessor.from_pretrained("suno/bark")
model = AutoModel.from_pretrained("suno/bark")

def generate_audio(text):
    # Prepare the input
    inputs = processor(text, return_tensors="pt")

    # Generate audio
    audio_array = model.generate(**inputs, do_sample=True)

    # Convert the audio array to int16 format
    audio_array = (audio_array.cpu().numpy().squeeze() * 32767).astype(np.int16)

    return audio_array

def save_audio(audio_array, filename="output.wav"):
    # Save the audio as a WAV file
    wavfile.write(filename, rate=22050, data=audio_array)

def main():
    if not os.getenv('HUGGING_FACE_API_KEY'):
        print("Error: Hugging Face API key not found. Please check your .env file.")
        return

    print("Welcome to the Bark Text-to-Speech Generator!")
    while True:
        text = input("Enter the text you want to convert to speech (or 'q' to quit): ")
        if text.lower() == 'q':
            break

        print("Generating audio...")
        audio_array = generate_audio(text)
        
        filename = input("Enter the filename to save the audio (default: output.wav): ")
        if not filename:
            filename = "output.wav"
        
        save_audio(audio_array, filename)
        print(f"Audio saved as {filename}")

if __name__ == "__main__":
    main()