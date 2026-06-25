import sqlite3
import pandas as pd
import os

def run_queries(csv_path, sql_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")
    if not os.path.exists(sql_path):
        raise FileNotFoundError(f"SQL file not found at: {sql_path}")
        
    print(f"Loading data from {csv_path} into SQLite in-memory database...")
    df = pd.read_csv(csv_path)
    
    # Establish SQLite connection
    conn = sqlite3.connect(':memory:')
    df.to_sql('deliveries', conn, index=False, if_exists='replace')
    
    # Read queries file
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
        
    # Parse queries by semicolon or name annotations
    queries = []
    current_query_lines = []
    current_name = ""
    
    for line in sql_content.splitlines():
        trimmed = line.strip()
        if trimmed.startswith('-- NAME:'):
            current_name = trimmed.replace('-- NAME:', '').strip()
            continue
        elif trimmed.startswith('--') or not trimmed:
            continue
            
        current_query_lines.append(line)
        if ';' in line:
            query_str = '\n'.join(current_query_lines).strip()
            queries.append((current_name, query_str))
            current_query_lines = []
            current_name = ""
            
    print("=" * 70)
    print("            LOGISTICS DELIVERY PERFORMANCE SQL ANALYTICS           ")
    print("=" * 70)
    
    for idx, (name, q_text) in enumerate(queries, 1):
        title = name if name else f"Query {idx}"
        print(f"\n>>> {idx}. {title}:")
        print("-" * (len(title) + 7))
        try:
            res_df = pd.read_sql_query(q_text, conn)
            # Format float numbers for better readability in prints
            for col in res_df.columns:
                if res_df[col].dtype == 'float64':
                    res_df[col] = res_df[col].round(2)
            print(res_df.to_string(index=False))
        except Exception as e:
            print(f"Execution Error: {e}")
        print("-" * 70)
        
    conn.close()

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'Delivery_Logistics.csv')
    sql_path = os.path.join(base_dir, 'sql', 'queries.sql')
    run_queries(csv_path, sql_path)
