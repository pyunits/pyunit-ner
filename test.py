#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/4/11 11:44
# @Author: Jtyoui@qq.com
import pprint
import time
from pyunit_ner import ernie_st, ernie_match, ERNIE_LABEL_MAP, ERNIE_MODEL_PARAMETER, parseNER


def test():
    # 默认的模型参数和映射表
    model = '/home/jtyoui/Documents/model'
    s = ernie_st(new_model_path=model, new_config=ERNIE_MODEL_PARAMETER, new_label_map_config=ERNIE_LABEL_MAP)
    start = time.time()
    for i in range(10):
        data = ernie_match('刘万光对李伟说：在贵阳市南明村永乐乡发生了一件恐怖的事情', s)
        result = parseNER(data)
    print(time.time() - start)
    return result


if __name__ == '__main__':
    pprint.pprint(test())
