
# -*- coding: utf-8 -*-

# 导入其他类的函数
from transform import RequestApi
from audio import Audio
from gpt import GPT
from say import Say

# 导入需要的第三方库
import tkinter as tk
import threading
import ctypes
import sys


class ConsoleOutput:
    """
    打印控制台信息
    """

    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert('end', message)
        self.text_widget.see('end')


class GUI:
    """
    展示GUI页面
    """

    def __init__(self):
        """
        设置GUI相关信息
        """
        self.root = tk.Tk()
        self.root.title('easy-chat')
        self.root.geometry("926x270+400+300")
        self.root.resizable(False, False)
        self.interface()

    def interface(self):
        """
        设置按钮位置

        :return: None
        """

        # 文本输入按钮
        self.button_text = tk.Button(self.root, text="文本", command=self.start_text, width=10, height=4, bg="#14776c")
        self.button_text.grid(row=1, column=2)

        # 语音输入按钮
        self.button_audio = tk.Button(self.root, text="语音", command=self.start_audio, width=10, height=4, bg="#9b4072")
        self.button_audio.grid(row=1, column=3)

        # 打印屏幕信息
        self.window_output = tk.Text(self.root, width=80, height=10)
        self.window_output.grid(row=2, column=1)

        # 输入文本信息
        self.window_input = tk.Entry(self.root, width=80)
        self.window_input.grid(row=1, column=1)

        # 控制台日志
        self.window_log = tk.Text(self.root, width=22, height=10, bg="#3d6c90")
        self.window_log.grid(row=2, column=2, columnspan=2)

        self.console_output = ConsoleOutput(self.window_log)
        sys.stdout = self.console_output

    def event_text(self):
        """
        文本信息处理

        :return: None
        """
        input_text = self.window_input.get()

        self.window_output.insert(3.0, "Input:" + input_text + '\n')
        messages = [{'role': 'user', 'content': input_text}, ]

        gpt_model = GPT(messages)
        answer = gpt_model.gpt_35_api()
        self.window_output.insert(4.0, "Answer:" + answer + '\n')

    def event_audio(self):
        """
        语音信息处理

        :return: None
        """
        self.window_output.insert(1.0, "Please speak and wait." + '\n')
        # 设置录音时间为5秒
        sp = Audio(5)
        sp.play()

        # 将语音转换为文本
        api = RequestApi(upload_file_path=r"speak_wav/output.wav")
        text = api.get_result()

        self.window_output.insert(2.0, "Speak:" + text + '\n')

        # 将文本信息发送请求回去响应
        self.window_output.insert(3.0, "Please wait." + '\n')
        messages = [{'role': 'user', 'content': text}, ]

        gpt_model = GPT(messages)
        answer = gpt_model.gpt_35_api()
        self.window_output.insert(4.0, "Answer:" + answer + '\n')

        speak = Say(answer)
        speak.say_answer()

    def start_text(self):
        """
        文本信息线程

        :return: None
        """
        thread_text = threading.Thread(name='t2', target=self.event_text, daemon=True)
        thread_text.start()

    def start_audio(self):
        """
        视频信息线程

        :return: None
        """
        thread_audio = threading.Thread(name='t1', target=self.event_audio, daemon=True)
        thread_audio.start()


if __name__ == '__main__':

    # 设置GUI像素
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    gui = GUI()
    gui.root.mainloop()
