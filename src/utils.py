# -*- coding: utf-8 -*-
# @Time    : 2024/3/9 13:34
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : utils.py
# @Software: PyCharm

from py_mini_racer import MiniRacer

with open('./src/sign.js', encoding='utf-8') as f:
    js = f.read()


class Encrypt:
    def __init__(self):
        self.ctx = MiniRacer()
        self.ctx.eval(js)

    def sign(self, data):
        return self.ctx.eval(f'__encrypt({data})')


sign = Encrypt()
