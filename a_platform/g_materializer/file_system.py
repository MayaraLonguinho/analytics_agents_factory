import os
import shutil

class FileSystemOps:
    @staticmethod
    def ensure_directory(path: str):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def write_file(path: str, content: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
