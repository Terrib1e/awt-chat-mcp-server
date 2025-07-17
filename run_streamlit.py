#!/usr/bin/env python3
"""
Script to run the Streamlit MCP Server Dashboard
"""
import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    print("🚀 Starting MCP Server Streamlit Dashboard...")
    print("=" * 50)

    # Make sure we're in the right directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped.")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
        print("Make sure Streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main()