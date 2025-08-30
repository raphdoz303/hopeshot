import sqlite3
import os
from pathlib import Path

def create_database():
    """Create SQLite database with HopeShot schema matching GSheets"""
    
    # Create database in backend directory
    db_path = Path("hopeshot_news.db")
    
    # Connect to database (creates file if doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"🗄️ Creating database at: {db_path.absolute()}")
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # =========================================================================
    # 1. CATEGORIES TABLE
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            color TEXT,
            emoji TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # =========================================================================
    # 2. LOCATIONS TABLE (Hierarchical)
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            level TEXT NOT NULL CHECK (level IN ('continent', 'region', 'country')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES locations(id),
            UNIQUE(name, level)
        )
    """)
    
    # =========================================================================
    # 3. MAIN ARTICLES TABLE (Matches your 40-column GSheets)
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            -- Basic Article Data (9 fields)
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title TEXT NOT NULL,
            description TEXT,
            url_id TEXT NOT NULL UNIQUE,  -- For deduplication
            author TEXT,
            published_at TEXT,
            language TEXT,
            news_type TEXT,
            source_type TEXT,
            source_name TEXT,
            source_id TEXT,
            original_source TEXT,
            
            -- Sentiment Analysis (5 fields)
            uplift_score REAL,
            sentiment_positive INTEGER,
            sentiment_negative INTEGER,
            sentiment_neutral INTEGER,
            sentiment_confidence REAL,
            
            -- Target Emotions (6 fields) - 0.0 to 1.0 scores
            emotion_hope REAL,
            emotion_awe REAL,
            emotion_gratitude REAL,
            emotion_compassion REAL,
            emotion_relief REAL,
            emotion_joy REAL,
            
            -- Fact-checking Readiness (3 fields)
            source_credibility TEXT,
            fact_checkable_claims TEXT,
            evidence_quality TEXT,
            
            -- Content Analysis (4 fields)
            controversy_level TEXT,
            solution_focused TEXT,
            age_appropriate TEXT,
            truth_seeking TEXT,
            
            -- Geographic Analysis (2 new fields)
            geographical_impact_level TEXT,
            geographical_impact_location INTEGER,  -- FK to locations
            
            -- Enhanced Metadata (3 fields)
            reasoning TEXT,
            analyzer_type TEXT,
            
            -- A/B Testing Tracking (3 fields)
            prompt_id TEXT,
            prompt_name TEXT,
            
            -- Reserved fields for future expansion
            reserved1 TEXT,
            reserved2 TEXT,
            reserved3 TEXT,
            
            -- Foreign key constraint
            FOREIGN KEY (geographical_impact_location) REFERENCES locations(id)
        )
    """)
    
    # =========================================================================
    # 4. ARTICLE-CATEGORIES JUNCTION TABLE
    # =========================================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS article_categories (
            article_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY (article_id, category_id),
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        )
    """)
    
    # =========================================================================
    # 5. CREATE INDEXES FOR PERFORMANCE
    # =========================================================================
    
    # Primary lookup indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_url_id ON articles(url_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_timestamp ON articles(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_source_type ON articles(source_type)")
    
    # Sentiment analysis indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_uplift_score ON articles(uplift_score)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_emotion_hope ON articles(emotion_hope)")
    
    # Geographic indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_geo_level ON articles(geographical_impact_level)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_locations_level ON locations(level)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_locations_parent ON locations(parent_id)")
    
    # A/B Testing indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_prompt_id ON articles(prompt_id)")
    
    print("✅ Database schema created successfully!")
    print("\n📊 Tables created:")
    print("   • articles (main table with 40 columns)")
    print("   • categories (with metadata)")  
    print("   • locations (hierarchical)")
    print("   • article_categories (junction)")
    print("   • 8 performance indexes")
    
    conn.commit()
    return conn

if __name__ == "__main__":
    conn = create_database()
    
    # Show table info
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n🗃️ Database ready with {len(tables)} tables: {[t[0] for t in tables]}")
    
    conn.close()
    print("\n🚀 Ready for article storage!")