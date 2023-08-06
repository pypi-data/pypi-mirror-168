# encoding: utf-8
"""
@project: djangoModel->custom_tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 自定义工具类
@created_time: 2022/9/5 13:57
"""


def is_number(s):
    """识别任何语言的数字字符串"""
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
