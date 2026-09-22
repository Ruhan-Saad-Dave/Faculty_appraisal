# DYPIU Keycloak SSO Integration Guide — Faculty Appraisal Backend

## Overview
This document serves as the central reference guide for the **Single Sign-On (SSO)** implementation in the Faculty Appraisal System.

The goal of this integration is to enable seamless authentication via **DYPIU Keycloak** (which uses **Google Workspace** as upstream identity provider). Users logged into the central portal (UniOne / DYPIU Portal) are redirected to the Faculty Appraisal System without needing to re-enter credentials or see the local login page.

---

## 1. Authentication & Identity Architecture

```text
UniOne / Central Portal / Browser
         ↓ OIDC Authorization Code Flow + PKCE
DYPIU Keycloak Realm
         ↓ Identity Federation
Google Workspace (@dypiu.ac.in)
         ↓
Keycloak Access Token (JWT)
         ↓ HTTP Header `Authorization: Bearer <access_token>`
Faculty Appraisal FastAPI Backend
         ↓
Resolve Keycloak `sub` → Existing Local `FacultyProfile`
         ↓
Local RBAC Authorization (Faculty, HOD, Director, Dean, VC, Admin)
```

### Key Principles:
1. **Separation of Concerns**: Keycloak verifies **who the user is** (`sub`, `email`), while the Faculty Appraisal database determines **what the user is authorized to do** (appraisal roles, school/department scoping, review workflows).
2. **Zero Direct Privilege Delegation**: Roles and permissions are *never* accepted from untrusted client input.
3. **Graceful Account Linking**: Existing faculty accounts with historical appraisal records are linked to Keycloak subjects upon their first authenticated session via institutional email matching.
4. **Environment Isolation**:
   - `ENVIRONMENT="production"`: Users authenticate exclusively via Keycloak SSO.
   - `ENVIRONMENT="testing"`: Local password authentication and test endpoints remain enabled since developers do not have direct access to the live Keycloak staging/production servers.

---

## 2. File System Changes & Code Structure

### Summary of Modified & Created Files

| File | Type | Purpose |
|---|---|---|
| `src/models/core.py` | Model | Added `keycloak_sub` column with unique index and validator to `FacultyProfile`. |
| `src/schema/core.py` | Schema | Added optional `keycloak_sub` to `FacultyProfileBase` and `FacultyProfileUpdate`. |
| `src/crud/core.py` | CRUD Helpers | Added `get_faculty_by_keycloak_sub()` and `resolve_and_link_keycloak_faculty()`. |
| `migrations/040_add_keycloak_sub_to_faculty_profiles.sql` | Migration | SQL upgrade script for live databases (safe, idempotent, partial unique index). |
| `alembic/versions/e1f2a3b4c5d6_add_keycloak_sub_to_faculty_profiles.py` | Migration | Alembic version script for automated container startup migrations. |
| `migrations/README.md` | Documentation | Updated migration tracking registry with migration 040. |
| `Docs/schema.sql` | Baseline Schema | Updated master SQL DDL schema for fresh installs. |
| `.env.example` & `.env` | Configuration | Added `ENVIRONMENT="testing"` variable. |
| `tests/test_sso_identity.py` | Automated Tests | Unit and integration tests covering Keycloak lookup and account linking logic. |

---

## 3. Database Schema & Migration Details

### `faculty_profiles` Table Addition
- **Column**: `keycloak_sub` (`VARCHAR` / `TEXT`, `NULLABLE`, `UNIQUE`, `INDEXED`).
- Stores the unique OIDC subject claim (`sub`) issued by Keycloak.

### Migration SQL (`migrations/040_add_keycloak_sub_to_faculty_profiles.sql`)
```sql
-- Safe for live DB upgrades: nullable initially, unique index on non-null values
ALTER TABLE public.faculty_profiles
ADD COLUMN IF NOT EXISTS keycloak_sub text default null;

CREATE UNIQUE INDEX IF NOT EXISTS idx_faculty_profiles_keycloak_sub
ON public.faculty_profiles (keycloak_sub)
WHERE keycloak_sub IS NOT NULL;
```

---

## 4. SSO User Resolution Logic

The resolution algorithm implemented in `src/crud/core.py` ensures seamless zero-touch onboarding for existing staff:

```python
async def resolve_and_link_keycloak_faculty(
    db: AsyncSession,
    keycloak_sub: str,
    email: Optional[str] = None
) -> Optional[FacultyProfile]:
```

### Step-by-Step Resolution Flow:
1. **Direct `keycloak_sub` Lookup**:
   Checks if a `FacultyProfile` already has `keycloak_sub == token.sub`. If found, returns the profile immediately.
2. **First-Time Linking via Verified Institutional Email**:
   If no profile is matched by `keycloak_sub` and `email` is present in the validated token:
   - Finds existing active profile with normalized lowercase email.
   - Saves `profile.keycloak_sub = token.sub` and commits the transaction.
   - All subsequent logins resolve directly via step 1.
3. **Access Denial for Unknown / Inactive Identities**:
   - If no local `FacultyProfile` exists with that institutional email: returns `None` (triggers HTTP `403 Forbidden` with explanation that no appraisal profile is configured).
   - If the matching local profile has `is_active == False`: returns `None` (triggers HTTP `403 Forbidden`).

---

## 5. Environment Configuration

In `.env` and `.env.example`:

```env
# --- Security & Environment Mode ---
USE_LOCAL_AUTH="true"
JWT_SECRET_KEY="your-secret-key"
ALLOW_MOCK_USER="false"

# Environment Mode:
# "production" -> Single Sign-On is the primary auth method.
# "testing"    -> Local email/password authentication remains active for testing without Keycloak access.
ENVIRONMENT="testing"
```

---

## 6. Verification and Testing

Automated test suite located at `tests/test_sso_identity.py`:
- `test_get_faculty_by_keycloak_sub_found`: Verifies direct lookup by linked subject claim.
- `test_get_faculty_by_keycloak_sub_not_found`: Verifies graceful `None` return for nonexistent / empty keys.
- `test_resolve_and_link_keycloak_faculty_first_time`: Validates first-time email match, database persistence of `keycloak_sub`, and subsequent sub-based lookup.
- `test_resolve_keycloak_faculty_unregistered_returns_none`: Ensures unknown institutional emails cannot access the system without prior admin provisioning.
- `test_resolve_keycloak_faculty_inactive_account_denied`: Ensures deactivated staff accounts are rejected.

### Running Tests
```bash
pytest tests/test_sso_identity.py tests/test_v1_auth.py tests/test_hierarchy_unit.py tests/test_v1_authority.py
```

---

## 7. Roadmap & Next Milestones

- **Milestone 2**: Keycloak configuration contract (`KEYCLOAK_ISSUER_URL`, `KEYCLOAK_CLIENT_ID`, `KEYCLOAK_AUDIENCE`).
- **Milestone 3**: Keycloak OIDC/JWKS cryptographic token validation & caching.
- **Milestone 4**: SSO User Resolution in `get_current_user()` dependency.
- **Milestone 5**: Full authorization regression verification across all roles (Faculty, HOD, Director, Dean, Registrar, VC, Admin).
- **Milestone 6**: Frontend OIDC Integration / handoff specs for redirect flow and token forwarding.
- **Milestone 7**: Legacy auth deprecation & cleanup before production cutover.
