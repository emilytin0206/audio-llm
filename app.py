from flask import Flask, request, jsonify, send_file
from flask_cors import CORS 
import numpy as np
import whisper
from pydub import AudioSegment
import os
from io import BytesIO
import requests
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from tts import TextToSpeechService
from scipy.io.wavfile import write as write_wav


app = Flask(__name__) 
CORS(app) 


stt = whisper.load_model("base.en")
tts = TextToSpeechService()



template = """
You are a helpful and friendly AI assistant. You are polite, respectful, and aim to provide concise responses of less 
than 20 words.

The conversation transcript is as follows:
{history}

And here is the user's follow-up: {input}

Your response:
"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
chain = ConversationChain(
    prompt=PROMPT,
    verbose=False,
    memory=ConversationBufferMemory(ai_prefix="Assistant:"),
    llm=Ollama(),
)

@app.route('/api/convert', methods=['POST'])
def convert_audio():
    audio_file = request.files['audio']
    audio_data = audio_file.read()

    try:
        print("receive audio...")
        audio = AudioSegment.from_file(BytesIO(audio_data), format="webm")
        byte_stream = BytesIO()
        audio.export(byte_stream, format="wav")
        audio_np = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
    except Exception as e:
        return jsonify(error=str(e)), 400

    if audio_np.size > 0:
        print("whisper work....")
        text = transcribe(audio_np)
        try:
            print("ollama work....")
            response_text = get_llm_response(text)
        except requests.ConnectionError as e:
            return jsonify(error="Failed to connect to Ollama server: " + str(e)), 500

        print("bark work....")
        sample_rate, audio_array = tts.long_form_synthesize(response_text)

        #for debug
        # print("Sample rate:", sample_rate)
        # print("Audio array first 10 samples:", audio_array[:10])


        max_int16 = np.iinfo(np.int16).max
        audio_array = (audio_array * max_int16).astype(np.int16)

        byte_stream = BytesIO()
        write_wav(byte_stream, sample_rate, audio_array)
        byte_stream.seek(0)

        return send_file(
            byte_stream,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='response.wav'
        )
    else:
        return jsonify(error="No audio recorded"), 400


def transcribe(audio_np: np.ndarray) -> str:
    result = stt.transcribe(audio_np, fp16=False)  # Set fp16=True if using a GPU
    text = result["text"].strip()
    return text


def get_llm_response(text: str) -> str:
    response = chain.predict(input=text)
    if response.startswith("Assistant:"):
        response = response[len("Assistant:") :].strip()
    return response


if __name__ == '__main__':
    os.makedirs('audio_files', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)

