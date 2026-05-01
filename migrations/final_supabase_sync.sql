-- FINAL SUPABASE SCHEMA SYNC MIGRATION
-- This script adds missing columns to existing tables to align with the SQLAlchemy models.
-- It ensures every Part A and Part B category table has: faculty_id, sr_no, department, and document.

-- 0. Update Faculty table
ALTER TABLE IF EXISTS public.faculty 
ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'faculty';

-- 1. Part A Category Tables
-- 1.1 ACR
ALTER TABLE IF EXISTS public.annual_confidential_report 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.2 Course File
ALTER TABLE IF EXISTS public.course_file 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.3 Departmental Activities
ALTER TABLE IF EXISTS public.departmental_activities 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.4 Industry Connect Activity
ALTER TABLE IF EXISTS public.industry_connect_activity 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.5 Project (Part A)
ALTER TABLE IF EXISTS public.project 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.6 Qualification Enhancement
ALTER TABLE IF EXISTS public.qualification_enhancement 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.7 Social Contributions (Contribution to Society)
ALTER TABLE IF EXISTS public.contribution_to_society 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.8 Student Feedback
ALTER TABLE IF EXISTS public.student_feedback 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.9 Teaching Methods (Innovative Teaching Methods)
ALTER TABLE IF EXISTS public.innovative_teaching_methods 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.10 Teaching Process
ALTER TABLE IF EXISTS public.teaching_process 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 1.11 University Activities
ALTER TABLE IF EXISTS public.university_activities 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;


-- 2. Part B Category Tables
-- 2.1 Journal Publications (Published Papers)
ALTER TABLE IF EXISTS public.published_papers 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.2 Book Publications
ALTER TABLE IF EXISTS public.book_publications 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.3 Conference Paper (Academic Events)
ALTER TABLE IF EXISTS public.academic_events 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.4 ICT Pedagogy (ICT Teaching Content)
ALTER TABLE IF EXISTS public.ict_teaching_content 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.5 Industrial Training
ALTER TABLE IF EXISTS public.industrial_training 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.6 IPR
ALTER TABLE IF EXISTS public.ipr 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.7 Product Development (Products Developed)
ALTER TABLE IF EXISTS public.products_developed 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.8 Research Awards
ALTER TABLE IF EXISTS public.research_awards 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.9 Research Guidance
ALTER TABLE IF EXISTS public.research_guidance 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.10 Research Projects
ALTER TABLE IF EXISTS public.research_projects 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.11 Research Proposals
ALTER TABLE IF EXISTS public.research_proposals 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 2.12 Self Development (FDP)
ALTER TABLE IF EXISTS public.self_development 
ADD COLUMN IF NOT EXISTS faculty_id UUID REFERENCES public.faculty(id),
ADD COLUMN IF NOT EXISTS sr_no INTEGER,
ADD COLUMN IF NOT EXISTS department VARCHAR,
ADD COLUMN IF NOT EXISTS document VARCHAR;

-- 3. Overall / Remarks Tables (Already mostly correct in schema.txt, but adding sr_no for consistency if requested)
-- Note: User specifically asked for Part A and Part B tables. 
-- These overall tables already have faculty_id and department/document in schema.txt.
-- Adding sr_no just in case.

ALTER TABLE IF EXISTS public.appraisal_remarks ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.hod_remarks ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.director_remarks ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.dean_remarks ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.final_approval ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.enclosure_declaration ADD COLUMN IF NOT EXISTS sr_no INTEGER;
ALTER TABLE IF EXISTS public.enclosure_text_block ADD COLUMN IF NOT EXISTS sr_no INTEGER;
