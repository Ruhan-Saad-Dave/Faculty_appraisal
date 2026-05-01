-- MIGRATION: Expand Faculty Profile with Institutional Fields
-- Based on Docs/faculty.txt

ALTER TABLE IF EXISTS public.faculty 
ADD COLUMN IF NOT EXISTS employee_id VARCHAR UNIQUE,
ADD COLUMN IF NOT EXISTS designation VARCHAR,
ADD COLUMN IF NOT EXISTS qualification VARCHAR,
ADD COLUMN IF NOT EXISTS experience INTEGER, -- Years of teaching experience
ADD COLUMN IF NOT EXISTS phone VARCHAR,
ADD COLUMN IF NOT EXISTS academic_year VARCHAR; -- Current Academic Year for the profile

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_faculty_employee_id ON public.faculty(employee_id);
