"""
Analysis Prompts for MCP Server

This module demonstrates prompt templates for MCP:
1. Parameterized prompts
2. Context-aware templates
3. Prompt composition
4. Reusable prompt patterns
"""

from typing import List

from mcp.types import Prompt, PromptArgument

def get_analysis_prompts() -> List[Prompt]:
    """
    Return all available analysis prompts.

    This function demonstrates:
    - Prompt definition
    - Parameter specification
    - Template patterns
    - Reusable components
    """
    return [
        Prompt(
            name="analyze_data",
            description="Analyze data and provide insights on {data_type} with focus on {analysis_focus}",
            arguments=[
                PromptArgument(
                    name="data_type",
                    description="Type of data to analyze (e.g., CSV, JSON, numerical)",
                    required=True
                ),
                PromptArgument(
                    name="analysis_focus",
                    description="Focus area for analysis (e.g., trends, anomalies, patterns)",
                    required=True
                ),
                PromptArgument(
                    name="context",
                    description="Additional context about the data",
                    required=False
                )
            ]
        ),

        Prompt(
            name="code_review",
            description="Review {language} code for {review_type} and provide suggestions",
            arguments=[
                PromptArgument(
                    name="language",
                    description="Programming language (e.g., Python, JavaScript, Java)",
                    required=True
                ),
                PromptArgument(
                    name="review_type",
                    description="Type of review (e.g., security, performance, style)",
                    required=True
                ),
                PromptArgument(
                    name="complexity_level",
                    description="Code complexity level (beginner, intermediate, advanced)",
                    required=False
                )
            ]
        ),

        Prompt(
            name="system_troubleshooting",
            description="Troubleshoot {system_type} issues with {error_symptoms}",
            arguments=[
                PromptArgument(
                    name="system_type",
                    description="Type of system (e.g., web server, database, network)",
                    required=True
                ),
                PromptArgument(
                    name="error_symptoms",
                    description="Observed error symptoms or issues",
                    required=True
                ),
                PromptArgument(
                    name="urgency",
                    description="Urgency level (low, medium, high, critical)",
                    required=False
                )
            ]
        ),

        Prompt(
            name="documentation_generator",
            description="Generate {doc_type} documentation for {subject}",
            arguments=[
                PromptArgument(
                    name="doc_type",
                    description="Type of documentation (API, user guide, technical specs)",
                    required=True
                ),
                PromptArgument(
                    name="subject",
                    description="Subject to document (function, module, system)",
                    required=True
                ),
                PromptArgument(
                    name="audience",
                    description="Target audience (developers, users, administrators)",
                    required=False
                ),
                PromptArgument(
                    name="format",
                    description="Output format (markdown, HTML, plain text)",
                    required=False
                )
            ]
        ),

        Prompt(
            name="performance_analysis",
            description="Analyze performance metrics for {system_component} and identify optimization opportunities",
            arguments=[
                PromptArgument(
                    name="system_component",
                    description="System component to analyze (API, database, frontend)",
                    required=True
                ),
                PromptArgument(
                    name="metrics_data",
                    description="Performance metrics data or description",
                    required=True
                ),
                PromptArgument(
                    name="baseline_period",
                    description="Baseline period for comparison",
                    required=False
                )
            ]
        )
    ]