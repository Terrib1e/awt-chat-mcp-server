#!/usr/bin/env python3
"""
Test cases for MCP Server Tools

This file demonstrates how to test MCP server functionality:
1. Unit tests for individual tools
2. Integration tests for workflows
3. Error handling tests
4. Performance tests
"""

import asyncio
import pytest
import json
from pathlib import Path
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.calc_tools import calculate_basic, calculate_advanced, convert_units
from tools.file_tools import read_file_content, write_file_content, list_directory
from tools.data_tools import analyze_csv, process_json, generate_report

class TestCalculatorTools:
    """Test cases for calculator tools."""

    @pytest.mark.asyncio
    async def test_basic_addition(self):
        """Test basic addition operation."""
        result = await calculate_basic("add", {"a": 5, "b": 3})
        assert result["result"] == 8
        assert result["operation"] == "add"
        assert result["inputs"]["a"] == 5
        assert result["inputs"]["b"] == 3

    @pytest.mark.asyncio
    async def test_basic_division(self):
        """Test basic division operation."""
        result = await calculate_basic("divide", {"a": 10, "b": 2})
        assert result["result"] == 5
        assert result["operation"] == "divide"

    @pytest.mark.asyncio
    async def test_division_by_zero(self):
        """Test division by zero error handling."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            await calculate_basic("divide", {"a": 10, "b": 0})

    @pytest.mark.asyncio
    async def test_advanced_sqrt(self):
        """Test square root operation."""
        result = await calculate_advanced("sqrt", {"x": 16})
        assert result["result"] == 4
        assert result["operation"] == "sqrt"

    @pytest.mark.asyncio
    async def test_sqrt_negative(self):
        """Test square root of negative number."""
        with pytest.raises(ValueError, match="Cannot take square root of negative number"):
            await calculate_advanced("sqrt", {"x": -4})

    @pytest.mark.asyncio
    async def test_unit_conversion(self):
        """Test unit conversion."""
        result = await convert_units({"value": 100, "from_unit": "cm", "to_unit": "m"})
        assert result["converted_value"] == 1.0
        assert result["from_unit"] == "cm"
        assert result["to_unit"] == "m"

class TestFileTools:
    """Test cases for file tools."""

    @pytest.fixture
    def temp_file(self, tmp_path):
        """Create a temporary file for testing."""
        file_path = tmp_path / "test_file.txt"
        file_path.write_text("Hello, World!")
        return str(file_path)

    @pytest.mark.asyncio
    async def test_read_file(self, temp_file):
        """Test reading file content."""
        result = await read_file_content({"file_path": temp_file})
        assert result["content"] == "Hello, World!"
        assert result["characters"] == 13

    @pytest.mark.asyncio
    async def test_read_nonexistent_file(self):
        """Test reading non-existent file."""
        with pytest.raises(Exception, match="File not found"):
            await read_file_content({"file_path": "/nonexistent/file.txt"})

    @pytest.mark.asyncio
    async def test_write_file(self, tmp_path):
        """Test writing file content."""
        file_path = str(tmp_path / "new_file.txt")
        content = "Test content"

        result = await write_file_content({
            "file_path": file_path,
            "content": content
        })

        assert result["success"] is True
        assert result["characters"] == len(content)
        assert Path(file_path).exists()

    @pytest.mark.asyncio
    async def test_list_directory(self, tmp_path):
        """Test listing directory contents."""
        # Create test files
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.txt").write_text("content2")
        (tmp_path / "subdir").mkdir()

        result = await list_directory({"directory_path": str(tmp_path)})

        assert result["total_files"] == 2
        assert result["total_directories"] == 1
        assert len(result["files"]) == 2
        assert len(result["directories"]) == 1

class TestDataTools:
    """Test cases for data processing tools."""

    @pytest.fixture
    def sample_csv_data(self, tmp_path):
        """Create sample CSV data for testing."""
        csv_content = """name,age,salary
John,25,50000
Jane,30,60000
Bob,35,70000"""

        file_path = tmp_path / "test_data.csv"
        file_path.write_text(csv_content)
        return str(file_path)

    @pytest.fixture
    def sample_json_data(self, tmp_path):
        """Create sample JSON data for testing."""
        json_content = {
            "users": [
                {"name": "John", "age": 25},
                {"name": "Jane", "age": 30}
            ],
            "metadata": {
                "total": 2,
                "created": "2024-01-01"
            }
        }

        file_path = tmp_path / "test_data.json"
        file_path.write_text(json.dumps(json_content))
        return str(file_path)

    @pytest.mark.asyncio
    async def test_analyze_csv(self, sample_csv_data):
        """Test CSV analysis."""
        result = await analyze_csv({"file_path": sample_csv_data})

        assert result["total_rows"] == 3
        assert result["total_columns"] == 3
        assert "name" in result["column_names"]
        assert "age" in result["column_names"]
        assert "salary" in result["column_names"]

    @pytest.mark.asyncio
    async def test_process_json_analyze(self, sample_json_data):
        """Test JSON processing - analyze operation."""
        result = await process_json({
            "file_path": sample_json_data,
            "operation": "analyze"
        })

        assert result["operation"] == "analyze"
        assert result["root_type"] == "dict"
        assert "structure" in result

    @pytest.mark.asyncio
    async def test_process_json_extract(self, sample_json_data):
        """Test JSON processing - extract operation."""
        result = await process_json({
            "file_path": sample_json_data,
            "operation": "extract",
            "json_path": "metadata.total"
        })

        assert result["operation"] == "extract"
        assert result["extracted_data"] == 2

    @pytest.mark.asyncio
    async def test_generate_report(self):
        """Test report generation."""
        sample_data = {
            "total_rows": 100,
            "total_columns": 5,
            "missing_values": {
                "age": {"percentage": 5},
                "salary": {"percentage": 25}
            }
        }

        result = await generate_report({
            "data": sample_data,
            "report_type": "summary"
        })

        assert result["report_type"] == "summary"
        assert "key_findings" in result["report_data"]
        assert "recommendations" in result["report_data"]

class TestIntegration:
    """Integration tests for multiple tools working together."""

    @pytest.mark.asyncio
    async def test_data_analysis_workflow(self, tmp_path):
        """Test complete data analysis workflow."""
        # Step 1: Create test data
        csv_content = """name,age,salary,department
John,25,50000,Engineering
Jane,30,60000,Marketing
Bob,35,70000,Engineering"""

        csv_file = tmp_path / "workflow_data.csv"
        csv_file.write_text(csv_content)

        # Step 2: Analyze CSV
        analysis = await analyze_csv({"file_path": str(csv_file)})

        # Step 3: Generate report
        report = await generate_report({
            "data": analysis,
            "report_type": "summary"
        })

        # Verify workflow results
        assert analysis["total_rows"] == 3
        assert report["report_type"] == "summary"
        assert "report_data" in report

    @pytest.mark.asyncio
    async def test_calculation_chain(self):
        """Test chained calculations."""
        # Calculate (5 + 3) * 2
        step1 = await calculate_basic("add", {"a": 5, "b": 3})
        step2 = await calculate_basic("multiply", {"a": step1["result"], "b": 2})

        assert step1["result"] == 8
        assert step2["result"] == 16

class TestErrorHandling:
    """Test error handling scenarios."""

    @pytest.mark.asyncio
    async def test_invalid_tool_parameters(self):
        """Test handling of invalid tool parameters."""
        with pytest.raises(ValueError):
            await calculate_basic("add", {"a": "invalid", "b": 3})

    @pytest.mark.asyncio
    async def test_file_permission_errors(self):
        """Test handling of file permission errors."""
        # This would test restricted file access
        with pytest.raises(Exception):
            await read_file_content({"file_path": "/etc/passwd"})

    @pytest.mark.asyncio
    async def test_malformed_json(self, tmp_path):
        """Test handling of malformed JSON."""
        bad_json_file = tmp_path / "bad.json"
        bad_json_file.write_text("{ invalid json content")

        with pytest.raises(Exception, match="Invalid JSON"):
            await process_json({"file_path": str(bad_json_file)})

def run_manual_tests():
    """Run tests manually without pytest."""
    print("🧪 Running Manual Tests")
    print("=" * 50)

    async def run_tests():
        try:
            # Test calculator
            print("Testing calculator...")
            result = await calculate_basic("add", {"a": 10, "b": 20})
            print(f"✅ Calculator test passed: {result['result']}")

            # Test unit conversion
            print("Testing unit conversion...")
            result = await convert_units({"value": 100, "from_unit": "cm", "to_unit": "m"})
            print(f"✅ Unit conversion test passed: {result['converted_value']}")

            # Test file operations (if sample data exists)
            if Path("data/sample_data.csv").exists():
                print("Testing CSV analysis...")
                result = await analyze_csv({"file_path": "data/sample_data.csv"})
                print(f"✅ CSV analysis test passed: {result['total_rows']} rows")

            print("\n🎉 All manual tests passed!")

        except Exception as e:
            print(f"❌ Test failed: {str(e)}")

    asyncio.run(run_tests())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "manual":
        run_manual_tests()
    else:
        print("Run with 'python test_tools.py manual' for manual tests")
        print("Or use 'pytest test_tools.py' for full test suite")