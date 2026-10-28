"""
04_Supply_Chain_DataCo: Database Builder & Query Test Runner
Builds local supply_chain.db from star-schema CSVs and executes analytical KPI queries.
"""

import os
import sys
import time
import sqlite3
import pandas as pd

def build_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)
    db_path = os.path.join(base_dir, "supply_chain.db")
    schema_path = os.path.join(base_dir, "schema.sql")
    queries_path = os.path.join(base_dir, "queries.sql")
    clean_dir = os.path.join(project_dir, "data", "clean")

    # If data/clean doesn't exist, generate data first
    if not os.path.exists(os.path.join(clean_dir, "fact_order_items.csv")):
        print("Data files not found. Running generate_data.py...")
        gen_script = os.path.join(project_dir, "data", "generate_data.py")
        import subprocess
        subprocess.check_call([sys.executable, gen_script, "--samples", "25000"])

    print(f"Building SQLite database at: {db_path}...")
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Execute DDL Schema
    print("Executing schema.sql...")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    print("Star-schema tables and views created successfully.")

    # 2. Ingest Dimensional CSVs
    table_csv_map = [
        ("Dim_Customer", "dim_customer.csv"),
        ("Dim_Product", "dim_product.csv"),
        ("Dim_Shipping", "dim_shipping.csv"),
        ("Dim_Geography", "dim_geography.csv"),
        ("Dim_Date", "dim_date.csv"),
        ("Dim_Order_Status", "dim_order_status.csv"),
        ("Fact_Order_Items", "fact_order_items.csv")
    ]

    for table_name, csv_file in table_csv_map:
        csv_path = os.path.join(clean_dir, csv_file)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Missing required CSV: {csv_path}")
        df = pd.read_csv(csv_path, encoding="utf-8")
        df.to_sql(table_name, conn, if_exists="append", index=False)
        row_count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"Loaded {row_count:,} rows into {table_name}")

    conn.commit()

    # 3. Test View
    view_count = cursor.execute("SELECT COUNT(*) FROM vw_supply_chain_master").fetchone()[0]
    print(f"Verified vw_supply_chain_master: {view_count:,} total records.")

    # 4. Execute Analytical Queries from queries.sql
    print("\n" + "="*80)
    print("EXECUTING ANALYTICAL QUERIES (queries.sql)")
    print("="*80)

    with open(queries_path, "r", encoding="utf-8") as f:
        raw_queries = f.read()

    # Split queries by semicolon (preserving comments and CTEs)
    raw_blocks = [q.strip() for q in raw_queries.split(";") if q.strip()]
    individual_queries = []
    for b in raw_blocks:
        # Strip leading comments to verify there's actual SQL
        lines = [line for line in b.splitlines() if not line.strip().startswith("--")]
        if any(line.strip() for line in lines):
            individual_queries.append(b)

    query_titles = [
        "Query 1: OTIF %, Late-Delivery Rate & Delay Gap by Shipping Mode & Market",
        "Query 2: Product Category Profitability & Negative-Profit Order Concentration",
        "Query 3: Discount Banding vs Operating Profitability Matrix",
        "Query 4: Month-over-Month (MoM) Order Volume & Revenue Trend (LAG)",
        "Query 5: Top 10 Regional Fulfillment Bottlenecks"
    ]

    for idx, sql in enumerate(individual_queries):
        if idx >= len(query_titles):
            title = f"Query {idx+1}"
        else:
            title = query_titles[idx]

        print(f"\n--- {title} ---")
        t0 = time.time()
        try:
            res_df = pd.read_sql_query(sql, conn)
            elapsed = (time.time() - t0) * 1000
            print(f"Execution time: {elapsed:.2f} ms | Rows returned: {len(res_df)}")
            print(res_df.head(6).to_string(index=False))
        except Exception as e:
            print(f"Error executing query {idx+1}: {e}")
            raise e

    conn.close()
    print("\nDatabase build and query execution complete! (Exit code 0)")
    return 0

if __name__ == "__main__":
    sys.exit(build_database())
