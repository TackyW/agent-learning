# 科研项目智能管理助手
# 通过自然语言查询科研项目、调用本地工具获取信息，并把结果整理为 Pydantic 数据对象
from llm_model.llm import client,model
import json
# 模拟数据库 数据部分
PROJECTS = {
    "ResearchFlow": {
        "status": "开发中",
        "owner": "张三",
        "deadline": "2027-01-30",
        "tasks": [
            "完成 Function Calling",
            "实现 Agent Loop",
            "开发 RAG 模块"
        ]
    },
    "PaperRAG": {
        "status": "已完成",
        "owner": "李四",
        "deadline": "2026-11-01",
        "tasks": []
    },
    "NL2SQLAgent": {
        "status": "规划中",
        "owner": "王五",
        "deadline": None,
        "tasks": [
            "设计数据库",
            "实现 SQL 生成"
        ]
    }
}

"""
需要实现三个工具
函数名称	参数	  作用
list_projects()	无	查询所有项目名称
get_project_info(project_name)	项目名称	返回状态、负责人和截止日期
get_project_tasks(project_name)	项目名称	返回项目待办任务
"""
def list_projects() -> list[str]:
    """
    该工具的作用是，查询现在已有的所有项目的名称并返回
    """
    # # 下面这个代码可以优化成一句 return list(PROJECTS.keys())
    # projects_name = []
    # for project in PROJECTS.keys():
    #     projects_name.append(project)
    # # 返回所有项目名称
    # return projects_name
    return list(PROJECTS.keys())

def get_project_info(project_name:str) -> dict:
    """
    该工具的作用是，查询某个项目的信息并返回
    Args:
        project_name: 项目名称
    """
    if PROJECTS.get(project_name):
        return {
            "status":PROJECTS[project_name]["status"],
            "owner":PROJECTS[project_name]["owner"],
            "deadline":PROJECTS[project_name]["deadline"]
        }
    else:
        return {project_name:"数据库中不存在此项目信息"}

def get_project_tasks(project_name:str) -> dict:
    """
    该工具的作用是，查询某个项目的待办任务
    Args:
        project_name: 项目名称
    """
    if PROJECTS.get(project_name):
        return {
            "project_name":project_name,
            "tasks":PROJECTS[project_name]["tasks"]
        }
    else:
        return {project_name:"数据库中不存在此项目信息"}

from langchain_core.utils.function_calling import convert_to_openai_tool
# 将三个工具转化为tools_schema格式
functions = [list_projects,get_project_tasks,get_project_info]
tools = [convert_to_openai_tool(func) for func in functions]

messages = [{"role":"system","content": (
            "你是项目管理助手,在需要时可以查询已有工具"
        )}]
# 组织循环对话
while True:
    inputs = input("你好我是项目管理助手，有什么可以帮助到你的吗？(输入exit退出系统)\n").strip()
    if inputs.lower() == "exit":
        print("欢迎下次使用")
        break
    else:
        # 构造message 然后将messages全部传给大模型
        cur_message = {
            "role":"user",
            "content":inputs
        }
        messages.append(cur_message)
        response = client.chat.completions.create(
            # 此时需要传入工具了
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            parallel_tool_calls=True,
            extra_body={"enable_thinking": False}
        )
        tool_choice = "auto"
        counts = 0
        # 需要进行返回内容的判断 直到没有工具的调用为止
        while response.choices[0].message.tool_calls:
            # 将调用的信息放入到历史记录里
            messages.append(response.choices[0].message.model_dump(exclude_none=True))
            # 然后取执行里面所需要的工具 并重新传递给大模型
            for tool_call in response.choices[0].message.tool_calls:
                # 将 JSON 字符串解析为 Python 字典
                arguments = json.loads(
                    tool_call.function.arguments
                )
                if tool_call.function.name == "list_projects":
                    result = list_projects()
                elif tool_call.function.name == "get_project_info":
                    result = get_project_info(arguments["project_name"])
                elif tool_call.function.name == "get_project_tasks":
                    result = get_project_tasks(arguments["project_name"])
                else:
                    result = "没有找到对应的工具可使用，请重新检查一遍"
                messages.append({
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })
            # 重新发给大模型（因为可能包含很多个工具调用 因此 需要全部保存好 在上传到大模型）
            counts += 1
            if counts >= 5:
                print("超过调用工具最大次数，不允许")
                tool_choice = "none"
            response = client.chat.completions.create(
                # 此时需要传入工具了
                model=model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                parallel_tool_calls=True,
                extra_body={"enable_thinking": False}
            )
        # 此时工具调用全部完毕可以直接打印模型的最终回答
        print(response.choices[0].message.content)
        # 并且添加到历史记录里
        messages.append({
            "role":"assistant",
            "content":response.choices[0].message.content
        })