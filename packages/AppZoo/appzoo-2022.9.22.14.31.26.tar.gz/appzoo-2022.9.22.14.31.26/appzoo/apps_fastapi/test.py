#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : test
# @Time         : 2022/9/15 下午2:39
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from paddleocr import PaddleOCR
from PIL import Image

ocr = PaddleOCR(lang="ch", show_log=False,
                use_gpu=False,
                # use_tensorrt=True,
                # use_mp=True, # 多进程

                use_angle_cls=True,
                # enable_mkldnn=True,
                # use_pdserving=True,
                # use_zero_copy_run=True
                )

print(ocr.ocr('image.png'))