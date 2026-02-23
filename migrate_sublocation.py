import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('DATABASE_URL')

engine = create_engine(url)

with engine.connect() as conn:
    print("Checking for 'sub_location' column...")
    try:
        conn.execute(text("ALTER TABLE events ADD COLUMN sub_location VARCHAR(100) DEFAULT '';"))
        conn.commit()
        print("Column 'sub_location' added successfully!")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("Column 'sub_location' already exists.")
        else:
            print(f"Error: {e}")
