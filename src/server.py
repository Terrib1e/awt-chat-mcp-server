#!/usr/bin/env python3
"""
Main MCP Server Implementation

This file demonstrates how to create an MCP server with various types of function/tool calls.
It serves as the central hub that registers and manages all tools, resources, and prompts.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Sequence
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    GetPromptRequest,
    GetPromptResult,
    ListPromptsRequest,
    ListPromptsResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    TextContent,
    Tool,
    EmbeddedResource,
)

# Import our tool modules
from tools.calc_tools import (
    calculate_basic,
    calculate_advanced,
    convert_units,
    get_calculator_tools,
)
from tools.file_tools import (
    read_file_content,
    write_file_content,
    list_directory,
    get_file_tools,
)
from tools.web_tools import (
    fetch_webpage,
    search_web,
    download_file,
    get_web_tools,
)
from tools.data_tools import (
    analyze_csv,
    process_json,
    generate_report,
    get_data_tools,
)
from resources.file_resources import get_file_resources
from prompts.analysis_prompts import get_analysis_prompts

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPServer:
    """
    Main MCP Server class that manages all tools, resources, and prompts.

    This class demonstrates:
    1. How to register different types of tools
    2. How to handle tool calls with various parameter types
    3. How to manage resources and prompts
    4. How to implement proper error handling
    """

    def __init__(self):
        self.server = Server("chat-mcp-server")
        self.tools: Dict[str, Tool] = {}
        self.resources: Dict[str, Resource] = {}
        self.prompts: Dict[str, Prompt] = {}

        # Register all tools, resources, and prompts
        self._register_tools()
        self._register_resources()
        self._register_prompts()

        # Set up server handlers
        self._setup_handlers()

        logger.info("MCP Server initialized with %d tools, %d resources, %d prompts",
                   len(self.tools), len(self.resources), len(self.prompts))

    def _register_tools(self) -> None:
        """Register all available tools with the server."""
        # Calculator tools - demonstrate simple function calls
        for tool in get_calculator_tools():
            self.tools[tool.name] = tool

        # File tools - demonstrate file system operations
        for tool in get_file_tools():
            self.tools[tool.name] = tool

        # Web tools - demonstrate network operations
        for tool in get_web_tools():
            self.tools[tool.name] = tool

        # Data tools - demonstrate data processing
        for tool in get_data_tools():
            self.tools[tool.name] = tool

        logger.info("Registered %d tools", len(self.tools))

    def _register_resources(self) -> None:
        """Register all available resources with the server."""
        for resource in get_file_resources():
            self.resources[resource.uri] = resource

        logger.info("Registered %d resources", len(self.resources))

    def _register_prompts(self) -> None:
        """Register all available prompts with the server."""
        for prompt in get_analysis_prompts():
            self.prompts[prompt.name] = prompt

        logger.info("Registered %d prompts", len(self.prompts))

    def _setup_handlers(self) -> None:
        """Set up all the server request handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """Return all available tools."""
            return ListToolsResult(tools=list(self.tools.values()))

        @self.server.call_tool()
        async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
            """Handle tool calls - this is where the magic happens!"""
            tool_name = request.params.name
            arguments = request.params.arguments or {}

            logger.info(f"Calling tool: {tool_name} with args: {arguments}")

            try:
                # Route to appropriate tool handler
                if tool_name in ["add", "subtract", "multiply", "divide"]:
                    result = await calculate_basic(tool_name, arguments)
                elif tool_name in ["power", "sqrt", "log", "sin", "cos", "tan"]:
                    result = await calculate_advanced(tool_name, arguments)
                elif tool_name == "convert_units":
                    result = await convert_units(arguments)
                elif tool_name == "read_file":
                    result = await read_file_content(arguments)
                elif tool_name == "write_file":
                    result = await write_file_content(arguments)
                elif tool_name == "list_directory":
                    result = await list_directory(arguments)
                elif tool_name == "fetch_webpage":
                    result = await fetch_webpage(arguments)
                elif tool_name == "search_web":
                    result = await search_web(arguments)
                elif tool_name == "download_file":
                    result = await download_file(arguments)
                elif tool_name == "analyze_csv":
                    result = await analyze_csv(arguments)
                elif tool_name == "process_json":
                    result = await process_json(arguments)
                elif tool_name == "generate_report":
                    result = await generate_report(arguments)
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")

                return CallToolResult(
                    content=[TextContent(type="text", text=str(result))]
                )

            except Exception as e:
                logger.error(f"Error calling tool {tool_name}: {str(e)}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")]
                )

        @self.server.list_resources()
        async def handle_list_resources() -> ListResourcesResult:
            """Return all available resources."""
            return ListResourcesResult(resources=list(self.resources.values()))

        @self.server.read_resource()
        async def handle_read_resource(request: ReadResourceRequest) -> ReadResourceResult:
            """Handle resource reading."""
            uri = request.params.uri

            if uri not in self.resources:
                raise ValueError(f"Resource not found: {uri}")

            # This is a simplified example - in practice, you'd implement
            # proper resource reading based on the resource type
            try:
                if uri.startswith("file://"):
                    file_path = uri[7:]  # Remove "file://" prefix
                    with open(file_path, 'r') as f:
                        content = f.read()
                    return ReadResourceResult(
                        contents=[TextContent(type="text", text=content)]
                    )
                else:
                    raise ValueError(f"Unsupported resource type: {uri}")

            except Exception as e:
                logger.error(f"Error reading resource {uri}: {str(e)}")
                raise

        @self.server.list_prompts()
        async def handle_list_prompts() -> ListPromptsResult:
            """Return all available prompts."""
            return ListPromptsResult(prompts=list(self.prompts.values()))

        @self.server.get_prompt()
        async def handle_get_prompt(request: GetPromptRequest) -> GetPromptResult:
            """Handle prompt retrieval with argument substitution."""
            prompt_name = request.params.name
            arguments = request.params.arguments or {}

            if prompt_name not in self.prompts:
                raise ValueError(f"Prompt not found: {prompt_name}")

            prompt = self.prompts[prompt_name]

            # Simple template substitution
            description = prompt.description
            if description:
                for key, value in arguments.items():
                    description = description.replace(f"{{{key}}}", str(value))

            return GetPromptResult(
                description=description,
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=description or "")
                    )
                ]
            )

async def main():
    """Main server entry point."""
    logger.info("Starting MCP Server...")

    # Create server instance
    mcp_server = MCPServer()

    # Set up server options
    options = InitializationOptions(
        server_name="chat-mcp-server",
        server_version="1.0.0",
        capabilities={
            "tools": {},
            "resources": {},
            "prompts": {}
        }
    )

    # Run the server
    async with stdio_server(mcp_server.server, options) as (read_stream, write_stream):
        await mcp_server.server.run(
            read_stream,
            write_stream,
            options
        )

if __name__ == "__main__":
    asyncio.run(main())