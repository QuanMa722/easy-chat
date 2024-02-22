
# -*- coding: utf-8 -*-

# 导入需要的第三方库
import pyaudio
import wave


class Audio:
    # 录音设置
    FORMAT = pyaudio.paInt16  # 表示音频样本的格式，表示16位整数音频格式。
    CHANNELS = 1  # 指定音频通道的数量，表示单声道音频。
    RATE = 44100  # 常见采样率
    CHUNK = 1024  # 确定每个缓冲区中的帧数
    WAVE_OUTPUT_FILENAME = "speak_wav\\output.wav"  # 录制存放地址

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

        # 停止录制
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # 保存录音为.wav文件
        with wave.open(self.WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

        print("Audio saved as", self.WAVE_OUTPUT_FILENAME)


