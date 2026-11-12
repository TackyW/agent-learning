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

model = os.environ["LLM_MODEL"]