import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('DATABASE_URL')

engine = create_engine(url)

with engine.connect() as conn:
    print("Migrating for Group Collaboration...")
    
    # 1. Add invite_code to events
    try:
        conn.execute(text("ALTER TABLE events ADD COLUMN invite_code VARCHAR(20) UNIQUE;"))
        conn.commit()
        print("- Added 'invite_code' to events")
    except Exception as e:
        print(f"- invite_code column: {e}")

    # 2. Create group_members table
    try:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS group_members (
                id SERIAL PRIMARY KEY,
                event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
                name VARCHAR(100) NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()
        print("- Created 'group_members' table")
    except Exception as e:
        print(f"- group_members table: {e}")

    # 3. Create chat_messages table
    try:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id SERIAL PRIMARY KEY,
                event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
                sender_name VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()
        print("- Created 'chat_messages' table")
    except Exception as e:
        print(f"- chat_messages table: {e}")
