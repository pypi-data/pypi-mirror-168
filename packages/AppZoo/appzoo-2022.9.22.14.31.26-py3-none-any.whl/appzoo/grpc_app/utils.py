#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : utils
# @Time         : 2022/9/8 下午4:27
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


_options = [
    ('grpc.so_reuseport', 0),
    ('grpc.max_send_message_length', 32 * 1024 * 1024),  # 32 MB
    ('grpc.max_receive_message_length', 32 * 1024 * 1024),
    ('grpc.enable_retries', 1)
]
