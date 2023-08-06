#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Sun
# datetime:2022/9/19
# flask框架单元测试样例脚本
import json
from pathlib import Path
from urllib import parse
from functools import reduce

import pytest
from python_for_pytest import (init_template, setup_read_main)

_file_name = "mock_data.xls"
_title_type = 1  # 0：报文参数名写在行，1：报文参数名写在列
_base_path = Path(__file__).resolve().parent

# TODO： 0.根据接口报文初始化生成测试数据模板【您需要更改下面request_data变量代表的请求报文】
request_mock_data = {
    "uri": "/test",
    "method": "post",
    "result": "0",
    "message": "操作成功，符合预期",
    "head": {
        "sysCode": "S2022",
        "appCode": "A520",
        "reqTime": "2022-09-19 00:00:00",
    },
    "biz": {
        "phoneNumber": "18638720197",
        "prodOfferCode": "7240110003400005",
        "prod_info": [
            {
                "prod_nbr": ""
            }
        ]
    }
}

init_template(data=request_mock_data, base_path=_base_path, excel_file_name=_file_name, t_type=_title_type)

# TODO： 1.读取配置好的测试数据
source_data = setup_read_main(source_path=_base_path, f_name=_file_name, t_type=_title_type)
# [{},{}] 如果每个接口的响应格式一样可以采用下面的方面将每个接口合并在一起测试
demo_data = reduce(lambda x, y: x + y, source_data.values())


# 2. 接口测试，需先使用flask提供的测试客户端进行测试，flask自带测试客户端，直接模拟终端请求
@pytest.fixture
def api_mock_client():
    """
    构建业务的测试客户端，从而能调用业务应用的接口
    :return:
    """
    # TODO : 2.导入业务应用对象
    from YourApplication import app
    with app.test_client() as client:
        yield client


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
        request_data = parse.urlencode(request_data)
        request_uri = f"{request_uri.rstrip('/')}?{request_data}" if request_uri.endswith(
            "/") else f"{request_uri}?{request_data}"
        response = api_mock_client.get(request_uri, headers=http_headers)

    print(f"原始响应为:{response.data}")

    # TODO ：4.如果不同接口响应结构不同，请自行修改下面的代码
    response_data = response.json
    assert int(response_data["code"]) == int(test_result), test_message

#  flask模拟客户端初步使用结论：
#  get请求，参数只能拼接到url上，post请求，使用参数data，类型需要是json；
#  响应对象为WrapperTestResponse，默认为bytes，数据获取使用：response.data，转为字符串需要decode(),
#  如果响应数据为json，也可以直接调用response.json就不用手动解码与解析了
