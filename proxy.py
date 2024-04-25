import grpc
import siprec

class SIPRECToGRPCService(siprec.SIPRECServiceServicer):

    def __init__(self):
        self.dialogflow_client = dialogflow.AgentsClient()

    def StartStream(self, request, context):
        # Receive the SIPREC audio feed.
        audio_feed = request.audio_feed

        # Convert the SIPREC audio feed to a gRPC stream.
        grpc_stream = siprec.to_grpc_stream(audio_feed)

        # Forward the gRPC stream to Dialogflow.
        dialogflow_response = self.dialogflow_client.streaming_detect_intent(grpc_stream)

        # Return the Dialogflow response.
        return dialogflow_response
