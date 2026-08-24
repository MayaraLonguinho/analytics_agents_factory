import urllib.request
from typing import Dict, Any

def handle_browser(url: str) -> Dict[str, Any]:
    """
    Lê o conteúdo raw de uma URL via HTTP.
    """
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            return {"success": True, "content": html}
    except Exception as e:
        return {"success": False, "error": str(e)}

browser_schema = {
    "name": "browser_mcp",
    "description": "Reads raw content from a URL via HTTP.",
    "input_schema": {
        "url": "string"
    },
    "output_schema": {
        "success": "boolean",
        "content": "string (optional)",
        "error": "string (optional)"
    },
    "handler": handle_browser
}
