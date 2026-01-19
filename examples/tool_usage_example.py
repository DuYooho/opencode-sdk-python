#!/usr/bin/env python3
"""
Tool Usage Example for Opencode SDK Python

This example demonstrates how to:
1. Create a client and session
2. Configure and use tools in chat
3. Monitor tool execution states
4. Handle tool outputs and errors
"""

from opencode_ai import Opencode
from opencode_ai.types import TextPartInputParam


def basic_tool_usage():
    """Basic example of using tools in a chat session"""
    
    # Initialize client
    client = Opencode()
    
    # Create a new session
    session = client.session.create()
    print(f"Created session: {session.id}")
    
    # Send a message with specific tools enabled
    response = client.session.chat(
        id=session.id,
        model_id="your-model-id",  # Replace with actual model ID
        provider_id="your-provider-id",  # Replace with actual provider ID
        parts=[
            TextPartInputParam(
                text="Please help me analyze this code",
                type="text"
            )
        ],
        tools={
            "code_analyzer": True,  # Enable code analyzer tool
            "file_reader": True,    # Enable file reader tool
            "search": False,        # Disable search tool
        }
    )
    
    # Process the response
    print(f"\nReceived {len(response.parts)} parts in response:")
    
    for i, part in enumerate(response.parts, 1):
        print(f"\nPart {i}:")
        print(f"  Type: {part.type}")
        
        if part.type == "text":
            print(f"  Text: {part.text[:100]}...")  # First 100 chars
            
        elif part.type == "tool":
            print(f"  Tool: {part.tool}")
            print(f"  Status: {part.state.status}")
            
            # Handle different tool states
            if part.state.status == "pending":
                print("  Tool is waiting to execute")
                
            elif part.state.status == "running":
                print(f"  Tool is running...")
                if part.state.title:
                    print(f"  Title: {part.state.title}")
                    
            elif part.state.status == "completed":
                print(f"  Title: {part.state.title}")
                print(f"  Input: {part.state.input}")
                print(f"  Output: {part.state.output}")
                print(f"  Duration: {part.state.time.end - part.state.time.start}s")
                
            elif part.state.status == "error":
                print(f"  Error occurred: {part.state.error}")
                print(f"  Input: {part.state.input}")


def check_available_modes():
    """Check available modes and their tool configurations"""
    
    client = Opencode()
    
    # Get available modes
    modes_response = client.app.modes()
    
    print("Available modes and their tools:\n")
    for mode in modes_response.modes:
        print(f"Mode: {mode.name}")
        print(f"  Tools:")
        for tool_name, enabled in mode.tools.items():
            status = "✓" if enabled else "✗"
            print(f"    {status} {tool_name}")
        
        if mode.model:
            print(f"  Model: {mode.model.api_model_id}")
        if mode.temperature:
            print(f"  Temperature: {mode.temperature}")
        print()


def monitor_tool_execution():
    """Example of monitoring tool execution in real-time"""
    
    client = Opencode()
    session = client.session.create()
    
    # Send a request that will trigger tool usage
    response = client.session.chat(
        id=session.id,
        model_id="your-model-id",
        provider_id="your-provider-id",
        parts=[
            TextPartInputParam(
                text="Analyze the repository structure",
                type="text"
            )
        ],
        tools={
            "file_reader": True,
            "directory_scanner": True,
        }
    )
    
    # Count tools by state
    tool_states = {
        "pending": 0,
        "running": 0,
        "completed": 0,
        "error": 0
    }
    
    for part in response.parts:
        if part.type == "tool":
            tool_states[part.state.status] += 1
    
    print("Tool Execution Summary:")
    print(f"  Pending: {tool_states['pending']}")
    print(f"  Running: {tool_states['running']}")
    print(f"  Completed: {tool_states['completed']}")
    print(f"  Errors: {tool_states['error']}")


def async_tool_usage():
    """Example using async client"""
    import asyncio
    from opencode_ai import AsyncOpencode
    
    async def run_async():
        client = AsyncOpencode()
        
        # Create session
        session = await client.session.create()
        
        # Send message with tools
        response = await client.session.chat(
            id=session.id,
            model_id="your-model-id",
            provider_id="your-provider-id",
            parts=[
                TextPartInputParam(
                    text="Execute async operation",
                    type="text"
                )
            ],
            tools={"async_tool": True}
        )
        
        # Process response
        for part in response.parts:
            if part.type == "tool":
                print(f"Tool {part.tool}: {part.state.status}")
    
    asyncio.run(run_async())


if __name__ == "__main__":
    print("=" * 60)
    print("Opencode SDK - Tool Usage Examples")
    print("=" * 60)
    
    print("\n1. Checking available modes...")
    try:
        check_available_modes()
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Make sure you have valid API credentials configured")
    
    print("\n2. Basic tool usage...")
    try:
        basic_tool_usage()
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Replace 'your-model-id' and 'your-provider-id' with actual values")
    
    print("\n" + "=" * 60)
    print("Example completed")
    print("=" * 60)
