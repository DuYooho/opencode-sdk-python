# Tool Architecture in Opencode SDK Python

## 架构图 / Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Opencode Client                           │
│                     (Opencode / AsyncOpencode)                   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ creates
                               ▼
                    ┌──────────────────┐
                    │     Session      │
                    └────────┬─────────┘
                             │
                             │ sends chat with tools config
                             ▼
                    ┌──────────────────┐
                    │  Chat Message    │
                    │  ┌────────────┐  │
                    │  │ model_id   │  │
                    │  │ provider_id│  │
                    │  │ parts[]    │  │
                    │  │ tools{}    │◄─── tools: Dict[str, bool]
                    │  └────────────┘  │      {"tool_name": True/False}
                    └────────┬─────────┘
                             │
                             │ returns
                             ▼
                    ┌──────────────────────────────────┐
                    │    AssistantMessage              │
                    │                                  │
                    │    parts: List[Part]             │
                    │    ┌──────────────────────────┐  │
                    │    │  Part (Union type)       │  │
                    │    │  ├─ TextPart            │  │
                    │    │  ├─ FilePart            │  │
                    │    │  ├─ ToolPart ◄──────────┼──┼─── Tool Execution
                    │    │  ├─ StepStartPart       │  │
                    │    │  ├─ StepFinishPart      │  │
                    │    │  ├─ SnapshotPart        │  │
                    │    │  └─ PatchPart           │  │
                    │    └──────────────────────────┘  │
                    └──────────────┬───────────────────┘
                                   │
                                   │ contains
                                   ▼
```

## ToolPart 结构 / ToolPart Structure

```
┌─────────────────────────────────────────────────────────────┐
│                         ToolPart                             │
│                                                              │
│  id: str                    ← Unique identifier             │
│  call_id: str               ← Tool call identifier          │
│  message_id: str            ← Parent message ID             │
│  session_id: str            ← Parent session ID             │
│  tool: str                  ← Tool name (e.g., "search")    │
│  type: "tool"               ← Type discriminator            │
│  state: State               ← Current execution state       │
│         │                                                    │
│         └─► Union of:                                       │
│             ├─ ToolStatePending                            │
│             ├─ ToolStateRunning                            │
│             ├─ ToolStateCompleted                          │
│             └─ ToolStateError                              │
└─────────────────────────────────────────────────────────────┘
```

## 工具状态生命周期 / Tool State Lifecycle

```
┌──────────┐
│  START   │
└────┬─────┘
     │
     ▼
┌──────────────────┐
│  ToolStatePending │  ← Tool is queued
│  ┌──────────────┐│
│  │ status:      ││
│  │  "pending"   ││
│  └──────────────┘│
└────────┬─────────┘
         │
         │ execution starts
         ▼
┌──────────────────┐
│ ToolStateRunning │  ← Tool is executing
│ ┌──────────────┐ │
│ │ status:      │ │
│ │  "running"   │ │
│ │ time:        │ │
│ │  start: float│ │
│ │ input: obj?  │ │
│ │ title: str?  │ │
│ └──────────────┘ │
└────────┬─────────┘
         │
         ├────────────────┬──────────────┐
         │ success        │ failure      │
         ▼                ▼              │
┌─────────────────┐  ┌──────────────┐   │
│ToolStateCompleted│  │ToolStateError│   │
│┌───────────────┐│  │┌────────────┐│   │
││ status:       ││  ││ status:    ││   │
││  "completed"  ││  ││  "error"   ││   │
││ time:         ││  ││ error: str ││   │
││  start: float ││  ││ input: {}  ││   │
││  end: float   ││  ││ time:      ││   │
││ input: {}     ││  ││  start: f  ││   │
││ output: str   ││  ││  end: f    ││   │
││ metadata: {}  ││  │└────────────┘│   │
││ title: str    ││  └──────────────┘   │
│└───────────────┘│                     │
└─────────┬───────┘                     │
          │                             │
          └─────────────┬───────────────┘
                        ▼
                   ┌────────┐
                   │  DONE  │
                   └────────┘
```

## Mode 中的工具配置 / Tool Configuration in Mode

```
┌──────────────────────────────────────────┐
│              Mode                         │
│                                          │
│  name: str              ← Mode name      │
│  tools: Dict[str, bool] ← Tool config    │
│      {                                   │
│        "file_reader": true,  ← enabled   │
│        "web_search": true,   ← enabled   │
│        "calculator": false   ← disabled  │
│      }                                   │
│  model: Optional[Model]                  │
│  prompt: Optional[str]                   │
│  temperature: Optional[float]            │
└──────────────────────────────────────────┘
```

## 使用流程 / Usage Flow

```
1. Create Client
   ├─► client = Opencode()
   └─► async_client = AsyncOpencode()

2. Create Session
   └─► session = client.session.create()

3. Configure Tools and Send Message
   └─► response = client.session.chat(
           id=session.id,
           model_id="...",
           provider_id="...",
           parts=[...],
           tools={
               "tool_1": True,   ← Enable tool_1
               "tool_2": False,  ← Disable tool_2
           }
       )

4. Process Response Parts
   └─► for part in response.parts:
           if part.type == "tool":
               ├─► Check: part.state.status
               ├─► If "completed": process part.state.output
               ├─► If "error": handle part.state.error
               └─► Access: part.tool (tool name)

5. Monitor Tool Execution
   └─► Track states: pending → running → completed/error
```

## 关键类型定义 / Key Type Definitions

```python
# Tool configuration format
tools: Dict[str, bool] = {
    "tool_name": True,   # Enable
    "other_tool": False, # Disable
}

# State type (discriminated union)
State = Union[
    ToolStatePending,     # status: "pending"
    ToolStateRunning,     # status: "running"
    ToolStateCompleted,   # status: "completed"
    ToolStateError        # status: "error"
]

# Part type (discriminated union)
Part = Union[
    TextPart,        # type: "text"
    FilePart,        # type: "file"
    ToolPart,        # type: "tool"
    StepStartPart,   # type: "step_start"
    StepFinishPart,  # type: "step_finish"
    SnapshotPart,    # type: "snapshot"
    PatchPart        # type: "patch"
]
```

## 注意事项 / Important Notes

1. **没有 "Task" 工具**: 仓库中不存在名为 "Task" 的独立工具
   - **No "Task" Tool**: There is no standalone tool named "Task" in the repository

2. **工具通过名称标识**: 工具使用字符串名称，如 "file_reader", "search" 等
   - **Tools Identified by Name**: Tools use string names like "file_reader", "search", etc.

3. **类型安全**: 使用 Pydantic 模型和 TypedDict 提供类型安全
   - **Type Safety**: Uses Pydantic models and TypedDict for type safety

4. **状态跟踪**: 工具执行状态通过 ToolPart.state 跟踪
   - **State Tracking**: Tool execution state tracked via ToolPart.state

5. **配置灵活**: 可在 Mode 或 Session 级别配置工具
   - **Flexible Configuration**: Configure tools at Mode or Session level
```
