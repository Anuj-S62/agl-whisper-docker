import whisper

class STTModel:
    def __init__(self, model_path):
        self.model = whisper.load_model(model_path)

    def transcribe(self, audio_data):
        return self.model.transcribe(audio_data, fp16=False)