import autogen
from typing import Dict, List, Any, Optional
from autogen_bird.utils import get_table_schema, validate_sql
from autogen_bird.table_aware import generate_table_aware_prompt, enhance_query_with_ta

class AdvancedAgentSystem:
    """An advanced multi-agent system that incorporates Table-Aware techniques."""
    
    def __init__(self, api_key: str, model: str, sql_dialect: str):
        self.api_key = api_key
        self.model = model
        self.sql_dialect = sql_dialect
        self.agents = self._create_agents()
    
    def _create_agents(self):
        # Configure agents with OpenAI API
        config_list = [
            {
                "model": self.model,
                "api_key": self.api_key,
            }
        ]
        
        # Create agents with enhanced prompts
        coordinator = autogen.AssistantAgent(
            name="Coordinator",
            system_message=f"""You are the coordinator of a multi-agent system for generating SQL queries in {self.sql_dialect}.
            Your job is to manage the workflow and ensure the final SQL query is correct.
            You will receive a question, database schema, and possibly external knowledge evidence.
            
            Follow these steps:
            1. First, ask the Schema Analyzer to identify relevant tables and relationships
            2. Then, ask the Query Planner to outline the query approach
            3. Next, ask the Query Generator to write the initial SQL query
            4. Then, ask the Query Validator to check for errors
            5. Finally, ask the Final Reviewer to ensure the query answers the original question
            
            After all agents have contributed, provide the FINAL SQL QUERY with no additional text.""",
            llm_config={"config_list": config_list},
        )
        
        schema_analyzer = autogen.AssistantAgent(
            name="SchemaAnalyzer",
            system_message=f"""You are a database schema expert specialized in {self.sql_dialect}.
            Your job is to analyze the database schema and identify the relevant tables and columns needed to answer the question.
            
            For each relevant table:
            1. List the important columns and their data types
            2. Identify primary and foreign keys
            3. Explain how tables should be joined
            4. Note any important constraints or indexes
            
            Be thorough but concise in your analysis.""",
            llm_config={"config_list": config_list},
        )
        
        query_planner = autogen.AssistantAgent(
            name="QueryPlanner",
            system_message=f"""You are a SQL query planning expert specialized in {self.sql_dialect}.
            Your job is to outline the approach for constructing the SQL query before actual coding.
            
            Based on the schema analysis and question, provide:
            1. The main tables needed and