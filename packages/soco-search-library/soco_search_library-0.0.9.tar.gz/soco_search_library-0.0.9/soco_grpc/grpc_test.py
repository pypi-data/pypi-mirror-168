from tqdm import tqdm
import time
import grpc
from soco_grpc import plugins_pb2_grpc
from soco_grpc import plugins_pb2
import json
import zlib
import numpy as np


def run(body: dict) -> None:
    # open a gRPC channel
    with grpc.insecure_channel('192.168.1.125:30029') as channel:
        # create a stub (client)
        stub = plugins_pb2_grpc.PluginsStub(channel)
        # Test basic response
        data_list = []
        for item in body["data"]:
            data_list.append(json.dumps(item))

        resp = stub.plugin(plugins_pb2.Input(
            body={
                "data": plugins_pb2.Value(list_value=plugins_pb2.ListValue(values=data_list))
            }
        ))

        resp_dict = json.loads(resp.resp)
        print(resp_dict[0].keys())
        # if resp_dict["success"]:
        #     print("Got Resp")


if __name__ == '__main__':
    body = {
        "data": [{
            "value": 'http://192.168.1.125:30041/video/sample_video.mp4', "configs":{}
        }]
    }
    run(body)
