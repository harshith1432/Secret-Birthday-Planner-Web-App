import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('DATABASE_URL')

engine = create_engine(url)

with engine.connect() as conn:
    print("Migrating for Authentication...")
    
    # 1. Create users table
    try:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                unique_number VARCHAR(20) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()
        print("- Created 'users' table")
    except Exception as e:
        print(f"- users table: {e}")

    # 2. Add creator_id to events
    try:
        conn.execute(text("ALTER TABLE events ADD COLUMN creator_id INTEGER REFERENCES users(id) ON DELETE SET NULL;"))
        conn.commit()
        print("- Added 'creator_id' to events")
    except Exception as e:
        print(f"- creator_id column: {e}")
