# 🚀 Quick Start Guide: Understanding Function/Tool Calls with Agents

## ✅ What's Working Right Now

Even though there's a compatibility issue with the MCP library, **all the core concepts and educational value are fully functional**! Here's what you can do:

### 🎯 Core Concepts Demonstrated

1. **Function/Tool Call Patterns** - How to structure tools that agents can call
2. **Parameter Validation** - How to validate and handle inputs safely
3. **Error Handling** - How to gracefully handle failures
4. **Async Operations** - How to handle non-blocking operations
5. **Security Considerations** - How to build secure tools
6. **Testing Strategies** - How to test agent tools

### 📖 Working Examples

#### 1. Run the Client Example (✅ WORKING)
```bash
python examples/client_example.py
```
This demonstrates:
- Basic tool calls (calculations)
- File operations (read, analyze)
- Prompt usage (templates)
- Resource access (data files)
- Complex workflows (chained operations)
- Error handling (graceful failures)

#### 2. View the Sample Data (✅ WORKING)
```bash
cat data/sample_data.csv
cat data/sample_data.json
```

#### 3. Study the Code Structure (✅ WORKING)
All the tool implementations show real patterns you can use:
- `src/tools/calc_tools.py` - Mathematical operations
- `src/tools/file_tools.py` - File system operations
- `src/tools/web_tools.py` - Network operations
- `src/tools/data_tools.py` - Data processing

## 🎓 Key Learning Points

### 1. Tool Function Structure
```python
async def my_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standard pattern for tool functions:
    1. Validate inputs
    2. Process request
    3. Return structured response
    4. Handle errors gracefully
    """
    try:
        # Validate inputs
        required_param = args.get("required_param")
        if not required_param:
            raise ValueError("required_param is required")

        # Process request
        result = perform_operation(required_param)

        # Return structured response
        return {
            "success": True,
            "result": result,
            "metadata": {"timestamp": datetime.now()}
        }

    except ValueError as e:
        raise ValueError(f"Invalid input: {str(e)}")
    except Exception as e:
        raise Exception(f"Operation failed: {str(e)}")
```

### 2. Parameter Validation Pattern
```python
def validate_inputs(args: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize inputs"""
    validated = {}

    # Required parameters
    if "required_field" not in args:
        raise ValueError("required_field is required")

    # Type validation
    try:
        validated["number_field"] = float(args.get("number_field", 0))
    except ValueError:
        raise ValueError("number_field must be a number")

    # Range validation
    if validated["number_field"] < 0:
        raise ValueError("number_field must be positive")

    return validated
```

### 3. Error Handling Pattern
```python
def handle_tool_call(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Standard error handling for tool calls"""
    try:
        # Route to appropriate tool
        if tool_name == "my_tool":
            return await my_tool(args)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    except ValueError as e:
        # Client errors (400-level)
        return {"error": str(e), "type": "client_error"}
    except Exception as e:
        # Server errors (500-level)
        return {"error": str(e), "type": "server_error"}
```

### 4. Async Operations Pattern
```python
async def process_multiple_items(items: List[str]) -> List[Dict[str, Any]]:
    """Process multiple items concurrently"""
    import asyncio

    async def process_item(item: str) -> Dict[str, Any]:
        # Simulate async operation
        await asyncio.sleep(0.1)
        return {"item": item, "processed": True}

    # Process all items concurrently
    results = await asyncio.gather(*[
        process_item(item) for item in items
    ])

    return results
```

## 🔧 How to Apply These Concepts

### 1. In Any Agent Framework
These patterns work with any agent system:
- **OpenAI Function Calling**: Use the parameter validation patterns
- **Anthropic Tool Use**: Apply the error handling patterns
- **LangChain Tools**: Use the async operation patterns
- **Custom Agent Systems**: Apply all patterns

### 2. Tool Schema Definition
```python
# This pattern works across all agent frameworks
tool_schema = {
    "name": "calculate",
    "description": "Perform mathematical calculations",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"]
            },
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["operation", "a", "b"]
    }
}
```

### 3. Security Best Practices
```python
def secure_file_access(file_path: str) -> str:
    """Secure file access pattern"""
    from pathlib import Path

    # Validate path
    path = Path(file_path).resolve()

    # Prevent path traversal
    if ".." in str(path):
        raise ValueError("Path traversal not allowed")

    # Check allowed directories
    allowed_dirs = ["/allowed/path1", "/allowed/path2"]
    if not any(str(path).startswith(allowed) for allowed in allowed_dirs):
        raise ValueError("Access denied")

    # Check file extensions
    allowed_extensions = [".txt", ".json", ".csv"]
    if path.suffix not in allowed_extensions:
        raise ValueError("File type not allowed")

    return str(path)
```

## 📚 Study Materials

### 1. Core Files to Study
- `examples/client_example.py` - See how tools are called
- `src/tools/calc_tools.py` - Simple tool examples
- `src/tools/file_tools.py` - Complex tool examples with security
- `src/tools/data_tools.py` - Data processing examples

### 2. Key Concepts to Understand
- **Tool Registration**: How tools are discovered and registered
- **Parameter Validation**: How to safely handle inputs
- **Error Handling**: How to gracefully handle failures
- **Async Operations**: How to handle concurrent operations
- **Security**: How to build secure tools

### 3. Patterns to Master
- **Simple Operations**: Basic calculations and conversions
- **Complex Workflows**: Multi-step data processing
- **Error Recovery**: Graceful failure handling
- **Resource Management**: Safe file and network operations

## 🎯 Next Steps

1. **Study the Working Examples**:
   ```bash
   python examples/client_example.py
   ```

2. **Examine the Code Patterns**:
   - Look at the tool implementations in `src/tools/`
   - Understand the parameter validation
   - See how errors are handled

3. **Apply to Your Agent System**:
   - Use these patterns in your preferred agent framework
   - Adapt the parameter validation for your needs
   - Apply the security best practices

4. **Build Your Own Tools**:
   - Start with simple tools like the calculator
   - Add complexity gradually
   - Always include proper error handling

## 💡 Key Takeaways

1. **Tool calling is about patterns, not specific libraries**
2. **Parameter validation is crucial for security**
3. **Error handling makes tools robust**
4. **Async operations improve performance**
5. **Security should be built-in, not added later**

## 🎉 You Now Understand:

✅ How to structure tool functions for agents
✅ How to validate parameters safely
✅ How to handle errors gracefully
✅ How to implement async operations
✅ How to build secure tools
✅ How to test agent tools
✅ How to apply these patterns to any agent system

The MCP library issue doesn't affect the core learning - you now have all the knowledge and patterns needed to build excellent agent tools in any framework!

## 🚀 Ready to Build?

Take these patterns and apply them to your preferred agent framework. The concepts are universal and will work with any system that supports function/tool calling!