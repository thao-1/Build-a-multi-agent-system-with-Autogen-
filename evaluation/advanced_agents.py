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
            1. The main tables needed and their relationships
            2. The key columns to select and filter on
            3. Any necessary joins and their conditions
            4. The order of operations (WHERE, GROUP BY, etc.)
            5. Any special considerations for the specific SQL dialect
            
            Be clear and structured in your planning.""",
            llm_config={"config_list": config_list},
        )
        
        query_generator = autogen.AssistantAgent(
            name="QueryGenerator",
            system_message=f"""You are a SQL query generation expert specialized in {self.sql_dialect}.
            Your job is to write the actual SQL query based on the planning and schema analysis.
            
            Follow these guidelines:
            1. Use proper {self.sql_dialect} syntax and conventions
            2. Include all necessary joins and conditions
            3. Handle NULL values appropriately
            4. Use appropriate aggregation functions
            5. Add helpful comments for complex parts
            
            Generate only the SQL query with no additional explanation.""",
            llm_config={"config_list": config_list},
        )
        
        query_validator = autogen.AssistantAgent(
            name="QueryValidator",
            system_message=f"""You are a SQL query validation expert specialized in {self.sql_dialect}.
            Your job is to check the generated query for potential issues.
            
            Check for:
            1. Syntax errors and dialect-specific issues
            2. Missing or incorrect joins
            3. Logical errors in conditions
            4. Performance considerations
            5. Proper handling of edge cases
            
            If you find issues, explain them clearly and suggest fixes.""",
            llm_config={"config_list": config_list},
        )
        
        final_reviewer = autogen.AssistantAgent(
            name="FinalReviewer",
            system_message=f"""You are a final review expert for SQL queries in {self.sql_dialect}.
            Your job is to ensure the query correctly answers the original question.
            
            Verify that:
            1. The query addresses all aspects of the question
            2. The results will be in the expected format
            3. All necessary data is included
            4. The query is optimized for performance
            5. The query follows best practices
            
            If you find any issues, explain them and suggest improvements.""",
            llm_config={"config_list": config_list},
        )
        
        return {
            "coordinator": coordinator,
            "schema_analyzer": schema_analyzer,
            "query_planner": query_planner,
            "query_generator": query_generator,
            "query_validator": query_validator,
            "final_reviewer": final_reviewer
        }
    
    def generate_query(self, question: str, db_schema: str, evidence: Optional[str] = None) -> str:
        """Generate a SQL query using the multi-agent system."""
        
        # Prepare the initial message
        initial_message = f"""Question: {question}

Database Schema:
{db_schema}

{f'Additional Evidence:\n{evidence}' if evidence else ''}

Please analyze this request and generate a SQL query in {self.sql_dialect}."""
        
        # Start the conversation with the coordinator
        chat_messages = self.agents["coordinator"].initiate_chat(
            self.agents["schema_analyzer"],
            message=initial_message
        )
        
        # Return the final SQL query from the last message
        return chat_messages[-1]["content"]