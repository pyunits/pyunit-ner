#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/11/7 10:26
# @Author: Jtyoui@qq.com
import re

from .run_msra import ernie_st, ernie_match, ERNIE_MODEL_PARAMETER, ERNIE_LABEL_MAP  # 实体识别


def parseNER(msra) -> dict:
    """解析出实体

    :param msra: msra识别出的数据
    :return: 实体
    """
    number = [str(i) for i in msra[0]]
    data = {'number': number, 'word': list(msra[1])}
    num = ''.join(number)
    word = msra[1]
    if len(num) != len(word):
        raise TypeError('识别出现异常！')
    match = re.finditer('(?=0)[01]+', num)
    data['person'] = [word[r.start():r.end()] for r in match]
    match = re.finditer('(?=2)[23]+', num)
    data['organization'] = [word[r.start():r.end()] for r in match]
    match = re.finditer('(?=4)[45]+', num)
    data['address'] = [word[r.start():r.end()] for r in match]
    return data


__version__ = '2020.8.12'
__author__ = 'Jtyoui'
__description__ = '百度实体抽取模型'
__email__ = 'jtyoui@qq.com'
__names__ = 'pyUnit_ner'
__url__ = 'https://github.com/PyUnit/pyunit-ner'
