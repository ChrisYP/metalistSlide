# -*- coding: utf-8 -*-
# @Time    : 2024/3/7 18:54
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : slide.py
# @Software: PyCharm
import base64
import json
import time

import requests
from src.locator import GapLocator
from src.utils import sign
from loguru import logger


class Slide:
    def __init__(self):
        self.headers = {
            'authority': 'game.metalist.io',
            'accept': '*/*',
            'accept-language': 'en',
            'authorization-token': '',
            'cache-control': 'no-cache',
            'client-app-id': '13x67d4icclyebny',
            'dnt': '1',
            'origin': 'https://cardsahoy.metalist.io',
            'pragma': 'no-cache',
            'referer': 'https://cardsahoy.metalist.io/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        self.session = requests.session()
        self.session.headers = self.headers

    def init_slide(self):
        return self.session.post('https://game.metalist.io/api/user/genCaptcha', json={}).json()

    @staticmethod
    def generate_trajectory(final_x, total_time):
        trajectory = []
        current_x = 0
        current_time = 0
        time_step = total_time // final_x
        while current_x < final_x:
            x_step = min((current_x // 10) + 1, final_x - current_x)
            current_x += x_step
            current_time += time_step

            trajectory.append({'x': current_x, 'y': 0, 't': current_time})

            if current_x >= final_x or current_time >= total_time:
                break

        if trajectory[-1]['x'] != final_x or trajectory[-1]['t'] != total_time:
            trajectory[-1]['x'] = final_x
            trajectory[-1]['t'] = total_time

        return trajectory

    @staticmethod
    def get_x(block, bg):
        return GapLocator(block, bg).run()

    def check(self, x, _id):
        json_data = {
            'id': _id,
            'bgImageWidth': 295,
            'bgImageHeight': 180,
            'startTime': str(round(time.time() * 1000)),
            'endTime': str(round(time.time() * 1000) + 7056),
            'trackPointList': self.generate_trajectory(x, 7056),
        }
        data = json.loads(sign.sign(json.dumps(json_data)))

        return self.session.post('https://game.metalist.io/api/user/v2/checkCaptcha', json=data).json()

    def run(self):
        ret = self.init_slide()
        block = ret.get("data", {}).get('tpImage').replace("data:image/png;base64,", "")
        bg = ret.get("data", {}).get('bgImage').replace("data:image/jpeg;base64,", "")
        img_id = ret['data']['id']
        x = self.get_x(base64.b64decode(block), base64.b64decode(bg))

        ret = self.check(round(x * 0.496277915632754), img_id)

        if ret.get("code") == '000000':
            logger.info(f"验证成功 {ret} {img_id}")
            return img_id
        else:
            logger.error(ret)


if __name__ == '__main__':
    for _ in range(1):
        Slide().run()
