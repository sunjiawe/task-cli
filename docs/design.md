# 设计文档：Xixi - AI 项目管理助手

本文档遵循 [Agentic Coding 指南](../GEMINI.md) 来设计和实现 Xixi 项目。

## 1. 需求

我们需要一个命令行项目管理助手，名为 Xixi。核心需求如下：

- **项目初始化**: 能在任意目录通过 `init` 子命令创建项目，并记录项目名称和目标。
- **数据存储**: 数据存储路径为当前路径的`.xixi`目录，项目与任务的数据存储在 `.xixi/db.json` 文件中。
- **交互式终端**: 应用启动后进入一个多轮对话终端，通过 `/` 前缀的子命令与助手交互。
- **任务管理**:
  - `/decompose`: 核心功能。将用户的复杂需求拆解为可执行的任务和子任务，并评估难度、工时、截止日期和依赖关系。
  - `/list`: 查看任务列表。
  - `/howto`: 获取具体任务的执行建议。
- **项目洞察**:
  - `/report`: 生成标准化的项目报告。
  - `/qa`: 基于项目数据，智能回答用户提问。
- **程序控制**:
  - `/exit`: 退出应用。

## 2. 流程设计 (Flow Design)

应用的核心流程分为两部分：初始化流程和主交互流程。

### 初始化流程 (`init`)

```mermaid
graph TD
    A[用户执行 `xixi init`] --> B{检查 .xixi/db.json 是否存在};
    B -->|是| C[提示项目已存在并退出];
    B -->|否| D[询问项目名];
    D --> E[询问项目目标];
    E --> F[创建 .xixi 目录];
    F --> G[生成项目元数据并保存为 .xixi/db.json];
    G --> H[提示初始化成功];
```

### 主交互流程 (REPL)

```mermaid
graph TD
    subgraph "启动"
        A[用户执行 `xixi`] --> B{检查 .xixi/db.json 是否存在};
        B -->|否| C[提示需要初始化并退出];
        B -->|是| D[加载项目数据];
    end

    subgraph "主循环 (REPL)"
        D --> E[进入交互式终端];
        E --> F[等待用户输入];
        F --> G{输入是否为 /subcommand?};
        G -->|是| H[执行对应子命令];
        G -->|否| I[作为需求输入，执行 /decompose];
        H --> E;
        I --> E;
    end

    subgraph "子命令"
        H --> H_decompose[/decompose];
        H --> H_list[/list];
        H --> H_howto[/howto];
        H --> H_report[/report];
        H --> H_qa[/qa];
        H --> H_exit[/exit];
    end
    
    H_exit --> J[退出程序];

    subgraph "LLM 调用流程 (已优化)"
        subgraph Decompose
            I --> D_Start
            D_Start[获取用户需求] --> D_Ctx[准备上下文(项目目标、**未完成的**任务)] --> D_LLM[调用 LLM 拆解] --> D_Parse[解析并校验 LLM 响应] --> D_Save[保存新任务到 db.json] --> D_Display[向用户展示新任务]
            note right of D_Ctx: 使用 storage.query_tasks(status=['todo', 'in_progress', 'blocked']) 过滤上下文
        end
        
        subgraph Howto
            H_howto --> HT_Start
            HT_Start[获取任务ID] --> HT_Ctx[准备上下文(任务详情)] --> HT_LLM[调用 LLM 生成建议] --> HT_Display[向用户展示建议]
        end

        subgraph QA
            H_qa --> QA_Start
            QA_Start[获取用户问题] --> QA_Ctx[准备上下文(项目元数据、**相关的**任务)] --> QA_LLM[调用 LLM 生成回答] --> QA_Display[向用户展示回答]
            note right of QA_Ctx: 默认使用 query_tasks 仅传递未完成的任务，<br>除非问题明确涉及历史数据
        end
    end
```

## 3. 工具 (Utilities)

- `storage.py`: 封装所有对 `.xixi/db.json` 的读写操作。
  - `init_project(name, goal)`: 初始化项目数据库文件。
  - `load_db()`: 加载整个 JSON 数据库。
  - `save_db(data)`: 将整个数据对象保存回 JSON 文件。
  - `query_tasks(status=None, overdue=None)`: 根据条件查询任务。`status` 是一个状态列表 (e.g., `['todo', 'in_progress']`)；`overdue` 为 `True` 时返回超期任务。
- `llm_api.py`: 封装与大语言模型交互的接口。
  - `decompose_requirement(requirement, project_context)`: 拆解需求。
  - `get_task_advice(task, project_context)`: 为任务生成建议。
  - `generate_report(project_context)`: 生成报告。
  - `answer_question(question, project_context)`: 回答问题。
- `display.py`: 负责格式化输出，例如以表格形式打印任务列表。

## 4. 数据设计 (Data Design)

所有数据以 JSON 格式统一存储在 `.xixi/db.json` 文件中。

```json
{
  "project": {
    "project_id": "uuid-v4-string",
    "project_name": "项目名称",
    "project_goal": "项目目标",
    "created_at": "iso-timestamp"
  },
  "tasks": [
    {
      "task_id": "short-unique-id-1",         // 必填
      "parent_id": "short-unique-id-parent",  // 可为空, 用于表示子任务
      "title": "任务标题",                      // 必填
      "description": "任务的详细描述",            // 可为空
      "status": "todo" | "in_progress" | "done" | "blocked", // 必填
      "difficulty": 1,                        // 可为空, 1-5
      "estimated_hours": 8,                   // 可为空
      "due_date": "YYYY-MM-DD",               // 可为空
      "dependencies": ["short-unique-id-2"],  // 可为空, 依赖的任务ID列表
      "checklist": [                          // 可为空
        { "item": "检查点1", "done": false }
      ],
      "created_at": "iso-timestamp",          // 必填
      "updated_at": "iso-timestamp"           // 必填
    }
  ]
}
```

## 5. 节点设计 (Node Design)

虽然这是一个 CLI 应用而非 PocketFlow 流程，但我们可以将每个命令看作一个独立的逻辑节点。

- **`InitNode`**:
  - `exec`: 执行初始化逻辑，与用户交互并调用 `storage.py`。
- **`ReplNode`**:
  - `exec`: 启动主循环，监听和分发用户命令。
- **`DecomposeNode`**:
  - `prep`: 收集用户输入的需求和当前项目上下文。
  - `exec`: 调用 `llm_api.decompose_requirement`。
  - `post`: 将返回的任务存入数据库并展示给用户。
- **`ListNode`**:
  - `prep`: 调用 `storage.py` 加载任务。
  - `exec`: 调用 `display.py` 格式化任务列表。
  - `post`: 打印结果。
- **`HowtoNode`**:
  - `prep`: 根据用户指定的 `task_id` 加载任务和项目上下文。
  - `exec`: 调用 `llm_api.get_task_advice`。
  - `post`: 打印建议。

## 6. 实现规划

1.  **环境搭建**: 创建 `main.py` 作为入口，`requirements.txt` 添加所需依赖（如 `rich` 用于美化终端输出，`questionary` 用于交互式提问）。
2.  **骨架先行**: 实现 `main.py` 的基本逻辑，包括 `init` 子命令的框架和主循环的启动检查。
3.  **数据层**: 实现 `utils/storage.py`，完成对 `.xixi/db.json` 的原子化读写操作。
4.  **命令实现**: 逐一实现 `/list`, `/exit` 等简单命令。
5.  **LLM 集成**: 实现 `utils/llm_api.py`，并完成核心的 `/decompose`、`/howto`、`/qa` 和 `/report` 功能。
6.  **交互优化**: 使用 `rich` 和 `questionary` 优化输入输出体验，例如实现 `/` 的自动补全提示。

## 7. 示例文件结构

```
xixi-project/
├── .xixi/
│   └── db.json
├── main.py           # 应用主入口
├── cli.py            # Click 或 Argparse 的命令定义
├── commands/
│   ├── __init__.py
│   ├── list.py
│   ├── howto.py
│   └── ...           # 其他命令模块
├── utils/
│   ├── __init__.py
│   ├── storage.py    # 数据存储
│   ├── llm_api.py    # LLM 调用
│   └── display.py    # 格式化输出
└── requirements.txt
```