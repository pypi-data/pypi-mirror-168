#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : client
# @Time         : 2022/8/19 下午5:15
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import grpc
from appzoo.grpc_app.utils import _options
from appzoo.grpc_app.protos.base_pb2 import Request, Response
from appzoo.grpc_app.protos.base_pb2_grpc import GrpcServiceServicer, GrpcServiceStub, add_GrpcServiceServicer_to_server

from pickle import dumps, loads


class Client(object):

    def __init__(self, ip='0.0.0.0', port=8000, options=None, is_async=False):
        self.options = options if options else _options

        if is_async:
            self.conn = grpc.aio.insecure_channel(f"{ip}:{port}", options=self.options)
        self.conn = grpc.insecure_channel(f"{ip}:{port}", options=self.options)

        self._client = GrpcServiceStub(channel=self.conn)

    def request(self, data): # todo: 生成 http 服务
        input = dumps(data)
        request = Request(data=input)
        response = self._client._request(request)
        output = loads(response.data)
        return output

    @classmethod
    def muiti_request(cls, batch_data, max_workers=2, **kwargs):
        from meutils.pipe import xThreadPoolExecutor
        return list(batch_data | xThreadPoolExecutor(cls(**kwargs).request, max_workers))


if __name__ == '__main__':
    client = Client(is_async=True)

    # import sys

    # i = ['1, 2, 3, 4', 'as'] * 10000
    # print(sys.getsizeof(dumps(i)) / 1024 ** 2)
    # _ = client.request(i)
    # print(_)

    # Client.muiti_request(range(10))

    print(client.request(1))
