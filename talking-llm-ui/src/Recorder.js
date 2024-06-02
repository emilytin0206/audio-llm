import React, { useState, useRef } from 'react';
import axios from 'axios';
import './Recorder.css';

const Recorder = () => {
    const [isRecording, setIsRecording] = useState(false);
    const [chatHistory, setChatHistory] = useState([]);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

    const handleStartRecording = async () => {
        setIsRecording(true);
        audioChunksRef.current = [];
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        mediaRecorderRef.current.ondataavailable = event => {
            if (event.data.size > 0) {
                audioChunksRef.current.push(event.data);
            }
        };
        mediaRecorderRef.current.start();
    };

    const handleStopRecording = () => {
        if (mediaRecorderRef.current) {
            setIsRecording(false);
            mediaRecorderRef.current.stop();
            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                const formData = new FormData();
                formData.append('audio', audioBlob);

                try {
                    const response = await axios.post('http://localhost:5000/api/convert', formData, { responseType: 'blob' });

                    const audioUrl = URL.createObjectURL(response.data);
                    const audio = new Audio(audioUrl);
                    audio.play();

                    const assistantMessage = {
                        role: 'assistant',
                        content: 'Audio response received and playing...',
                    };
                    setChatHistory(prevHistory => [...prevHistory, assistantMessage]);
                } catch (error) {
                    console.error('Error sending audio to server:', error);
                    setChatHistory(prevHistory => [...prevHistory, { role: 'system', content: 'Error sending audio to server.' }]);
                }
            };
        }
    };

    return (
        <div className="recorder">
            <div className="chat-history">
                {chatHistory.map((message, index) => (
                    <div key={index} className={`chat-message ${message.role}`}>
                        <div className="message-content">{message.content}</div>
                    </div>
                ))}
            </div>
            <button
                className={`record-button ${isRecording ? 'recording' : ''}`}
                onClick={isRecording ? handleStopRecording : handleStartRecording}
            >
                <img src="microphone-icon.png" alt="Record" />
            </button>
        </div>
    );
};

export default Recorder;
