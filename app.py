#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/12/27 17:48
# @Author: Jtyoui@qq.com
import json
import os

from flask import Flask, request, jsonify

from pyunit_ner import ernie_match, ernie_st, parseNER

app = Flask(__name__)
ERNIE_MODEL_PATH = os.environ['MODEL_PATH']
ENTITY = []


def flask_content_type(requests):
    """根据不同的content_type来解析数据"""
    if requests.method == 'POST':
        if requests.content_type == 'application/x-www-form-urlencoded':
            data = requests.form
        elif requests.content_type == 'application/json':
            data = json.loads(requests.data)
        else:  # 无法被解析出来的数据
            raise Exception('POST的Content-Type必须是:application/x-www-form-urlencoded')
    elif requests.method == 'GET':
        data = requests.args
    else:
        raise Exception('只支持GET和POST请求')
    return data


@app.before_first_request
def first():
    global ENTITY
    ENTITY = ernie_st(ERNIE_MODEL_PATH)


@app.route('/')
def hello():
    return jsonify(code=200, result='welcome to pyunit-ner entity')


@app.route('/pyunit/ner', methods=['POST', 'GET'])
def st():
    """实体抽取"""
    data = flask_content_type(request)
    try:
        word = data.get('data')
        data = ernie_match(word, ENTITY)
        entity = parseNER(data)
        return jsonify(entity=entity, msg='success', code=200)
    except Exception as e:
        return jsonify(code=400, msg=str(e))


if __name__ == '__main__':
    app.run(port=9000)
