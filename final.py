
# -*- coding: utf-8 -*-

from openai import OpenAI
import tkinter as tk
import threading
import requests
import pyaudio
import hashlib
import pyttsx3
import urllib
import ctypes
import base64
import hmac
import json
import wave
import time
import sys
import os
import re


class ConsoleOutput:

    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert('end', message)
        self.text_widget.see('end')


class GUI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title('easy-chat')
        self.root.geometry("926x270+400+300")
        self.root.resizable(False, False)
        self.interface()

    def interface(self):

        self.button_text = tk.Button(self.root, text="文本", command=self.start_text, width=10, height=4, bg="#14776c")
        self.button_text.grid(row=1, column=2)

        self.button_audio = tk.Button(self.root, text="语音", command=self.start_audio, width=10, height=4, bg="#9b4072")
        self.button_audio.grid(row=1, column=3)

        self.window_output = tk.Text(self.root, width=80, height=10)
        self.window_output.grid(row=2, column=1)

        self.window_input = tk.Entry(self.root, width=80)
        self.window_input.grid(row=1, column=1)

        self.window_log = tk.Text(self.root, width=22, height=10, bg="#3d6c90")
        self.window_log.grid(row=2, column=2, columnspan=2)

        self.console_output = ConsoleOutput(self.window_log)
        sys.stdout = self.console_output

    def event_text(self):
        input_text = self.window_input.get()

        self.window_output.insert(3.0, "Input:" + input_text + '\n')
        messages = [{'role': 'user', 'content': input_text}, ]

        gpt_model = GPT(messages)
        answer = gpt_model.gpt_35_api()
        self.window_output.insert(4.0, "Answer:" + answer + '\n')

    def event_audio(self):
        self.window_output.insert(1.0, "Please speak and wait." + '\n')
        sp = Audio(5)
        sp.play()

        api = RequestApi(upload_file_path=r"speak_wav/output.wav")
        text = api.get_result()

        self.window_output.insert(2.0, "Speak:" + text + '\n')

        self.window_output.insert(3.0, "Please wait." + '\n')
        messages = [{'role': 'user', 'content': text}, ]

        gpt_model = GPT(messages)
        answer = gpt_model.gpt_35_api()
        self.window_output.insert(4.0, "Answer:" + answer + '\n')

        speak = Say(answer)
        speak.say_answer()

    def start_text(self):
        thread_text = threading.Thread(name='t2', target=self.event_text, daemon=True)
        thread_text.start()

    def start_audio(self):
        thread_audio = threading.Thread(name='t1', target=self.event_audio, daemon=True)
        thread_audio.start()


class Audio:
    # 录音设置
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = "speak_wav\\output.wav"

    def __init__(self, time):
        self.time = time

    def play(self):

        audio = pyaudio.PyAudio()

        # 开始录制
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        print("Recording...")

        frames = []

        for i in range(0, int(self.RATE / self.CHUNK * self.time)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print("Finished recording.")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

        print("Audio saved as", self.WAVE_OUTPUT_FILENAME)


class GPT:

    client = OpenAI(
        api_key="",
        base_url=""
    )

    def __init__(self, message):
        self.message = message

    def gpt_35_api(self):

        try:
            completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=self.message)
            answer = completion.choices[0].message.content
            # print(answer)
            return answer

        except Exception as e:
            print(f"An error occurred: {e}")


class Say:

    def __init__(self, answer):
        self.answer = answer
        self.engine = pyttsx3.init()

    def set(self):

        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 200)

        volume = self.engine.getProperty('volume')
        self.engine.setProperty('volume', 1)

        # voices = self.engine.getProperty('voices')
        # self.engine.setProperty('voice', voices[0].id)

        print(f"rate: {rate} volume: {volume}")

    def say_answer(self):
        self.set()
        pyttsx3.speak(self.answer)


class RequestApi(object):
    def __init__(self, upload_file_path):
        self.appid = ""
        self.secret_key = ""
        self.lfasr_host = 'https://raasr.xfyun.cn/v2/api'
        self.api_upload = '/upload'
        self.api_get_result = '/getResult'
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()


    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa


    def upload(self):

        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"

        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url = self.lfasr_host + self.api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)

        result = json.loads(response.text)

        return result


    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"

        try:
            status = 3
            # 建议使用回调的方式查询结果，查询接口有请求频率限制
            while status == 3:
                response = requests.post(url=self.lfasr_host + self.api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                         headers={"Content-type": "application/json"})
                # print("get_result_url:",response.request.url)
                result = json.loads(response.text)

                status = result['content']['orderInfo']['status']
                print("Please wait.")
                if status == 4:
                    break

            order_result = json.loads(result['content']['orderResult'])
            lattice = order_result['lattice']
            chinese_text = ""

            for item in lattice:
                json_1best = item.get('json_1best', '')
                chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
                chinese_chars = chinese_pattern.findall(json_1best)
                chinese_text += " ".join(chinese_chars) + " "

            text = chinese_text.replace(" ", '')
            # print("Speak:" + text)
            return text
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':

    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    gui = GUI()
    gui.root.mainloop()
