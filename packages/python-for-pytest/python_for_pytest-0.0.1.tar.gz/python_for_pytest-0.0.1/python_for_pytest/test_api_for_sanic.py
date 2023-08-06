#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Sun
# datetime:2022/9/19
# sanic框架单元测试样例脚本
import re
import json
from pathlib import Path
from urllib import parse
from functools import reduce

import pytest

from python_for_pytest import (init_template, setup_read_main)

_file_name = "mock_data.xls"
_title_type = 1  # 0：报文参数名写在行，1：报文参数名写在列
_base_path = Path(__file__).resolve().parent

# TODO： 0.根据接口报文初始化生成测试数据模板
request_mock_data = [{
    "uri": "/biz/query/tiktok",
    "method": "get",
    "result": "2",
    "message": "参数非法，符合预期",
    "app_id": "",
    "receive_id": "111111",

},
    {"uri": "/health_check",
     "method": "get",
     "result": "success",
     "message": "连接成功，符合预期",
     }
]
init_template(data=request_mock_data, base_path=_base_path, excel_file_name=_file_name, t_type=_title_type)
# TODO： 1.读取配置好的测试数据
source_data = setup_read_main(source_path=_base_path, f_name=_file_name, t_type=_title_type)
# [{},{}] 如果每个接口的响应格式一样可以采用下面的方面将每个接口合并在一起测试
demo_data = reduce(lambda x, y: x + y, source_data.values())


@pytest.fixture
def api_mock_client():
    # TODO : 2.导入业务应用对象
    from YourApplication import app
    return app.test_client


# TODO：3.编写测试样例【本例适用与api接口测试，以统一响应格式的code进行判断是否符合预期】
@pytest.mark.parametrize("mock_data", demo_data)
def test_api(mock_data: dict, api_mock_client):
    http_headers = {"User-Agent": "TestApp"}
    http_method = mock_data.pop("method")
    request_uri = mock_data.pop("uri")
    test_result = mock_data.pop("result")
    test_message = mock_data.pop("message")
    request_data = mock_data

    print(f"请求{http_method}|{request_uri}报文:{request_data}")

    if http_method.upper() == "POST":
        response = api_mock_client.post(request_uri, data=json.dumps(request_data), headers=http_headers)
    else:
        request_data = parse.urlencode(request_data) if request_data else ""
        request_uri = f"{request_uri.rstrip('/')}?{request_data}" if request_uri.endswith(
            "/") else f"{request_uri}?{request_data}"
        request, response = api_mock_client.get(request_uri, headers=http_headers)

    print(f"原始响应为:{response.body},类型为:{type(response.body)}")

    # TODO ：4.如果不同接口响应结构不同，只能自行判断
    if re.match(r'^/health_check*', request_uri):
        assert response.body.decode('utf-8') == str(test_result), test_message
    else:
        response = response.json
        assert int(response["code"]) == int(test_result), test_message
