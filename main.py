import os
from dotenv import load_dotenv
from openai import OpenAI

# 读取 .env 文件
load_dotenv()

# 初始化模型客户端
client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url=os.environ["LLM_BASE_URL"]
)

messages = [
    {
        "role": "user",
        "content": "你好，今天广州天气怎么样呀？"
    }
]

# 向模型发送请求
response = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=messages
)

# 查看模型回答
print(response.choices[0].message.content)

# # 查看Token使用情况
# print(response.usage)
# 查看response的完整东西
# 由于response对象是基于BaseModel类 也就是Pydantic的基类
# 而model_dump_json 是 Pydantic提供的一个方法 用于序列化对象成为json格式串方便查看
print(response.model_dump_json(indent=2))