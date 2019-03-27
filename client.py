import grpc
import json

# import the generated classes
from NLP.grpcs import nlp_pb2_grpc, nlp_pb2

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = nlp_pb2_grpc.NlpProcessorStub(channel)

# create a valid request message
data = json.dumps({"kind": "course", "img": {"src": "https://cdn.filestackcontent.com/UqtJqsGSRPiYq8um9fQ7"}, "lxp": {"rating": None, "groups": None, "channels": None, "published_at": 1438214400.0, "prices_data": [], "is_public": False, "users_with_access": None, "category": [{"type": "provider_name", "value": "BFS"}], "additional_metadata": None, "user_id": None, "title": "101 India BFS Commercial TDIC New Hire TREASURY PAYMENT_India_NewHireLP", "restricted_groups": None, "hidden": False, "status": 2, "description": "This Training belongs to New hires. The leaners will understand process specific fundamentals and overview which will help them perform effecctively during OJT and IPRGFTE phases.", "tags": None, "pack_items": [], "organization_id": 15, "plan": ["free"], "restricted_users": None, "source_type_name": "csod", "duration_metadata": {"calculated_duration": 12600, "calculated_duration_display": "about 4 hours"}, "is_private": False, "source_type_id": "7fea23ad-3a0c-43cb-9752-956ab27d65c4", "language": "en", "level": None, "is_paid": False, "readable_card_type": "Curriculum", "content_type": "course", "source_id": "3b5dc86e-6c34-4451-bade-14e1d7db5d05", "external_id": "f27ddfe1-cac2-4c14-819a-0489c4ce207b"}, "headline": "101 India BFS Commercial TDIC New Hire TREASURY PAYMENT_India_NewHireLP", "abstract": None, "oid": "02ef433c-8fe2-4865-9fd4-d3db752ec6d0", "excerpt": None, "uri": "https://genpact.csod.com/samldefault.aspx?ouid=2&returnurl=https%3A%2F%2Fgenpact.csod.com%2FLMS%2FLoDetails%2FDetailsLo.aspx%3Floid%3Df27ddfe1-cac2-4c14-819a-0489c4ce207b", "ts": 1553683632.633, "images": [{"src": "https://cdn.filestackcontent.com/UqtJqsGSRPiYq8um9fQ7"}], "_id": "02ef433c-8fe2-4865-9fd4-d3db752ec6d0"})
idata = nlp_pb2.idata(oid="02ef433c-8fe2-4865-9fd4-d3db752ec6d0", data=data, stemming=False,
                      named_entities=False, remove_stops=True, lemmatize=True)

# make the call
response = stub.process_nlp(idata)

# response
print(response.value)