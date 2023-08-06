#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : demo
# @Time         : 2022/9/9 上午8:42
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


def get_module_mains(dir='multi_apps', pattern='*.py', filters=None):  # todo: 优化
    """加载当前app_dir文件夹下的所有app（递归）, 入口函数都是main
    1. 过滤掉 _ 开头的py文件
    2. 支持单文件

    appcli easy-run <app_dir>
    """
    if filters is None:
        filters = []
    filters += ['__init__.py']

    app_home = Path(sys_path_append(dir))
    n = app_home.parts.__len__()

    main_map = {}
    for p in app_home.rglob(pattern):
        if p.name in filters:
            continue

        home_parts = p.parts[n:]
        module_name = '.'.join(home_parts).strip('.py')
        module = importlib.import_module(module_name)

        if hasattr(module, 'main'):  # 含有main入口函数的
            main_map[f'{app_home.stem}.{module_name}'] = getattr(module, 'main')

    return main_map


main_map = get_module_mains()

print(main_map)
