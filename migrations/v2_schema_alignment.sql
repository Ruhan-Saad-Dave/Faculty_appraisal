-- FINAL SUPABASE SCHEMA SYNC (V2)
-- Run this in your Supabase SQL Editor to align your database with the latest backend refactors.

-- 1. ADD MISSING SR_NO COLUMNS TO PART A TABLES
-- This ensures consistent ordering of entries as expected by the new schemas.
ALTER TABLE IF EXISTS public.annual_confidential_report ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.course_file ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.departmental_activities ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.industry_connect_activity ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.project ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.qualification_enhancement ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.contribution_to_society ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.student_feedback ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.innovative_teaching_methods ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.teaching_process ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.university_activities ADD COLUMN IF NOT EXISTS sr_no INTEGER;

-- 2. ALIGN ENCLOSURE & DECLARATION TABLES
-- Renames columns to match the refactored SQLAlchemy models and Pydantic schemas.
DO $$ 
BEGIN
    -- Update Enclosure table (enclosure_text_block)
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='enclosure_text_block' AND column_name='description') THEN
        ALTER TABLE public.enclosure_text_block RENAME COLUMN description TO enclosure_text;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='enclosure_text_block' AND column_name='document_url') THEN
        ALTER TABLE public.enclosure_text_block RENAME COLUMN document_url TO document;
    END IF;

    -- Update Declaration table (enclosure_declaration)
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='enclosure_declaration' AND column_name='date') THEN
        ALTER TABLE public.enclosure_declaration RENAME COLUMN date TO submission_date;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='enclosure_declaration' AND column_name='is_declared') THEN
        ALTER TABLE public.enclosure_declaration DROP COLUMN is_declared;
    END IF;
END $$;

-- 3. ENSURE PART B CONSISTENCY
-- Aligning 'issn_isbn' and 'issn_isbn_no' in published_papers
DO $$ 
BEGIN
    -- If both exist, drop the redundant 'issn_isbn' so we can use 'issn_isbn_no'
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='published_papers' AND column_name='issn_isbn') 
       AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='published_papers' AND column_name='issn_isbn_no') THEN
        ALTER TABLE public.published_papers DROP COLUMN issn_isbn;
    -- If only 'issn_isbn' exists, rename it to 'issn_isbn_no'
    ELSIF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='published_papers' AND column_name='issn_isbn') THEN
        ALTER TABLE public.published_papers RENAME COLUMN issn_isbn TO issn_isbn_no;
    END IF;
END $$;
