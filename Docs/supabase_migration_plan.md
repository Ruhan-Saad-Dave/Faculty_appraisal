# Supabase Migration & PDF Upload Integration Plan

This document outlines the plan to migrate the Faculty Appraisal backend to Supabase and integrate PDF upload functionality for Part B categories.

## 1. Database Migration Strategy
Since the project already uses SQLAlchemy, we will continue using it to maintain compatibility with both Supabase and standard Postgres.
- **Action:** Update the `DATABASE_URL` in the `.env` file to point to your Supabase Postgres connection string.
- **Portability:** By using SQLAlchemy, we can switch between Supabase and any other Postgres provider by simply changing the `DATABASE_URL`.

## 2. PDF Upload Strategy (Supabase Storage)
We will use Supabase Storage to handle PDF uploads as it provides a secure and scalable way to manage files with Row Level Security (RLS).
- **Action:** Create a private bucket named `faculty-docs` in the Supabase Dashboard.
- **Implementation:** We will add a utility to handle uploads to Supabase Storage using the `supabase-py` SDK.
- **Database Storage:** We will store the relative path of the file in the `document` column of our tables.

## 3. Required Setup Steps

### A. Supabase Project Setup
1. Create a project on [Supabase](https://supabase.com/).
2. Go to **Database** -> **Connection string** -> **URI** and copy the URI.
3. Go to **Storage** and create a new bucket named `faculty-docs`. Set it to **Private**.
4. (Optional but Recommended) Set up RLS policies for the `faculty-docs` bucket as described in `@references/document.txt`.

### B. Environment Variables (`.env`)
Update or create your `.env` file with the following variables:

```dotenv
# Postgres Connection (Standard Postgres or Supabase)
DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@[YOUR-DB-HOST]:5432/postgres"

# Supabase Credentials for Storage & Auth
SUPABASE_URL="https://[YOUR-PROJECT-ID].supabase.co"
SUPABASE_ANON_KEY="[YOUR-ANON-KEY]"
```

## 4. Planned Code Changes

### Setup Updates
- **`src/setup/supabase_client.py`:** New utility to initialize the Supabase client.
- **`src/setup/database.py`:** Ensure it reads the updated `DATABASE_URL`.

### Part B API Updates
For each category in Part B (starting with Journal Publications):
- Update the `POST` and `PUT` endpoints to accept an `UploadFile`.
- Implement logic to upload the file to `faculty-docs/{faculty_id}/{filename}`.
- Store the resulting path/URL in the database.

## 5. Execution Steps
1. Create this plan (Done).
2. Set up the Supabase client utility.
3. Update Pydantic schemas to handle form data (for file uploads).
4. Update CRUD operations to handle the `document` field correctly.
5. Update API routers to handle `Multipart/form-data`.
6. Verify the implementation with tests.
