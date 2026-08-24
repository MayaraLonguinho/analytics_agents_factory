import sqlite3
from typing import Dict, Any

def handle_database(query: str, db_path: str = "local.db") -> Dict[str, Any]:
    """
    Executa uma query em um banco local SQLite para fins de materialização e testes de Schema.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            conn.close()
            return {"success": True, "data": rows}
        else:
            conn.commit()
            conn.close()
            return {"success": True, "message": "Query executada com sucesso."}
    except sqlite3.Error as e:
        return {"success": False, "error": str(e)}

database_schema = {
    "name": "database_mcp",
    "description": "Executes SQL queries on a local SQLite database.",
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
