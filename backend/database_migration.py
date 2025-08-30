import sqlite3
from pathlib import Path

def migrate_to_multi_location():
    """
    Migrate database from single location column to junction table approach
    """
    db_path = Path("hopeshot_news.db")
    
    if not db_path.exists():
        print("❌ Database not found. Run database_setup.py first.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔄 Migrating database to multi-location support...")
    
    try:
        # 1. Create article_locations junction table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS article_locations (
                article_id INTEGER,
                location_id INTEGER,
                PRIMARY KEY (article_id, location_id),
                FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
                FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE
            )
        """)
        print("✅ Created article_locations junction table")
        
        # 2. Create index for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_article_locations_article 
            ON article_locations(article_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_article_locations_location 
            ON article_locations(location_id)
        """)
        print("✅ Created junction table indexes")
        
        # 3. Check if we need to migrate existing data
        cursor.execute("SELECT COUNT(*) FROM articles")
        article_count = cursor.fetchone()[0]
        
        if article_count > 0:
            print(f"📊 Found {article_count} existing articles")
            
            # Migrate existing single location data to junction table
            cursor.execute("""
                INSERT INTO article_locations (article_id, location_id)
                SELECT id, geographical_impact_location 
                FROM articles 
                WHERE geographical_impact_location IS NOT NULL 
                AND geographical_impact_location != ''
            """)
            migrated_count = cursor.rowcount
            print(f"📋 Migrated {migrated_count} location relationships")
        
        # 4. Remove the single location column from articles table
        # SQLite doesn't support DROP COLUMN directly, so we'll keep it for now
        # In production, you'd create a new table without this column
        print("⚠️ geographical_impact_location column kept for backward compatibility")
        print("   (New articles will use junction table, old data preserved)")
        
        conn.commit()
        print("\n🚀 Migration completed successfully!")
        
        # Show final table structure
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        print(f"\n📋 Database now has {len(tables)} tables:")
        for table in tables:
            print(f"   • {table[0]}")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Migration failed: {e}")
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    success = migrate_to_multi_location()
    if success:
        print("\n🎯 Next step: Update DatabaseService to use junction table")
    else:
        print("\n❌ Fix migration errors before proceeding")