"""
Tests for Milestone 1: Keycloak SSO Identity Mapping in FacultyProfile and CRUD helpers.
"""

import pytest
from sqlalchemy import select
from src.setup.database import AsyncSessionLocal
from src.models.core import FacultyProfile
from src.crud.core import (
    get_faculty_by_email,
    get_faculty_by_keycloak_sub,
    resolve_and_link_keycloak_faculty,
)
from src.setup.local_auth import get_password_hash

SSO_TEST_EMAIL = "sso_user@test.com"
SSO_KEYCLOAK_SUB = "dypiu-keycloak-sub-12345"
PASSWORD = "testpassword123"


async def _seed_user(email: str, keycloak_sub: str = None, is_active: bool = True):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(FacultyProfile).where(FacultyProfile.email == email))
        user = result.scalar_one_or_none()
        if not user:
            user = FacultyProfile(
                email=email,
                password_hash=get_password_hash(PASSWORD),
                full_name="SSO Test User",
                appraisal_role="faculty",
                school="SoCSEA",
                department="Computer Science",
                is_verified=True,
                is_active=is_active,
                keycloak_sub=keycloak_sub,
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user


@pytest.mark.asyncio
async def test_get_faculty_by_keycloak_sub_found(db):
    await _seed_user("linked_user@test.com", keycloak_sub="sub-abc-999")
    profile = await get_faculty_by_keycloak_sub(db, "sub-abc-999")
    assert profile is not None
    assert profile.email == "linked_user@test.com"
    assert profile.keycloak_sub == "sub-abc-999"


@pytest.mark.asyncio
async def test_get_faculty_by_keycloak_sub_not_found(db):
    profile = await get_faculty_by_keycloak_sub(db, "non-existent-sub")
    assert profile is None

    # Empty and whitespace inputs should return None safely
    assert await get_faculty_by_keycloak_sub(db, "") is None
    assert await get_faculty_by_keycloak_sub(db, "   ") is None
    assert await get_faculty_by_keycloak_sub(db, None) is None


@pytest.mark.asyncio
async def test_resolve_and_link_keycloak_faculty_first_time(db):
    # User exists by institutional email, but keycloak_sub is not yet linked
    await _seed_user(SSO_TEST_EMAIL, keycloak_sub=None)

    # Initial resolve by SSO token claims (sub + email)
    resolved = await resolve_and_link_keycloak_faculty(
        db, keycloak_sub=SSO_KEYCLOAK_SUB, email=SSO_TEST_EMAIL.upper()
    )
    assert resolved is not None
    assert resolved.email == SSO_TEST_EMAIL
    assert resolved.keycloak_sub == SSO_KEYCLOAK_SUB

    # Verify DB persistence
    db_profile = await get_faculty_by_email(db, SSO_TEST_EMAIL)
    assert db_profile.keycloak_sub == SSO_KEYCLOAK_SUB

    # Subsequent resolve should resolve directly via keycloak_sub even without email
    subsequent = await resolve_and_link_keycloak_faculty(
        db, keycloak_sub=SSO_KEYCLOAK_SUB, email=None
    )
    assert subsequent is not None
    assert subsequent.id == resolved.id
    assert subsequent.keycloak_sub == SSO_KEYCLOAK_SUB


@pytest.mark.asyncio
async def test_resolve_keycloak_faculty_unregistered_returns_none(db):
    # Unregistered user identity should not auto-create account
    resolved = await resolve_and_link_keycloak_faculty(
        db, keycloak_sub="unknown-sub-999", email="unknown_user@test.com"
    )
    assert resolved is None


@pytest.mark.asyncio
async def test_resolve_keycloak_faculty_inactive_account_denied(db):
    # Inactive account exists
    await _seed_user("inactive_sso@test.com", keycloak_sub=None, is_active=False)

    resolved = await resolve_and_link_keycloak_faculty(
        db, keycloak_sub="inactive-sub-000", email="inactive_sso@test.com"
    )
    assert resolved is None


# ---------------------------------------------------------------------------
# API Integration Tests for SSO Bearer Tokens (Milestone 8)
# ---------------------------------------------------------------------------

import jwt
import os
from datetime import datetime, timedelta

TEST_CENTRAL_SECRET = "test-central-sso-secret-key-123456789"


def _make_central_token(
    sub: str = "keycloak-sub-test-1",
    email: str = "api_sso_user@test.com",
    expired: bool = False,
    extra: dict = None,
) -> str:
    """Helper to generate a central JWT for testing."""
    os.environ["CENTRAL_JWT_SECRET"] = TEST_CENTRAL_SECRET
    os.environ["CENTRAL_ALGORITHM"] = "HS256"

    payload = {
        "sub": sub,
        "email": email,
        "exp": datetime.utcnow() + (timedelta(seconds=-10) if expired else timedelta(hours=1)),
        "iat": datetime.utcnow(),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, TEST_CENTRAL_SECRET, algorithm="HS256")


@pytest.mark.asyncio
async def test_sso_api_first_login_links_and_succeeds(client):
    # 1. Seed user with institutional email and NO keycloak_sub
    email = "first_sso_login@test.com"
    sub = "kc-sub-first-login-001"
    await _seed_user(email, keycloak_sub=None)

    # 2. Call GET /auth/me with valid central SSO bearer token
    token = _make_central_token(sub=sub, email=email)
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == email
    assert body["appraisal_role"] == "faculty"

    # 3. Verify keycloak_sub was persisted in DB
    async with AsyncSessionLocal() as db:
        profile = await get_faculty_by_email(db, email)
        assert profile.keycloak_sub == sub


@pytest.mark.asyncio
async def test_sso_api_subsequent_login_by_sub(client):
    # Seed user already linked to a keycloak_sub
    email = "linked_sso_user@test.com"
    sub = "kc-sub-linked-002"
    await _seed_user(email, keycloak_sub=sub)

    # Call with matching sub
    token = _make_central_token(sub=sub, email=email)
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    assert resp.json()["email"] == email


@pytest.mark.asyncio
async def test_sso_api_unassigned_user_returns_403(client):
    # Token for user who has NO FacultyProfile in local DB
    token = _make_central_token(sub="kc-sub-unknown-999", email="stranger@test.com")
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 403
    assert "no Faculty Appraisal account is assigned" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_sso_api_inactive_user_returns_403(client):
    # User exists but is_active=False
    email = "disabled_user@test.com"
    sub = "kc-sub-disabled-003"
    await _seed_user(email, keycloak_sub=sub, is_active=False)

    token = _make_central_token(sub=sub, email=email)
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 403
    assert "inactive" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_sso_api_expired_token_returns_401(client):
    email = "expired_token_user@test.com"
    await _seed_user(email)

    token = _make_central_token(email=email, expired=True)
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_sso_api_invalid_signature_returns_401(client):
    email = "forged_token_user@test.com"
    await _seed_user(email)

    # Signed with wrong secret
    forged_token = jwt.encode(
        {"sub": "forged-sub", "email": email, "exp": datetime.utcnow() + timedelta(hours=1)},
        "wrong-secret-key-xyz",
        algorithm="HS256",
    )
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {forged_token}"})

    assert resp.status_code == 401

