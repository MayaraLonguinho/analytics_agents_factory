def format_content(filename: str, content: str) -> str:
    # Dummy formatter: In the future, this could run black or prettier via subprocess
    return content.strip() + "\n"
