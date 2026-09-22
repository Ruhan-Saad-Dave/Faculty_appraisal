-- Migration 040: Add keycloak_sub to faculty_profiles
-- Used for DYPIU Keycloak SSO identity linking.
-- Safe for live DB upgrades: nullable initially, unique index on non-null values.

ALTER TABLE public.faculty_profiles
ADD COLUMN IF NOT EXISTS keycloak_sub text default null;

CREATE UNIQUE INDEX IF NOT EXISTS idx_faculty_profiles_keycloak_sub
ON public.faculty_profiles (keycloak_sub)
WHERE keycloak_sub IS NOT NULL;
