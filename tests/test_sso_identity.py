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
