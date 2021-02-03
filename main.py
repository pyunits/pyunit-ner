#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/12/27 17:48
# @Author: Jtyoui@qq.com
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pyunit_ner import ernie_match, ernie_st, parseNER
from pydantic import BaseModel

app = FastAPI(title='实体抽取', description='实体抽取接口文档', version='1.0')
ERNIE_MODEL_PATH = os.environ.get('MODEL_PATH', '/mnt/model')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENTITY = ernie_st(ERNIE_MODEL_PATH)


class ResponseModal(BaseModel):
    """返回格式类型"""
    msg: str = 'success'
    code: int = 200
    entity: dict = {
        "address": [],
        "number": [],
        "organization": [],
        "person": [],
        "word": []
    }


@app.get('/pyunit/ner', summary='实体接口', response_model=ResponseModal)
def st(data: str = Query(..., description='文本数据', min_length=1)):
    """实体抽取"""
    try:
        word = ernie_match(data, ENTITY)
        entity = parseNER(word)
        return ResponseModal(entity=entity)
    except Exception as e:
        return ResponseModal(msg=str(e))
