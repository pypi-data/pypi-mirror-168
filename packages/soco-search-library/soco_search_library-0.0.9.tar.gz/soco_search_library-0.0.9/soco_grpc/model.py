import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import json
from soco_grpc import plugins_pb2
from soco_grpc import plugins_pb2_grpc


class Model(plugins_pb2_grpc.PluginsServicer):
    def __init__(self, _model):
        self.vs = _model()

    def plugin(self, request, context) -> plugins_pb2.Output:
        batch = []
        for key in request.body:
            data = request.body[key]
            data_list = data.list_value
            for item in data_list.values:
                batch.append(json.loads(item))
        return plugins_pb2.Output(resp=json.dumps(self.vs.plugin_method(batch)))
