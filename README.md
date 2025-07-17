# MCP Server Learning Project

This project demonstrates how to create function/tool calls that AI agents can use, focusing on the **Model Context Protocol (MCP)** but with **universal patterns** that work with any agent framework.

## 🚀 Quick Start (Recommended)

### Option 1: Web Interface (NEW!)
```bash
# Install dependencies
pip install -r requirements.txt

# Launch the web interface
python run_streamlit.py

# Access in browser: http://localhost:8501
```

### Option 2: Command Line
**👉 [See QUICK_START.md](QUICK_START.md) for immediate, working examples!**

The core educational value of this project is **fully functional** and ready to use. Even though there's a compatibility issue with the MCP library, all the fundamental concepts and patterns are demonstrated with working examples.

## ✅ What's Working Right Now

### 1. Web Interface (Streamlit)
- **Interactive Dashboard**: Point-and-click interface for all tools
- **Real-time Results**: Instant feedback and execution history
- **Visual Analytics**: Charts and graphs for tool usage
- **Sample Data**: Pre-loaded files for testing data analysis

### 2. Command Line Examples
```bash
# Run the comprehensive client example
python examples/client_example.py
```

### 2. Study Real Implementation Patterns
- **Calculator Tools**: Parameter validation, error handling, type conversion
- **File Operations**: Security validation, async operations, metadata extraction
- **Web Tools**: HTTP requests, rate limiting, HTML parsing
- **Data Processing**: CSV analysis, JSON processing, report generation

### 3. Core Learning Materials
- `QUICK_START.md` - Immediate practical guide
- `TUTORIAL.md` - Comprehensive learning resource
- `PROJECT_SUMMARY.md` - Detailed project explanation

## 🎯 What You'll Learn

### Universal Patterns for Agent Tools
1. **Function/Tool Call Structure** - How to build tools agents can call
2. **Parameter Validation** - Safe input handling and validation
3. **Error Handling** - Graceful failure management
4. **Async Operations** - Non-blocking operations for performance
5. **Security Best Practices** - Input validation, path traversal prevention
6. **Testing Strategies** - Unit and integration testing for agent tools

### Framework Compatibility
These patterns work with **any agent framework**:
- ✅ OpenAI Function Calling
- ✅ Anthropic Tool Use
- ✅ LangChain Tools
- ✅ Custom Agent Systems
- ✅ Any MCP-compatible system

## 📋 Project Structure

```
chat-mcp-server/
├── 📄 QUICK_START.md           # 👈 START HERE!
├── 📄 TUTORIAL.md              # Comprehensive learning guide
├── 📄 PROJECT_SUMMARY.md       # Detailed project explanation
├── 📄 README.md                # This file
├── 📁 examples/                # Working examples
│   └── 📄 client_example.py    # Interactive demonstrations
├── 📁 src/tools/               # Tool implementation patterns
│   ├── 📄 calc_tools.py        # Mathematical operations
│   ├── 📄 file_tools.py        # File system operations
│   ├── 📄 web_tools.py         # Network operations
│   └── 📄 data_tools.py        # Data processing
├── 📁 data/                    # Sample data for testing
│   ├── 📄 sample_data.csv      # Sample CSV data
│   └── 📄 sample_data.json     # Sample JSON data
└── 📁 tests/                   # Test examples
    └── 📄 test_tools.py        # Testing patterns
```

## 🛠️ Tools Demonstrated

### 1. Calculator Tools
- **Basic Operations**: add, subtract, multiply, divide
- **Advanced Math**: power, sqrt, log, trigonometry
- **Unit Conversion**: length, weight, temperature
- **Features**: Parameter validation, error handling, type safety

### 2. File System Tools
- **File Operations**: read, write, list directories
- **Security**: Path validation, extension checking, access control
- **Features**: Async operations, atomic writes, metadata extraction

### 3. Web Tools
- **HTTP Operations**: webpage fetching, HTML parsing
- **API Integration**: search functionality, file downloading
- **Features**: Rate limiting, content validation, error handling

### 4. Data Processing Tools
- **Analysis**: CSV statistics, JSON processing
- **Reporting**: Multi-format report generation
- **Features**: Data validation, statistical analysis, insights generation

## 📚 Learning Resources

### 1. Quick Start
- **[QUICK_START.md](QUICK_START.md)** - Immediate practical guide with working examples

### 2. Comprehensive Tutorial
- **[TUTORIAL.md](TUTORIAL.md)** - Complete learning guide with step-by-step instructions

### 3. Project Summary
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Detailed explanation of everything built

### 4. Code Examples
- **examples/client_example.py** - Interactive demonstrations
- **src/tools/** - Real implementation patterns

## 🎓 Key Learning Outcomes

By studying this project, you'll understand:

1. **Tool Architecture** - How to structure tools for agents
2. **Parameter Handling** - Safe validation and processing
3. **Error Management** - Robust error handling patterns
4. **Security** - Input validation and access control
5. **Performance** - Async operations and optimization
6. **Testing** - Comprehensive testing strategies
7. **Universal Patterns** - Concepts that work across frameworks

## 🚀 Getting Started

### Option 1: Quick Start (Recommended)
```bash
# 1. Read the quick start guide
# 👉 Open QUICK_START.md

# 2. Run the working example
python examples/client_example.py

# 3. Study the implementation patterns
# 👉 Look at src/tools/*.py files
```

### Option 2: Full Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run examples
python examples/client_example.py

# 3. Study the comprehensive tutorial
# 👉 Open TUTORIAL.md
```

## 💡 Key Insight

**The most important learning is about patterns, not specific libraries.** This project teaches you the fundamental concepts of building agent tools that will work with any framework or system that supports function/tool calling.

## 🎯 Next Steps

1. **Start with QUICK_START.md** - Get immediate value
2. **Run the examples** - See the patterns in action
3. **Study the code** - Understand the implementation details
4. **Apply to your system** - Use these patterns in your preferred framework
5. **Build your own tools** - Create custom functionality

## 🤝 Contributing

Feel free to contribute by:
- Adding new tool patterns
- Improving documentation
- Sharing use cases
- Fixing issues
- Adding framework-specific examples

## 📝 Status Note

While there's currently a compatibility issue with the MCP library dependencies, **this doesn't affect the educational value**. The core concepts, patterns, and examples are all functional and demonstrate everything you need to know about building agent tools.

The patterns shown here are universal and will work with any agent framework that supports function/tool calling.

---

**🎉 Ready to build amazing agent tools? Start with [QUICK_START.md](QUICK_START.md)!**