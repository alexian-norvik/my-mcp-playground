#!/usr/bin/env python3
"""
MCP Learning Server - A comprehensive example demonstrating MCP concepts

This server demonstrates:
1. Tools - Functions that AI can call
2. Resources - Data sources that AI can read
3. Prompts - Templates for AI interactions
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    CallToolResult,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    ReadResourceResult,
    Resource,
    TextContent,
    Tool,
)

# Create a simple in-memory "database" for our examples
TASKS_DB = [
    {"id": 1, "title": "Learn MCP basics", "completed": False, "created": "2025-08-15"},
    {
        "id": 2,
        "title": "Build a simple tool",
        "completed": True,
        "created": "2025-08-14",
    },
    {
        "id": 3,
        "title": "Understand resources",
        "completed": False,
        "created": "2025-08-15",
    },
]

NOTES_DIR = Path("./notes")
NOTES_DIR.mkdir(exist_ok=True)

# Create some sample notes
sample_notes = {
    "mcp_basics.md": """# MCP Basics

Model Context Protocol (MCP) is a standard for connecting AI assistants to external data sources.

## Key Concepts:
- **Tools**: Functions that AI can call to perform actions
- **Resources**: Data sources that AI can read from
- **Prompts**: Templates for AI interactions

## Benefits:
- Standardized interface
- Secure connections
- Real-time data access
""",
    "learning_goals.md": """# Learning Goals

## Today's Goals:
1. Understand MCP architecture
2. Create tools for task management
3. Implement resource reading
4. Build custom prompts

## Next Steps:
- Connect to external APIs
- Add file system operations
- Implement database connections
""",
}

for filename, content in sample_notes.items():
    (NOTES_DIR / filename).write_text(content)

server = Server("mcp-learning-server")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="add_task",
            description="Add a new task to the task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The task title"},
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                    },
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="list_tasks",
            description="List all tasks with their status",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to complete",
                    }
                },
                "required": ["task_id"],
            },
        ),
        Tool(
            name="get_weather",
            description="Get current weather information (simulated)",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name"}
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="calculate",
            description="Perform basic mathematical calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate",
                    }
                },
                "required": ["expression"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls."""
    if name == "add_task":
        title = arguments["title"]
        description = arguments.get("description", "")

        new_task = {
            "id": max(task["id"] for task in TASKS_DB) + 1 if TASKS_DB else 1,
            "title": title,
            "description": description,
            "completed": False,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }
        TASKS_DB.append(new_task)

        return CallToolResult(
            content=[
                TextContent(
                    type="text", text=f"Task '{title}' added with ID {new_task['id']}"
                )
            ]
        )

    elif name == "list_tasks":
        if not TASKS_DB:
            return CallToolResult(
                content=[TextContent(type="text", text="No tasks found.")]
            )

        task_list = "Current Tasks:\n"
        for task in TASKS_DB:
            status = "✅" if task["completed"] else "⏳"
            task_list += f"{status} [{task['id']}] {task['title']} (created: {task['created']})\n"

        return CallToolResult(content=[TextContent(type="text", text=task_list)])

    elif name == "complete_task":
        task_id = arguments["task_id"]

        for task in TASKS_DB:
            if task["id"] == task_id:
                task["completed"] = True
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"Task '{task['title']}' marked as completed!",
                        )
                    ]
                )

        return CallToolResult(
            content=[
                TextContent(type="text", text=f"Task with ID {task_id} not found.")
            ]
        )

    elif name == "get_weather":
        city = arguments["city"]
        # Simulated weather data
        weather_data = {
            "San Francisco": {"temp": "68°F", "condition": "Foggy", "humidity": "85%"},
            "New York": {"temp": "75°F", "condition": "Sunny", "humidity": "60%"},
            "London": {"temp": "62°F", "condition": "Rainy", "humidity": "90%"},
        }

        weather = weather_data.get(
            city, {"temp": "72°F", "condition": "Unknown", "humidity": "70%"}
        )
        result = f"Weather in {city}:\n🌡️ Temperature: {weather['temp']}\n🌤️ Condition: {weather['condition']}\n💧 Humidity: {weather['humidity']}"

        return CallToolResult(content=[TextContent(type="text", text=result)])

    elif name == "calculate":
        expression = arguments["expression"]
        try:
            # Simple safe evaluation for basic math
            allowed_chars = set("0123456789+-*/.() ")
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return CallToolResult(
                    content=[TextContent(type="text", text=f"{expression} = {result}")]
                )
            else:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="Invalid expression. Only basic math operations allowed.",
                        )
                    ]
                )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Calculation error: {str(e)}")]
            )

    else:
        raise ValueError(f"Unknown tool: {name}")


@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List all available resources."""
    resources = []

    # Add task database as a resource
    resources.append(
        Resource(
            uri="tasks://database",
            name="Task Database",
            description="Current task list with completion status",
            mimeType="application/json",
        )
    )

    # Add notes files as resources
    for note_file in NOTES_DIR.glob("*.md"):
        resources.append(
            Resource(
                uri=f"file://{note_file}",
                name=f"Note: {note_file.stem}",
                description=f"Learning note about {note_file.stem.replace('_', ' ')}",
                mimeType="text/markdown",
            )
        )

    # Add system info as a resource
    resources.append(
        Resource(
            uri="system://info",
            name="System Information",
            description="Current system date and time information",
            mimeType="application/json",
        )
    )

    return resources


@server.read_resource()
async def handle_read_resource(uri: str) -> ReadResourceResult:
    """Read resource content."""
    if uri == "tasks://database":
        return ReadResourceResult(
            contents=[TextContent(type="text", text=json.dumps(TASKS_DB, indent=2))]
        )

    elif uri.startswith("file://"):
        file_path = Path(uri[7:])  # Remove "file://" prefix
        if file_path.exists() and file_path.is_file():
            content = file_path.read_text()
            return ReadResourceResult(contents=[TextContent(type="text", text=content)])
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    elif uri == "system://info":
        system_info = {
            "current_time": datetime.now().isoformat(),
            "server_name": "mcp-learning-server",
            "platform": os.name,
            "working_directory": str(Path.cwd()),
        }
        return ReadResourceResult(
            contents=[TextContent(type="text", text=json.dumps(system_info, indent=2))]
        )

    else:
        raise ValueError(f"Unknown resource URI: {uri}")


@server.list_prompts()
async def handle_list_prompts() -> List[Prompt]:
    """List all available prompts."""
    return [
        Prompt(
            name="task_summary",
            description="Generate a summary of current tasks",
            arguments=[
                PromptArgument(
                    name="include_completed",
                    description="Whether to include completed tasks",
                    required=False,
                )
            ],
        ),
        Prompt(
            name="learning_plan",
            description="Create a personalized MCP learning plan",
            arguments=[
                PromptArgument(
                    name="skill_level",
                    description="Current skill level (beginner, intermediate, advanced)",
                    required=True,
                ),
                PromptArgument(
                    name="focus_area",
                    description="Specific area to focus on (tools, resources, prompts, etc.)",
                    required=False,
                ),
            ],
        ),
        Prompt(
            name="explain_concept",
            description="Explain an MCP concept in detail",
            arguments=[
                PromptArgument(
                    name="concept",
                    description="The MCP concept to explain (tools, resources, prompts, servers, clients)",
                    required=True,
                )
            ],
        ),
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict) -> GetPromptResult:
    """Handle prompt requests."""
    if name == "task_summary":
        include_completed = arguments.get("include_completed", "true").lower() == "true"

        if include_completed:
            tasks_to_show = TASKS_DB
            prompt_text = "Please provide a comprehensive summary of all tasks (completed and pending)."
        else:
            tasks_to_show = [task for task in TASKS_DB if not task["completed"]]
            prompt_text = "Please provide a summary of pending tasks only."

        task_data = json.dumps(tasks_to_show, indent=2)
        prompt_text += f"\n\nCurrent tasks data:\n{task_data}"

        return GetPromptResult(
            description="Task summary prompt with current task data",
            messages=[
                PromptMessage(
                    role="user", content=TextContent(type="text", text=prompt_text)
                )
            ],
        )

    elif name == "learning_plan":
        skill_level = arguments["skill_level"]
        focus_area = arguments.get("focus_area", "general MCP concepts")

        prompt_text = f"""Create a personalized learning plan for MCP (Model Context Protocol) based on the following:

Skill Level: {skill_level}
Focus Area: {focus_area}

Please provide:
1. Learning objectives appropriate for this skill level
2. Recommended sequence of topics to study
3. Practical exercises to reinforce learning
4. Resources for further reading
5. Expected timeline for mastery

Consider the current MCP server capabilities available in this playground environment."""

        return GetPromptResult(
            description=f"Personalized MCP learning plan for {skill_level} level",
            messages=[
                PromptMessage(
                    role="user", content=TextContent(type="text", text=prompt_text)
                )
            ],
        )

    elif name == "explain_concept":
        concept = arguments["concept"]

        prompt_text = f"""Please provide a detailed explanation of the MCP concept: "{concept}"

Include:
1. Definition and purpose
2. How it works in the MCP architecture
3. Real-world use cases and examples
4. Best practices for implementation
5. Common pitfalls to avoid
6. How it relates to other MCP concepts

Use examples from this MCP learning server where relevant to illustrate the concepts."""

        return GetPromptResult(
            description=f"Detailed explanation of MCP concept: {concept}",
            messages=[
                PromptMessage(
                    role="user", content=TextContent(type="text", text=prompt_text)
                )
            ],
        )

    else:
        raise ValueError(f"Unknown prompt: {name}")


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    from mcp.types import ServerCapabilities

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-learning-server",
                server_version="1.0.0",
                capabilities=ServerCapabilities(tools={}, resources={}, prompts={}),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
