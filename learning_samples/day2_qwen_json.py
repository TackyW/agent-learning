import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ConfigDict, ValidationError


# 1. 定义数据模型
class PaperInfo(BaseModel):
    model_config = ConfigDict(
        strict=True,
        extra="forbid"
    )

    title: str = Field(min_length=1)
    authors: list[str]
    year: int = Field(ge=1950, le=2026)
    keywords: list[str]


# 2. 加载环境配置
load_dotenv()

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url=os.environ["LLM_BASE_URL"]
)


# 3. 准备用户输入
user_text = """
论文《基于深度学习的图像分类》
由张三和李四在2024年发表，
主要研究CNN和图像识别。
"""


# 4. 调用Qwen
response = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[
        {
            "role": "system",
            "content": (
                "你是论文信息抽取助手。"
                "请从文本中提取title、authors、year、keywords。"
                "请按照JSON格式输出。"
                "title是字符串，authors是字符串数组，"
                "year是整数，keywords是字符串数组。"
                "不要编造原文中不存在的信息。"
            )
        },
        {
            "role": "user",
            "content": user_text
        }
    ],
    response_format={"type": "json_object"}
)


# 5. 获取模型输出
content = response.choices[0].message.content

if not content:
    raise ValueError("模型未返回文本内容")


print("===== Qwen 原始输出 =====")
print(content)


# 6. 用Pydantic验证
try:
    paper = PaperInfo.model_validate_json(content)

    print("\n===== 验证通过 =====")
    print("论文标题：", paper.title)
    print("论文作者：", paper.authors)
    print("发表年份：", paper.year)
    print("关键词：", paper.keywords)

except ValidationError as e:
    print("\n===== 数据验证失败 =====")
    print(e)


# 7. Token统计
if response.usage:
    print("\nToken用量：", response.usage.total_tokens)
