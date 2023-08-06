#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : service
# @Time         : 2022/8/19 下午5:14
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 支持多个文件多个主函数


import grpc
from appzoo.grpc_app.utils import _options
from appzoo.grpc_app.protos.base_pb2 import Request, Response
from appzoo.grpc_app.protos.base_pb2_grpc import GrpcServiceServicer, GrpcServiceStub, add_GrpcServiceServicer_to_server

from meutils.pipe import *
from pickle import dumps, loads


class Service(GrpcServiceServicer):

    def __init__(self, debug=False, options=None):
        self.debug = debug
        self.options = options if options else _options

    def main(self, *args, **kwargs):
        """主逻辑"""
        raise NotImplementedError('Method not implemented!')

    @logger.catch()
    def _request(self, request, context):
        input = loads(request.data)  # 反序列化
        if self.debug:
            logger.debug(input)

        try:
            output = self.main(input)
        except Exception as e:
            output = {'error': e}

        return Response(data=dumps(output))  # 序列化

    def run(self, port=8000, max_workers=None, is_async=False):
        if is_async:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait([self.async_server()]))
            loop.close()

        server = grpc.server(ThreadPoolExecutor(max_workers), options=self.options)  # compression = None
        add_GrpcServiceServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{port}')

        logger.info("GrpcService Running ...")
        logger.info(f"{LOCAL_HOST}:{port}")

        server.start()
        server.wait_for_termination()

    async def async_server(self, port=8000, max_workers=None):
        server = grpc.aio.server(ThreadPoolExecutor(max_workers), options=self.options)
        add_GrpcServiceServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{port}')

        logger.info("Async GrpcService Running ...")
        logger.info(f"{LOCAL_HOST}:{port}")

        await server.start()
        await server.wait_for_termination()


if __name__ == '__main__':
    class MyService(Service):

        def main(self, data):
            1 / 0


    # from meutils.path_utils import import_mains
    #
    # mains = import_mains('multi_apps')
    #
    # class MyService(Service):
    #
    #     def main(self, data):
    #         method, data = data
    #         if method in mains:
    #             return mains[method](data)

    MyService(debug=True).run(max_workers=2)
