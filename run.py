#!/usr/bin/env python3
"""
Main runner script for the AI Caption Generator
"""

import os
import sys
import subprocess
import argparse

def run_streamlit():
    """Run the Streamlit frontend"""
    cmd = ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    subprocess.run(cmd)

def run_api():
    """Run the FastAPI backend"""
    cmd = ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    subprocess.run(cmd)

def run_docker():
    """Run with Docker Compose"""
    cmd = ["docker-compose", "up", "--build"]
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="AI Caption Generator Runner")
    parser.add_argument(
        "mode", 
        choices=["streamlit", "api", "docker"], 
        help="Choose how to run the application"
    )
    
    args = parser.parse_args()
    
    if args.mode == "streamlit":
        print("🚀 Starting Streamlit frontend...")
        run_streamlit()
    elif args.mode == "api":
        print("🚀 Starting FastAPI backend...")
        run_api()
    elif args.mode == "docker":
        print("🐳 Starting with Docker Compose...")
        run_docker()

if __name__ == "__main__":
    main()