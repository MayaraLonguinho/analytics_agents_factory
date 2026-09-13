import sqlite3
from typing import Dict, Any
import re

def is_safe_query(query: str) -> bool:
    # Impede anexar bancos externos ou dropar o banco todo por engano
    forbidden_keywords = [r'\bATTACH\b', r'\bDETACH\b']
    for kw in forbidden_keywords:
        if re.search(kw, query, re.IGNORECASE):
            return False
    return True

def handle_database(query: str, db_path: str = "local.db") -> Dict[str, Any]:
    """
    Executa uma query em um banco local SQLite.
    Possui restrições contra manipulações externas.
    """
    if not is_safe_query(query):
        return {"success": False, "error": "Query contém palavras-chave proibidas no escopo deste MCP."}
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # SQLite pode precisar de executescript se houver múltiplas statements
        if ';' in query:
            cursor.executescript(query)
            conn.commit()
            rows = []
        else:
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT") or query.strip().upper().startswith("PRAGMA"):
                rows = cursor.fetchall()
            else:
                conn.commit()
                rows = []
                
        conn.close()
        return {"success": True, "data": rows, "message": "Query executada com sucesso."}
    except sqlite3.Error as e:
        return {"success": False, "error": str(e)}

database_schema = {
    "name": "database_mcp",
    "description": "Executes SQL queries on a local SQLite database with basic safety constraints.",
    "input_schema": {
        "query": "string",
        "db_path": "string (optional)"
    },
    "output_schema": {
        "success": "boolean",
        "data": "list (optional)",
        "message": "string (optional)",
        "error": "string (optional)"
    },
    "handler": handle_database

}
