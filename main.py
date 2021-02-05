#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/12/27 17:48
# @Author: Jtyoui@qq.com
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pyunit_ner import reader_text
from pydantic import BaseModel

app = FastAPI(title='实体抽取', description='实体抽取接口文档', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResponseModal(BaseModel):
    """返回格式类型"""
    msg: str = 'success'
    code: int = 200
    entity: list = [{
        "address": [],
        "number": [],
        "organization": [],
        "person": [],
        "word": []
    }]


@app.get('/pyunit/ner', summary='实体接口', response_model=ResponseModal)
async def st(data: str = Query(..., description='文本数据,多文本格式：文本-分割符-文本', min_length=1),
             sep: str = Query(None, description='分割符，默认是：|，比如：文本|文本|文本', min_length=1)):
    """实体抽取"""
    try:
        sep = sep or '|'
        ls = data.split(sep)
        entity = reader_text(ls)
        return ResponseModal(entity=entity)
    except Exception as e:
        return ResponseModal(msg=str(e))
