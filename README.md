# Local Talking LLM

This project is a local talking LLM (Large Language Model) application that allows users to interact with an AI assistant through voice commands. The assistant uses Whisper for speech-to-text conversion, Ollama for generating responses, and Bark for text-to-speech synthesis.

## Features

- **Speech-to-Text**: Converts user's voice input to text using Whisper.
- **Text Generation**: Generates responses using the Ollama language model.
- **Text-to-Speech**: Converts the generated text responses back to speech using Bark.
- **Interactive Chat Interface**: Displays the conversation in a chat bubble format for a more interactive experience.

## Requirements

- Python 3.8 or higher
- Node.js 14 or higher
- pip for Python package management
- npm for Node.js package management

## Setup
1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/local-talking-llm.git
   cd local-talking-llm
2. **Virtual environment**
   u can use miniconda3
3. **Install Python dependencies**
   ```sh
   pip install -r requirements.txt
4. **Run the backend server**
   ```sh
   python app.py
5. **Frontend setup**
   ```sh
   cd talking-llm-ui
   npm install
   npm start
   
## How It Works
- Recording: Press the record button and speak into your microphone.
- Transcription: The audio is sent to the backend server where Whisper transcribes it to text.
- Response Generation: The transcribed text is processed by Ollama to generate a response.
- Text-to-Speech: The response is converted back to speech using Bark and played back to the user.
- Chat Interface: The conversation is displayed in chat bubbles for easy readability.
   
