import sqlite3

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="sqlite", port=8000)


@mcp.resource("schema://main")
def sqlite_get_schema() -> str:
    """Provide the database schema as a resource"""
    conn = sqlite3.connect("database.db")
    schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    return "\n".join(sql[0] for sql in schema if sql[0])


@mcp.tool()
def sqlite_query_data(sql: str) -> str:
    """Execute SQL queries safely"""
    conn = sqlite3.connect("database.db")
    try:
        result = conn.execute(sql).fetchall()
        return "\n".join(str(row) for row in result)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def sqlite_write_data(sql: str, params: tuple = ()) -> str:
    """
    Execute INSERT/UPDATE/DELETE with params in tuple form.
    """
    conn = sqlite3.connect("database.db")
    try:
        cursor = conn.execute(sql, params)
        conn.commit()
        return f"Operación exitosa, filas afectadas: {cursor.rowcount}"
    except Exception as e:
        conn.rollback()
        return f"Error al ejecutar operación: {str(e)}"
    finally:
        conn.close()


if __name__ == "__main__":
    mcp.run(transport="sse")
