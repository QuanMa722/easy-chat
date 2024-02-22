
# -*- coding: utf-8 -*-

import pyttsx3


class Say:

    def __init__(self, answer):
        self.answer = answer
        self.engine = pyttsx3.init()

    def set(self):

        rate = self.engine.getProperty('rate')  # 获取当前语速的详细信息
        self.engine.setProperty('rate', 200)

        volume = self.engine.getProperty('volume')  # 获取当前音量（最小为0，最大为1）
        self.engine.setProperty('volume', 1)  # 在0到1之间重设音量

        # voices = self.engine.getProperty('voices')  # 获取当前发音的详细信息
        # self.engine.setProperty('voice', voices[0].id)  # 设置第一个语音合成器

        print(f"rate: {rate} volume: {volume}")

    def say_answer(self):
        self.set()
        pyttsx3.speak(self.answer)



