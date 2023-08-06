#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# datetime:2022/9/19

__all__ = ["init_pytest_for_flask", "init_pytest_for_sanic", "init_template", "setup_write_main", "setup_read_main"]

import xlrd
import xlwt
import shutil
import json_flatten
from pathlib import Path
from pprint import pprint
from typing import Dict, Any, List


# 将多层级报文平铺一层便于写入excel
# def single_layer_json(j: Dict[str, Any]) -> Dict[str, Any]:
#     """ 多层json展开变成一层(如果包含列表项会为其标记序号)
#     """
#     flag = True
#     while flag:
#         flag = False
#         for k in list(j.keys()):
#             # 如果键值对的值为空，直接进入下一循环
#             if not j[k]:
#                 continue
#             if isinstance(j[k], dict):
#                 for kk in list(j[k].keys()):  # 逐级用下划线拼接key
#                     j[k + '.' + kk] = j[k][kk]
#                 del j[k]
#                 flag = True
#             elif isinstance(j[k], list):  # 遇到列表项用下划线拼接index
#                 for i, v in enumerate(j[k]):
#                     # j[k + '.' + str(i)] = v
#                     # j[f"{k}.[{str(i)}]"] = v
#                     j[k + '.' + '[' + str(i) + ']'] = v
#                 del j[k]
#                 flag = True
#     return j


def single_layer_json(j: Dict[str, Any]) -> Dict[str, Any]:
    """ 多层json展开变成一层(如果包含列表项会为其标记序号)
    """
    return json_flatten.flatten(j)


#  写入excel-设置字体样式
def set_excel_style(name=u'微软雅黑', height=0x00C8, bold=False, pattern_fore_colour=0x40, line_bold=1):
    """
    设定excel单元格格式
    或者直接调用style = xlwt.easyxf()
    :param name:
    :param height:
    :param bold:
    :param pattern_fore_colour:单元格背景前景色
    :param line_bold: 单元格线的宽度
    :return:
    """
    # 初始化样式
    style = xlwt.XFStyle()
    # 为样式创建字体，配置字体样式
    font = xlwt.Font()
    font.name = name  # 字体类型，如 Times New Roman  新罗马体
    font.bold = bold  # True 表示是否加粗
    font.height = height  # 字体大小
    font.colour_index = 0x7FFF  # 字体颜色
    font.italic = False  # 字体是否为斜体

    # 设置单元格对齐方式
    alignment = xlwt.Alignment()
    # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
    alignment.horz = 0x01
    # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
    alignment.vert = 0x00
    # 是否自动换行
    alignment.wrap = 0

    # 设置边框
    borders = xlwt.Borders()
    # # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
    # # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
    borders.left = line_bold
    borders.right = line_bold
    borders.top = line_bold
    borders.bottom = line_bold
    # borders.left_colour = i
    # borders.right_colour = i
    # borders.top_colour = i
    # borders.bottom_colour = i

    # 设置单元格填充颜色
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour = pattern_fore_colour  # 给背景颜色赋值 0代表黑色，1代表白色，2代表红色

    style.font = font
    style.alignment = alignment
    style.pattern = pattern
    style.borders = borders

    return style


# 写入excel-写入数据,生成测试样例报文模板
def write_excel(data: List[Dict], file_name: str, title_type=0):
    """
    data=[{api01},{api02}] or {api01}

    :param title_type: 默认为0即写入行，0：数据标题水平写在一行，1：数据标题水平写在一列
    :param data: 每个接口请求报文转化的平铺字典
    :param file_name: 保存的文件路径
    :return:
    """
    workbook = xlwt.Workbook()

    if isinstance(data, list):
        # 单个或多个接口
        for d in data:
            sheet_name = str(d.get("uri", "")).replace('/', '-').lstrip("-")
            if not sheet_name:
                raise Exception("请在样例报文第一层级添加代表接口路径字段:uri,例如{'uri':'/api/get'}")

            worksheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)
            # 动态写入第一行标题列，并且添加预期结果字段result，如果没有在报文中增加，就新增
            column_names = list(d.keys())
            if "result" not in column_names:
                column_names.append("result")
                d["result"] = ""

            # 写入标题
            for col_index, col_name in enumerate(column_names):
                if not title_type:
                    # 字段水平放在每列上
                    worksheet.write(0, col_index, col_name, set_excel_style(bold=True, pattern_fore_colour=53))
                else:
                    # 字段垂直放在每行上
                    worksheet.write(col_index, 0, col_name, set_excel_style(bold=True, pattern_fore_colour=53))

            # 写入模拟报文数据
            if title_type:
                # 标题写在一列:字段垂直时写入每列数据
                row = 0
                col = 1  # 因为第一列写了标题，则数据从第二列开始写入
                for col_index, col_name in enumerate(column_names):  # 遍历字段
                    value = d[col_name]
                    worksheet.write(row + col_index, col, value, set_excel_style(pattern_fore_colour=1))
            else:
                # 标题写在一行：字段水平时写入每行数据
                row = 1
                col = 0
                for col_index, col_name in enumerate(column_names):  # 遍历字段
                    value = d[col_name]
                    worksheet.write(row, col + col_index, value, set_excel_style(pattern_fore_colour=1))
                row += 1
    else:
        raise Exception("请咨询工具管理员，按要求提供合格的格式的报文，谢谢！")
    workbook.save(file_name)


# 读取excel数据【通用函数】
def read_excel(file_name: str, title_type: int = 0, start: int = 0, end: int = None) -> Dict:
    """
    标题列写在第一行的数据读取方法**
    x y z
    1 2 3

    标题列写在第一列
    x 1
    y 2
    z 3
    :param file_name: 数据源文件路径
    :param title_type: 默认为0即写入行，0：数据标题水平写在一行，1：数据标题水平写在一列
    :param start: 指定区间的数据源开始位置,默认为0，即从记录开始获取,负数如-5代表最后5个接口的数据
    :param end: 指定区间的数据源结束位置
    :return: 所有数据,格式例如：
            [{每一个字典都是一个完整的测试用例数据},{}]
    """
    # 1. 读取excel文件工作簿对象
    wb = xlrd.open_workbook(file_name)

    # 2. 获取标签页对象及每个标签页名称【本文件名称为每天日期】
    sheets = wb.sheets()[start:end]
    sheet_name_list = wb.sheet_names()[start:end]

    # 3. 获取所有标签页的数据
    data = {}
    sheet_index = 0
    for sheet in sheets:
        sheet_data = []
        api_name = sheet_name_list[sheet_index]
        if not title_type:
            # 获取标签页的第一行数据即标题行
            col_names = sheet.row_values(rowx=0)
            # 获取当前标签页有数据的总行数
            s_rows = sheet.nrows
            # 获取每一行数据
            for row_num in range(1, s_rows):
                row_value = sheet.row_values(rowx=row_num)
                if row_value:
                    cell = {}
                    for col_index in range(len(col_names)):
                        cell[col_names[col_index]] = row_value[col_index]
                    # 将扁平化的数据转成嵌套json
                    sheet_data.append(json_flatten.unflatten(cell))
            data[api_name] = sheet_data  # [api00:[{},{}],api01:[{},{}]]
            sheet_index += 1
        else:
            # 获取标签页的第一列数据即标题列
            col_names = sheet.col_values(colx=0)
            # 获取当前标签页有数据的总列数
            s_cols = sheet.ncols
            # 获取每一列
            for col_num in range(1, s_cols):
                col_value = sheet.col_values(colx=col_num)
                print(col_value)
                if col_value:
                    cell = {}
                    for col_index, col_name in enumerate(col_names):
                        cell[col_name] = col_value[col_index]
                    sheet_data.append(json_flatten.unflatten(cell))
            data[api_name] = sheet_data
            sheet_index += 1

    # 4. 即按key排序
    return dict(sorted(data.items(), key=lambda item: item[0]))


# 测试数据模型写入excel生成模板
def setup_write_main(api_request: Dict or List[Dict], target_path: str, f_name: str = "mock_data.xls",
                     t_type: int = 0) -> None:
    """
    将提供的接口报文写入excel文件生成接口模板
    :param api_request: 接口请求报文样例
    :param target_path: 文件保存路径
    :param t_type: 构建模板标题列是写入行：0，写入列：1
    :param f_name: 保存的文件名
    :return:
    """
    mock_data = [single_layer_json(api) for api in api_request] if isinstance(api_request, list) else [
        single_layer_json(api_request)]
    # pprint(mock_data)
    write_excel(mock_data, file_name=Path(target_path, f_name), title_type=t_type)


# 读取excel测试数据入口
def setup_read_main(source_path: str, f_name: str = "mock_data.xls", t_type: int = 0) -> Dict[str, List]:
    """读取测试数据"""
    result = read_excel(Path(source_path, f_name), title_type=t_type)
    # pprint(result)
    return result


# 初始化生成excel模板
def init_template(data: Dict or List[Dict],
                  base_path: str,
                  excel_file_name: str = "mock_data.xls",
                  t_type: int = 0) -> None:
    """
    :param data: 测试用例数据源
    :param base_path: 测试用例脚本的父目录路径
    :param excel_file_name: 构建的excel文件名
    :param t_type: 构建模板标题列是写入行：0，写入列：1
    """
    if not Path(base_path, excel_file_name).exists():
        setup_write_main(api_request=data,
                         target_path=base_path,
                         f_name=excel_file_name,
                         t_type=t_type)

    # 初始化pytest.ini配置文件
    if not Path(base_path, "pytest.ini").exists():
        with open(Path(base_path, "pytest.ini"), "w", encoding="utf-8") as f:
            f.write(
                """[pytest]
python_files = test_*.py  *_test.py
python_classes = Test*
python_functions = test_*

addopts= -vs  --html=./status/report.html --capture=sys --self-contained-html --cov=../ --cov-report=html --cov-report=term-missing -p no:warnings
                """
            )


def init_pytest_for_flask(base_path: str,
                          script_name="test_api_for_flask.py") -> None:
    """
    初始化自动生成flask框架可通用的测试脚本文件

    :param base_path: 测试用例脚本的父目录路径
    :param script_name: 构建测试用例脚本名
    :return:
    """

    if not Path(base_path, script_name).exists():
        print(Path(__file__).resolve().parent)
        shutil.copy(Path(Path(__file__).resolve().parent, "test_api_for_flask.py"),
                    Path(base_path, script_name))


def init_pytest_for_sanic(base_path: str,
                          script_name="test_api_for_sanic.py") -> None:
    """
    初始化自动生成sanic框架可通用的测试脚本文件
    :param base_path:
    :param script_name:
    :return:
    """
    if not Path(base_path, script_name).exists():
        shutil.copy(Path(Path(__file__).resolve().parent, "test_api_for_sanic.py"),
                    Path(base_path, script_name))
