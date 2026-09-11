# pyrefly: ignore [missing-import]
import pytest
import os

def test_repository_integrity():
    root_dir = os.getcwd()
    
    for root, dirs, files in os.walk(root_dir):
        if ".git" in root or "venv" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if file.endswith(".py") or file.endswith(".yaml") or file.endswith(".yml") or file.endswith(".md"):
                if file == ".gitkeep":
                    continue
                
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                
                assert size > 0, f"File {filepath} is completely empty!"
