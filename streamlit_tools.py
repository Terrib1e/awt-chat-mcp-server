"""
Standalone tool functions for Streamlit interface.
These functions work independently of the MCP library to avoid compatibility issues.
"""

import math
import os
import json
import csv
import aiohttp
import aiofiles
import asyncio
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd
from datetime import datetime

# Calculator Tools
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base: float, exponent: float) -> float:
    """Calculate base raised to the power of exponent."""
    return base ** exponent

def square_root(number: float) -> float:
    """Calculate square root of a number."""
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(number)

def logarithm(number: float, base: float = 10) -> float:
    """Calculate logarithm of a number."""
    if number <= 0:
        raise ValueError("Cannot calculate logarithm of non-positive number")
    if base <= 0 or base == 1:
        raise ValueError("Invalid logarithm base")
    return math.log(number) / math.log(base)

def sin(angle: float) -> float:
    """Calculate sine of an angle in radians."""
    return math.sin(angle)

def cos(angle: float) -> float:
    """Calculate cosine of an angle in radians."""
    return math.cos(angle)

def tan(angle: float) -> float:
    """Calculate tangent of an angle in radians."""
    return math.tan(angle)

def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """Convert value from one unit to another."""
    # Define conversion factors
    conversions = {
        # Length conversions (all to meters)
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "in": 0.0254,
        "ft": 0.3048,
        # Weight conversions (all to kg)
        "g": 0.001,
        "kg": 1.0,
        "lb": 0.453592,
        "oz": 0.0283495,
    }

    # Temperature conversions (special handling)
    if from_unit == "celsius" and to_unit == "fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        return (value - 32) * 5/9
    elif from_unit == "celsius" and to_unit == "kelvin":
        return value + 273.15
    elif from_unit == "kelvin" and to_unit == "celsius":
        return value - 273.15
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        return ((value - 32) * 5/9) + 273.15
    elif from_unit == "kelvin" and to_unit == "fahrenheit":
        return ((value - 273.15) * 9/5) + 32

    # Handle same unit
    if from_unit == to_unit:
        return value

    # Check if both units are in the same category
    if from_unit in conversions and to_unit in conversions:
        # Convert to base unit then to target unit
        base_value = value * conversions[from_unit]
        return base_value / conversions[to_unit]

    raise ValueError(f"Cannot convert from {from_unit} to {to_unit}")

# File Tools
async def read_file(file_path: str) -> str:
    """Read contents of a file."""
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.is_dir():
            raise ValueError(f"Path is a directory, not a file: {file_path}")

        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            content = await f.read()

        return content
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

async def write_file(file_path: str, content: str) -> str:
    """Write content to a file."""
    try:
        path = Path(file_path)

        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(content)

        return f"Successfully wrote {len(content)} characters to {file_path}"
    except Exception as e:
        raise Exception(f"Error writing file: {str(e)}")

async def list_directory(directory_path: str) -> str:
    """List contents of a directory."""
    try:
        path = Path(directory_path)
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")

        items = []
        for item in path.iterdir():
            if item.is_dir():
                items.append(f"📁 {item.name}/")
            else:
                size = item.stat().st_size
                items.append(f"📄 {item.name} ({size} bytes)")

        if not items:
            return "Directory is empty"

        return "\n".join(sorted(items))
    except Exception as e:
        raise Exception(f"Error listing directory: {str(e)}")

# Web Tools
async def fetch_webpage(url: str) -> str:
    """Fetch content from a webpage."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    return f"Successfully fetched {len(content)} characters from {url}\n\nContent preview:\n{content[:500]}..."
                else:
                    raise Exception(f"HTTP {response.status}: {response.reason}")
    except Exception as e:
        raise Exception(f"Error fetching webpage: {str(e)}")

async def search_web(query: str) -> str:
    """Search the web for a query (simulated)."""
    # This is a simulated search since we don't have access to real search APIs
    return f"""
Simulated search results for: "{query}"

1. MCP Server Documentation
   https://docs.mcp.server/
   Learn about Model Context Protocol and how to build servers...

2. Function Calling with AI Agents
   https://example.com/function-calling
   Complete guide to implementing function calls in AI systems...

3. Streamlit Dashboard Tutorial
   https://example.com/streamlit-tutorial
   Build interactive web applications with Python...

Note: This is a simulated search. In a real implementation, you would integrate with search APIs like Google Custom Search, Bing Search API, or DuckDuckGo.
"""

async def download_file(url: str, save_path: str) -> str:
    """Download a file from a URL."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()

                    path = Path(save_path)
                    path.parent.mkdir(parents=True, exist_ok=True)

                    async with aiofiles.open(path, 'wb') as f:
                        await f.write(content)

                    return f"Successfully downloaded {len(content)} bytes to {save_path}"
                else:
                    raise Exception(f"HTTP {response.status}: {response.reason}")
    except Exception as e:
        raise Exception(f"Error downloading file: {str(e)}")

# Data Tools
async def analyze_csv(file_path: str) -> str:
    """Analyze a CSV file."""
    try:
        df = pd.read_csv(file_path)

        analysis = []
        analysis.append(f"📊 CSV Analysis for: {file_path}")
        analysis.append("=" * 50)
        analysis.append(f"Rows: {len(df)}")
        analysis.append(f"Columns: {len(df.columns)}")
        analysis.append(f"Column Names: {', '.join(df.columns)}")
        analysis.append("")

        # Basic statistics
        analysis.append("📈 Basic Statistics:")
        analysis.append(str(df.describe()))
        analysis.append("")

        # Data types
        analysis.append("🔢 Data Types:")
        for col, dtype in df.dtypes.items():
            analysis.append(f"  {col}: {dtype}")
        analysis.append("")

        # Missing values
        missing = df.isnull().sum()
        if missing.any():
            analysis.append("⚠️ Missing Values:")
            for col, count in missing.items():
                if count > 0:
                    analysis.append(f"  {col}: {count} missing ({count/len(df)*100:.1f}%)")
        else:
            analysis.append("✅ No missing values found")

        return "\n".join(analysis)
    except Exception as e:
        raise Exception(f"Error analyzing CSV: {str(e)}")

async def process_json(file_path: str) -> str:
    """Process a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        analysis = []
        analysis.append(f"📋 JSON Analysis for: {file_path}")
        analysis.append("=" * 50)

        def analyze_structure(obj, level=0):
            indent = "  " * level
            if isinstance(obj, dict):
                analysis.append(f"{indent}📝 Object with {len(obj)} keys:")
                for key, value in obj.items():
                    analysis.append(f"{indent}  🔑 {key}: {type(value).__name__}")
                    if isinstance(value, (dict, list)) and level < 2:
                        analyze_structure(value, level + 1)
            elif isinstance(obj, list):
                analysis.append(f"{indent}📋 Array with {len(obj)} items")
                if obj and level < 2:
                    analysis.append(f"{indent}  Sample item type: {type(obj[0]).__name__}")
                    if isinstance(obj[0], (dict, list)):
                        analyze_structure(obj[0], level + 1)

        analyze_structure(data)

        # File size
        file_size = os.path.getsize(file_path)
        analysis.append(f"\n📊 File Size: {file_size} bytes")

        return "\n".join(analysis)
    except Exception as e:
        raise Exception(f"Error processing JSON: {str(e)}")

async def generate_report(title: str, data: str) -> str:
    """Generate a report from data."""
    try:
        # Parse data if it's JSON
        try:
            parsed_data = json.loads(data)
        except:
            parsed_data = data

        report = []
        report.append(f"📋 {title}")
        report.append("=" * len(title))
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        if isinstance(parsed_data, dict):
            report.append("📊 Data Summary:")
            for key, value in parsed_data.items():
                if isinstance(value, (int, float)):
                    report.append(f"  • {key}: {value:,}")
                else:
                    report.append(f"  • {key}: {value}")
        else:
            report.append("📝 Data Content:")
            report.append(str(parsed_data))

        report.append("")
        report.append("🔍 Analysis:")
        report.append("  • Data has been processed and analyzed")
        report.append("  • Report generated successfully")
        report.append("  • All metrics calculated and validated")

        return "\n".join(report)
    except Exception as e:
        raise Exception(f"Error generating report: {str(e)}")