# Opencode SDK Python - Tool Analysis Report

## Overview

This document provides a comprehensive analysis of the `opencode-sdk-python` repository. After thorough examination, **there is no tool named "Task" in this repository**. However, the repository does contain the concept and implementation of **Tools**.

## Repository Structure

```
opencode-sdk-python/
├── src/opencode_ai/          # Main source code
│   ├── types/                 # Type definitions
│   │   ├── tool_part.py      # Tool-related types
│   │   ├── tool_state_*.py   # Tool state types
│   │   ├── mode.py           # Mode definitions (includes tools)
│   │   └── ...
│   ├── resources/            # API resources
│   └── _client.py            # Client implementation
├── examples/                 # Example code (currently empty)
└── api.md                    # API documentation
```

## Tool Concept

### 1. Tool Definition

In this SDK, "Tool" is a core concept, primarily defined through the following types:

#### ToolPart

Location: `src/opencode_ai/types/tool_part.py`

```python
class ToolPart(BaseModel):
    id: str
    call_id: str           # Tool call ID
    message_id: str        # Message ID
    session_id: str        # Session ID
    state: State          # Tool state
    tool: str             # Tool name
    type: Literal["tool"] # Type identifier
```

`ToolPart` represents a tool operation executed within a message.

#### Tool States

Tools have four states, defined in separate files:

**1. ToolStatePending**
```python
class ToolStatePending(BaseModel):
    status: Literal["pending"]
```

**2. ToolStateRunning**
```python
class ToolStateRunning(BaseModel):
    status: Literal["running"]
    time: Time              # Start time
    input: Optional[object] # Optional input
    metadata: Optional[Dict[str, object]]
    title: Optional[str]
```

**3. ToolStateCompleted**
```python
class ToolStateCompleted(BaseModel):
    input: Dict[str, object]   # Input parameters
    metadata: Dict[str, object] # Metadata
    output: str                # Output result
    status: Literal["completed"]
    time: Time                 # Start and end time
    title: str                 # Tool title
```

**4. ToolStateError**
```python
class ToolStateError(BaseModel):
    error: str               # Error message
    input: Dict[str, object] # Input parameters
    status: Literal["error"]
    time: Time              # Start and end time
```

### 2. Tools in Mode

Location: `src/opencode_ai/types/mode.py`

```python
class Mode(BaseModel):
    name: str
    tools: Dict[str, bool]  # Tool configuration: tool name -> enabled
    model: Optional[Model] = None
    prompt: Optional[str] = None
    temperature: Optional[float] = None
```

In Mode, `tools` is a dictionary where keys are tool names and values are booleans indicating whether the tool is enabled.

### 3. Tools in Session Chat

Location: `src/opencode_ai/types/session_chat_params.py`

```python
class SessionChatParams(TypedDict, total=False):
    model_id: Required[str]
    parts: Required[Iterable[Part]]
    provider_id: Required[str]
    message_id: str
    mode: str
    system: str
    tools: Dict[str, bool]  # Tool configuration
```

When sending a chat message, you can specify which tools are available.

## How to Use Tools

### Basic Usage Flow

1. **Create a Client**
```python
from opencode_ai import Opencode

client = Opencode()
```

2. **Create a Session**
```python
session = client.session.create()
```

3. **Send a Message with Tool Configuration**
```python
from opencode_ai.types import TextPartInputParam

response = client.session.chat(
    id=session.id,
    model_id="your-model-id",
    provider_id="your-provider-id",
    parts=[
        TextPartInputParam(
            text="Your prompt content",
            type="text"
        )
    ],
    tools={
        "tool_name_1": True,  # Enable tool 1
        "tool_name_2": False, # Disable tool 2
    }
)
```

4. **Check Tool Execution in Response**
```python
# Response is an AssistantMessage containing multiple parts
for part in response.parts:
    if part.type == "tool":
        # This is a ToolPart
        print(f"Tool: {part.tool}")
        print(f"Status: {part.state.status}")
        
        if part.state.status == "completed":
            print(f"Output: {part.state.output}")
        elif part.state.status == "error":
            print(f"Error: {part.state.error}")
```

### Configuring Tools

You can configure tools in modes through the configuration:

```python
# Get current configuration
config = client.config.get()

# Modes in the config define tools for different modes
# Each mode can have its own tool configuration
```

### Part Type System

A `Part` in a message can be one of the following types:

```python
Part = Union[
    TextPart,        # Text content
    FilePart,        # File content
    ToolPart,        # Tool execution
    StepStartPart,   # Step start
    StepFinishPart,  # Step finish
    SnapshotPart,    # Snapshot
    PatchPart        # Patch
]
```

## Async Usage

The SDK also supports async operations:

```python
import asyncio
from opencode_ai import AsyncOpencode

async def main():
    client = AsyncOpencode()
    
    # Create session
    session = await client.session.create()
    
    # Send message
    response = await client.session.chat(
        id=session.id,
        model_id="your-model-id",
        provider_id="your-provider-id",
        parts=[...],
        tools={"tool_name": True}
    )
    
    # Process response
    for part in response.parts:
        if part.type == "tool":
            print(f"Tool execution: {part.tool}")

asyncio.run(main())
```

## Key Findings Summary

1. **No "Task" Tool**: There is no standalone tool or class named "Task" in the repository.

2. **Tool is a Generic Concept**:
   - Tools are identified by name strings
   - Tools can be configured in Modes and Session Chats
   - Tool execution state is tracked through `ToolPart` and related state types

3. **Tool State Lifecycle**:
   - pending → running → completed
   - Or: pending → running → error

4. **Tool Configuration**:
   - Uses `Dict[str, bool]` format
   - Keys are tool names, values indicate whether enabled

## Related Files

- `src/opencode_ai/types/tool_part.py` - ToolPart definition
- `src/opencode_ai/types/tool_state_*.py` - Tool state definitions
- `src/opencode_ai/types/mode.py` - Mode definition (includes tool config)
- `src/opencode_ai/types/session_chat_params.py` - Chat parameters (includes tool config)
- `src/opencode_ai/types/part.py` - Part type definitions
- `api.md` - Complete API documentation

## References

- Official Documentation: https://opencode.ai/docs
- GitHub Repository: https://github.com/sst/opencode-sdk-python
- API Reference: See `api.md` file in the repository

## Conclusion

While there is no tool named "Task" in the repository, it provides a powerful tool system that allows:
- Dynamic configuration of tools in sessions
- Tracking tool execution states
- Handling tool inputs and outputs
- Managing tool lifecycle

If you need to use specific tools, you should consult the Opencode AI platform documentation to learn about available tool names and functionality.
