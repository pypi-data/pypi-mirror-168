# 定义访问data network的接口

import json
import requests
import pandas as pd

CITYBRAIN_URL = "http://192.168.15.48:8080/api/getData"

def get_data(data_address, payload = '', token = None):
    """
    从data address中获取数据。目前支持json格式
    """
    ## TODO: lack of data_address checking
    resp = requests.post(url=CITYBRAIN_URL, 
        headers=build_headers(token),
        data=build_param(data_address, payload))
    ## TODO: lack of response status checking
    return handle_data(resp.json())


def build_headers(token = None):
    """
    构建参数头
    @param token citybrain的token，非public的data system访问需要
    @return Dictional
    """
    headers = {'content-type': 'application/json;charset=utf8'}
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    return headers


def build_param(data_address, payload = ''):
    """
    构建请求参数
    """
    ## TODO: lack of payload detail checking like database or hyperlink
    return json.dumps({
        'dpAddress': data_address,
        'payload': payload
    })

def handle_data(body):
    """
    处理requests得到的json格式的数据
    @param data json格式的数据，包含 code, message, data 字段
    @return DataFrame 返回一个pandas的dataframe数据
    """
    code = body['code']    
    if code != 200:
        print('code is not 200. code: ', code, type(code))
        # TODO: lack of error handling logic code
        return None
    data = body['data'] # TODO: 为什么要剥两层？两层都是在哪里做的？
    inner_body = json.loads(data)
    return pd.DataFrame(inner_body['data'])
    