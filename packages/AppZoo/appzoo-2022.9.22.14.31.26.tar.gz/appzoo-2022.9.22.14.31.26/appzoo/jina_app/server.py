#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : server
# @Time         : 2022/9/9 下午4:59
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

import jieba
from jina import Document, DocumentArray, Executor, Flow, requests


class MyExec(Executor):
    @requests(on='/search')
    async def add_text(self, docs: DocumentArray, **kwargs):
        for d in docs:
            d.text += 'hello, world!'


class Cut(Executor):
    @requests(on='/cut')
    async def add_text(self, docs: DocumentArray, **kwargs):
        for d in docs:
            d.tensor = jieba.lcut(d.text)


# f = Flow(port=9955).add(uses=MyExec).add(uses=Exec)
f = Flow(port=9955).add(uses=MyExec).add(uses=Cut)

# with f:
#     r = f.post('/', DocumentArray.empty(2))
#     print(r.texts)
#
#
with f:
    # backend server forever
    f.block()
