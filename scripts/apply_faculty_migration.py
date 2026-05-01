import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(override=True)
db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url)

with open('migrations/update_faculty_profile.sql') as f:
    sql = f.read()

with engine.connect() as conn:
    for statement in sql.split(';'):
        if statement.strip():
            conn.execute(text(statement.strip()))
            conn.commit()
print("Migration applied successfully")
