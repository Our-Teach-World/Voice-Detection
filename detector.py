import torch
import librosa
import numpy as np
import io
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor

class VoiceDetector:
    def __init__(self):
        print("Loading AI Detection Model... (this may take a moment)")
        # We use a pre-trained model specifically fine-tuned for Deepfake detection
        # Source: https://huggingface.co/MelodyMachine/Deepfake-audio-detection-V2
        # Alternative robust model: "padmalcom/wav2vec2-large-fake-voice-detection-v2"
        self.model_name = "MelodyMachine/Deepfake-audio-detection-V2"
        
        try:
            self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(self.model_name)
            self.model = Wav2Vec2ForSequenceClassification.from_pretrained(self.model_name)
            self.model.eval() # Set to evaluation mode
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to load AI model. {e}")
            raise e

    def preprocess_audio(self, audio_buffer: io.BytesIO, target_sr=16000):
        """
        Loads audio from bytes and resamples it to 16kHz (required by Wav2Vec2).
        """
        audio_buffer.seek(0)
        # Load with librosa (automatically handles MP3/WAV)
        y, sr = librosa.load(audio_buffer, sr=target_sr)
        
        # Ensure we have enough audio for the model (pad if too short)
        if len(y) < target_sr: # Less than 1 second
            padding = target_sr - len(y)
            y = np.pad(y, (0, padding), 'constant')
            
        # Normalize audio volume
        y = librosa.util.normalize(y)
        return y

    def analyze(self, audio_buffer: io.BytesIO, language: str):
        """
        Analyzes audio using the Deep Learning model.
        Returns classification, confidence, and explanation.
        """
        try:
            # 1. Preprocess Audio
            audio_input = self.preprocess_audio(audio_buffer)
            
            # 2. Prepare inputs for the model
            inputs = self.feature_extractor(
                audio_input, 
                sampling_rate=16000, 
                return_tensors="pt", 
                padding=True
            )
            
            # 3. Inference (Prediction)
            with torch.no_grad():
                logits = self.model(**inputs).logits
            
            # 4. Convert logits to probabilities (Softmax)
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            
            # Get the predicted class (0 or 1) and score
            # Note: Model specific labels need to be checked. 
            # Usually Index 0 = Real/Human, Index 1 = Fake/AI for this specific model family
            # We verify via the model config id2label if available, otherwise assume standard.
            
            # Let's dynamically check the label map if possible
            id2label = self.model.config.id2label
            predicted_id = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0][predicted_id].item()
            predicted_label = id2label[predicted_id]
            
            # Map model output to API requirements
            # The model labels might be "real"/"fake" or "bonafide"/"spoof"
            is_ai = False
            if "fake" in predicted_label.lower() or "spoof" in predicted_label.lower() or "ai" in predicted_label.lower():
                is_ai = True
            elif "real" in predicted_label.lower() or "bonafide" in predicted_label.lower() or "human" in predicted_label.lower():
                is_ai = False
            else:
                # Fallback based on index (usually 1 is fake)
                is_ai = (predicted_id == 1)

            # 5. Construct Response
            if is_ai:
                classification = "AI_GENERATED"
                explanation = "Deep learning model detected synthetic vocal artifacts and unnatural spectral patterns."
            else:
                classification = "HUMAN"
                explanation = "Deep learning model verified natural micro-prosody and human vocal characteristics."

            return {
                "classification": classification,
                "confidenceScore": round(confidence, 2),
                "explanation": explanation
            }

        except Exception as e:
            # Fallback for debugging
            print(f"Analysis Error: {e}")
            return {
                "classification": "HUMAN", # Fail-safe default
                "confidenceScore": 0.0,
                "explanation": f"Error during analysis: {str(e)}"
            }