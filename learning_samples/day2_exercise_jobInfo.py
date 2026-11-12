# 实习岗位信息提取模型
import os
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from llm_model.llm import client,model


class JobInfo(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        strict=True,
        from_attributes=True
    )

    # 属性名
    company: str | None
    position: str
    city: str
    skills: list[str]
    days_per_week: int = Field(ge=1,le=7)

# 获取一个pydantic类的schema
# schema = JobInfo.model_json_schema()
# print(type(schema))
# print(schema)

# 使用qwen去搜索一些常见的JD要求，然后用json串的形式返回 然后进行校验
messages = [
    {
        "role":"system",
        "content":"你是一位知道众多计算机公司及岗位要求的小助手"
    },
    {
        "role":"user",
        "content":"""
        请你找一个计算机的岗位的招聘信息并且按指定格式返回给我。
        """
    }
]

# 得到回答
response = client.chat.completions.parse(model=model,messages=messages,response_format=JobInfo).choices[0].message.content

# 验证
try:
    jobinfo = JobInfo.model_validate_json(response)
    print("验证通过")
    print(jobinfo.company)
    print(jobinfo.position)
    print(jobinfo.city)
    print(jobinfo.skills)
    print(jobinfo.days_per_week)
except ValidationError as e:
    print("验证不通过")
    print(e)
# import json
#
# data = {
#     "name": "张三",
#     "age": 22,
#     "graduated": False,
#     "company": None
# }
# # 将字典对象转化成json对象（本质字符串）
# json_data = json.dumps(data)
# print(type(json_data))
# print(json_data)
#
# # 将json串转成python对象
# convert_data = json.loads(json_data)
# print(type(convert_data))
# print(convert_data)
#
# r"""
# <class 'str'>
# {"name": "\u5f20\u4e09", "age": 22, "graduated": false, "company": null}
# <class 'dict'>
# {'name': '张三', 'age': 22, 'graduated': False, 'company': None}
# """