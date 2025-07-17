"""
Calculator Tools for MCP Server

This module demonstrates basic function calls with mathematical operations.
It shows how to:
1. Define tool schemas with parameters
2. Handle different parameter types
3. Perform calculations and return results
4. Handle errors gracefully
"""

import math
from typing import Any, Dict, List, Union

from mcp.types import Tool

# Unit conversion constants
CONVERSION_FACTORS = {
    # Length
    "mm_to_cm": 0.1,
    "cm_to_m": 0.01,
    "m_to_km": 0.001,
    "in_to_ft": 1/12,
    "ft_to_yd": 1/3,
    "yd_to_mi": 1/1760,
    # Weight
    "g_to_kg": 0.001,
    "kg_to_lb": 2.20462,
    "lb_to_oz": 16,
    # Temperature (special handling)
    "celsius_to_fahrenheit": lambda c: (c * 9/5) + 32,
    "fahrenheit_to_celsius": lambda f: (f - 32) * 5/9,
    "celsius_to_kelvin": lambda c: c + 273.15,
    "kelvin_to_celsius": lambda k: k - 273.15,
}

async def calculate_basic(operation: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle basic arithmetic operations.

    This function demonstrates:
    - Parameter validation
    - Error handling
    - Different operation types
    - Result formatting
    """
    try:
        a = float(args.get("a", 0))
        b = float(args.get("b", 0))

        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("Cannot divide by zero")
            result = a / b
        else:
            raise ValueError(f"Unknown operation: {operation}")

        return {
            "operation": operation,
            "inputs": {"a": a, "b": b},
            "result": result,
            "formatted": f"{a} {operation} {b} = {result}"
        }

    except ValueError as e:
        raise ValueError(f"Invalid input: {str(e)}")
    except Exception as e:
        raise Exception(f"Calculation error: {str(e)}")

async def calculate_advanced(operation: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle advanced mathematical operations.

    This function demonstrates:
    - Single parameter functions
    - Mathematical library usage
    - Range validation
    - Scientific notation support
    """
    try:
        x = float(args.get("x", 0))

        if operation == "power":
            y = float(args.get("y", 2))
            result = pow(x, y)
        elif operation == "sqrt":
            if x < 0:
                raise ValueError("Cannot take square root of negative number")
            result = math.sqrt(x)
        elif operation == "log":
            if x <= 0:
                raise ValueError("Cannot take logarithm of non-positive number")
            base = args.get("base", math.e)
            result = math.log(x, base)
        elif operation == "sin":
            result = math.sin(math.radians(x))
        elif operation == "cos":
            result = math.cos(math.radians(x))
        elif operation == "tan":
            result = math.tan(math.radians(x))
        else:
            raise ValueError(f"Unknown operation: {operation}")

        return {
            "operation": operation,
            "input": x,
            "result": result,
            "formatted": f"{operation}({x}) = {result}"
        }

    except ValueError as e:
        raise ValueError(f"Invalid input: {str(e)}")
    except Exception as e:
        raise Exception(f"Calculation error: {str(e)}")

async def convert_units(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert between different units.

    This function demonstrates:
    - Complex parameter handling
    - Conditional logic
    - Custom conversion functions
    - Input validation
    """
    try:
        value = float(args.get("value", 0))
        from_unit = args.get("from_unit", "").lower()
        to_unit = args.get("to_unit", "").lower()

        conversion_key = f"{from_unit}_to_{to_unit}"

        if conversion_key in CONVERSION_FACTORS:
            factor = CONVERSION_FACTORS[conversion_key]
            if callable(factor):
                result = factor(value)
            else:
                result = value * factor
        else:
            # Try reverse conversion
            reverse_key = f"{to_unit}_to_{from_unit}"
            if reverse_key in CONVERSION_FACTORS:
                factor = CONVERSION_FACTORS[reverse_key]
                if callable(factor):
                    # Handle special cases for temperature
                    if "celsius" in reverse_key and "fahrenheit" in reverse_key:
                        result = (value - 32) * 5/9
                    elif "fahrenheit" in reverse_key and "celsius" in reverse_key:
                        result = (value * 9/5) + 32
                    else:
                        raise ValueError(f"Cannot reverse convert {from_unit} to {to_unit}")
                else:
                    result = value / factor
            else:
                raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported")

        return {
            "original_value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "converted_value": result,
            "formatted": f"{value} {from_unit} = {result} {to_unit}"
        }

    except ValueError as e:
        raise ValueError(f"Invalid input: {str(e)}")
    except Exception as e:
        raise Exception(f"Conversion error: {str(e)}")

def get_calculator_tools() -> List[Tool]:
    """
    Return all calculator tools with their schemas.

    This function demonstrates:
    - Tool schema definition
    - Parameter specification
    - Documentation
    - Tool organization
    """
    return [
        # Basic arithmetic tools
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
        ),
        Tool(
            name="subtract",
            description="Subtract second number from first number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="divide",
            description="Divide first number by second number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Dividend"},
                    "b": {"type": "number", "description": "Divisor (cannot be zero)"}
                },
                "required": ["a", "b"]
            }
        ),

        # Advanced mathematical tools
        Tool(
            name="power",
            description="Raise number to a power",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Base number"},
                    "y": {"type": "number", "description": "Exponent (default: 2)", "default": 2}
                },
                "required": ["x"]
            }
        ),
        Tool(
            name="sqrt",
            description="Calculate square root of a number",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Number to find square root of (must be non-negative)"}
                },
                "required": ["x"]
            }
        ),
        Tool(
            name="log",
            description="Calculate logarithm of a number",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Number to find logarithm of (must be positive)"},
                    "base": {"type": "number", "description": "Base of logarithm (default: e)", "default": math.e}
                },
                "required": ["x"]
            }
        ),
        Tool(
            name="sin",
            description="Calculate sine of angle (in degrees)",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Angle in degrees"}
                },
                "required": ["x"]
            }
        ),
        Tool(
            name="cos",
            description="Calculate cosine of angle (in degrees)",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Angle in degrees"}
                },
                "required": ["x"]
            }
        ),
        Tool(
            name="tan",
            description="Calculate tangent of angle (in degrees)",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Angle in degrees"}
                },
                "required": ["x"]
            }
        ),

        # Unit conversion tool
        Tool(
            name="convert_units",
            description="Convert between different units of measurement",
            inputSchema={
                "type": "object",
                "properties": {
                    "value": {"type": "number", "description": "Value to convert"},
                    "from_unit": {"type": "string", "description": "Source unit"},
                    "to_unit": {"type": "string", "description": "Target unit"}
                },
                "required": ["value", "from_unit", "to_unit"]
            }
        )
    ]