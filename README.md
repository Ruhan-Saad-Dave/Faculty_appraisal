# Faculty Appraisal System - Backend API

A high-performance FastAPI backend designed for institutional faculty appraisals across 8 schools. Featuring a multi-level hierarchical reporting system, dynamic form handling, and Supabase integration.

## 🚀 Key Features
- **Hierarchical Access Control:** Strict VC > Dean > Director > HOD > Faculty authorization logic.
- **Horizontal Data Isolation:** Departments and Schools are strictly isolated to prevent data leaks.
- **Dynamic Form Support:** Handles three distinct appraisal form types (Standard, Media, Arts/Design).
- **Submission Tracking:** Real-time dashboard for authorities to monitor appraisal progress.
- **Production Hardened:** Dockerized with `uv`, optimized for GCP hosting, and non-root security.

## 🛠 Tech Stack
- **Framework:** FastAPI (Python 3.12+)
- **Package Manager:** `uv` (Fast and reliable)
- **Database:** PostgreSQL (via Supabase)
- **Auth & Storage:** Supabase (JWT-based session management & PDF proofs)
- **Testing:** Pytest with Async support

## 📋 Prerequisites
- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) installed on your system
- A Supabase project with a `faculty-docs` storage bucket

## ⚙️ Setup & Installation

1.  **Configure Environment:**
    Create a `.env` file in the root:
    ```dotenv
    DATABASE_URL="postgresql://postgres.[ID]:[PWD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
    SUPABASE_URL="https://[ID].supabase.co"
    SUPABASE_ANON_KEY="your-anon-key"
    ```

2.  **Initialize Database:**
    Open your Supabase SQL Editor and run the scripts in order:
    - `migrations/phase1_hierarchy_setup.sql` (Creates Schools and Tracking)
    - `migrations/v2_schema_alignment.sql` (Fixes columns and names)

3.  **Run Locally:**
    ```bash
    # Install dependencies
    uv sync
    # Start the server
    uv run uvicorn main:app --reload
    ```

4.  **Testing:**
    ```bash
    $env:PYTHONPATH="."
    uv run pytest
    ```

## 🏗 Deployment (GCP)
This project is pre-configured for GCP (Cloud Run or GCE):
- **Dockerfile:** Optimized multi-stage build using `uv`.
- **Port:** Exposes `8000`.
- **Security:** Runs as a non-privileged `appuser`.

To build the image:
```bash
docker build -t faculty-appraisal-backend .
```

## 📚 Documentation
For detailed guides, please refer to the `Docs/` directory:
- [Developer Architecture Guide](Docs/DEVELOPER_GUIDE.md)
- [Frontend API Reference](Docs/FRONTEND_API_REFERENCE.md)
- [Testing Guide](Docs/testing_guide.md)

## ⚖️ License
Internal Institutional Use Only.
