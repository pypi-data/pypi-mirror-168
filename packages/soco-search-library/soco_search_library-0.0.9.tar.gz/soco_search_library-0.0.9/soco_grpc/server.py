import argparse
import asyncio
import logging

import grpc
from plugin_class import PluginClass

from soco_grpc import plugins_pb2_grpc
from soco_grpc.model import Model
from concurrent import futures


async def serve() -> None:
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description='Starting a GRPC server')
    parser.add_argument('--host', type=str, default='[::]')
    parser.add_argument('--port', type=int, default=50070)
    parser.add_argument('--workers', type=int, default=1)

    args = parser.parse_args()

    # create a gRPC server
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=args.workers))
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=args.workers))

    # to add the defined class to the server
    plugins_pb2_grpc.add_PluginsServicer_to_server(Model(PluginClass), server)

    # listen on port 50070
    logger.info('Starting server. Listening on port {}:{}'.format(args.host, args.port))
    server.add_insecure_port('{}:{}'.format(args.host, args.port))
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())
