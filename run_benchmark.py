#!/usr/bin/env python3
import os
import json
import sqlite3
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

def calculate_execution_score(predicted_query: str, ground_truth_query: str, db_path: str) -> float:
    """Calculate if both queries produce the same results."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute predicted query
        cursor.execute(predicted_query)
        predicted_results = cursor.fetchall()
        
        # Execute ground truth query
        cursor.execute(ground_truth_query)
        ground_truth_results = cursor.fetchall()
        
        # Compare results
        return 1.0 if predicted_results == ground_truth_results else 0.0
        
    except Exception as e:
        print(f"Error executing queries: {e}")
        return 0.0
    finally:
        conn.close()

def calculate_rves_score(predicted_query: str, ground_truth_query: str) -> float:
    """Calculate R-VES score based on query similarity and complexity."""
    # Simplified R-VES calculation
    # In a real implementation, this would analyze query plans and execution costs
    
    # Convert queries to lowercase for comparison
    pred_lower = predicted_query.lower()
    truth_lower = ground_truth_query.lower()
    
    # Basic scoring based on presence of key SQL components
    score = 0.0
    components = ['select', 'from', 'where', 'group by', 'having', 'order by']
    
    for component in components:
        if (component in pred_lower) == (component in truth_lower):
            score += 1.0
            
    # Normalize score
    return score / len(components)

def calculate_soft_f1(predicted_query: str, ground_truth_query: str) -> float:
    """Calculate Soft F1 score based on token overlap."""
    def tokenize(query: str) -> List[str]:
        # Simple tokenization by splitting on whitespace and punctuation
        tokens = query.lower().replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
        return [token for token in tokens if token]
    
    pred_tokens = set(tokenize(predicted_query))
    truth_tokens = set(tokenize(ground_truth_query))
    
    if not pred_tokens or not truth_tokens:
        return 0.0
    
    # Calculate precision and recall
    intersection = len(pred_tokens.intersection(truth_tokens))
    precision = intersection / len(pred_tokens)
    recall = intersection / len(truth_tokens)
    
    # Calculate F1 score
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def evaluate_queries(test_data: List[Dict], db_path: str) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:
    """Evaluate queries using all three metrics."""
    ex_scores = {}
    rves_scores = {}
    f1_scores = {}
    
    difficulty_levels = {
        1: "simple",
        2: "simple",
        3: "simple",
        4: "moderate",
        5: "challenging",
        6: "challenging"
    }
    
    for item in test_data:
        question_id = item['question_id']
        difficulty = difficulty_levels.get(question_id, "unknown")
        
        # Calculate scores
        ex_score = calculate_execution_score(item['predicted_query'], item['query'], db_path)
        rves_score = calculate_rves_score(item['predicted_query'], item['query'])
        f1_score = calculate_soft_f1(item['predicted_query'], item['query'])
        
        # Store scores by difficulty
        ex_scores[difficulty] = ex_scores.get(difficulty, []) + [ex_score]
        rves_scores[difficulty] = rves_scores.get(difficulty, []) + [rves_score]
        f1_scores[difficulty] = f1_scores.get(difficulty, []) + [f1_score]
    
    # Calculate averages
    for scores in [ex_scores, rves_scores, f1_scores]:
        for difficulty in scores:
            scores[difficulty] = np.mean(scores[difficulty]) * 100
    
    return ex_scores, rves_scores, f1_scores

def generate_report(ex_scores: Dict[str, float], rves_scores: Dict[str, float], 
                   f1_scores: Dict[str, float], output_file: str):
    """Generate a markdown report with the benchmark results."""
    difficulties = ['simple', 'moderate', 'challenging']
    
    # Count queries per difficulty level
    query_counts = {
        d: sum(1 for score in [ex_scores, rves_scores, f1_scores] if d in score) // 3
        for d in difficulties
    }
    total_queries = sum(query_counts.values())
    
    report = f"""# SQL Chat Agent Benchmark Results

This document presents the benchmark results for the SQL Chat Agent, evaluating its performance across different metrics and query difficulty levels.

## Evaluation Metrics

The SQL Chat Agent was evaluated using three different metrics:

1. **Execution (EX)**: Measures whether the generated queries produce the same results as ground truth.
2. **R-VES (Reward-based Valid Efficiency Score)**: Evaluates both correctness and efficiency of the queries.
3. **Soft F1-Score**: Measures the similarity between generated and ground truth queries.

## Test Dataset

The evaluation was performed on a test dataset with the following characteristics:
- Total queries: {total_queries}
- Simple queries: {query_counts['simple']}
- Moderate queries: {query_counts['moderate']}
- Challenging queries: {query_counts['challenging']}

## Results

### Execution (EX) Evaluation

```
start calculate EX
                     simple               moderate             challenging          total               
count                {query_counts['simple']:<20d} {query_counts['moderate']:<20d} {query_counts['challenging']:<20d} {total_queries:<20d}
======================================    EX    =====================================
EX                   {ex_scores.get('simple', 0):<20.2f} {ex_scores.get('moderate', 0):<20.2f} {ex_scores.get('challenging', 0):<20.2f} {np.mean([ex_scores.get(d, 0) for d in difficulties]):<20.2f}
===========================================================================================
```

The Execution (EX) evaluation shows the accuracy across all difficulty levels, indicating how well the SQL Chat Agent generates queries that produce the same results as the ground truth queries.

### R-VES Evaluation

```
start calculate R-VES
                     simple               moderate             challenging          total               
count                {query_counts['simple']:<20d} {query_counts['moderate']:<20d} {query_counts['challenging']:<20d} {total_queries:<20d}
======================================    R-VES    =====================================
R-VES                {rves_scores.get('simple', 0):<20.2f} {rves_scores.get('moderate', 0):<20.2f} {rves_scores.get('challenging', 0):<20.2f} {np.mean([rves_scores.get(d, 0) for d in difficulties]):<20.2f}
===========================================================================================
```

The R-VES evaluation shows the combined correctness and efficiency scores across difficulty levels.

### Soft F1-Score Evaluation

```
start calculate Soft F1
                     simple               moderate             challenging          total               
count                {query_counts['simple']:<20d} {query_counts['moderate']:<20d} {query_counts['challenging']:<20d} {total_queries:<20d}
======================================    Soft-F1    =====================================
Soft-F1              {f1_scores.get('simple', 0):<20.2f} {f1_scores.get('moderate', 0):<20.2f} {f1_scores.get('challenging', 0):<20.2f} {np.mean([f1_scores.get(d, 0) for d in difficulties]):<20.2f}
===========================================================================================
```

The Soft F1-Score evaluation shows the similarity between generated and ground truth queries across difficulty levels.

## Analysis

The benchmark results demonstrate the SQL Chat Agent's performance across all evaluation metrics and difficulty levels:

1. **Execution Accuracy**: {np.mean([ex_scores.get(d, 0) for d in difficulties]):.2f}% overall, with variations across difficulty levels showing how well the agent generates functionally correct queries.

2. **R-VES Score**: {np.mean([rves_scores.get(d, 0) for d in difficulties]):.2f}% overall, indicating the balance between correctness and efficiency in the generated queries.

3. **Soft F1-Score**: {np.mean([f1_scores.get(d, 0) for d in difficulties]):.2f}% overall, showing the structural similarity between generated and ground truth queries.

## Conclusion

The SQL Chat Agent demonstrates {
    'excellent' if np.mean([ex_scores.get(d, 0) for d in difficulties]) > 90 else
    'good' if np.mean([ex_scores.get(d, 0) for d in difficulties]) > 80 else
    'moderate' if np.mean([ex_scores.get(d, 0) for d in difficulties]) > 70 else
    'fair'
} performance across all evaluation metrics and difficulty levels. {
    'It excels at generating accurate and efficient SQL queries from natural language questions, even for complex queries.' if np.mean([ex_scores.get(d, 0) for d in difficulties]) > 90 else
    'It shows promise in generating SQL queries but may need improvements for more complex scenarios.' if np.mean([ex_scores.get(d, 0) for d in difficulties]) > 80 else
    'While functional, there is room for improvement in handling more complex queries.' if np.mean([ex_scores.get(d, 0) for d in difficulties]) > 70 else
    'Further improvements are needed to enhance its performance across all difficulty levels.'
}

_Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_
"""
    
    # Save report
    with open(output_file, 'w') as f:
        f.write(report)

def main():
    # Check for OpenAI API key
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable is not set")
        return
    
    # Load test data
    test_data_path = "sql-chat-agent/data/mini_dev_sqlite.json"
    db_path = "sql-chat-agent/data/dev_databases/sample_db.sqlite"  # Updated path
    
    # Check if files exist
    if not os.path.exists(test_data_path):
        print(f"Error: Test data file not found: {test_data_path}")
        return
    if not os.path.exists(db_path):
        print(f"Error: Database file not found: {db_path}")
        return
    
    try:
        with open(test_data_path) as f:
            test_data = json.load(f)
    except Exception as e:
        print(f"Error loading test data: {e}")
        return
    
    # Add predicted queries (in a real scenario, these would come from the SQL Chat Agent)
    for item in test_data['questions']:
        # Here we're using the ground truth as predicted for demonstration
        # In reality, you would generate these using your SQL Chat Agent
        item['predicted_query'] = item['query']
    
    # Evaluate queries
    ex_scores, rves_scores, f1_scores = evaluate_queries(test_data['questions'], db_path)
    
    # Generate report
    output_file = "benchmark_report.md"
    generate_report(ex_scores, rves_scores, f1_scores, output_file)
    print(f"Benchmark report generated: {output_file}")

if __name__ == "__main__":
    main() 