import os
import uuid
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('DATABASE_URL')

engine = create_engine(url)

with engine.connect() as conn:
    print("Repairing Invite Codes...")
    # Get all events with NULL invite_code
    result = conn.execute(text("SELECT id FROM events WHERE invite_code IS NULL OR invite_code = '';"))
    events = result.fetchall()
    
    for row in events:
        new_code = str(uuid.uuid4())[:8].upper()
        conn.execute(text("UPDATE events SET invite_code = :code WHERE id = :id"), {"code": new_code, "id": row[0]})
        print(f" - Assigned {new_code} to Event ID {row[0]}")
    
    conn.commit()
    print("Repair Complete!")
