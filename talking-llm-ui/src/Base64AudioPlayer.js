import React from 'react';

const Base64AudioPlayer = () => {
    const handleTestAudio = async () => {
        const testBase64String = "UklGRhIAAABXQVZFZm10IBAAAAABAAEAgD4AAAB9AAACABAAZGF0YQAAAAA="; // 这里替换为你的有效Base64编码的WAV文件
        const audioBuffer = await convertBase64ToArrayBuffer(testBase64String);
        await playAudio(audioBuffer);
    };

    const convertBase64ToArrayBuffer = (base64String) => {
        const binaryString = atob(base64String);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        return bytes.buffer;
    };

    const playAudio = async (audioBuffer) => {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        try {
            const audioData = await audioContext.decodeAudioData(audioBuffer);
            const audioSource = audioContext.createBufferSource();
            audioSource.buffer = audioData;
            audioSource.connect(audioContext.destination);
            audioSource.start();
        } catch (error) {
            console.error('Error decoding audio data:', error);
            console.log("Audio Buffer (for debugging):", audioBuffer);
        }
    };

    return (
        <div>
            <button onClick={handleTestAudio}>Test Audio</button>
        </div>
    );
};

export default Base64AudioPlayer;
