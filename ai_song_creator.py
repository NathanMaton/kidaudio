import openai
import requests
import os
from pydub import AudioSegment
from pydub.generators import Sine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

# Bark API setup
BARK_API_URL = "https://api-inference.huggingface.co/models/suno/bark"
BARK_HEADERS = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

def generate_melody_and_chords(lyrics):
    prompt = f"Generate a simple melody and chord progression for these lyrics:\n\n{lyrics}\n\nProvide the output in the following format:\nMelody: [Notes separated by spaces]\nChords: [Chord progression]"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def generate_vocals(lyrics):
    response = requests.post(BARK_API_URL, headers=BARK_HEADERS, json={"inputs": lyrics})
    return response.content

def create_instrumental(melody, chords, duration_ms):
    audio = AudioSegment.silent(duration=duration_ms)
    
    # Create a simple sine wave for the melody
    for note in melody.split():
        freq = note_to_freq(note)
        tone = Sine(freq).to_audio_segment(duration=500)
        audio = audio.overlay(tone)
    
    # Add simple chord progression
    for chord in chords.split():
        freq = note_to_freq(chord[0])
        chord_tone = Sine(freq).to_audio_segment(duration=2000)
        audio = audio.overlay(chord_tone)
    
    return audio

def note_to_freq(note):
    # This is a simplified conversion, you might want to use a more accurate method
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = 4
    if note[-1].isdigit():
        octave = int(note[-1])
        note = note[:-1]
    semitones = notes.index(note)
    return 440 * (2 ** ((semitones - 9) / 12)) * (2 ** (octave - 4))

def main():
    if not openai.api_key or not HUGGING_FACE_API_KEY:
        print("Error: API keys not found. Please check your .env file.")
        return

    print("Welcome to the AI Song Creator!")
    lyrics = input("Enter your song lyrics:\n")
    
    print("Generating melody and chords...")
    melody_and_chords = generate_melody_and_chords(lyrics)
    print(melody_and_chords)
    
    melody, chords = melody_and_chords.split("\n")
    melody = melody.split(": ")[1]
    chords = chords.split(": ")[1]
    
    print("Generating vocals...")
    vocals_audio = generate_vocals(lyrics)
    
    with open("vocals.wav", "wb") as f:
        f.write(vocals_audio)
    
    vocals = AudioSegment.from_wav("vocals.wav")
    
    print("Creating instrumental...")
    instrumental = create_instrumental(melody, chords, len(vocals))
    
    print("Mixing the song...")
    final_song = instrumental.overlay(vocals)
    
    output_file = "ai_generated_song.mp3"
    final_song.export(output_file, format="mp3")
    print(f"Song created and saved as {output_file}")

if __name__ == "__main__":
    main()