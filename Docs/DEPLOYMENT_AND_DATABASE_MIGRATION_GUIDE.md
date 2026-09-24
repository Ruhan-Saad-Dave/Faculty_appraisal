# Complete Production Deployment, Database Migration & Restore Guide

> **Target Systems**: 
> - **Backend API**: `Faculty_appraisal` (FastAPI / PostgreSQL / SQLAlchemy)
> - **Faculty Frontend**: `Appraisal-form-2.0` (React / Vite / Tailwind)
> - **Admin Portal**: `pbas_admin` (React / Vite / Tailwind)
> - **Identity Provider**: Keycloak 24+ / Google Workspace SSO + Native Password Fallback

---

## Table of Contents
1. [Architecture & System Overview](#1-architecture--system-overview)
2. [Why Old Production Backups Caused Database Issues](#2-why-old-production-backups-caused-database-issues)
3. [Zero Data Loss Guarantee (Non-Destructive Design)](#3-zero-data-loss-guarantee-non-destructive-design)
4. [Database Upgrade & Self-Healing Utilities](#4-database-upgrade--self-healing-utilities)
5. [Step-by-Step Runbooks](#5-step-by-step-runbooks)
   - [Runbook A: Restoring Production Backup to Testing Server](#runbook-a-restoring-production-backup-to-testing-server)
   - [Runbook B: Deploying Dynamic Forms & SSO to Production](#runbook-b-deploying-dynamic-forms--sso-to-production)
   - [Runbook C: Local Developer Workstation Setup](#runbook-c-local-developer-workstation-setup)
6. [Environment Variables Matrix (.env Reference)](#6-environment-variables-matrix-env-reference)
7. [Troubleshooting & Emergency Playbook](#7-troubleshooting--emergency-playbook)

---

## 1. Architecture & System Overview

The Faculty Appraisal System v2.0 introduces two major architectural enhancements:
1. **Dynamic Form Builder & Multi-Track Schools**: Supports customizable sections, school-specific form variants (Standard, Creative Media, Creative Design, CISR), and dynamic Part D / Registrar workflows.
2. **Universal Single Sign-On (SSO)**: OIDC PKCE authentication via Keycloak and Google Workspace with seamless fallback to traditional email/password login for local developers and offline testing environments.

```mermaid
flowchart TD
    subgraph Users
        F[Faculty User]
        A[Admin / Reviewer]
        D[Local Developer]
    end

    subgraph Authentication
        KC[Keycloak / Google SSO]
        LP[Local Password Auth]
    end

    subgraph Frontend
        AF[Appraisal-form-2.0 :5173]
        AD[pbas_admin :5174]
    end

    subgraph Backend
        FA[Faculty_appraisal FastAPI :8000]
        DB[(PostgreSQL 15+)]
    end

    F -->|Production/Testing| KC
    A -->|Production/Testing| KC
    D -->|Localhost Fallback| LP

    KC --> AF
    KC --> AD
    LP --> AF
    LP --> AD

    AF -->|Bearer JWT| FA
    AD -->|Bearer JWT| FA
    FA --> DB
```

---

## 2. Why Old Production Backups Caused Database Issues

When an older production backup is restored onto a testing server running the newer codebase, database errors occur due to **schema divergence**:

### The Problem
The current backend code expects database tables and columns introduced in migrations `026` through `040`. The older production database dump lacks these objects:

| Missing Object | Impact on New Codebase |
| :--- | :--- |
| `custom_fields` (JSONB on 28 section tables) | Faculty submission queries crash with `column "custom_fields" does not exist`. |
| `schools` table columns (`form_variant`, `form_type`, `form_label`) | Routing faculty to the correct form variant fails on login. |
| `custom_section_rows` table | Custom form builder tables crash on load. |
| `form_section_definitions` table | Dynamic form configuration fails to load. |
| `faculty_profiles` columns (`keycloak_sub`, `is_active`, `reports_to_registrar`) | SSO identity linking fails with missing column errors. |
| `declarations` columns (`part_d_status`, `part_c_total`, `part_d_total`) | Part D approval workflow and score calculation fail. |

---

## 3. Zero Data Loss Guarantee (Non-Destructive Design)

**Upgrading the production database will NOT result in any data loss.**

All 40 migration scripts (`001` through `040`) follow strict non-destructive database principles:
1. **Additive Only**: Every column change uses `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` with safe default values (e.g., `DEFAULT '{}'::jsonb`, `DEFAULT 'standard'`, `DEFAULT TRUE`).
2. **Idempotent Tables**: All tables use `CREATE TABLE IF NOT EXISTS`.
3. **Safe Seeding**: Catalog inserts use `ON CONFLICT (code) DO NOTHING`.
4. **No Drop Commands**: There are **zero** `DROP TABLE` or `DROP COLUMN` commands.
5. **Historical Integrity**: All past faculty submissions (Part A, Part B, Part C, uploaded PDF proofs, reviewer scores, ACR records, declarations) remain 100% untouched.

---

## 4. Database Upgrade & Self-Healing Utilities

We have provided two automated layers to keep any database in sync:

### Layer 1: Self-Healing Auto-Migrations (`src/setup/database.py`)
On application startup, `run_auto_migrations()` automatically:
- Executes `Base.metadata.create_all` to build missing ORM tables.
- Applies direct `ADD COLUMN IF NOT EXISTS` patches for critical fields.
- Checks `schema_migrations` and applies any unapplied migration scripts (`001` to `040`).
- Self-heals: if a migration was recorded as applied in an older state but columns are missing in PostgreSQL, it automatically cleans up the ledger and re-applies the migration.

### Layer 2: Dedicated Upgrade CLI Utility (`scripts/upgrade_database.py`)
A standalone CLI script located at `Faculty_appraisal/scripts/upgrade_database.py`. It runs in seconds, applies all column patches, seeds the default schools catalog, and prints a data health report.

---

## 5. Step-by-Step Runbooks

### Runbook A: Restoring Production Backup to Testing Server

Use this procedure whenever you want to load a fresh production database dump into the testing server.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as SysAdmin / Developer
    participant TestDB as Testing PostgreSQL
    participant Script as upgrade_database.py
    participant App as FastAPI Backend

    Admin->>TestDB: 1. psql -f production_backup.sql (Restore Dump)
    Admin->>Script: 2. python scripts/upgrade_database.py
    Script->>TestDB: Add missing columns & custom_fields JSONB
    Script->>TestDB: Seed canonical schools catalog
    Script->>TestDB: Sync schema_migrations ledger
    Script-->>Admin: Prints Verification Health Report (Data Intact)
    Admin->>App: 3. Start/Restart Backend (uvicorn / systemctl)
```

#### Step 1: Restore the SQL Dump
```bash
# Drop and recreate clean test DB (optional, if performing fresh restore)
dropdb -h localhost -U postgres faculty_appraisal_test
createdb -h localhost -U postgres faculty_appraisal_test

# Restore the production backup dump
psql -h localhost -U postgres -d faculty_appraisal_test -f /path/to/production_backup.sql
```

#### Step 2: Run the Upgrade Script
```bash
cd Faculty_appraisal
python scripts/upgrade_database.py
```
*Expected Output:*
```text
========================================================
  FACULTY APPRAISAL DATABASE COMPATIBILITY UPGRADE
  Target: localhost/faculty_appraisal_test
========================================================

[1/5] Ensuring all base ORM tables exist...
      -> Core ORM tables verified.
[2/5] Applying non-destructive column upgrades...
      -> Column patches applied.
[3/5] Verifying schools catalog...
      -> Schools catalog verified.
[4/5] Synchronizing migrations ledger...
      -> Migration ledger in sync.
[5/5] Performing data health check...

========================================================
  UPGRADE VERIFICATION REPORT (DATA PRESERVED)
========================================================
  Faculty Profiles  : 342
  Declarations      : 310
  Appraisal Reviews : 285
  Configured Schools: 10
========================================================
  STATUS: [SUCCESS] Database is 100% compatible & ready!
```

#### Step 3: Start the Backend Service
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

---

### Runbook B: Deploying Dynamic Forms & SSO to Production

Follow this checklist when deploying the new release to the production server.

#### Pre-Deployment Checklist
- [ ] Ensure all unit/integration tests pass (`python -m pytest tests/` $\rightarrow$ 228 passed).
- [ ] Build production frontends (`npm run build` in both `Appraisal-form-2.0` and `pbas_admin`).
- [ ] Schedule a 5-minute maintenance window (optional, zero-downtime is supported).

#### Step 1: Take a Fresh Production Database Snapshot
```bash
# Dump the active production database before making changes
pg_dump -h localhost -U postgres -d faculty_appraisal_prod -F p -f /opt/backups/pre_v2_deploy_$(date +%F_%T).sql
```

#### Step 2: Pull Latest Code
```bash
# On the production server:
cd /opt/faculty_appraisal
git pull origin main
```

#### Step 3: Update Environment Variables (`.env`)
Ensure the Keycloak SSO variables are added to `/opt/faculty_appraisal/Faculty_appraisal/.env` (see Section 6 for full reference).

#### Step 4: Run the Database Upgrade Script
```bash
cd /opt/faculty_appraisal/Faculty_appraisal
python scripts/upgrade_database.py
```

#### Step 5: Deploy Frontend Builds & Restart Backend
```bash
# Restart the backend service
sudo systemctl restart faculty_appraisal
# or if using docker:
# docker compose restart backend

# Build and copy frontend distribution files to web root (Nginx)
cd /opt/faculty_appraisal/Appraisal-form-2.0
npm run build
sudo cp -r dist/* /var/www/faculty_appraisal/

cd /opt/faculty_appraisal/pbas_admin
npm run build
sudo cp -r dist/* /var/www/pbas_admin/

sudo systemctl reload nginx
```

#### Step 6: Post-Deployment Smoke Test
1. Log in via Keycloak SSO with a test faculty account.
2. Confirm existing historical appraisals (e.g. 2024-2025) open with all previous scores and files.
3. Open Admin Portal -> Form Configuration -> verify school form variants load.

---

### Runbook C: Local Developer Workstation Setup

Developers running the system locally do **not** need access to Keycloak SSO or production databases.

1. **Backend**:
   - In `Faculty_appraisal/.env`, set `SKIP_AUTO_MIGRATIONS=false`.
   - `KEYCLOAK_URL` can be left blank or omitted.
   - Run `python scripts/upgrade_database.py` once against local SQLite or local PostgreSQL.
2. **Frontends**:
   - In `Appraisal-form-2.0/.env` and `pbas_admin/.env`, omit `VITE_KEYCLOAK_URL`.
   - The UI will automatically hide the SSO button and present the standard email/password login form.

---

## 6. Environment Variables Matrix (.env Reference)

### 1. Backend (`Faculty_appraisal/.env`)

| Variable | Localhost / Developer | Testing Server | Production Server |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite+aiosqlite:///./test.db` or `postgresql+asyncpg://postgres:pass@localhost:5432/test_db` | `postgresql+asyncpg://user:pass@test-db:5432/appraisal_test` | `postgresql+asyncpg://user:pass@prod-db:5432/appraisal_prod` |
| `JWT_SECRET` | `local_dev_jwt_secret_key_32_chars_min` | `<strong-testing-jwt-secret>` | `<strong-production-jwt-secret>` |
| `CENTRAL_AUTH_ENABLED` | `false` | `true` | `true` |
| `KEYCLOAK_URL` | *(blank)* | `https://sso-test.dypiu.ac.in` | `https://sso.dypiu.ac.in` |
| `KEYCLOAK_REALM` | *(blank)* | `dypiu-realm` | `dypiu-realm` |
| `KEYCLOAK_CLIENT_ID` | *(blank)* | `pbas-appraisal` | `pbas-appraisal` |
| `KEYCLOAK_AUDIENCE` | *(blank)* | `pbas-appraisal` | `pbas-appraisal` |
| `UPLOAD_DIR` | `./uploads` | `/opt/faculty_appraisal/uploads` | `/opt/faculty_appraisal/uploads` |

---

### 2. Faculty Frontend (`Appraisal-form-2.0/.env`)

| Variable | Localhost / Developer | Testing Server | Production Server |
| :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | `http://localhost:8000/api/v1` | `https://test-api.appraisal.dypiu.ac.in/api/v1` | `https://api.appraisal.dypiu.ac.in/api/v1` |
| `VITE_KEYCLOAK_URL` | *(omit to enable password login)* | `https://sso-test.dypiu.ac.in` | `https://sso.dypiu.ac.in` |
| `VITE_KEYCLOAK_REALM`| *(omit)* | `dypiu-realm` | `dypiu-realm` |
| `VITE_KEYCLOAK_CLIENT_ID`| *(omit)* | `pbas-frontend` | `pbas-frontend` |
| `VITE_KEYCLOAK_REDIRECT_URI`| *(omit)* | `https://test.appraisal.dypiu.ac.in/login` | `https://appraisal.dypiu.ac.in/login` |

---

### 3. Admin Portal (`pbas_admin/.env`)

| Variable | Localhost / Developer | Testing Server | Production Server |
| :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | `http://localhost:8000/api/v1` | `https://test-api.appraisal.dypiu.ac.in/api/v1` | `https://api.appraisal.dypiu.ac.in/api/v1` |
| `VITE_KEYCLOAK_URL` | *(omit to enable password login)* | `https://sso-test.dypiu.ac.in` | `https://sso.dypiu.ac.in` |
| `VITE_KEYCLOAK_REALM`| *(omit)* | `dypiu-realm` | `dypiu-realm` |
| `VITE_KEYCLOAK_CLIENT_ID`| *(omit)* | `pbas-admin` | `pbas-admin` |
| `VITE_KEYCLOAK_REDIRECT_URI`| *(omit)* | `https://test-admin.appraisal.dypiu.ac.in/login` | `https://admin.appraisal.dypiu.ac.in/login` |

---

## 7. Troubleshooting & Emergency Playbook

### Issue 1: `column "custom_fields" of relation "teaching_process" does not exist`
- **Cause**: Database dump was restored without running schema upgrades.
- **Fix**: Run `python scripts/upgrade_database.py` in the `Faculty_appraisal` directory.

### Issue 2: `403 Forbidden: User not assigned to any school` on SSO Login
- **Cause**: The user logged in with a valid Google/Keycloak email, but their email does not exist in `faculty_profiles` or their `school` is `NULL`.
- **Fix**: Admin must register or assign the faculty member's email to a valid School in the Admin Portal.

### Issue 3: `401 Unauthorized: Keycloak JWKS public key decode failed`
- **Cause**: The backend could not fetch the JWKS key from Keycloak (network issue or wrong realm/URL).
- **Fix**: Verify `KEYCLOAK_URL` and `KEYCLOAK_REALM` in `.env`. Ensure the backend server can reach `https://<KEYCLOAK_URL>/realms/<REALM>/protocol/openid-connect/certs`.

### Issue 4: Emergency Rollback
If you ever need to rollback to the pre-deployment state:
```bash
# 1. Restore the pre-deployment database dump
psql -h localhost -U postgres -d faculty_appraisal_prod -f /opt/backups/pre_v2_deploy_<timestamp>.sql

# 2. Checkout the previous stable git commit
git checkout <previous-stable-tag-or-commit>

# 3. Restart services
sudo systemctl restart faculty_appraisal
```
