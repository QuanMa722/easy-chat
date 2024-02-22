
# -*- coding: utf-8 -*-

from openai import OpenAI


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







