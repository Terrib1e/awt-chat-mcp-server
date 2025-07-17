"""
Data Processing Tools for MCP Server

This module demonstrates data processing and analysis capabilities:
1. CSV and JSON file processing
2. Data analysis and statistics
3. Report generation
4. Data validation
5. Format conversion
"""

import json
import csv
import statistics
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime
import pandas as pd
from io import StringIO

from mcp.types import Tool

async def analyze_csv(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a CSV file and return statistics.

    This function demonstrates:
    - CSV file processing
    - Data type detection
    - Statistical analysis
    - Missing value handling
    - Data validation
    """
    try:
        file_path = args.get("file_path", "")
        delimiter = args.get("delimiter", ",")
        max_rows = args.get("max_rows", 1000)

        if not file_path:
            raise ValueError("file_path is required")

        path = Path(file_path)
        if not path.exists():
            raise ValueError(f"File not found: {file_path}")

        # Read CSV file
        try:
            df = pd.read_csv(path, delimiter=delimiter, nrows=max_rows)
        except Exception as e:
            raise ValueError(f"Error reading CSV: {str(e)}")

        # Basic information
        total_rows, total_columns = df.shape
        column_names = df.columns.tolist()

        # Data types
        data_types = {}
        for col in df.columns:
            data_types[col] = str(df[col].dtype)

        # Missing values
        missing_values = {}
        for col in df.columns:
            missing_count = df[col].isna().sum()
            missing_values[col] = {
                "count": int(missing_count),
                "percentage": float(missing_count / total_rows * 100)
            }

        # Statistical analysis for numeric columns
        numeric_stats = {}
        for col in df.select_dtypes(include=['number']).columns:
            series = df[col].dropna()
            if len(series) > 0:
                numeric_stats[col] = {
                    "mean": float(series.mean()),
                    "median": float(series.median()),
                    "std": float(series.std()),
                    "min": float(series.min()),
                    "max": float(series.max()),
                    "q25": float(series.quantile(0.25)),
                    "q75": float(series.quantile(0.75)),
                    "unique_count": int(series.nunique())
                }

        # Categorical analysis
        categorical_stats = {}
        for col in df.select_dtypes(include=['object']).columns:
            series = df[col].dropna()
            if len(series) > 0:
                value_counts = series.value_counts().head(10)
                categorical_stats[col] = {
                    "unique_count": int(series.nunique()),
                    "most_common": value_counts.to_dict(),
                    "sample_values": series.head(5).tolist()
                }

        # Sample data
        sample_data = df.head(5).to_dict('records')

        return {
            "file_path": str(path),
            "total_rows": total_rows,
            "total_columns": total_columns,
            "column_names": column_names,
            "data_types": data_types,
            "missing_values": missing_values,
            "numeric_statistics": numeric_stats,
            "categorical_statistics": categorical_stats,
            "sample_data": sample_data,
            "analysis_timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise Exception(f"CSV analysis failed: {str(e)}")

async def process_json(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process and analyze a JSON file.

    This function demonstrates:
    - JSON parsing and validation
    - Structure analysis
    - Data extraction
    - Schema inference
    - Nested data handling
    """
    try:
        file_path = args.get("file_path", "")
        operation = args.get("operation", "analyze")  # analyze, extract, transform
        json_path = args.get("json_path", "")  # JSONPath-like syntax

        if not file_path:
            raise ValueError("file_path is required")

        path = Path(file_path)
        if not path.exists():
            raise ValueError(f"File not found: {file_path}")

        # Read and parse JSON
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")

        def _analyze_structure(obj, path="root"):
            """Recursively analyze JSON structure."""
            if isinstance(obj, dict):
                return {
                    "type": "object",
                    "path": path,
                    "keys": list(obj.keys()),
                    "key_count": len(obj),
                    "children": {k: _analyze_structure(v, f"{path}.{k}") for k, v in obj.items()}
                }
            elif isinstance(obj, list):
                return {
                    "type": "array",
                    "path": path,
                    "length": len(obj),
                    "element_types": list(set(type(item).__name__ for item in obj)),
                    "sample_element": _analyze_structure(obj[0], f"{path}[0]") if obj else None
                }
            else:
                return {
                    "type": type(obj).__name__,
                    "path": path,
                    "value": obj if not isinstance(obj, str) or len(str(obj)) < 100 else str(obj)[:100] + "..."
                }

        def _extract_by_path(obj, path_parts):
            """Extract data by path."""
            if not path_parts:
                return obj

            current = path_parts[0]
            remaining = path_parts[1:]

            if isinstance(obj, dict):
                if current in obj:
                    return _extract_by_path(obj[current], remaining)
                else:
                    raise KeyError(f"Key '{current}' not found")
            elif isinstance(obj, list):
                try:
                    index = int(current)
                    if 0 <= index < len(obj):
                        return _extract_by_path(obj[index], remaining)
                    else:
                        raise IndexError(f"Index {index} out of range")
                except ValueError:
                    raise ValueError(f"Invalid array index: {current}")
            else:
                raise TypeError(f"Cannot access '{current}' on {type(obj).__name__}")

        result = {
            "file_path": str(path),
            "operation": operation,
            "file_size": path.stat().st_size,
            "processing_timestamp": datetime.now().isoformat()
        }

        if operation == "analyze":
            result.update({
                "structure": _analyze_structure(data),
                "root_type": type(data).__name__,
                "is_valid": True
            })

        elif operation == "extract" and json_path:
            path_parts = json_path.split('.')
            extracted = _extract_by_path(data, path_parts)
            result.update({
                "json_path": json_path,
                "extracted_data": extracted,
                "extracted_type": type(extracted).__name__
            })

        elif operation == "transform":
            # Simple transformation examples
            if isinstance(data, list):
                result.update({
                    "original_length": len(data),
                    "transformed_data": data[:10],  # First 10 items
                    "transformation": "truncate_to_10"
                })
            elif isinstance(data, dict):
                result.update({
                    "original_keys": list(data.keys()),
                    "transformed_data": {k: v for k, v in data.items() if not k.startswith('_')},
                    "transformation": "remove_private_keys"
                })

        return result

    except Exception as e:
        raise Exception(f"JSON processing failed: {str(e)}")

async def generate_report(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a data report from analysis results.

    This function demonstrates:
    - Report generation
    - Data visualization (text-based)
    - Summary statistics
    - Insight generation
    - Format conversion
    """
    try:
        data = args.get("data", {})
        report_type = args.get("report_type", "summary")  # summary, detailed, insights
        format_type = args.get("format", "json")  # json, markdown, csv

        if not data:
            raise ValueError("data is required")

        def _generate_summary_report(data):
            """Generate a summary report."""
            summary = {
                "report_type": "summary",
                "generated_at": datetime.now().isoformat(),
                "overview": {},
                "key_findings": [],
                "recommendations": []
            }

            # Basic overview
            if "total_rows" in data:
                summary["overview"]["total_records"] = data["total_rows"]
            if "total_columns" in data:
                summary["overview"]["total_fields"] = data["total_columns"]

            # Key findings
            if "missing_values" in data:
                high_missing = {k: v for k, v in data["missing_values"].items()
                              if v["percentage"] > 20}
                if high_missing:
                    summary["key_findings"].append({
                        "type": "data_quality",
                        "finding": "High missing values detected",
                        "details": high_missing
                    })

            if "numeric_statistics" in data:
                for col, stats in data["numeric_statistics"].items():
                    if stats["std"] > stats["mean"]:
                        summary["key_findings"].append({
                            "type": "statistical",
                            "finding": f"High variability in {col}",
                            "details": {
                                "mean": stats["mean"],
                                "std": stats["std"],
                                "coefficient_of_variation": stats["std"] / stats["mean"]
                            }
                        })

            # Recommendations
            if "missing_values" in data:
                high_missing_fields = [k for k, v in data["missing_values"].items()
                                     if v["percentage"] > 10]
                if high_missing_fields:
                    summary["recommendations"].append({
                        "type": "data_cleaning",
                        "action": "Address missing values",
                        "affected_fields": high_missing_fields
                    })

            return summary

        def _generate_detailed_report(data):
            """Generate a detailed report."""
            return {
                "report_type": "detailed",
                "generated_at": datetime.now().isoformat(),
                "full_analysis": data,
                "data_quality_score": _calculate_quality_score(data),
                "field_analysis": _analyze_fields(data)
            }

        def _generate_insights_report(data):
            """Generate insights report."""
            insights = {
                "report_type": "insights",
                "generated_at": datetime.now().isoformat(),
                "insights": []
            }

            # Generate insights based on data patterns
            if "numeric_statistics" in data:
                for col, stats in data["numeric_statistics"].items():
                    insights["insights"].append({
                        "field": col,
                        "insight": f"Values range from {stats['min']:.2f} to {stats['max']:.2f}",
                        "type": "range_analysis"
                    })

            if "categorical_statistics" in data:
                for col, stats in data["categorical_statistics"].items():
                    insights["insights"].append({
                        "field": col,
                        "insight": f"Contains {stats['unique_count']} unique values",
                        "type": "uniqueness_analysis"
                    })

            return insights

        def _calculate_quality_score(data):
            """Calculate data quality score."""
            if "missing_values" not in data:
                return 100

            total_missing = sum(v["percentage"] for v in data["missing_values"].values())
            avg_missing = total_missing / len(data["missing_values"])
            quality_score = max(0, 100 - avg_missing)
            return round(quality_score, 2)

        def _analyze_fields(data):
            """Analyze individual fields."""
            field_analysis = {}

            if "missing_values" in data:
                for field, missing_info in data["missing_values"].items():
                    field_analysis[field] = {
                        "completeness": 100 - missing_info["percentage"],
                        "missing_count": missing_info["count"]
                    }

            return field_analysis

        def _format_as_markdown(report_data):
            """Convert report to markdown format."""
            md_lines = [
                f"# Data Report - {report_data.get('report_type', 'Unknown').title()}",
                f"Generated at: {report_data.get('generated_at', 'Unknown')}",
                ""
            ]

            if "overview" in report_data:
                md_lines.extend([
                    "## Overview",
                    f"- Total Records: {report_data['overview'].get('total_records', 'N/A')}",
                    f"- Total Fields: {report_data['overview'].get('total_fields', 'N/A')}",
                    ""
                ])

            if "key_findings" in report_data:
                md_lines.extend(["## Key Findings", ""])
                for finding in report_data["key_findings"]:
                    md_lines.append(f"- **{finding['type']}**: {finding['finding']}")
                md_lines.append("")

            return "\n".join(md_lines)

        # Generate report based on type
        if report_type == "summary":
            report_data = _generate_summary_report(data)
        elif report_type == "detailed":
            report_data = _generate_detailed_report(data)
        elif report_type == "insights":
            report_data = _generate_insights_report(data)
        else:
            raise ValueError(f"Unknown report type: {report_type}")

        # Format output
        if format_type == "markdown":
            formatted_output = _format_as_markdown(report_data)
        elif format_type == "json":
            formatted_output = json.dumps(report_data, indent=2)
        else:
            formatted_output = str(report_data)

        return {
            "report_type": report_type,
            "format": format_type,
            "report_data": report_data,
            "formatted_output": formatted_output,
            "generation_timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise Exception(f"Report generation failed: {str(e)}")

def get_data_tools() -> List[Tool]:
    """
    Return all data processing tools with their schemas.

    This function demonstrates:
    - Data tool schemas
    - Complex parameter handling
    - Validation rules
    - Processing options
    """
    return [
        Tool(
            name="analyze_csv",
            description="Analyze a CSV file and return statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the CSV file to analyze"
                    },
                    "delimiter": {
                        "type": "string",
                        "description": "CSV delimiter character",
                        "default": ","
                    },
                    "max_rows": {
                        "type": "integer",
                        "description": "Maximum number of rows to analyze",
                        "default": 1000,
                        "minimum": 1,
                        "maximum": 10000
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="process_json",
            description="Process and analyze a JSON file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the JSON file to process"
                    },
                    "operation": {
                        "type": "string",
                        "description": "Operation to perform",
                        "enum": ["analyze", "extract", "transform"],
                        "default": "analyze"
                    },
                    "json_path": {
                        "type": "string",
                        "description": "JSONPath for extraction (e.g., 'users.0.name')"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="generate_report",
            description="Generate a data report from analysis results",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "Data to generate report from"
                    },
                    "report_type": {
                        "type": "string",
                        "description": "Type of report to generate",
                        "enum": ["summary", "detailed", "insights"],
                        "default": "summary"
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format",
                        "enum": ["json", "markdown", "text"],
                        "default": "json"
                    }
                },
                "required": ["data"]
            }
        )
    ]