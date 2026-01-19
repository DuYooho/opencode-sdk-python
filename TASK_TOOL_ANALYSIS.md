# Opencode SDK Python - 工具（Tool）分析报告

## 概述

本文档提供了对 `opencode-sdk-python` 仓库的全面分析。经过详细检查，**仓库中不存在名为 "Task" 的工具**。但是，仓库中确实存在 **Tool（工具）** 的概念和实现。

## 仓库结构

```
opencode-sdk-python/
├── src/opencode_ai/          # 主要源代码
│   ├── types/                 # 类型定义
│   │   ├── tool_part.py      # Tool 相关类型
│   │   ├── tool_state_*.py   # Tool 状态类型
│   │   ├── mode.py           # 模式定义（包含 tools）
│   │   └── ...
│   ├── resources/            # API 资源
│   └── _client.py            # 客户端实现
├── examples/                 # 示例代码（目前为空）
└── api.md                    # API 文档
```

## Tool（工具）概念

### 1. Tool 的定义

在这个 SDK 中，"Tool" 是一个核心概念，主要通过以下类型定义：

#### ToolPart（工具部分）

位置：`src/opencode_ai/types/tool_part.py`

```python
class ToolPart(BaseModel):
    id: str
    call_id: str           # 工具调用 ID
    message_id: str        # 消息 ID
    session_id: str        # 会话 ID
    state: State          # 工具状态
    tool: str             # 工具名称
    type: Literal["tool"] # 类型标识
```

`ToolPart` 代表在消息中执行的工具操作。

#### Tool 状态

Tool 有四种状态，分别定义在不同的文件中：

**1. ToolStatePending（待处理）**
```python
class ToolStatePending(BaseModel):
    status: Literal["pending"]
```

**2. ToolStateRunning（运行中）**
```python
class ToolStateRunning(BaseModel):
    status: Literal["running"]
    time: Time              # 开始时间
    input: Optional[object] # 可选输入
    metadata: Optional[Dict[str, object]]
    title: Optional[str]
```

**3. ToolStateCompleted（已完成）**
```python
class ToolStateCompleted(BaseModel):
    input: Dict[str, object]   # 输入参数
    metadata: Dict[str, object] # 元数据
    output: str                # 输出结果
    status: Literal["completed"]
    time: Time                 # 开始和结束时间
    title: str                 # 工具标题
```

**4. ToolStateError（错误）**
```python
class ToolStateError(BaseModel):
    error: str               # 错误信息
    input: Dict[str, object] # 输入参数
    status: Literal["error"]
    time: Time              # 开始和结束时间
```

### 2. Mode（模式）中的 Tools

位置：`src/opencode_ai/types/mode.py`

```python
class Mode(BaseModel):
    name: str
    tools: Dict[str, bool]  # 工具配置：工具名称 -> 是否启用
    model: Optional[Model] = None
    prompt: Optional[str] = None
    temperature: Optional[float] = None
```

在 Mode 中，`tools` 是一个字典，键是工具名称，值是布尔值表示该工具是否启用。

### 3. Session Chat 中的 Tools

位置：`src/opencode_ai/types/session_chat_params.py`

```python
class SessionChatParams(TypedDict, total=False):
    model_id: Required[str]
    parts: Required[Iterable[Part]]
    provider_id: Required[str]
    message_id: str
    mode: str
    system: str
    tools: Dict[str, bool]  # 工具配置
```

在发送聊天消息时，可以指定哪些工具可用。

## 如何使用 Tool

### 基本使用流程

1. **创建客户端**
```python
from opencode_ai import Opencode

client = Opencode()
```

2. **创建会话**
```python
session = client.session.create()
```

3. **发送带工具配置的消息**
```python
from opencode_ai.types import TextPartInputParam

response = client.session.chat(
    id=session.id,
    model_id="your-model-id",
    provider_id="your-provider-id",
    parts=[
        TextPartInputParam(
            text="你的提示内容",
            type="text"
        )
    ],
    tools={
        "tool_name_1": True,  # 启用工具 1
        "tool_name_2": False, # 禁用工具 2
    }
)
```

4. **检查响应中的工具执行**
```python
# 响应是一个 AssistantMessage，包含多个 parts
for part in response.parts:
    if part.type == "tool":
        # 这是一个 ToolPart
        print(f"工具: {part.tool}")
        print(f"状态: {part.state.status}")
        
        if part.state.status == "completed":
            print(f"输出: {part.state.output}")
        elif part.state.status == "error":
            print(f"错误: {part.state.error}")
```

### 配置工具

可以通过配置文件来配置模式中的工具：

```python
# 获取当前配置
config = client.config.get()

# 配置中的 modes 定义了不同模式的工具
# 每个模式可以有自己的工具配置
```

### Part 类型系统

消息中的 `Part` 可以是以下类型之一：

```python
Part = Union[
    TextPart,        # 文本内容
    FilePart,        # 文件内容
    ToolPart,        # 工具执行
    StepStartPart,   # 步骤开始
    StepFinishPart,  # 步骤结束
    SnapshotPart,    # 快照
    PatchPart        # 补丁
]
```

## 异步使用

SDK 也支持异步操作：

```python
import asyncio
from opencode_ai import AsyncOpencode

async def main():
    client = AsyncOpencode()
    
    # 创建会话
    session = await client.session.create()
    
    # 发送消息
    response = await client.session.chat(
        id=session.id,
        model_id="your-model-id",
        provider_id="your-provider-id",
        parts=[...],
        tools={"tool_name": True}
    )
    
    # 处理响应
    for part in response.parts:
        if part.type == "tool":
            print(f"工具执行: {part.tool}")

asyncio.run(main())
```

## 关键发现总结

1. **没有 "Task" 工具**：仓库中不存在名为 "Task" 的独立工具或类。

2. **Tool 是一个通用概念**：
   - 工具通过名称字符串标识
   - 工具可以在模式（Mode）和会话聊天（Session Chat）中配置
   - 工具的执行状态通过 `ToolPart` 和相关状态类型跟踪

3. **工具状态生命周期**：
   - pending（待处理）→ running（运行中）→ completed（已完成）
   - 或者：pending（待处理）→ running（运行中）→ error（错误）

4. **工具配置**：
   - 使用 `Dict[str, bool]` 格式
   - 键是工具名称，值表示是否启用

## 相关文件

- `src/opencode_ai/types/tool_part.py` - ToolPart 定义
- `src/opencode_ai/types/tool_state_*.py` - 工具状态定义
- `src/opencode_ai/types/mode.py` - 模式定义（包含工具配置）
- `src/opencode_ai/types/session_chat_params.py` - 聊天参数（包含工具配置）
- `src/opencode_ai/types/part.py` - Part 类型定义
- `api.md` - 完整 API 文档

## 参考资源

- 官方文档：https://opencode.ai/docs
- GitHub 仓库：https://github.com/sst/opencode-sdk-python
- API 参考：查看仓库中的 `api.md` 文件

## 结论

虽然仓库中没有名为 "Task" 的工具，但它提供了一个强大的工具系统，允许：
- 在会话中动态配置工具
- 跟踪工具执行状态
- 处理工具的输入和输出
- 管理工具的生命周期

如果您需要使用特定的工具，应该查阅 Opencode AI 平台的文档，了解可用的工具名称和功能。
