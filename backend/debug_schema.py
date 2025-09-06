import sqlite3

def inspect_database_schema():
    """Show complete articles table schema"""
    
    try:
        conn = sqlite3.connect('hopeshot_news.db')
        cursor = conn.cursor()
        
        # Get all columns in articles table
        cursor.execute('PRAGMA table_info(articles)')
        columns = cursor.fetchall()
        
        print("=== ARTICLES TABLE SCHEMA ===")
        print(f"Total columns: {len(columns)}")
        print()
        
        for i, col in enumerate(columns, 1):
            col_id, name, data_type, not_null, default_val, primary_key = col
            print(f"{i:2d}. {name:<25} {data_type:<15} {'NOT NULL' if not_null else ''} {'PK' if primary_key else ''}")
        
        # Show a sample row to see actual data structure
        cursor.execute('SELECT * FROM articles LIMIT 1')
        sample_row = cursor.fetchone()
        
        if sample_row:
            print("\n=== SAMPLE DATA ===")
            for i, (col_info, value) in enumerate(zip(columns, sample_row)):
                col_name = col_info[1]
                print(f"{col_name}: {value}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error inspecting schema: {e}")

if __name__ == "__main__":
    inspect_database_schema()