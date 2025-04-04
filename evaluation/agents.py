import autogen
from typing import Dict, List, Any, Optional
from autogen_bird.utils import get_table_schema, validate_sql

class AgentSystem:
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
        
        # Create agents
        coordinator = autogen.AssistantAgent(
            name="Coordinator",
            system_message="""You are the coordinator of a multi-agent system for generating SQL queries.
            Your job is to manage the workflow between different specialized agents and ensure the final SQL query is correct.
            You will receive a question, database schema, and possibly external knowledge evidence.
            Coordinate with the Schema Analyzer, Query Generator, Query Validator, and Final Reviewer to produce the best SQL query.""",
            llm_config={"config_list": config_list},
        )
        
        schema_analyzer = autogen.AssistantAgent(
            name="SchemaAnalyzer",
            system_message=f"""You are a database schema expert specialized in {self.sql_dialect}.
            Your job is to analyze the database schema and identify the relevant tables and columns needed to answer the question.
            Provide a detailed analysis of how the tables should be joined and which columns are relevant for filtering and selection.""",
            llm_config={"config_list": config_list},
        )
        
        query_generator = autogen.AssistantAgent(
            name="QueryGenerator",
            system_message=f"""You are a SQL expert specialized in {self.sql_dialect}.
            Your job is to generate a SQL query based on the question and schema analysis.
            Make sure to follow the specific syntax for {self.sql_dialect} and use appropriate joins, filters, and aggregations.
            Always double-check your query for correctness before submitting.""",
            llm_config={"config_list": config_list},
        )
        
        query_validator = autogen.AssistantAgent(
            name="QueryValidator",
            system_message=f"""You are a SQL validator specialized in {self.sql_dialect}.
            Your job is to check the generated SQL query for syntax errors, logical errors, and performance issues.
            If you find any issues, provide specific feedback on how to fix them.
            Pay special attention to join conditions, aggregation functions, and filtering conditions.""",
            llm_config={"config_list": config_list},
        )
        
        final_reviewer = autogen.AssistantAgent(
            name="FinalReviewer",
            system_message=f"""You are a final reviewer for SQL queries specialized in {self.sql_dialect}.
            Your job is to ensure the SQL query correctly answers the original question.
            Check that all requirements from the question are addressed in the query.
            Make any final adjustments to improve the query's accuracy and readability.
            The final output should be ONLY the SQL query without any explanations or comments.""",
            llm_config={"config_list": config_list},
        )
        
        user_proxy = autogen.UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            is_termination_msg=lambda msg: "FINAL SQL QUERY:" in msg["content"],
        )
        
        return {
            "coordinator": coordinator,
            "schema_analyzer": schema_analyzer,
            "query_generator": query_generator,
            "query_validator": query_validator,
            "final_reviewer": final_reviewer,
            "user_proxy": user_proxy
        }
    
    def generate_sql(self, question: str, db_path: str, evidence: str = "") -> str:
        """Generate SQL query using the multi-agent system."""
        # Get database schema
        schema = get_table_schema(db_path, self.sql_dialect)
        
        # Prepare initial message
        initial_message = f"""
        I need to generate a SQL query for the following question:
        
        QUESTION: {question}
        
        DATABASE SCHEMA:
        {schema}
        """
        
        if evidence:
            initial_message += f"""
            EXTERNAL KNOWLEDGE EVIDENCE:
            {evidence}
            """
        
        # Start the conversation
        self.agents["user_proxy"].initiate_chat(
            self.agents["coordinator"],
            message=initial_message
        )
        
        # Extract the final SQL query from the conversation
        for message in reversed(self.agents["user_proxy"].chat_messages[self.agents["coordinator"]]):
            if "FINAL SQL QUERY:" in message["content"]:
                sql_query = message["content"].split("FINAL SQL QUERY:")[1].strip()
                return sql_query
        
        # If no final SQL query was found, return an empty string
        return ""

def create_agent_system(api_key: str, model: str, sql_dialect: str) -> AgentSystem:
    """Create and return an agent system."""
    return AgentSystem(api_key, model, sql_dialect)