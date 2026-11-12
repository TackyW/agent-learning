# 🚀 Agent Learning

> 从零开始学习 AI Agent 开发，通过理论学习、代码实践和项目实战，逐步掌握 AI Agent 应用的核心技术。

## 📖 项目简介

本仓库主要用于记录我学习 **AI Agent 开发** 的全过程。

在已有 Python、机器学习和深度学习基础上，我希望进一步掌握大语言模型（LLM）的应用开发技术，从最基础的模型 API 调用开始，逐步实现具有工具调用、知识检索、多轮对话和任务执行能力的智能 Agent。

仓库将持续更新学习笔记、代码练习和综合实战项目。

**学习方式：理论理解 → 动手实现 → 综合练习 → 项目开发。**

## 🛠️ 技术栈

- **开发语言**：Python
- **大语言模型**：Qwen（阿里云百炼 API）
- **模型接口**：OpenAI Python SDK
- **数据验证**：Pydantic、JSON Schema
- **工具调用**：Function Calling
- **后续学习**：RAG、LangChain、LangGraph、MCP、FastAPI

## 📚 学习进度

### 第一阶段：LLM 应用基础

- [x] Day 1：LLM API 调用、多轮对话与上下文管理
- [x] Day 2：Pydantic、JSON Schema 与结构化输出
- [x] Day 3：Function Calling、工具注册与 Agent Loop

### 第二阶段：Agent 核心能力

- [ ] RAG 与 Embedding
- [ ] 向量数据库与知识检索
- [ ] Agent Memory 与上下文管理
- [ ] LangChain 基础
- [ ] LangGraph 工作流与状态管理
- [ ] MCP 工具集成

### 第三阶段：Agent 工程化与项目实战

- [ ] FastAPI 与 Agent 服务开发
- [ ] Agent 异常处理、日志与性能优化
- [ ] Agent 测试、评估与部署
- [ ] 完整 Agent 应用项目开发

## 💻 当前实践项目

### ResearchFlow Mini Agent

一个基于 Qwen 和 Function Calling 的科研项目智能管理助手。

目前已经实现的基础功能：

- 通过自然语言与用户交互
- 支持多轮对话与历史消息管理
- 使用 Python 函数作为外部工具
- 自动生成 Tool Schema
- 根据模型返回的工具调用请求执行对应函数
- 将工具执行结果返回大模型
- 使用 Agent Loop 支持连续工具调用
- 限制 Agent 的最大工具调用轮数

目前使用 Python 字典模拟数据库，重点是理解 Agent 的核心运行机制，而不是依赖现成框架完成所有功能。

## 🎯 学习目标

1. 理解 AI Agent 的基本原理和核心架构。
2. 掌握 LLM API、工具调用、RAG 和工作流编排。
3. 能够不依赖高级框架，手动实现简单 Agent。
4. 熟练使用 LangGraph、MCP 等技术构建 Agent 应用。
5. 具备开发、测试和部署 AI Agent 项目的实践能力。

## 📝 说明

这是一个持续更新的个人学习仓库，主要用于记录学习过程、验证技术原理和积累项目经验。

部分代码属于学习阶段的简化实现，并非完整的生产级方案。

随着学习深入，将逐步完善项目结构、异常处理、测试和工程化能力。

---

**Keep Learning, Keep Building. 🚀**