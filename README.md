<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/sunjiawe/task-cli?style=social)](https://github.com/sunjiawe/task-cli/stargazers)
[![License](https://img.shields.io/github/license/sunjiawe/task-cli)](https://github.com/sunjiawe/task-cli/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)


**一个AI驱动的 项目管理agent** （灵感来源：gemini-cli、claude-task-master）

[English](./docs/README_EN.md) | 中文文档

</div>

## 🔍 使用场景

- **智能项目管理** - 自动为你的项目进行任务分解和进度报告。
- **项目进度可视化** - 通过甘特图清晰地展示任务依赖和时间线。

## ✨ 特性

- 🔧 **强大的命令行工具** - 提供 `init`, `decompose`, `gantt`, `report` 等丰富的命令，覆盖项目全生命周期。
- 📝 **自动化任务分解** - 基于高阶目标，利用 LLM 自动将复杂任务分解为可执行的子任务。支持多轮对话、不断调整 LLM 生成的任务规划。
- 📊 **可视化甘特图** - 根据项目计划自动生成交互式甘特图，直观地跟踪项目进度。
- 💬 **项目智能问答 (Q&A)** - 与你的项目数据库对话，快速获取项目信息。


## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/sunjiawe/task-cli.git
cd task-cli

# 安装依赖
pip install -r requirements.txt
```

## 📖 详细使用指南

### 初始化项目

使用 `init` 命令开始一个新项目：

```bash
python main.py init
```

### 启动项目助手

在使用之前，你需要配置环境变量`DEEPSEEK_API_KEY`才能正常使用LLM的api

项目初始化完成之后，运行程序进入助手终端：
```
set DEEPSEEK_API_KEY="your-api-key"
python main.py
```

### 子命令

输入 `/` 触发子命令的自动补全

```bash
# 让 AI Agent 帮助你分解任务
/decompose <描述你的需求>

# 查看任务清单
/list

# 咨询助手，对执行单一任务给与指导
/howto 

# 更新任务状态
/update

# 生成甘特图(静态html文件)
/gantt

# 项目总结报告
/report

# 自然语言对话，询问关于项目的任何问题
/qa

# 显示帮助信息
/help
```

调试提示词： 设置环境变量DEBUG_MODE=true
```
set DEBUG_MODE=true
```

## 🤝 贡献

欢迎通过提交 Pull Request 或创建 Issue 来为本项目做出贡献！

## 📄 许可证

本项目使用 Apache 2.0 许可证。

## 🙏 致谢

- [Pocket Flow](https://github.com/The-Pocket/PocketFlow) - 驱动本项目的极简 Agent 框架。
- [gemini-cli](https://github.com/google-gemini/gemini-cli) - An open-source AI agent that brings the power of Gemini directly into your terminal.
