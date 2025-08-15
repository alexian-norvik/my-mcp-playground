#!/usr/bin/env python3
"""
Simple MCP Demo - Shows MCP concepts without complex client-server setup

This demonstrates the core MCP concepts in a simplified way.
"""

import json
from datetime import datetime
from pathlib import Path


# Simulate the MCP data structures and functionality
class MCPDemo:
    def __init__(self):
        # Sample task database
        self.tasks = [
            {
                "id": 1,
                "title": "Learn MCP basics",
                "completed": False,
                "created": "2025-08-15",
            },
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

        # Ensure notes directory exists
        self.notes_dir = Path("./notes")
        self.notes_dir.mkdir(exist_ok=True)

    def demonstrate_tools(self):
        """Demonstrate MCP Tools - Functions that AI can call"""
        print("🔧 MCP TOOLS DEMONSTRATION")
        print("-" * 30)
        print("Tools are functions that AI assistants can call to perform actions.")
        print()

        # Tool 1: Add Task
        print("📝 Tool: add_task")
        new_task = {
            "id": 4,
            "title": "Test MCP integration",
            "completed": False,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }
        self.tasks.append(new_task)
        print(f"✅ Added task: '{new_task['title']}' with ID {new_task['id']}")
        print()

        # Tool 2: List Tasks
        print("📋 Tool: list_tasks")
        for task in self.tasks:
            status = "✅" if task["completed"] else "⏳"
            print(
                f"  {status} [{task['id']}] {task['title']} (created: {task['created']})"
            )
        print()

        # Tool 3: Calculator
        print("🧮 Tool: calculate")
        expression = "15 + 25 * 2"
        result = eval(expression)  # Simplified for demo
        print(f"  {expression} = {result}")
        print()

        # Tool 4: Weather (simulated)
        print("🌤️ Tool: get_weather")
        weather_data = {"temp": "72°F", "condition": "Sunny", "humidity": "65%"}
        print("  Weather in San Francisco:")
        print(f"  🌡️ Temperature: {weather_data['temp']}")
        print(f"  ☀️ Condition: {weather_data['condition']}")
        print(f"  💧 Humidity: {weather_data['humidity']}")
        print()

    def demonstrate_resources(self):
        """Demonstrate MCP Resources - Data sources that AI can read"""
        print("📚 MCP RESOURCES DEMONSTRATION")
        print("-" * 32)
        print("Resources are data sources that AI assistants can read from.")
        print()

        # Resource 1: Task Database
        print("📊 Resource: tasks://database")
        print(f"  Task database contains {len(self.tasks)} tasks:")
        print(f"  {json.dumps(self.tasks[:2], indent=2)}")  # Show first 2 tasks
        print("  ... (additional tasks)")
        print()

        # Resource 2: Notes Files
        print("📝 Resource: file://notes/*.md")
        sample_note = """# MCP Learning Notes

Key concepts learned today:
- Tools: Functions AI can call
- Resources: Data AI can read
- Prompts: Templates for interactions

Next steps: Build more complex integrations!"""

        note_file = self.notes_dir / "demo_notes.md"
        note_file.write_text(sample_note)
        print(f"  Created note file: {note_file}")
        print(f"  Content preview: {sample_note[:100]}...")
        print()

        # Resource 3: System Information
        print("💻 Resource: system://info")
        system_info = {
            "current_time": datetime.now().isoformat(),
            "working_directory": str(Path.cwd()),
            "python_version": "3.12",
            "mcp_server": "learning-demo",
        }
        print("  System information:")
        print(f"  {json.dumps(system_info, indent=2)}")
        print()

    def demonstrate_prompts(self):
        """Demonstrate MCP Prompts - Templates for AI interactions"""
        print("💭 MCP PROMPTS DEMONSTRATION")
        print("-" * 31)
        print("Prompts are templates that help AI assistants generate responses.")
        print()

        # Prompt 1: Task Summary
        print("📋 Prompt: task_summary")
        completed_tasks = [t for t in self.tasks if t["completed"]]
        pending_tasks = [t for t in self.tasks if not t["completed"]]

        prompt_text = f"""Please provide a summary of the current tasks:

Total tasks: {len(self.tasks)}
Completed: {len(completed_tasks)}
Pending: {len(pending_tasks)}

Task details:
{json.dumps(self.tasks, indent=2)}

Please analyze the progress and suggest next steps."""

        print("  Generated prompt for AI:")
        print(f"  {prompt_text[:150]}...")
        print()

        # Prompt 2: Learning Plan
        print("🎓 Prompt: learning_plan")
        learning_prompt = """Create a personalized MCP learning plan:

Skill Level: beginner
Focus Area: tools

Available MCP capabilities in this environment:
- 5 different tools (tasks, calculator, weather, etc.)
- 3 resource types (database, files, system info)
- 3 prompt templates

Please suggest a step-by-step learning path."""

        print("  Generated learning prompt:")
        print(f"  {learning_prompt[:150]}...")
        print()

    def run_complete_demo(self):
        """Run the complete MCP demonstration"""
        print("🚀 WELCOME TO MCP LEARNING PLAYGROUND!")
        print("=" * 50)
        print("Model Context Protocol (MCP) enables AI assistants to:")
        print("• Call tools to perform actions")
        print("• Read resources to access data")
        print("• Use prompts for templated interactions")
        print()

        self.demonstrate_tools()
        self.demonstrate_resources()
        self.demonstrate_prompts()

        print("🎉 CONGRATULATIONS!")
        print("=" * 20)
        print("You've seen all three core MCP concepts in action:")
        print("✅ Tools - Functions that perform actions")
        print("✅ Resources - Data sources for reading")
        print("✅ Prompts - Templates for AI interactions")
        print()
        print("🎯 NEXT STEPS:")
        print("1. Explore the full MCP server in 'mcp_server.py'")
        print("2. Try running: uv run python mcp_server.py")
        print("3. Build your own tools and resources")
        print("4. Connect to real APIs and databases")
        print()
        print("📚 Your MCP playground is ready for experimentation!")


if __name__ == "__main__":
    demo = MCPDemo()
    demo.run_complete_demo()
