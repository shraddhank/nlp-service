import grpc
from concurrent import futures
import time

# import the generated classes
from NLP.grpcs import nlp_pb2_grpc, nlp_pb2


# import the original NLP.py
from NLP.nlp_proc import NlpProc




# create a class to define the server functions, derived from
# calculator_pb2_grpc.CalculatorServicer
class NlpProcessorServicer(nlp_pb2_grpc.NlpProcessorServicer):

    # calculator.square_root is exposed here
    # the request and response are of the data type
    # calculator_pb2.Number
    def process_nlp(self, request, context):
        response = nlp_pb2.odata()
        nlp_proc = NlpProc()
        response.oid, response.data = nlp_proc.perform_nlp(request.oid, request.data, request.stemming,
                                              request.named_entities, request.remove_stops, request.lemmatize)
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
nlp_pb2_grpc.add_NlpProcessorServicer_to_server(
    NlpProcessorServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        print("server running.....")
        time.sleep(86400)
except KeyboardInterrupt:
    print("server stopped")
    server.stop(0)
