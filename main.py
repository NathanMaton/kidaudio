import requests
import os
from playsound import playsound
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/suno/bark"
headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def save_audio(audio_bytes, filename="output.wav"):
	with open(filename, "wb") as audio_file:
		audio_file.write(audio_bytes)
	return filename

def main():
	if not os.getenv('HUGGING_FACE_API_KEY'):
		print("Error: Hugging Face API key not found. Please check your .env file.")
		return

	while True:
		text = input("Enter the text you want to convert to speech (or 'q' to quit): ")
		if text.lower() == 'q':
			break

		print("Generating audio...")
		audio_bytes = query({
			"inputs": ' ♪ ' + text + ' ♪ ',
		})
		
		filename = input("Enter the filename to save the audio (default: output.wav): ")
		if not filename:
			filename = "output.wav"
		
		saved_file = save_audio(audio_bytes, filename)
		print(f"Audio saved as {saved_file}")
		
		play_audio = input("Do you want to play the audio? (y/n): ")
		if play_audio.lower() == 'y':
			try:
				playsound(saved_file)
			except Exception as e:
				print(f"Error playing audio: {e}")

if __name__ == "__main__":
	main()