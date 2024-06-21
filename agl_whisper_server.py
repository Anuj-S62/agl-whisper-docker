import grpc
from concurrent import futures
from generated import audio_processing_pb2_grpc
import logging
from servicer.audio_processing_servicer import AudioProcessingServicer


def run_server(server_port, model_path):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_processing_pb2_grpc.add_AudioProcessingServicer_to_server(AudioProcessingServicer(model_path), server)
    server.add_insecure_port(f'[::]:{server_port}')
    logging.info("Starting server on %s...",server_port)
    server.start()
    server.wait_for_termination()
