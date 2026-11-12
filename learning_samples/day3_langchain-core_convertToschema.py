# 利用langchain-core的方法
# 将一个python函数生成符合 OpenAI Tool Calling 格式的工具定义。

import json
from langchain_core.utils.function_calling import convert_to_openai_tool

projects = {
        "ResearchFlow": "开发中",
        "PaperRAG": "已完成"
    }
def get_project_status(project_name: str) -> str:
    """
    查询项目的当前开发状态。
    Args:
        project_name: 需要查询的项目名称。
    """
    return projects.get(project_name, "项目不存在")


# 自动生成工具的 JSON Schema
tool_schema = convert_to_openai_tool(get_project_status)

print(json.dumps(tool_schema, ensure_ascii=False, indent=2))
