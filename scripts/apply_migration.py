import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

def run_migration():
    if not DATABASE_URL:
        print("DATABASE_URL not found in .env")
        return

    engine = create_engine(DATABASE_URL)
    
    migration_sql = """
    -- FINAL SUPABASE SCHEMA SYNC
    ALTER TABLE IF EXISTS public.faculty ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'faculty';

    -- Adding missing columns to category tables
    DO $$ 
    DECLARE 
        t text;
    BEGIN
        FOR t IN SELECT table_name 
                 FROM information_schema.tables 
                 WHERE table_schema = 'public' 
                 AND table_name IN (
                     'teaching_process', 'course_file', 'innovative_teaching_methods', 
                     'project', 'qualification_enhancement', 'student_feedback', 
                     'departmental_activities', 'university_activities', 
                     'contribution_to_society', 'industry_connect_activity', 
                     'annual_confidential_report', 'published_papers', 
                     'book_publications', 'ict_teaching_content', 
                     'research_guidance', 'research_projects', 'ipr', 
                     'research_awards', 'academic_events', 'research_proposals', 
                     'products_developed', 'self_development', 'industrial_training'
                 )
        LOOP
            EXECUTE format('ALTER TABLE public.%I ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id)', t);
            EXECUTE format('ALTER TABLE public.%I ADD COLUMN IF NOT EXISTS sr_no INTEGER', t);
            EXECUTE format('ALTER TABLE public.%I ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP', t);
            EXECUTE format('ALTER TABLE public.%I ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP', t);
        END LOOP;
    END $$;
    """

    print("Running migration on Supabase...")
    try:
        with engine.connect() as conn:
            conn.execute(text(migration_sql))
            conn.commit()
        print("Migration successful!")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    run_migration()
