import grpc

# import the generated classes
from grpcs import nlp_pb2
from grpcs import nlp_pb2_grpc



# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = nlp_pb2_grpc.NlpProcessorStub(channel)

# create a valid request message
text = "The SciPy stack in Python is a mature and quickly expanding platform for scientific and numerical computing. The platform hosts libraries such as scikit-learn the general purpose machine learning library that can be used with your deep learning models.It is because of these benefits of the Python ecosystem that two top numerical libraries for deep learning were developed for Python, Theano and the newer TensorFlow library released by Google (and adopted recently by the Google DeepMind research group).Theano and TensorFlow are two top numerical libraries for developing deep learning models, but are too technical and complex for the average practitioner. They are intended more for research and development teams and academics interested in developing wholly new deep learning algorithms."
idata = nlp_pb2.idata(oid="123", data=text)

# make the call
response = stub.process_nlp(idata)

# response
print(response.value)