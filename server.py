from concurrent import futures

import grpc

from . import siprec

class SIPRECToGRPCService(siprec.SIPRECServiceServicer):

    def __init__(self):
        pass

    def StartStream(self, request, context):
        # Receive the SIPREC audio feed.
        audio_feed = request.audio_feed

        # Convert the SIPREC audio feed to a gRPC stream.
        grpc_stream = siprec.to_grpc_stream(audio_feed)

        # Forward the gRPC stream to Dialogflow.
        dialogflow_response = self.dialogflow_client.streaming_detect_intent(grpc_stream)

        # Return the Dialogflow response.
        return dialogflow_response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    siprec_to_grpc_service = SIPRECToGRPCService()
    siprec.add_SIPRECServiceServicer_to_server(siprec_to_grpc_service, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()