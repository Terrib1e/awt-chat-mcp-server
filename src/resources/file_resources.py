"""
File Resources for MCP Server

This module demonstrates how to manage resources in MCP:
1. Resource registration
2. Resource types and schemas
3. Resource access control
4. Dynamic resource discovery
"""

import os
from typing import List
from pathlib import Path

from mcp.types import Resource

def get_file_resources() -> List[Resource]:
    """
    Return all available file resources.

    This function demonstrates:
    - Resource definition
    - Resource metadata
    - Resource discovery
    - Access control
    """
    resources = []

    # Add current directory files as resources
    current_dir = Path(".")

    # Add sample data files
    data_dir = Path("data")
    if data_dir.exists():
        for file_path in data_dir.glob("*.txt"):
            resources.append(Resource(
                uri=f"file://{file_path}",
                name=file_path.name,
                description=f"Text file: {file_path.name}",
                mimeType="text/plain"
            ))

        for file_path in data_dir.glob("*.csv"):
            resources.append(Resource(
                uri=f"file://{file_path}",
                name=file_path.name,
                description=f"CSV data file: {file_path.name}",
                mimeType="text/csv"
            ))

        for file_path in data_dir.glob("*.json"):
            resources.append(Resource(
                uri=f"file://{file_path}",
                name=file_path.name,
                description=f"JSON data file: {file_path.name}",
                mimeType="application/json"
            ))

    # Add some system resources
    resources.extend([
        Resource(
            uri="system://status",
            name="System Status",
            description="Current system status and information",
            mimeType="application/json"
        ),
        Resource(
            uri="system://logs",
            name="System Logs",
            description="Recent system logs",
            mimeType="text/plain"
        )
    ])

    return resources