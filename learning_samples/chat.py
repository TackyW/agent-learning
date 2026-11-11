# 多轮对话
"""
使用 while True 让用户可以连续输入问题。
使用一个 messages 列表保存对话历史。
每次调用 Qwen 后，把模型回答也加入 messages。
用户输入 exit 后结束程序。
"""

import os

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url=os.environ["LLM_BASE_URL"]
)

messages = [
    {
        "role":"system",
        "content":"你是一个Python高级编程师"
    }
]

while True:
    inputs = input("请输入问题(输入exit为退出):").strip()
    if not inputs:
        # 输入空 那就重新输入
        print("您的输入为空,请重新输入。")
        continue
    if inputs.lower() == "exit":
        print("欢迎下次使用!")
        break
    cur_message = {"role":"user","content":inputs}
    # 添加到历史信息并发送给llm
    messages.append(cur_message)
    response = client.chat.completions.create(
        model = os.environ["LLM_MODEL"],
        messages=messages
    )
    answer = response.choices[0].message.content
    # print("AI回答:\n"+answer) # 以后如果是包含工具返回 而 没有内容返回这里就有点问题可以优化
    print("AI回答:\n" + (answer or "大模型没有返回文本回答"))
    # 添加到历史信息
    messages.append({"role":"assistant","content":answer})

