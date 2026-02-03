from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import os
import traceback
from utils import decode_base64_audio, convert_mp3_to_wav
from detector import VoiceDetector

app = FastAPI(title="AI Voice Detection API")
detector = VoiceDetector()

# Configuration
API_KEY = os.getenv("API_KEY", "sk_test_123456789")
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

class DetectionRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

@app.post("/api/voice-detection")
async def detect_voice(
    request: DetectionRequest,
    x_api_key: str = Header(None)
):
    # 1. Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key or malformed request")

    # 2. Validation
    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Language {request.language} not supported")
    
    if request.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Only MP3 format is supported")

    try:
        # 3. Process Audio
        mp3_buffer = decode_base64_audio(request.audioBase64)
        wav_buffer = convert_mp3_to_wav(mp3_buffer)
        
        # 4. Analyze
        result = detector.analyze(wav_buffer, request.language)
        
        # 5. Return Response
        return {
            "status": "success",
            "language": request.language,
            "classification": result["classification"],
            "confidenceScore": result["confidenceScore"],
            "explanation": result["explanation"]
        }
        
    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
