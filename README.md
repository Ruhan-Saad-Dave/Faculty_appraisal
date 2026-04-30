# To run the FastAPI application:

1.  **Set up your Supabase project:**
    *   Create a project on Supabase.
    *   Configure Row Level Security (RLS) for your tables.

2.  **Configure the environment:**
    *   Create a `.env` file in the root directory.
    *   Add your Supabase credentials:
        ```dotenv
        DATABASE_URL="postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
        SUPABASE_URL="https://[PROJECT_ID].supabase.co"
        SUPABASE_ANON_KEY="your-anon-key"
        ```

3.  **Run the Database Migration:**
    *   **CRITICAL:** This project now uses UUIDs for all identifiers and matches a specific Supabase schema.
    *   Open your Supabase SQL Editor and run the contents of `migration_add_faculty_id.sql`.
    *   This adds the necessary `faculty_id` (UUID) columns to link records to faculty members.

4.  **Run the application:**
    *   Install dependencies: `uv sync`.
    *   Run with Uvicorn:
        ```bash
        uvicorn main:app --reload
        ```
    *   Access documentation at `http://127.0.0.1:8000/docs`.

**Important Changes:**
*   **UUID Identifiers:** All primary keys and `faculty_id` fields are now `UUID` strings.
*   **Schema Alignment:** Python table names now match the Supabase schema (e.g., `published_papers` instead of `journal_publications`).
*   **No Auto-Creation:** `Base.metadata.create_all` is disabled in `main.py`. Database changes must be handled via Supabase SQL Editor or migrations.