import os
import json
import argparse
from tqdm import tqdm
from autogen_bird.agents import create_agent_system
from autogen_bird.utils import load_data, save_results

def main():
    parser = argparse.ArgumentParser(description="Autogen BIRD-SQL Multi-Agent System")
    parser.add_argument("--eval_path", type=str, default="./data/mini_dev_sqlite.json", 
                        help="Path to evaluation data")
    parser.add_argument("--db_root_path", type=str, default="./data/dev_databases/", 
                        help="Path to database files")
    parser.add_argument("--output_path", type=str, default="./output/", 
                        help="Path to save results")
    parser.add_argument("--sql_dialect", type=str, default="SQLite", 
                        choices=["SQLite", "MySQL", "PostgreSQL"],
                        help="SQL dialect to use")
    parser.add_argument("--api_key", type=str, required=True, 
                        help="OpenAI API key")
    parser.add_argument("--model", type=str, default="gpt-4-turbo", 
                        help="OpenAI model to use")
    parser.add_argument("--num_samples", type=int, default=-1, 
                        help="Number of samples to process (-1 for all)")
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_path, exist_ok=True)
    
    # Load data
    data = load_data(args.eval_path)
    
    # Limit samples if specified
    if args.num_samples > 0:
        data = data[:args.num_samples]
    
    # Process each sample
    results = {}
    for idx, sample in enumerate(tqdm(data, desc="Processing samples")):
        db_id = sample["db_id"]
        question = sample["question"]
        evidence = sample.get("evidence", "")
        
        # Get database path
        db_path = os.path.join(args.db_root_path, db_id)
        
        # Create agent system
        agent_system = create_agent_system(
            api_key=args.api_key,
            model=args.model,
            sql_dialect=args.sql_dialect
        )
        
        # Generate SQL query
        sql_query = agent_system.generate_sql(
            question=question,
            db_path=db_path,
            evidence=evidence
        )
        
        # Store result
        results[str(idx)] = f"{sql_query}\t----- bird -----\t{db_id}"
    
    # Save results
    output_file = os.path.join(
        args.output_path, 
        f"predict_mini_dev_autogen_{args.model.replace('-', '_')}_{args.sql_dialect}.json"
    )
    save_results(results, output_file)
    
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()