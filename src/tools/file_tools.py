"""
File System Tools for MCP Server

This module demonstrates file system operations and how to handle:
1. File reading and writing
2. Directory listing
3. Path validation
4. Error handling for file operations
5. Security considerations
"""

import os
import json
import mimetypes
from pathlib import Path
from typing import Any, Dict, List, Union
import aiofiles

from mcp.types import Tool

# Security: Define allowed file operations
ALLOWED_EXTENSIONS = {'.txt', '.md', '.json', '.csv', '.log', '.py', '.js', '.html', '.css'}
RESTRICTED_PATHS = {'/etc', '/usr', '/bin', '/sbin', '/var', '/root', '/home'}

def _validate_path(file_path: str) -> Path:
    """
    Validate file path for security.

    This function demonstrates:
    - Path validation
    - Security checks
    - Path normalization
    - Error handling
    """
    try:
        path = Path(file_path).resolve()

        # Security: Check if path is within allowed directories
        for restricted in RESTRICTED_PATHS:
            if str(path).startswith(restricted):
                raise ValueError(f"Access to {restricted} is restricted")

        # Security: Check for path traversal attempts
        if '..' in str(path):
            raise ValueError("Path traversal not allowed")

        return path

    except Exception as e:
        raise ValueError(f"Invalid path: {str(e)}")

def _check_file_extension(file_path: Path) -> bool:
    """Check if file extension is allowed."""
    return file_path.suffix.lower() in ALLOWED_EXTENSIONS

async def read_file_content(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read content from a file.

    This function demonstrates:
    - Async file operations
    - Error handling
    - File type detection
    - Content validation
    """
    try:
        file_path = args.get("file_path", "")
        if not file_path:
            raise ValueError("file_path is required")

        path = _validate_path(file_path)

        if not path.exists():
            raise ValueError(f"File not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        if not _check_file_extension(path):
            raise ValueError(f"File extension not allowed: {path.suffix}")

        # Read file content
        async with aiofiles.open(path, 'r', encoding='utf-8') as file:
            content = await file.read()

        # Get file metadata
        stat = path.stat()
        mime_type, _ = mimetypes.guess_type(str(path))

        return {
            "file_path": str(path),
            "content": content,
            "size": stat.st_size,
            "mime_type": mime_type,
            "last_modified": stat.st_mtime,
            "lines": len(content.splitlines()),
            "characters": len(content)
        }

    except Exception as e:
        raise Exception(f"Failed to read file: {str(e)}")

async def write_file_content(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Write content to a file.

    This function demonstrates:
    - File creation
    - Content validation
    - Backup creation
    - Atomic writes
    """
    try:
        file_path = args.get("file_path", "")
        content = args.get("content", "")
        create_backup = args.get("create_backup", False)

        if not file_path:
            raise ValueError("file_path is required")

        path = _validate_path(file_path)

        if not _check_file_extension(path):
            raise ValueError(f"File extension not allowed: {path.suffix}")

        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        # Create backup if requested and file exists
        backup_path = None
        if create_backup and path.exists():
            backup_path = path.with_suffix(f"{path.suffix}.backup")
            async with aiofiles.open(path, 'r', encoding='utf-8') as src:
                backup_content = await src.read()
            async with aiofiles.open(backup_path, 'w', encoding='utf-8') as dst:
                await dst.write(backup_content)

        # Write content atomically
        temp_path = path.with_suffix(f"{path.suffix}.tmp")
        async with aiofiles.open(temp_path, 'w', encoding='utf-8') as file:
            await file.write(content)

        # Atomic move
        temp_path.replace(path)

        # Get file metadata
        stat = path.stat()

        return {
            "file_path": str(path),
            "size": stat.st_size,
            "lines": len(content.splitlines()),
            "characters": len(content),
            "backup_created": backup_path is not None,
            "backup_path": str(backup_path) if backup_path else None,
            "success": True
        }

    except Exception as e:
        raise Exception(f"Failed to write file: {str(e)}")

async def list_directory(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    List directory contents.

    This function demonstrates:
    - Directory traversal
    - File filtering
    - Metadata collection
    - Recursive listing
    """
    try:
        dir_path = args.get("directory_path", ".")
        recursive = args.get("recursive", False)
        include_hidden = args.get("include_hidden", False)
        file_filter = args.get("file_filter", "")

        path = _validate_path(dir_path)

        if not path.exists():
            raise ValueError(f"Directory not found: {dir_path}")

        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {dir_path}")

        files = []
        directories = []

        def _should_include(item_path: Path) -> bool:
            """Check if item should be included based on filters."""
            if not include_hidden and item_path.name.startswith('.'):
                return False
            if file_filter and file_filter not in item_path.name:
                return False
            return True

        def _collect_items(current_path: Path, level: int = 0) -> None:
            """Recursively collect directory items."""
            try:
                for item in current_path.iterdir():
                    if not _should_include(item):
                        continue

                    stat = item.stat()
                    mime_type, _ = mimetypes.guess_type(str(item))

                    item_info = {
                        "name": item.name,
                        "path": str(item),
                        "size": stat.st_size,
                        "last_modified": stat.st_mtime,
                        "level": level,
                        "mime_type": mime_type
                    }

                    if item.is_file():
                        item_info["type"] = "file"
                        files.append(item_info)
                    elif item.is_dir():
                        item_info["type"] = "directory"
                        directories.append(item_info)

                        if recursive:
                            _collect_items(item, level + 1)

            except PermissionError:
                pass  # Skip directories we can't read

        _collect_items(path)

        return {
            "directory_path": str(path),
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories),
            "recursive": recursive,
            "include_hidden": include_hidden
        }

    except Exception as e:
        raise Exception(f"Failed to list directory: {str(e)}")

def get_file_tools() -> List[Tool]:
    """
    Return all file system tools with their schemas.

    This function demonstrates:
    - Complex tool schemas
    - Optional parameters
    - Parameter validation
    - Security considerations
    """
    return [
        Tool(
            name="read_file",
            description="Read content from a text file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="write_file",
            description="Write content to a text file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    },
                    "create_backup": {
                        "type": "boolean",
                        "description": "Create backup of existing file",
                        "default": False
                    }
                },
                "required": ["file_path", "content"]
            }
        ),
        Tool(
            name="list_directory",
            description="List contents of a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "Path to the directory to list",
                        "default": "."
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "List subdirectories recursively",
                        "default": False
                    },
                    "include_hidden": {
                        "type": "boolean",
                        "description": "Include hidden files and directories",
                        "default": False
                    },
                    "file_filter": {
                        "type": "string",
                        "description": "Filter files by name substring",
                        "default": ""
                    }
                },
                "required": []
            }
        )
    ]