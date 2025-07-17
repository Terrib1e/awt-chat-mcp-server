import streamlit as st
import asyncio
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys
from pathlib import Path

# Import the wrapper functions
from streamlit_tools import (
    add, subtract, multiply, divide, power, square_root, logarithm, sin, cos, tan, convert_units,
    read_file, write_file, list_directory,
    fetch_webpage, search_web, download_file,
    analyze_csv, process_json, generate_report
)

# Configure the page
st.set_page_config(
    page_title="MCP Server Tools Dashboard",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .tool-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }

    .result-success {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }

    .result-error {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }

    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'execution_history' not in st.session_state:
    st.session_state.execution_history = []

def log_execution(tool_name, args, result, success=True):
    """Log tool execution to history"""
    st.session_state.execution_history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'tool': tool_name,
        'args': args,
        'result': result,
        'success': success
    })

def display_result(result, success=True):
    """Display result with appropriate styling"""
    if success:
        st.markdown(f"""
        <div class="result-success">
            <strong>✅ Success:</strong><br>
            {result}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-error">
            <strong>❌ Error:</strong><br>
            {result}
        </div>
        """, unsafe_allow_html=True)

# Main app header
st.markdown("""
<div class="main-header">
    <h1>🛠️ MCP Server Tools Dashboard</h1>
    <p>Interactive web interface for testing and using MCP server tools</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🧭 Navigation")
tool_category = st.sidebar.radio(
    "Select Tool Category:",
    ["🧮 Calculator", "📁 File Operations", "🌐 Web Tools", "📊 Data Analysis", "📈 Execution History"]
)

# Calculator Tools Section
if tool_category == "🧮 Calculator":
    st.header("🧮 Calculator Tools")

    # Basic arithmetic
    st.subheader("Basic Arithmetic")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.write("**Addition & Subtraction**")
        num1 = st.number_input("First number", value=0.0, key="basic_num1")
        num2 = st.number_input("Second number", value=0.0, key="basic_num2")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Add"):
                try:
                    result = add(num1, num2)
                    display_result(f"{num1} + {num2} = {result}")
                    log_execution("add", {"a": num1, "b": num2}, result)
                except Exception as e:
                    display_result(str(e), success=False)
                    log_execution("add", {"a": num1, "b": num2}, str(e), success=False)

        with col_b:
            if st.button("Subtract"):
                try:
                    result = subtract(num1, num2)
                    display_result(f"{num1} - {num2} = {result}")
                    log_execution("subtract", {"a": num1, "b": num2}, result)
                except Exception as e:
                    display_result(str(e), success=False)
                    log_execution("subtract", {"a": num1, "b": num2}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.write("**Multiplication & Division**")
        num3 = st.number_input("First number", value=1.0, key="mult_num1")
        num4 = st.number_input("Second number", value=1.0, key="mult_num2")

        col_c, col_d = st.columns(2)
        with col_c:
            if st.button("Multiply"):
                try:
                    result = multiply(num3, num4)
                    display_result(f"{num3} × {num4} = {result}")
                    log_execution("multiply", {"a": num3, "b": num4}, result)
                except Exception as e:
                    display_result(str(e), success=False)
                    log_execution("multiply", {"a": num3, "b": num4}, str(e), success=False)

        with col_d:
            if st.button("Divide"):
                try:
                    result = divide(num3, num4)
                    display_result(f"{num3} ÷ {num4} = {result}")
                    log_execution("divide", {"a": num3, "b": num4}, result)
                except Exception as e:
                    display_result(str(e), success=False)
                    log_execution("divide", {"a": num3, "b": num4}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

    # Advanced math
    st.subheader("Advanced Mathematics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.write("**Power & Root**")
        base = st.number_input("Base", value=2.0, key="power_base")
        exp = st.number_input("Exponent", value=2.0, key="power_exp")

        if st.button("Calculate Power"):
            try:
                result = power(base, exp)
                display_result(f"{base}^{exp} = {result}")
                log_execution("power", {"base": base, "exponent": exp}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("power", {"base": base, "exponent": exp}, str(e), success=False)

        sqrt_num = st.number_input("Square Root of", value=9.0, key="sqrt_num")
        if st.button("Calculate Square Root"):
            try:
                result = square_root(sqrt_num)
                display_result(f"√{sqrt_num} = {result}")
                log_execution("square_root", {"number": sqrt_num}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("square_root", {"number": sqrt_num}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.write("**Trigonometry**")
        angle = st.number_input("Angle (radians)", value=0.0, key="trig_angle")

        if st.button("Calculate Sin"):
            try:
                result = sin(angle)
                display_result(f"sin({angle}) = {result}")
                log_execution("sin", {"angle": angle}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("sin", {"angle": angle}, str(e), success=False)

        if st.button("Calculate Cos"):
            try:
                result = cos(angle)
                display_result(f"cos({angle}) = {result}")
                log_execution("cos", {"angle": angle}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("cos", {"angle": angle}, str(e), success=False)

        if st.button("Calculate Tan"):
            try:
                result = tan(angle)
                display_result(f"tan({angle}) = {result}")
                log_execution("tan", {"angle": angle}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("tan", {"angle": angle}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.write("**Unit Conversion**")
        value = st.number_input("Value", value=1.0, key="convert_value")
        from_unit = st.selectbox("From Unit", ["m", "km", "ft", "in", "kg", "lb", "celsius", "fahrenheit"], key="from_unit")
        to_unit = st.selectbox("To Unit", ["m", "km", "ft", "in", "kg", "lb", "celsius", "fahrenheit"], key="to_unit")

        if st.button("Convert Units"):
            try:
                result = convert_units(value, from_unit, to_unit)
                display_result(f"{value} {from_unit} = {result} {to_unit}")
                log_execution("convert_units", {"value": value, "from_unit": from_unit, "to_unit": to_unit}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("convert_units", {"value": value, "from_unit": from_unit, "to_unit": to_unit}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

# File Operations Section
elif tool_category == "📁 File Operations":
    st.header("📁 File Operations")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.subheader("📖 Read File")
        read_path = st.text_input("File path to read", value="data/sample_data.csv", key="read_path")

        if st.button("Read File"):
            try:
                result = asyncio.run(read_file(read_path))
                display_result(f"File contents:\n{result}")
                log_execution("read_file", {"file_path": read_path}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("read_file", {"file_path": read_path}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.subheader("📂 List Directory")
        dir_path = st.text_input("Directory path", value=".", key="dir_path")

        if st.button("List Directory"):
            try:
                result = asyncio.run(list_directory(dir_path))
                display_result(f"Directory contents:\n{result}")
                log_execution("list_directory", {"directory_path": dir_path}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("list_directory", {"directory_path": dir_path}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.subheader("✍️ Write File")
        write_path = st.text_input("File path to write", value="output.txt", key="write_path")
        content = st.text_area("Content to write", value="Hello from Streamlit!", key="write_content")

        if st.button("Write File"):
            try:
                result = asyncio.run(write_file(write_path, content))
                display_result(f"File written: {result}")
                log_execution("write_file", {"file_path": write_path, "content": content}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("write_file", {"file_path": write_path, "content": content}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

# Web Tools Section
elif tool_category == "🌐 Web Tools":
    st.header("🌐 Web Tools")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.subheader("🌍 Fetch Webpage")
        url = st.text_input("URL to fetch", value="https://httpbin.org/json", key="fetch_url")

        if st.button("Fetch Webpage"):
            try:
                result = asyncio.run(fetch_webpage(url))
                display_result(f"Webpage content:\n{result[:500]}...")
                log_execution("fetch_webpage", {"url": url}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("fetch_webpage", {"url": url}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.subheader("🔍 Search Web")
        query = st.text_input("Search query", value="MCP server", key="search_query")

        if st.button("Search Web"):
            try:
                result = asyncio.run(search_web(query))
                display_result(f"Search results:\n{result}")
                log_execution("search_web", {"query": query}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("search_web", {"query": query}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.subheader("⬇️ Download File")
        download_url = st.text_input("File URL to download", value="https://httpbin.org/json", key="download_url")
        save_path = st.text_input("Save as", value="downloaded_file.json", key="save_path")

        if st.button("Download File"):
            try:
                result = asyncio.run(download_file(download_url, save_path))
                display_result(f"Download result: {result}")
                log_execution("download_file", {"url": download_url, "save_path": save_path}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("download_file", {"url": download_url, "save_path": save_path}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

# Data Analysis Section
elif tool_category == "📊 Data Analysis":
    st.header("📊 Data Analysis Tools")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.subheader("📈 Analyze CSV")
        csv_path = st.text_input("CSV file path", value="data/sample_data.csv", key="csv_path")

        if st.button("Analyze CSV"):
            try:
                result = asyncio.run(analyze_csv(csv_path))
                display_result(f"CSV analysis:\n{result}")
                log_execution("analyze_csv", {"file_path": csv_path}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("analyze_csv", {"file_path": csv_path}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.subheader("🔧 Process JSON")
        json_path = st.text_input("JSON file path", value="data/sample_data.json", key="json_path")

        if st.button("Process JSON"):
            try:
                result = asyncio.run(process_json(json_path))
                display_result(f"JSON processing:\n{result}")
                log_execution("process_json", {"file_path": json_path}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("process_json", {"file_path": json_path}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tool-section">', unsafe_allow_html=True)
        st.subheader("📋 Generate Report")
        report_title = st.text_input("Report title", value="MCP Server Analysis", key="report_title")
        report_data = st.text_area("Report data (JSON format)", value='{"metric1": 100, "metric2": 200}', key="report_data")

        if st.button("Generate Report"):
            try:
                result = asyncio.run(generate_report(report_title, report_data))
                display_result(f"Report generated:\n{result}")
                log_execution("generate_report", {"title": report_title, "data": report_data}, result)
            except Exception as e:
                display_result(str(e), success=False)
                log_execution("generate_report", {"title": report_title, "data": report_data}, str(e), success=False)
        st.markdown('</div>', unsafe_allow_html=True)

# Execution History Section
elif tool_category == "📈 Execution History":
    st.header("📈 Execution History")

    if st.session_state.execution_history:
        # Statistics
        col1, col2, col3, col4 = st.columns(4)

        total_executions = len(st.session_state.execution_history)
        successful_executions = sum(1 for h in st.session_state.execution_history if h['success'])
        failed_executions = total_executions - successful_executions
        success_rate = (successful_executions / total_executions) * 100 if total_executions > 0 else 0

        with col1:
            st.metric("Total Executions", total_executions)
        with col2:
            st.metric("Successful", successful_executions)
        with col3:
            st.metric("Failed", failed_executions)
        with col4:
            st.metric("Success Rate", f"{success_rate:.1f}%")

        # Chart of tool usage
        tool_counts = {}
        for h in st.session_state.execution_history:
            tool_counts[h['tool']] = tool_counts.get(h['tool'], 0) + 1

        if tool_counts:
            fig = px.bar(
                x=list(tool_counts.keys()),
                y=list(tool_counts.values()),
                title="Tool Usage Distribution",
                labels={'x': 'Tool', 'y': 'Number of Executions'}
            )
            st.plotly_chart(fig, use_container_width=True)

        # Execution timeline
        df = pd.DataFrame(st.session_state.execution_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig_timeline = px.scatter(
            df,
            x='timestamp',
            y='tool',
            color='success',
            title='Execution Timeline',
            color_discrete_map={True: 'green', False: 'red'}
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Detailed history table
        st.subheader("Detailed Execution History")
        if st.button("Clear History"):
            st.session_state.execution_history = []
            st.rerun()

        for i, execution in enumerate(reversed(st.session_state.execution_history)):
            with st.expander(f"#{total_executions - i}: {execution['tool']} - {execution['timestamp']}"):
                st.write(f"**Tool:** {execution['tool']}")
                st.write(f"**Arguments:** {execution['args']}")
                st.write(f"**Success:** {'✅' if execution['success'] else '❌'}")
                st.write(f"**Result:**")
                st.code(str(execution['result']))
    else:
        st.info("No execution history yet. Try using some tools to see the history here!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🛠️ MCP Server Tools Dashboard | Built with Streamlit</p>
    <p>Use the sidebar to navigate between different tool categories</p>
</div>
""", unsafe_allow_html=True)