# 模拟本地项目数据库
from llm_model.llm import client, model
from langchain_core.utils.function_calling import convert_to_openai_tool
PROJECTS = {
    "ResearchFlow": "开发中",
    "NL2SQL Agent": "尚未开始",
    "PaperRAG": "已完成"
}


def get_project_status(project_name: str):
    """根据项目名称查询项目状态"""
    return {
        "project_name": project_name,
        "status": PROJECTS.get(project_name, "未找到该项目")
    }

# json_schema格式 描述这个工具
"""
字段	含义
type: "function"	声明这是一个函数工具
name	模型请求调用时使用的工具名称
description	向模型解释这个工具的用途
parameters	定义函数接收的参数结构
properties	描述每一个参数
required	定义必须提供的参数
"""
# 用langchian-core的工具代替这串
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_project_status",
#             "description": "根据项目名称查询本地项目数据库中的状态",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "project_name": {
#                         "type": "string",
#                         "description": "需要查询的项目名称"
#                     }
#                 },
#                 "required": ["project_name"],
#                 "additionalProperties": False
#             }
#         }
#     }
# ]
tools = []
tools.append(convert_to_openai_tool(get_project_status))

messages = [
    {
        "role": "system",
        "content": (
            "你是项目管理助手。"
            "查询项目状态时，请使用提供的工具，"
            "不要猜测项目状态。"
        )
    },
    {
        "role": "user",
        "content": "NL2SQL Agent项目现在是什么状态？"
    }
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    # 将可用工具的描述提供给模型
    tools=tools,
    # 让模型自行决定是否需要调用工具
    tool_choice="auto",
    # 限制本次请求并行提出多个工具调用，便于初学者理解。
    parallel_tool_calls=False,
    extra_body={"enable_thinking": False}
)

message = response.choices[0].message

print(message.model_dump_json(indent=2))

# 工具调用信息在 tool_calls属性  是一个字典
print(message.tool_calls)

# 这时候就可以调用了 如果有工具调用信息的话
import json

if message.tool_calls:
    # 保存模型的工具调用请求
    messages.append(message.model_dump(exclude_none=True))

    # 遍历模型请求调用的工具
    for tool_call in message.tool_calls:
        print(tool_call)
        function_name = tool_call.function.name

        # 将 JSON 字符串解析为 Python 字典
        arguments = json.loads(
            tool_call.function.arguments
        )

        print("模型选择的工具：", function_name)
        print("模型生成的参数：", arguments)

        # Python 程序真正调用工具
        if function_name == "get_project_status":
            result = get_project_status(
                project_name=arguments["project_name"]
            )
        else:
            result = {"error": "不支持的工具"}

        print("工具执行结果：", result)

        # 将工具结果添加到 messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result, ensure_ascii=False)
        })

    # 第二次请求：让模型根据工具结果生成回答
    final_response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="none",
        extra_body={"enable_thinking": False}
    )

    print(
        "Qwen最终回答：",
        final_response.choices[0].message.content
    )

else:
    print("模型没有调用工具：", message.content)