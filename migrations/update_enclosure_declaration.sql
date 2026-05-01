-- MIGRATION: Align Supabase schema with recent code changes in Enclosure and Declaration models
-- And add missing sr_no columns to Part A tables for consistency.

-- 1. Update Enclosure table (enclosure_text_block)
-- Note: Re-adding enclosure_text if it was accidentally named description in code but enclosure_text in SQL
-- In schema.txt it's already enclosure_text, but the code was using description.
-- Let's make sure the column exists and is named enclosure_text.
ALTER TABLE IF EXISTS public.enclosure_text_block RENAME COLUMN description TO enclosure_text;
ALTER TABLE IF EXISTS public.enclosure_text_block RENAME COLUMN document_url TO document;

-- 2. Update Declaration table (enclosure_declaration)
ALTER TABLE IF EXISTS public.enclosure_declaration DROP COLUMN IF EXISTS is_declared;
ALTER TABLE IF EXISTS public.enclosure_declaration RENAME COLUMN date TO submission_date;

-- 3. Add missing sr_no to Part A tables (some might already have it from previous partial syncs)
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
