from flask import Flask, request
from concurrent import futures
import grpc
import audio_pb2, audio_pb2_grpc

app = Flask(__name__)

class AudioService(audio_pb2_grpc.AudioServiceServicer):
    def StreamAudio(self, request_iterator, context):
        for audio_chunk in request_iterator:
            # process the audio chunk...
            pass

        return audio_pb2.StreamAudioResponse(message='Audio streamed successfully')

def convert_to_grpc(audio_stream):
    chunk_size = 1024

    if not isinstance(audio_stream, bytes):
        audio_stream = bytes(audio_stream, 'utf-8')

    for i in range(0, len(audio_stream), chunk_size):
        chunk = audio_stream[i:i+chunk_size]
        yield audio_pb2.AudioChunk(data=chunk)

@app.route('/siprec', methods=['POST'])
def handle_siprec():
    audio_stream = request.data

    grpc_stream = convert_to_grpc(audio_stream)

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = audio_pb2_grpc.AudioServiceStub(channel)
        response = stub.StreamAudio(grpc_stream)

    return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_AudioServiceServicer_to_server(AudioService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    # Run the Flask app in the same process
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    serve()