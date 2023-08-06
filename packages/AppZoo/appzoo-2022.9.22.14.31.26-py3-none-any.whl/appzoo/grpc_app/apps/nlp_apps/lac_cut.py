#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : cut
# @Time         : 2022/9/16 上午11:10
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from LAC import LAC

lac = LAC()


def main(w, custom_dictionary=()):
    """单个词"""
    if custom_dictionary:
        lac.model.custom = None
        lac.add_word(' '.join(custom_dictionary))

    ws = w.strip().split()
    return lac.run(ws) | xmap(lambda x: x[0]) | xchain | xlist


if __name__ == '__main__':
    print(main('我们的质押 率'))
