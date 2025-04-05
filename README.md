# SQL Chat Agent

A simple chat agent that uses OpenAI's API to generate SQL queries based on natural language questions.

## Features

- Interactive chat interface
- SQL query generation
- Retry logic for handling connection issues
- Configurable API settings
- Multiple evaluation metrics for SQL query accuracy

## Architecture and Design Decisions

### SQL Chat Agent Architecture

The SQL Chat Agent is built with a modular architecture consisting of the following components:

1. **User Interface Layer**: Handles user input and output, providing an interactive chat experience.
2. **Query Generation Layer**: Uses OpenAI's API to convert natural language questions into SQL queries.
3. **Database Interaction Layer**: Executes the generated SQL queries against the target database.
4. **Evaluation Layer**: Assesses the accuracy and efficiency of the generated SQL queries.

### Design Decisions

1. **Multiple Evaluation Metrics**: We implemented three different evaluation metrics to provide a comprehensive assessment of SQL query generation:
   - **Execution (EX)**: Measures whether the generated queries produce the same results as ground truth.
   - **R-VES**: Evaluates both correctness and efficiency of the queries.
   - **Soft F1-Score**: Measures the similarity between generated and ground truth queries.

2. **Modular Design**: The system is designed with modularity in mind, allowing for easy extension and modification of individual components.

3. **Error Handling**: Robust error handling and retry logic ensure the system can recover from temporary API failures.

4. **Configurable Settings**: The system allows for easy configuration of API settings, database connections, and evaluation parameters.

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key:
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```
4. Run the chat agent:
   ```
   cd run
   ./run_chat.sh
   ```

## Usage

- Type your questions about SQL queries
- The agent will generate SQL queries based on your questions
- Type 'exit' to quit the chat agent

## Evaluation

The system provides three different evaluation metrics to assess the accuracy of generated SQL queries:

### 1. Execution (EX) Evaluation

This metric evaluates whether the generated SQL queries produce the same results as the ground truth queries.

```bash
python -m evaluation.evaluation_ex \
  --predicted_sql_path ./exp_results/results_SQLite.json \
  --ground_truth_path ./data/mini_dev_sqlite_gold.sql \
  --db_root_path ./data/dev_databases/ \
  --sql_dialect SQLite \
  --diff_json_path ./data/mini_dev_difficulty.json
```

### 2. R-VES (Reward-based Valid Efficiency Score) Evaluation

This metric evaluates both the correctness and efficiency of the generated SQL queries.

```bash
python -m evaluation.evaluation_ves \
  --predicted_sql_path ./exp_results/results_SQLite.json \
  --ground_truth_path ./data/mini_dev_sqlite_gold.sql \
  --db_root_path ./data/dev_databases/ \
  --sql_dialect SQLite \
  --diff_json_path ./data/mini_dev_difficulty.json
```

### 3. Soft F1-Score Evaluation

This metric evaluates the similarity between the generated SQL queries and the ground truth queries.

```bash
python -m evaluation.evaluation_f1 \
  --predicted_sql_path ./exp_results/results_SQLite.json \
  --ground_truth_path ./data/mini_dev_sqlite_gold.sql \
  --db_root_path ./data/dev_databases/ \
  --sql_dialect SQLite \
  --diff_json_path ./data/mini_dev_difficulty.json
```

### Required Files for Evaluation

- `predicted_sql_path`: JSON file containing the generated SQL queries
- `ground_truth_path`: SQL file containing the ground truth queries
- `db_root_path`: Directory containing the database files
- `sql_dialect`: SQL dialect used (e.g., SQLite, MySQL, PostgreSQL)
- `diff_json_path`: JSON file containing the difficulty classification for each query

## Example

Here's a simple example of how to use the SQL Chat Agent:

1. Start the chat agent:
   ```
   cd run
   ./run_chat.sh
   ```

2. Ask a question about SQL:
   ```
   > What is the average age of users over 18?
   ```

3. The agent will generate a SQL query:
   ```
   SELECT AVG(age) FROM users WHERE age > 18
   ```

4. The agent will execute the query and return the result:
   ```
   Result: 27.5
   ```

## Requirements

- Python 3.6+
- OpenAI API key
- Required Python packages (see requirements.txt)
- SQLite, MySQL, or PostgreSQL database (depending on the SQL dialect used)
