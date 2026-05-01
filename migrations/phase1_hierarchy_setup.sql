-- PHASE 1 MIGRATION: Multi-School Hierarchy & Status Tracking (CLEAN SYNC)

-- 1. Resolve 'college_name' conflict and align School Table
DO $$ 
BEGIN
    -- If the table exists and has the old 'college_name' column, rename it to 'name'
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='school' AND column_name='college_name') THEN
        -- If 'name' also exists, we might need to merge or drop. For a fresh setup, we'll drop 'college_name'
        -- but the error Detail showed 'name' was at index 3 and 'college_name' at index 2 (null).
        -- We will drop the NOT NULL constraint on college_name and then drop the column.
        ALTER TABLE public.school ALTER COLUMN college_name DROP NOT NULL;
        ALTER TABLE public.school DROP COLUMN college_name;
    END IF;

    -- Standard structure alignment
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'school') THEN
        CREATE TABLE public.school (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR UNIQUE NOT NULL,
            division VARCHAR NOT NULL,
            form_type VARCHAR DEFAULT 'Type 1'
        );
    ELSE
        -- Ensure columns exist
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='school' AND column_name='name') THEN
            ALTER TABLE public.school ADD COLUMN name VARCHAR UNIQUE;
            UPDATE public.school SET name = 'Default School' WHERE name IS NULL;
            ALTER TABLE public.school ALTER COLUMN name SET NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='school' AND column_name='division') THEN
            ALTER TABLE public.school ADD COLUMN division VARCHAR NOT NULL DEFAULT 'Engineering';
            ALTER TABLE public.school ALTER COLUMN division DROP DEFAULT;
        END IF;

        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='school' AND column_name='form_type') THEN
            ALTER TABLE public.school ADD COLUMN form_type VARCHAR DEFAULT 'Type 1';
        END IF;
    END IF;
END $$;

-- 2. Update Faculty Table
ALTER TABLE IF EXISTS public.faculty 
ADD COLUMN IF NOT EXISTS school_id UUID REFERENCES public.school(id);

-- 3. Create Appraisal Summary Tracking Table
CREATE TABLE IF NOT EXISTS public.appraisal_summary_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    faculty_id UUID UNIQUE REFERENCES public.faculty(id),
    academic_year VARCHAR(20) NOT NULL,
    status VARCHAR DEFAULT 'Pending',
    overall_score DOUBLE PRECISION DEFAULT 0.0,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Seed Schools (Initial Data based on hierarchi.txt)
-- We use INSERT ... ON CONFLICT to ensure we don't duplicate but update existing
INSERT INTO public.school (name, division, form_type) VALUES
('School of Computer Science, Engineering & Applications', 'Engineering', 'Type 1'),
('School of Commerce and Management', 'Non-Engineering', 'Type 1'),
('School of Bio-Engineering & Bio-Science', 'Engineering', 'Type 1'),
('School of Media & Communication Study', 'Non-Engineering', 'Type 2'),
('School of Design', 'Non-Engineering', 'Type 3'),
('School of Application Arts', 'Non-Engineering', 'Type 3'),
('School of Continual Education', 'Engineering', 'Type 1'),
('School of Engineering, Management & Research', 'Engineering', 'Type 1')
ON CONFLICT (name) DO UPDATE SET division = EXCLUDED.division, form_type = EXCLUDED.form_type;
