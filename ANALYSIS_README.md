# Task Tool 分析 / Task Tool Analysis

## 📋 分析结论 / Analysis Conclusion

经过对 `opencode-sdk-python` 仓库的全面检查，**仓库中不存在名为 "Task" 的工具**。

After comprehensive examination of the `opencode-sdk-python` repository, **there is no tool named "Task" in this repository**.

## 📚 文档 / Documentation

本分析提供了以下文档：

This analysis provides the following documents:

1. **[TASK_TOOL_ANALYSIS.md](./TASK_TOOL_ANALYSIS.md)** - 中文详细分析报告
   - Tool 概念和定义
   - Tool 状态生命周期
   - 使用示例和最佳实践

2. **[TASK_TOOL_ANALYSIS_EN.md](./TASK_TOOL_ANALYSIS_EN.md)** - English detailed analysis report
   - Tool concepts and definitions
   - Tool state lifecycle
   - Usage examples and best practices

3. **[TOOL_ARCHITECTURE.md](./TOOL_ARCHITECTURE.md)** - 架构图和可视化
   - Tool 系统架构图
   - 状态生命周期可视化
   - 使用流程图

4. **[examples/tool_usage_example.py](./examples/tool_usage_example.py)** - Python 实用示例
   - 完整的工具使用代码示例
   - 同步和异步客户端示例
   - 工具状态监控示例

## 🔍 发现的内容 / What Was Found

虽然没有 "Task" 工具，但仓库包含了完整的 **Tool（工具）系统**：

While there is no "Task" tool, the repository contains a complete **Tool System**:

### 核心组件 / Core Components

1. **ToolPart** - 表示工具执行的消息部分
   - Represents tool execution in messages

2. **Tool States** - 四种工具状态
   - `pending` - 待处理
   - `running` - 运行中
   - `completed` - 已完成
   - `error` - 错误

3. **Tool Configuration** - 在 Mode 和 Session 中配置工具
   - Configure tools in Modes and Sessions
   - Format: `Dict[str, bool]` (tool_name → enabled)

## 🚀 快速开始 / Quick Start

```python
from opencode_ai import Opencode
from opencode_ai.types import TextPartInputParam

# 创建客户端 / Create client
client = Opencode()

# 创建会话 / Create session
session = client.session.create()

# 发送带工具配置的消息 / Send message with tool configuration
response = client.session.chat(
    id=session.id,
    model_id="your-model-id",
    provider_id="your-provider-id",
    parts=[
        TextPartInputParam(
            text="Your prompt",
            type="text"
        )
    ],
    tools={
        "tool_name": True  # 启用工具 / Enable tool
    }
)

# 处理响应 / Process response
for part in response.parts:
    if part.type == "tool":
        print(f"Tool: {part.tool}, Status: {part.state.status}")
```

## 📖 更多信息 / More Information

查看详细文档了解：
- Tool 类型系统的完整定义
- 工具状态的生命周期
- 实际使用案例
- 异步操作示例

See detailed documentation for:
- Complete Tool type system definitions
- Tool state lifecycle
- Practical use cases
- Async operation examples

## 🔗 相关资源 / Related Resources

- [Official Documentation](https://opencode.ai/docs)
- [GitHub Repository](https://github.com/sst/opencode-sdk-python)
- [API Reference](./api.md)

---

**注意 / Note**: 如需使用特定工具，请查阅 Opencode AI 平台文档获取可用工具列表和功能说明。

For specific tool usage, please consult the Opencode AI platform documentation for available tool names and functionality.
