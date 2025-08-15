# MCP Learning Playground 🚀

Welcome to your **Model Context Protocol (MCP)** learning playground! This project is designed to teach you MCP concepts through hands-on examples.

## What is MCP? 🤔

**Model Context Protocol (MCP)** is an open standard that enables AI assistants to securely connect to external data sources and tools. It provides a standardized way for AI systems to:

- 🔧 **Call Tools**: Execute functions and perform actions
- 📚 **Read Resources**: Access data from various sources
- 💭 **Use Prompts**: Leverage templated interactions

## Project Structure 📁

```
mcp-playground/
├── mcp_server.py      # Main MCP server with examples
├── test_client.py     # Client to test the server
├── notes/             # Learning materials
│   ├── mcp_basics.md
│   └── learning_goals.md
├── pyproject.toml     # Project configuration
└── README.md         # This file
```

## Getting Started 🎯

### 1. Test Your MCP Server

Run the comprehensive test suite:
```bash
uv run python test_client.py
```

This will demonstrate:
- ✅ Tool calls (task management, weather, calculator)
- 📖 Resource reading (task database, notes, system info)
- 🎯 Prompt generation (summaries, learning plans)

### 2. Interactive Demo

Try the interactive demo to experiment with MCP:
```bash
uv run python test_client.py --interactive
```

This lets you:
- Add and manage tasks
- Check weather (simulated)
- Perform calculations
- Read learning notes
- Experience MCP interactively

### 3. Run the Server Standalone

To run just the server (for integration with other MCP clients):
```bash
uv run python mcp_server.py
```

## Learning Path 🎓

### Phase 1: Understanding the Basics
1. **Run the test client** to see MCP in action
2. **Explore the server code** in `mcp_server.py`
3. **Read the generated notes** in the `notes/` directory

### Phase 2: Core Concepts

#### 🔧 Tools
Tools are functions that AI can call to perform actions. Our server includes:
- `add_task`: Create new tasks
- `list_tasks`: View all tasks
- `complete_task`: Mark tasks as done
- `get_weather`: Get weather data (simulated)
- `calculate`: Perform math operations

#### 📚 Resources
Resources are data sources that AI can read from:
- `tasks://database`: JSON task database
- `file://./notes/*.md`: Learning notes
- `system://info`: System information

#### 💭 Prompts
Prompts are templates for AI interactions:
- `task_summary`: Generate task summaries
- `learning_plan`: Create personalized learning plans
- `explain_concept`: Detailed MCP explanations

### Phase 3: Hands-On Experimentation
1. **Modify existing tools** to add new features
2. **Create new resources** for different data types
3. **Design custom prompts** for specific use cases
4. **Connect to external APIs** (advanced)

## Key MCP Concepts Demonstrated 📖

### Server Architecture

```python
# 1. Define tools with schemas
@handle_list_tools.list_tools()
async def handle_list_tools() -> List[Tool]:
    return [Tool(name="my_tool", description="...", inputSchema={...})]

# 2. Handle tool calls
@handle_list_tools.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
    # Your tool logic here
    return CallToolResult(content=[TextContent(...)])

# 3. Provide resources
@handle_list_tools.list_resources()
async def handle_list_resources() -> List[Resource]:
    return [Resource(uri="...", name="...", description="...")]
```

### Client Integration
```python
# Connect to server
async with ClientSession(server_params) as session:
    # Call tools
    result = await session.call_tool(CallToolRequest(...))

    # Read resources
    resource = await session.read_resource(ReadResourceRequest(...))

    # Use prompts
    prompt = await session.get_prompt(GetPromptRequest(...))
```

## Next Steps 🚀

Ready to go deeper? Try these challenges:

### Beginner Challenges
- [ ] Add a new tool for deleting tasks
- [ ] Create a resource for reading system environment variables
- [ ] Design a prompt for generating daily task reports

### Intermediate Challenges
- [ ] Connect to a real weather API
- [ ] Implement file system operations (read/write files)
- [ ] Add database integration (SQLite)

### Advanced Challenges
- [ ] Build a web scraping tool
- [ ] Integrate with external APIs (GitHub, Slack, etc.)
- [ ] Create a multi-server MCP setup

## Troubleshooting 🔧

### Common Issues

**Server won't start:**
```bash
# Make sure MCP is installed
uv add mcp

# Check Python version
python --version  # Should be 3.12+
```

**Client connection fails:**
- Ensure the server is running
- Check for any syntax errors in `mcp_server.py`

**Tool calls fail:**
- Verify the tool name and arguments match the schema
- Check the server logs for error details

## Resources for Further Learning 📚

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

## Contributing to Your Learning 🤝

As you learn MCP, consider:
1. **Documenting your experiments** in the `notes/` directory
2. **Creating new example tools** for different use cases
3. **Sharing your learnings** with the community

---

Happy learning! 🎉 MCP opens up amazing possibilities for AI integration.

## Quick Reference Commands

```bash
# Run comprehensive tests
uv run python test_client.py

# Interactive demo
uv run python test_client.py --interactive

# Start server only
uv run python mcp_server.py

# Add new dependencies
uv add package-name
```
