# 🌐 Streamlit Web Frontend Guide

## 🚀 Getting Started

### 1. Launch the App
```bash
# Option 1: Using the run script
python run_streamlit.py

# Option 2: Direct command
streamlit run streamlit_app.py --server.port 8501
```

### 2. Access the Web Interface
- **URL**: http://localhost:8501
- **Browser**: The app should automatically open in your default browser
- **Port**: 8501 (default Streamlit port)

## 🛠️ Available Tool Categories

### 🧮 Calculator Tools
Interactive calculators with real-time results:
- **Basic Arithmetic**: Addition, subtraction, multiplication, division
- **Advanced Math**: Power, square root, logarithms
- **Trigonometry**: Sin, cos, tan functions
- **Unit Conversion**: Length, weight, temperature conversions

### 📁 File Operations
File system interactions:
- **Read File**: View contents of any file
- **Write File**: Create or modify files
- **List Directory**: Browse folder contents

### 🌐 Web Tools
Internet and web-related operations:
- **Fetch Webpage**: Download and display web page content
- **Search Web**: Perform web searches (simulated)
- **Download File**: Save files from URLs

### 📊 Data Analysis
Data processing and analysis tools:
- **Analyze CSV**: Process and analyze CSV files
- **Process JSON**: Parse and manipulate JSON data
- **Generate Report**: Create formatted reports

### 📈 Execution History
Track and visualize your tool usage:
- **Statistics Dashboard**: Success rates, total executions
- **Usage Charts**: Visual representation of tool usage
- **Timeline View**: See when tools were executed
- **Detailed History**: Full log of all executions

## 🎯 Key Features

### Interactive Interface
- **Point & Click**: No command line required
- **Real-time Results**: Instant feedback for all operations
- **Error Handling**: Clear error messages and success indicators
- **Form Validation**: Input validation before execution

### Visual Feedback
- **Color-coded Results**: Green for success, red for errors
- **Progress Tracking**: Visual indicators for operations
- **Charts & Graphs**: Data visualization with Plotly
- **Responsive Design**: Works on desktop and mobile

### Data Management
- **Sample Data**: Pre-loaded CSV and JSON files for testing
- **File Upload**: Support for various file formats
- **Export Options**: Save results and reports
- **History Tracking**: Complete audit trail of all operations

## 📝 Usage Examples

### Example 1: Basic Calculator
1. Go to "🧮 Calculator" section
2. Enter numbers in the input fields
3. Click "Add", "Subtract", "Multiply", or "Divide"
4. See instant results with success indicators

### Example 2: File Analysis
1. Go to "📊 Data Analysis" section
2. Use the default path: `data/sample_data.csv`
3. Click "Analyze CSV"
4. View detailed analysis results

### Example 3: Web Operations
1. Go to "🌐 Web Tools" section
2. Enter a URL like `https://httpbin.org/json`
3. Click "Fetch Webpage"
4. View the downloaded content

## 🔧 Troubleshooting

### Common Issues

**App Won't Start**
```bash
# Check if dependencies are installed
pip install streamlit plotly pandas

# Try running directly
streamlit run streamlit_app.py
```

**Tools Not Working**
- Check that all dependencies are installed
- Verify file paths exist (especially for data files)
- Look at error messages in the red error boxes

**Port Already in Use**
```bash
# Use a different port
streamlit run streamlit_app.py --server.port 8502
```

### Performance Tips
- Use the execution history to track performance
- Clear history periodically for better performance
- File operations work best with small to medium files

## 🚀 Next Steps

1. **Test All Categories**: Try each tool category to see all features
2. **Check History**: Use the execution history to track your usage
3. **Experiment**: Try different inputs and see how tools respond
4. **Explore Data**: Use the sample data files to test analysis tools

## 📊 Sample Data Files

The app includes sample data for testing:
- `data/sample_data.csv`: Employee data with salary, department info
- `data/sample_data.json`: Company data with nested structures

## 🎨 Interface Overview

- **Sidebar Navigation**: Switch between tool categories
- **Main Content Area**: Interactive forms and results
- **Execution History**: Track all your tool usage
- **Visual Indicators**: Success/error feedback with colors

---

**🎉 Enjoy exploring your MCP server tools through the web interface!**