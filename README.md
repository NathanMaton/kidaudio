# AI Song Creator

This project uses AI to generate songs from input lyrics. It combines OpenAI's GPT model for melody and chord generation with Suno's Bark API for text-to-speech synthesis to create a complete song.

## Features

- Generate melodies and chord progressions from input lyrics
- Create vocal tracks using text-to-speech synthesis
- Combine instrumental and vocal tracks into a complete song

## Prerequisites

- Python 3.7+
- OpenAI API key
- Hugging Face API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-song-creator.git
   cd ai-song-creator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   HUGGING_FACE_API_KEY=your_hugging_face_api_key_here
   ```

## Usage

Run the main script:
