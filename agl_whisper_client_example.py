import grpc
from generated import audio_processing_pb2
from generated import audio_processing_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = audio_processing_pb2_grpc.AudioProcessingStub(channel)
        
        # Read audio file (must be 16kHz mono WAV file)
        with open('audio.wav', 'rb') as audio_file:
            audio_data = audio_file.read()
                
        # Create a request
        request = audio_processing_pb2.AudioRequest(audio_data=audio_data)
        
        # Send request and get response
        response = stub.ProcessAudio(request)
        
        print(f"Received text: {response.text}")

if __name__ == '__main__':
    run()
