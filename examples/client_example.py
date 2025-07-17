#!/usr/bin/env python3
"""
MCP Client Example

This script demonstrates how to interact with the MCP server and call tools.
It shows various patterns for using function/tool calls with agents.
"""

import asyncio
import json
from pathlib import Path

# This would normally be imported from the MCP client library
# For demonstration purposes, we'll simulate the interactions

class MockMCPClient:
    """Mock MCP client for demonstration purposes."""

    def __init__(self):
        self.tools = {}
        self.resources = {}
        self.prompts = {}

    async def list_tools(self):
        """List available tools."""
        print("📋 Available Tools:")
        print("=" * 50)

        # Simulate tool listing
        tools = [
            {"name": "add", "description": "Add two numbers together"},
            {"name": "multiply", "description": "Multiply two numbers"},
            {"name": "read_file", "description": "Read content from a text file"},
            {"name": "write_file", "description": "Write content to a text file"},
            {"name": "fetch_webpage", "description": "Fetch and parse a webpage"},
            {"name": "analyze_csv", "description": "Analyze a CSV file and return statistics"},
            {"name": "process_json", "description": "Process and analyze a JSON file"},
        ]

        for tool in tools:
            print(f"  • {tool['name']}: {tool['description']}")

        return tools

    async def call_tool(self, tool_name, arguments):
        """Call a tool with arguments."""
        print(f"\n🔧 Calling tool: {tool_name}")
        print(f"   Arguments: {arguments}")
        print("   Result:", end=" ")

        # Simulate tool calls
        if tool_name == "add":
            result = arguments.get("a", 0) + arguments.get("b", 0)
            print(f"{result}")
            return {"result": result}

        elif tool_name == "multiply":
            result = arguments.get("a", 1) * arguments.get("b", 1)
            print(f"{result}")
            return {"result": result}

        elif tool_name == "read_file":
            file_path = arguments.get("file_path", "")
            if Path(file_path).exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                print(f"Read {len(content)} characters from {file_path}")
                return {"content": content, "length": len(content)}
            else:
                print(f"File not found: {file_path}")
                return {"error": "File not found"}

        elif tool_name == "analyze_csv":
            file_path = arguments.get("file_path", "")
            if Path(file_path).exists():
                print(f"Analyzing CSV file: {file_path}")
                # Simulate CSV analysis
                return {
                    "total_rows": 10,
                    "total_columns": 5,
                    "column_names": ["name", "age", "city", "salary", "department"],
                    "sample_analysis": "Data contains employee information"
                }
            else:
                print(f"File not found: {file_path}")
                return {"error": "File not found"}

        else:
            print(f"Tool '{tool_name}' not implemented in mock client")
            return {"error": "Tool not implemented"}

    async def list_resources(self):
        """List available resources."""
        print("\n📁 Available Resources:")
        print("=" * 50)

        resources = [
            {"uri": "file://data/sample_data.csv", "name": "Sample CSV Data"},
            {"uri": "file://data/sample_data.json", "name": "Sample JSON Data"},
            {"uri": "system://status", "name": "System Status"},
        ]

        for resource in resources:
            print(f"  • {resource['name']}: {resource['uri']}")

        return resources

    async def get_prompt(self, prompt_name, arguments=None):
        """Get a prompt with arguments."""
        print(f"\n💬 Using prompt: {prompt_name}")
        if arguments:
            print(f"   Arguments: {arguments}")

        # Simulate prompt retrieval
        prompts = {
            "analyze_data": "Analyze the provided {data_type} data with focus on {analysis_focus}",
            "code_review": "Review this {language} code for {review_type} issues",
            "system_troubleshooting": "Help troubleshoot {system_type} issues: {error_symptoms}"
        }

        template = prompts.get(prompt_name, "Unknown prompt")
        if arguments:
            for key, value in arguments.items():
                template = template.replace(f"{{{key}}}", str(value))

        print(f"   Template: {template}")
        return {"template": template}

async def demonstrate_basic_calculations():
    """Demonstrate basic calculator functions."""
    print("\n🧮 BASIC CALCULATIONS")
    print("=" * 50)

    client = MockMCPClient()

    # Addition
    await client.call_tool("add", {"a": 15, "b": 25})

    # Multiplication
    await client.call_tool("multiply", {"a": 7, "b": 8})

    # Chain calculations
    result1 = await client.call_tool("add", {"a": 10, "b": 5})
    result2 = await client.call_tool("multiply", {"a": result1.get("result", 0), "b": 2})

    print(f"   Chained result: (10 + 5) * 2 = {result2.get('result', 'Error')}")

async def demonstrate_file_operations():
    """Demonstrate file operations."""
    print("\n📂 FILE OPERATIONS")
    print("=" * 50)

    client = MockMCPClient()

    # Read existing file
    await client.call_tool("read_file", {"file_path": "data/sample_data.csv"})

    # Analyze CSV
    await client.call_tool("analyze_csv", {"file_path": "data/sample_data.csv"})

async def demonstrate_prompts():
    """Demonstrate prompt usage."""
    print("\n💬 PROMPT USAGE")
    print("=" * 50)

    client = MockMCPClient()

    # Data analysis prompt
    await client.get_prompt("analyze_data", {
        "data_type": "CSV",
        "analysis_focus": "salary trends"
    })

    # Code review prompt
    await client.get_prompt("code_review", {
        "language": "Python",
        "review_type": "security"
    })

async def demonstrate_resource_access():
    """Demonstrate resource access."""
    print("\n📁 RESOURCE ACCESS")
    print("=" * 50)

    client = MockMCPClient()

    # List resources
    await client.list_resources()

async def demonstrate_complex_workflow():
    """Demonstrate a complex workflow combining multiple tools."""
    print("\n🔄 COMPLEX WORKFLOW")
    print("=" * 50)

    client = MockMCPClient()

    print("Workflow: Analyze data → Generate insights → Create report")
    print("-" * 50)

    # Step 1: Analyze data
    print("Step 1: Analyzing CSV data...")
    analysis = await client.call_tool("analyze_csv", {"file_path": "data/sample_data.csv"})

    # Step 2: Use analysis results in prompt
    print("\nStep 2: Generating insights...")
    insights = await client.get_prompt("analyze_data", {
        "data_type": "employee data",
        "analysis_focus": "department distribution and salary analysis"
    })

    # Step 3: Create report (simulated)
    print("\nStep 3: Creating report...")
    print("   Report generated with insights and recommendations")

async def demonstrate_error_handling():
    """Demonstrate error handling."""
    print("\n⚠️  ERROR HANDLING")
    print("=" * 50)

    client = MockMCPClient()

    # Try to read non-existent file
    await client.call_tool("read_file", {"file_path": "nonexistent.txt"})

    # Try to call non-existent tool
    await client.call_tool("nonexistent_tool", {})

async def main():
    """Main demonstration function."""
    print("🚀 MCP Server Client Example")
    print("=" * 50)
    print("This example demonstrates various MCP server interactions:")
    print("• Basic tool calls (calculations)")
    print("• File operations (read, analyze)")
    print("• Prompt usage (templates)")
    print("• Resource access (data files)")
    print("• Complex workflows (chained operations)")
    print("• Error handling (graceful failures)")

    # Run demonstrations
    await demonstrate_basic_calculations()
    await demonstrate_file_operations()
    await demonstrate_prompts()
    await demonstrate_resource_access()
    await demonstrate_complex_workflow()
    await demonstrate_error_handling()

    print("\n✅ All demonstrations completed!")
    print("\nTo run the actual MCP server:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run server: python src/server.py")
    print("3. Connect your MCP client to the server")

if __name__ == "__main__":
    asyncio.run(main())