
# -*- coding: utf-8 -*-

# 导入需要的第三方库
from openai import OpenAI


class GPT:

    client = OpenAI(
        api_key="your api_key here",
        base_url="your base_url here"
    )

    def __init__(self, message):
        self.message = message  # 获取传入信息

    def gpt_35_api(self) -> str:
        """
        发送请求获取响应（回答）

        :return: str answer
        """
        try:
            completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=self.message)
            answer = completion.choices[0].message.content
            # print(answer)
            return answer

        # 根据报错信息修改代码
        # 一般报错原因为 api_key 错误
        except Exception as e:
            print(f"An error occurred: {e}")




