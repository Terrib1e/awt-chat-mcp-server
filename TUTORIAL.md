# MCP Server Tutorial: Learning Function/Tool Calls with Agents

This tutorial will teach you everything you need to know about creating MCP servers and implementing function/tool calls that agents can use.

## 📋 Table of Contents

1. [What is MCP?](#what-is-mcp)
2. [Project Structure](#project-structure)
3. [Basic Concepts](#basic-concepts)
4. [Getting Started](#getting-started)
5. [Creating Your First Tool](#creating-your-first-tool)
6. [Advanced Tool Examples](#advanced-tool-examples)
7. [Resources and Prompts](#resources-and-prompts)
8. [Testing Your Tools](#testing-your-tools)
9. [Best Practices](#best-practices)
10. [Common Patterns](#common-patterns)
11. [Troubleshooting](#troubleshooting)

## What is MCP?

**MCP (Model Context Protocol)** is a standardized protocol that enables AI agents to interact with external tools, resources, and services. Think of it as a bridge between AI models and the real world.

### Key Benefits:
- **Standardized Interface**: Consistent way for agents to call functions
- **Type Safety**: Strong typing with JSON schemas
- **Extensibility**: Easy to add new tools and capabilities
- **Security**: Built-in validation and error handling
- **Async Support**: Non-blocking operations for better performance

### MCP Components:
1. **Tools**: Functions that agents can call
2. **Resources**: Data sources agents can access
3. **Prompts**: Reusable templates for AI interactions

## Project Structure

```
chat-mcp-server/
├── src/
│   ├── server.py          # Main server implementation
│   ├── tools/             # Tool implementations
│   │   ├── calc_tools.py  # Calculator functions
│   │   ├── file_tools.py  # File system operations
│   │   ├── web_tools.py   # Web scraping/API calls
│   │   └── data_tools.py  # Data processing
│   ├── resources/         # Resource handlers
│   └── prompts/           # Prompt templates
├── tests/                 # Test files
├── examples/              # Usage examples
├── data/                  # Sample data
└── requirements.txt       # Dependencies
```

## Basic Concepts

### 1. Tool Definition

A tool is defined with:
- **Name**: Unique identifier
- **Description**: What the tool does
- **Input Schema**: Parameter specification
- **Handler Function**: The actual implementation

```python
Tool(
    name="add",
    description="Add two numbers together",
    inputSchema={
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "required": ["a", "b"]
    }
)
```

### 2. Tool Handler

The handler function processes the tool call:

```python
async def calculate_basic(operation: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if operation == "add":
        result = args["a"] + args["b"]
        return {"result": result, "operation": "add"}
```

### 3. Error Handling

Always include proper error handling:

```python
try:
    result = perform_operation(args)
    return {"success": True, "result": result}
except ValueError as e:
    raise ValueError(f"Invalid input: {str(e)}")
except Exception as e:
    raise Exception(f"Operation failed: {str(e)}")
```

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Example

```bash
python examples/client_example.py
```

### 3. Test the Tools

```bash
python tests/test_tools.py manual
```

## Creating Your First Tool

Let's create a simple "hello world" tool:

### Step 1: Define the Tool Schema

```python
from mcp.types import Tool

def get_hello_tools():
    return [
        Tool(
            name="say_hello",
            description="Generate a personalized greeting",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Person's name"},
                    "language": {"type": "string", "description": "Language for greeting", "default": "en"}
                },
                "required": ["name"]
            }
        )
    ]
```

### Step 2: Implement the Handler

```python
async def say_hello(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args.get("name", "World")
    language = args.get("language", "en")

    greetings = {
        "en": f"Hello, {name}!",
        "es": f"¡Hola, {name}!",
        "fr": f"Bonjour, {name}!",
        "de": f"Hallo, {name}!"
    }

    greeting = greetings.get(language, greetings["en"])

    return {
        "greeting": greeting,
        "name": name,
        "language": language
    }
```

### Step 3: Register the Tool

Add to your server's `_register_tools()` method:

```python
def _register_tools(self):
    for tool in get_hello_tools():
        self.tools[tool.name] = tool
```

### Step 4: Add to Handler

In your server's `handle_call_tool()` method:

```python
if tool_name == "say_hello":
    result = await say_hello(arguments)
```

## Advanced Tool Examples

### 1. Calculator Tools

**Features Demonstrated:**
- Parameter validation
- Error handling
- Multiple operations
- Type conversion

```python
# Basic arithmetic
await calculate_basic("add", {"a": 5, "b": 3})
# Result: {"result": 8, "operation": "add"}

# Advanced math
await calculate_advanced("sqrt", {"x": 16})
# Result: {"result": 4, "operation": "sqrt"}

# Unit conversion
await convert_units({"value": 100, "from_unit": "cm", "to_unit": "m"})
# Result: {"converted_value": 1.0, "from_unit": "cm", "to_unit": "m"}
```

### 2. File Operations

**Features Demonstrated:**
- Async file handling
- Security validation
- Metadata extraction
- Atomic operations

```python
# Read file
await read_file_content({"file_path": "data/sample.txt"})

# Write file with backup
await write_file_content({
    "file_path": "output.txt",
    "content": "Hello, World!",
    "create_backup": True
})

# List directory
await list_directory({
    "directory_path": "data/",
    "recursive": True,
    "include_hidden": False
})
```

### 3. Web Operations

**Features Demonstrated:**
- HTTP requests
- HTML parsing
- Rate limiting
- Security controls

```python
# Fetch webpage
await fetch_webpage({
    "url": "https://example.com",
    "extract_links": True,
    "include_html": False
})

# Search web
await search_web({
    "query": "python programming",
    "max_results": 10
})
```

### 4. Data Processing

**Features Demonstrated:**
- CSV analysis
- JSON processing
- Statistical calculations
- Report generation

```python
# Analyze CSV
await analyze_csv({
    "file_path": "data/sample_data.csv",
    "max_rows": 1000
})

# Process JSON
await process_json({
    "file_path": "data/sample_data.json",
    "operation": "extract",
    "json_path": "users.0.name"
})

# Generate report
await generate_report({
    "data": analysis_results,
    "report_type": "summary",
    "format": "markdown"
})
```

## Resources and Prompts

### Resources

Resources provide read-only access to data:

```python
Resource(
    uri="file://data/sample_data.csv",
    name="Sample CSV Data",
    description="Employee data for analysis",
    mimeType="text/csv"
)
```

### Prompts

Prompts are reusable templates:

```python
Prompt(
    name="analyze_data",
    description="Analyze {data_type} data focusing on {focus_area}",
    arguments=[
        PromptArgument(
            name="data_type",
            description="Type of data to analyze",
            required=True
        ),
        PromptArgument(
            name="focus_area",
            description="What to focus on in the analysis",
            required=True
        )
    ]
)
```

## Testing Your Tools

### 1. Unit Tests

```python
@pytest.mark.asyncio
async def test_calculator_addition():
    result = await calculate_basic("add", {"a": 5, "b": 3})
    assert result["result"] == 8
    assert result["operation"] == "add"
```

### 2. Integration Tests

```python
@pytest.mark.asyncio
async def test_workflow():
    # Step 1: Analyze data
    analysis = await analyze_csv({"file_path": "test_data.csv"})

    # Step 2: Generate report
    report = await generate_report({"data": analysis})

    # Verify workflow
    assert report["report_type"] == "summary"
```

### 3. Manual Testing

```bash
python tests/test_tools.py manual
```

## Best Practices

### 1. Input Validation

Always validate inputs:

```python
def validate_file_path(file_path: str) -> Path:
    if not file_path:
        raise ValueError("file_path is required")

    path = Path(file_path).resolve()

    # Security checks
    if '..' in str(path):
        raise ValueError("Path traversal not allowed")

    return path
```

### 2. Error Handling

Use specific error types:

```python
try:
    result = risky_operation()
except ValueError as e:
    raise ValueError(f"Invalid input: {str(e)}")
except FileNotFoundError:
    raise Exception("File not found")
except Exception as e:
    raise Exception(f"Unexpected error: {str(e)}")
```

### 3. Type Safety

Use type hints:

```python
from typing import Dict, Any, List

async def process_data(args: Dict[str, Any]) -> Dict[str, Any]:
    file_path: str = args.get("file_path", "")
    options: Dict[str, Any] = args.get("options", {})

    # Implementation
    return {"success": True}
```

### 4. Documentation

Document your tools:

```python
async def complex_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Complex tool that demonstrates multiple concepts.

    Args:
        args: Dictionary containing:
            - param1 (str): Description of param1
            - param2 (int): Description of param2
            - options (dict): Optional parameters

    Returns:
        Dictionary containing:
            - result: The computed result
            - metadata: Additional information

    Raises:
        ValueError: If parameters are invalid
        Exception: If operation fails
    """
```

## Common Patterns

### 1. Chained Operations

```python
# Step 1: Get data
data = await read_file_content({"file_path": "data.csv"})

# Step 2: Process data
analysis = await analyze_csv({"file_path": "data.csv"})

# Step 3: Generate report
report = await generate_report({"data": analysis})
```

### 2. Conditional Logic

```python
async def smart_processor(args: Dict[str, Any]) -> Dict[str, Any]:
    file_path = args["file_path"]

    if file_path.endswith('.csv'):
        return await analyze_csv(args)
    elif file_path.endswith('.json'):
        return await process_json(args)
    else:
        raise ValueError("Unsupported file type")
```

### 3. Batch Operations

```python
async def process_multiple_files(args: Dict[str, Any]) -> Dict[str, Any]:
    file_paths = args["file_paths"]
    results = []

    for file_path in file_paths:
        try:
            result = await process_file({"file_path": file_path})
            results.append({"file": file_path, "result": result})
        except Exception as e:
            results.append({"file": file_path, "error": str(e)})

    return {"results": results}
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Solution: Install dependencies
   pip install -r requirements.txt
   ```

2. **Module Not Found**
   ```python
   # Solution: Add to Python path
   import sys
   sys.path.insert(0, 'src')
   ```

3. **Async Issues**
   ```python
   # Solution: Use proper async/await
   result = await async_function()  # ✅ Correct
   result = async_function()        # ❌ Wrong
   ```

4. **Schema Validation**
   ```python
   # Solution: Match schema exactly
   {
       "type": "object",
       "properties": {
           "param": {"type": "string"}  # Must match expected type
       },
       "required": ["param"]
   }
   ```

### Debugging Tips

1. **Add Logging**
   ```python
   import logging
   logger = logging.getLogger(__name__)

   logger.info(f"Processing: {args}")
   logger.error(f"Error: {str(e)}")
   ```

2. **Validate Inputs**
   ```python
   print(f"Received args: {args}")
   print(f"Processing tool: {tool_name}")
   ```

3. **Use Try/Except**
   ```python
   try:
       result = risky_operation()
   except Exception as e:
       print(f"Debug: {str(e)}")
       raise
   ```

## Next Steps

1. **Extend the Examples**: Add your own tools
2. **Create Complex Workflows**: Chain multiple tools together
3. **Add Real APIs**: Integrate with external services
4. **Implement Caching**: Add performance optimizations
5. **Add Authentication**: Secure your tools
6. **Deploy to Production**: Set up proper hosting

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Python Async Guide](https://docs.python.org/3/library/asyncio.html)
- [JSON Schema](https://json-schema.org/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

## Contributing

Feel free to contribute to this project by:
1. Adding new tools
2. Improving documentation
3. Fixing bugs
4. Adding tests
5. Sharing use cases

Happy coding! 🚀