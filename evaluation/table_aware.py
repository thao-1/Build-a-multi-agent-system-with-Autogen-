"""
Implementation of Table-Aware (TA) SQL generation techniques.
This module enhances SQL generation by providing better table structure understanding.
"""

import re
from typing import Dict, List, Any, Optional

def extract_table_info(schema: str) -> Dict[str, Dict[str, Any]]:
    """Extract table information from schema string."""
    tables = {}
    current_table = None
    
    for line in schema.split('\n'):
        if line.startswith('Table:'):
            current_table = line.replace('Table:', '').strip()
            tables[current_table] = {'columns': [], 'sample_data': []}
        elif current_table and line.startswith('Columns:'):
            columns_str = line.replace('Columns:', '').strip()
            columns = [col.strip() for col in columns_str.split(',')]
            tables[current_table]['columns'] = columns
        elif current_table and 'sample_data' in tables[current_table] and line and not line.startswith('Sample data:'):
            tables[current_table]['sample_data'].append(line.strip())
    
    return tables

def generate_table_aware_prompt(question: str, schema: str, evidence: str = "") -> str:
    """Generate a table-aware prompt for SQL generation."""
    table_info = extract_table_info(schema)
    
    # Create a structured representation of the database
    db_structure = []
    for table_name, info in table_info.items():
        db_structure.append(f"Table: {table_name}")
        db_structure.append(f"Columns: {', '.join(info['columns'])}")
        if info['sample_data']:
            db_structure.append("Sample data:")
            for data in info['sample_data'][:3]:  # Limit to 3 samples
                db_structure.append(f"  {data}")
                
    # Build the prompt
    prompt = f"""
    # SQL Generation Task
    
    ## Question
    {question}
    
    ## Database Structure
    {'\n'.join(db_structure)}
    """
    
    if evidence:
        prompt += f"""
        ## External Knowledge
        {evidence}
        """
    
    prompt += """
    ## Instructions
    1. Analyze the question carefully to understand what information is being requested.
    2. Identify the relevant tables and columns needed to answer the question.
    3. Determine the appropriate joins, filters, and aggregations.
    4. Write a SQL query that correctly answers the question.
    5. Ensure your query follows the specific syntax for the SQL dialect.
    6. Double-check your query for correctness before submitting.
    
    ## SQL Query
    ```sql
    """
    
    return prompt

def enhance_query_with_ta(query: str, schema: str) -> str:
    """Enhance a generated SQL query using table-aware techniques."""
    table_info = extract_table_info(schema)
    
    # Check for missing joins
    tables_in_query = []
    for table_name in table_info.keys():
        if re.search(r'\b' + re.escape(table_name) + r'\b', query, re.IGNORECASE):
            tables_in_query.append(table_name)
    
    # If multiple tables are used but no JOIN is present, suggest adding joins
    if len(tables_in_query) > 1 and "JOIN" not in query.upper():
        # This is a simplified approach - in a real system, you'd need more sophisticated join detection
        return query + "\n-- Warning: Multiple tables used but no explicit JOIN found"
    
    return query
