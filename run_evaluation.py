#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to run all evaluation metrics for the SQL Chat Agent.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    """
    Run a command and return its output.
    """
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
    return result.returncode == 0

def main():
    """
    Main function to run all evaluation metrics.
    """
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Define the common arguments
    common_args = [
        "--predicted_sql_path ./exp_results/results_SQLite.json",
        "--ground_truth_path ./data/mini_dev_sqlite_gold.sql",
        "--db_root_path ./data/dev_databases/",
        "--sql_dialect SQLite",
        "--diff_json_path ./data/mini_dev_difficulty.json"
    ]
    
    # Run Execution (EX) Evaluation
    ex_command = f"python -m evaluation.evaluation_ex {' '.join(common_args)}"
    if not run_command(ex_command):
        print("Error running Execution (EX) Evaluation")
        return 1
    
    # Run R-VES Evaluation
    rves_command = f"python -m evaluation.evaluation_ves {' '.join(common_args)}"
    if not run_command(rves_command):
        print("Error running R-VES Evaluation")
        return 1
    
    # Run Soft F1-Score Evaluation
    f1_command = f"python -m evaluation.evaluation_f1 {' '.join(common_args)}"
    if not run_command(f1_command):
        print("Error running Soft F1-Score Evaluation")
        return 1
    
    print("\nAll evaluations completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 