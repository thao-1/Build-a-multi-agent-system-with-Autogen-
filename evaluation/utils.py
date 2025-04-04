import os
import json
import sqlite3
import subprocess
from typing import Dict, List, Any, Optional

def load_data(file_path: str) -> List[Dict[str, Any]]:
    """Load data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_results(results: Dict[str, str], output_file: str) -> None:
    """Save results to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

def get_table_schema(db_path: str, sql_dialect: str) -> str:
    """Extract database schema information."""
    if sql_dialect == "SQLite":
        return get_sqlite_schema(db_path)
    elif sql_dialect == "MySQL":
        return get_mysql_schema(db_path)
    elif sql_dialect == "PostgreSQL":
        return get_postgresql_schema(db_path)
    else:
        raise ValueError(f"Unsupported SQL dialect: {sql_dialect}")

def get_sqlite_schema(db_path: str) -> str:
    """Get schema information from SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = []
    for table in tables:
        table_name = table[0]
        # Get table columns
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        column_info = []
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            is_pk = "PRIMARY KEY" if col[5] == 1 else ""
            column_info.append(f"{col_name} {col_type} {is_pk}".strip())
        
        # Get sample data (first 3 rows)
        try:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
            sample_data = cursor.fetchall()
            sample_str = "\n".join([str(row) for row in sample_data])
        except:
            sample_str = "No sample data available"
        
        schema_info.append(f"Table: {table_name}\nColumns: {', '.join(column_info)}\nSample data:\n{sample_str}\n")
    
    conn.close()
    return "\n".join(schema_info)

def get_mysql_schema(db_path: str) -> str:
    """Placeholder for MySQL schema extraction."""
    # In a real implementation, you would connect to MySQL and extract schema
    return f"MySQL schema extraction not implemented. Database path: {db_path}"

def get_postgresql_schema(db_path: str) -> str:
    """Placeholder for PostgreSQL schema extraction."""
    # In a real implementation, you would connect to PostgreSQL and extract schema
    return f"PostgreSQL schema extraction not implemented. Database path: {db_path}"

def validate_sql(sql_query: str, db_path: str, sql_dialect: str) -> bool:
    """Validate SQL query by attempting to execute it."""
    if sql_dialect == "SQLite":
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(sql_query)
            conn.close()
            return True
        except Exception as e:
            return False
    else:
        # For MySQL and PostgreSQL, we would need to implement proper validation
        return True  # Assume valid for now