"""
MCP Server for Data Query Builder with modular tool architecture.

This server provides SQL query and data analysis capabilities with:
- Modular tool architecture (each tool in its own class)
- System prompts loaded from separate documentation files
- Read-only security model (SELECT only)
- Automatic sample data loading
"""
import json
import sqlite3
import os
import sys
from mcp.server.fastmcp import FastMCP
from .sqlite_helper import create_db, load_csv_to_table

# Import tools package
from .tools import ToolManager

mcp = FastMCP("data-query-builder")

# Global database and tool manager
db: sqlite3.Connection | None = None
tool_manager: ToolManager | None = None


def get_db() -> sqlite3.Connection:
    """Initialize and return the global database connection."""
    global db
    if db is None:
        db = create_db()
        # Auto-load sample data if available
        if os.path.exists("data/sample_employees(in).csv"):
            try:
                load_csv_to_table(db, "data/sample_employees(in).csv", "employees")
            except Exception as e:
                print(f"Warning: Failed to auto-load sample data: {e}")
    return db


def get_tool_manager() -> ToolManager:
    """Initialize and return the global tool manager."""
    global tool_manager
    if tool_manager is None:
        tool_manager = ToolManager(get_db())
    return tool_manager


@mcp.tool()
def load_csv(file_path: str, table_name: str) -> str:
    """Load a CSV file into a new SQLite table with auto-detected column types.
    
    Use this when a user provides a new CSV file to analyze. Auto-detects whether columns
    are INTEGER, REAL (decimal), or TEXT. Table names should be descriptive and use snake_case.
    
    Args:
        file_path: Path to the CSV file (absolute or relative to current directory)
        table_name: Descriptive name for the new table (e.g., 'employees', 'sales_data')
    
    Returns: Success message with row count and column list, or error details
    
    Best practices:
    - Verify file exists before calling
    - Use descriptive table names in snake_case (singular preferred)
    - After loading, call describe_schema() to verify type detection
    - If types are wrong, guide user to fix CSV or use CAST in queries
    """
    manager = get_tool_manager()
    return manager.load_csv(file_path, table_name)


@mcp.tool()
def describe_schema() -> str:
    """List all tables and their columns with data types (INTEGER, REAL, or TEXT).
    
    Use this to understand the database structure before writing queries. This is essential
    for getting exact column names and verifying type detection from CSV loading.
    
    Returns: Formatted text showing all tables and their column definitions
    
    Best practices:
    - Call this first after loading CSV data
    - Use the exact column names shown here in your SQL queries
    - Call this before writing complex queries to avoid 'column not found' errors
    - Alert user if column types seem incorrect (may need CSV fix or query CAST)
    """
    manager = get_tool_manager()
    return manager.describe_schema()


@mcp.tool()
def run_query(sql: str, limit: int = 50) -> str:
    """Execute a SELECT query against the database and return results.
    
    This is your primary tool for data analysis. IMPORTANT: Only SELECT queries are allowed.
    Any attempt to DROP, DELETE, ALTER, INSERT, UPDATE, or use PRAGMA will be rejected.
    Automatically adds LIMIT if not specified. Maintains query history.
    
    Args:
        sql: A valid SQL SELECT query. Use exact column names from describe_schema().
        limit: Maximum rows to return (default 50). Use lower for exploration, higher for complete results.
    
    Returns: Results as formatted text with comma-separated values and column headers
    
    Example queries:
    - SELECT * FROM employees LIMIT 10
    - SELECT department, COUNT(*) FROM employees GROUP BY department
    - SELECT * FROM sales WHERE amount > 1000 ORDER BY date DESC LIMIT 20
    
    Best practices:
    - Always verify column names from describe_schema() first
    - Start with simple queries (LIMIT 10) to explore data
    - Use GROUP BY for aggregations, WHERE for filtering, ORDER BY for sorting
    - For joins, verify relationships between tables first
    - Use CAST() if comparing columns of different types
    """
    manager = get_tool_manager()
    return manager.run_query(sql, limit)


@mcp.tool()
def get_statistics(table_name: str, column: str) -> str:
    """Get summary statistics for a specific column: total rows, nulls, min, max, mean.
    
    Use this for quick statistical overview of a column. Returns total row count, non-null count,
    null count, minimum value, maximum value, and mean (for numeric columns only).
    Great for data quality assessment.
    
    Args:
        table_name: Exact table name from describe_schema()
        column: Exact column name from describe_schema()
    
    Returns: Formatted statistics including counts, range, and mean
    
    Best practices:
    - Verify table and column names from describe_schema() first
    - Use for quick data quality checks
    - High null counts indicate potential data issues
    - For complex statistics, use run_query() with custom GROUP BY/aggregation
    - Mean is computed for all column types but only meaningful for numeric columns
    """
    manager = get_tool_manager()
    return manager.get_statistics(table_name, column)


@mcp.tool()
def list_tables() -> str:
    """List all loaded tables in the database with their row counts.
    
    Use this for a quick overview of what data is available. Shows all table names and
    how many rows each table contains. Great for verifying successful CSV loads.
    
    Returns: List of all tables with row counts
    
    Best practices:
    - Call after loading CSV files to verify successful import
    - Use row counts to understand data scale and complexity
    - Combine with describe_schema() for complete overview
    - If expected table is missing, verify file path and table_name were correct
    """
    manager = get_tool_manager()
    return manager.list_tables()



@mcp.resource("db://schema")
def get_schema_resource() -> str:
    """Current database schema as JSON."""
    try:
        conn = get_db()
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        schema_dict = {}
        for table in tables:
            cursor = conn.execute(f"PRAGMA table_info({table})")
            columns = {col[1]: col[2] for col in cursor.fetchall()}
            schema_dict[table] = columns
        
        return json.dumps(schema_dict, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.resource("db://query-history")
def get_query_history_resource() -> str:
    """Queries executed in this session."""
    manager = get_tool_manager()
    return json.dumps(manager.get_query_history(), indent=2)


if __name__ == "__main__":
    mcp.run()
