#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : paddle_ocr
# @Time         : 2022/9/16 下午12:02
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.io.image import image_read

from paddleocr import PaddleOCR



model = PaddleOCR()
main = pickle_cache(model.ocr, location='ocr_cache')



if __name__ == '__main__':
    print(main(image_read('image.png')))