import grpc
import argparse
from generated import audio_processing_pb2
from generated import audio_processing_pb2_grpc

def run(ip, port, audio_file_path):
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = audio_processing_pb2_grpc.AudioProcessingStub(channel)
        
        # Read audio file (must be 16kHz mono WAV file)
        with open(audio_file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
                
        # Create a request
        request = audio_processing_pb2.AudioRequest(audio_data=audio_data)
        
        # Send request and get response
        response = stub.ProcessAudio(request)
        
        print(f"Received text: {response.text}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Audio processing client")
    parser.add_argument('--ip', type=str, required=True, help='IP address of the server')
    parser.add_argument('--port', type=int, required=True, help='Port of the server')
    parser.add_argument('--audio_file', type=str, required=True, help='Path to the audio file')
    
    args = parser.parse_args()
    
    run(args.ip, args.port, args.audio_file)
