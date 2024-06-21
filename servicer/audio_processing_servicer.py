import grpc
from concurrent import futures
from generated import audio_processing_pb2_grpc
from generated import audio_processing_pb2
import logging
import tempfile
import os
from stt_model import STTModel

# Configure logging
logging.basicConfig(level=logging.INFO)

class AudioProcessingServicer(audio_processing_pb2_grpc.AudioProcessingServicer):

    def __init__(self, model_path):
        logging.info("Loading STT model...")
        logging.info(f"model path: {model_path}")

        self.stt_model = STTModel(model_path)
        print("STT model loaded successfully")
        logging.info("STT model loaded successfully")

    def ProcessAudio(self, request, context):

        # Save audio data to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            temp_audio_file.write(request.audio_data)
            temp_audio_file_path = temp_audio_file.name

        logging.info("Processing audio data using Whisper model...")

        # Transcribe the audio using STT model
        try:
            result = self.stt_model.transcribe(temp_audio_file_path)
            text = result['text']
            logging.info(f"Recognition successful: {text}")
            return audio_processing_pb2.TextResponse(text=text)
        except Exception as e:
            logging.error(f"Error during transcription: {e}")
            return audio_processing_pb2.TextResponse(text=f"Error during transcription: {e}")
        finally:
            # Clean up temporary file
            os.remove(temp_audio_file_path)

 