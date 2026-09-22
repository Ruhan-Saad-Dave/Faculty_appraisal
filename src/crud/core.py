from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from src.models.core import FacultyProfile, Declaration, AppraisalReview, FormSectionDefinition, AppraisalDocument
from src.schema.core import FacultyProfileCreate, FacultyProfileUpdate, DeclarationBase, AppraisalReviewBase
from typing import List, Optional
from uuid import UUID
import logging
import traceback

logger = logging.getLogger(__name__)

# --- Faculty Profile CRUD ---
async def get_faculty_by_email(db: AsyncSession, email: str) -> Optional[FacultyProfile]:
    try:
        clean_email = email.strip().lower()
        result = await db.execute(
            select(FacultyProfile)
            .where(func.lower(func.trim(FacultyProfile.email)) == clean_email)
            .order_by(
                FacultyProfile.is_active.desc(),
                FacultyProfile.is_verified.desc(),
                FacultyProfile.created_at.desc()
            )
        )
        profiles = result.scalars().all()
        if not profiles:
            return None
        if len(profiles) > 1:
            logger.warning(f"Multiple faculty profiles found for email {email}. Returning the most relevant active/verified one.")
        return profiles[0]
    except Exception as e:
        logger.error(f"Error fetching faculty by email {email}: {str(e)}")
        logger.error(traceback.format_exc())
        raise

async def get_faculty_by_keycloak_sub(db: AsyncSession, keycloak_sub: str) -> Optional[FacultyProfile]:
    """
    Look up a FacultyProfile by unique keycloak_sub OIDC claim.
    """
    if not keycloak_sub or not str(keycloak_sub).strip():
        return None
    try:
        clean_sub = str(keycloak_sub).strip()
        result = await db.execute(
            select(FacultyProfile)
            .where(FacultyProfile.keycloak_sub == clean_sub)
            .order_by(
                FacultyProfile.is_active.desc(),
                FacultyProfile.is_verified.desc(),
                FacultyProfile.created_at.desc()
            )
        )
        profiles = result.scalars().all()
        if not profiles:
            return None
        if len(profiles) > 1:
            logger.warning(f"Multiple faculty profiles found for keycloak_sub {keycloak_sub}. Returning the most relevant active/verified one.")
        return profiles[0]
    except Exception as e:
        logger.error(f"Error fetching faculty by keycloak_sub {keycloak_sub}: {str(e)}")
        logger.error(traceback.format_exc())
        raise

async def resolve_and_link_keycloak_faculty(
    db: AsyncSession,
    keycloak_sub: str,
    email: Optional[str] = None
) -> Optional[FacultyProfile]:
    """
    SSO User Resolution:
    1. Lookup by keycloak_sub.
    2. If not linked yet, lookup by verified institutional email.
    3. If exactly one active/local account matches, save the Keycloak sub.
    4. Future logins resolve by keycloak_sub.
    """
    if not keycloak_sub or not str(keycloak_sub).strip():
        return None

    clean_sub = str(keycloak_sub).strip()

    # 1. Lookup by keycloak_sub
    profile = await get_faculty_by_keycloak_sub(db, clean_sub)
    if profile:
        return profile

    # 2. If not linked yet and email is provided, lookup by verified institutional email
    if email and str(email).strip():
        clean_email = str(email).strip().lower()
        profile = await get_faculty_by_email(db, clean_email)
        if profile and profile.is_active:
            # 3. Save keycloak_sub to link the account
            try:
                profile.keycloak_sub = clean_sub
                await db.commit()
                await db.refresh(profile)
                logger.info(f"Successfully linked Keycloak sub '{clean_sub}' to profile email '{clean_email}' (id: {profile.id})")
                return profile
            except Exception as e:
                await db.rollback()
                logger.error(f"Error linking keycloak_sub {clean_sub} to email {clean_email}: {str(e)}")
                raise

    return None

async def create_faculty_profile(db: AsyncSession, profile_in: FacultyProfileCreate) -> FacultyProfile:
    db_profile = FacultyProfile(
        **profile_in.model_dump(exclude={'password'}),
        password_hash=profile_in.password
    )
    try:
        db.add(db_profile)
        await db.commit()
        await db.refresh(db_profile)
        return db_profile
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating faculty profile for {profile_in.email}: {str(e)}")
        logger.error(traceback.format_exc())
        raise

# --- Declaration (Appraisal Tracking) CRUD ---
async def get_declaration(db: AsyncSession, email: str, year: str) -> Optional[Declaration]:
    try:
        result = await db.execute(select(Declaration).where(
            Declaration.faculty_email == email,
            Declaration.academic_year == year
        ))
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error fetching declaration for {email}/{year}: {str(e)}")
        raise

async def create_or_update_declaration(db: AsyncSession, data: DeclarationBase) -> Declaration:
    db_decl = await get_declaration(db, data.faculty_email, data.academic_year)
    if db_decl:
        for key, value in data.model_dump(exclude={"submission_attempt"}).items():
            setattr(db_decl, key, value)
    else:
        db_decl = Declaration(**data.model_dump())
        db.add(db_decl)
    return db_decl

# --- Appraisal Review CRUD ---
async def get_reviews_by_faculty(db: AsyncSession, email: str, year: str) -> List[AppraisalReview]:
    try:
        result = await db.execute(select(AppraisalReview).where(
            AppraisalReview.faculty_email == email,
            AppraisalReview.academic_year == year
        ))
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error fetching reviews for {email}/{year}: {str(e)}")
        raise

async def create_or_update_review(db: AsyncSession, data: AppraisalReviewBase) -> AppraisalReview:
    try:
        result = await db.execute(select(AppraisalReview).where(
            AppraisalReview.faculty_email == data.faculty_email,
            AppraisalReview.academic_year == data.academic_year,
            AppraisalReview.reviewer_role == data.reviewer_role
        ))
        db_review = result.scalar_one_or_none()
        if db_review:
            for key, value in data.model_dump().items():
                setattr(db_review, key, value)
        else:
            db_review = AppraisalReview(**data.model_dump())
            db.add(db_review)
        return db_review
    except Exception as e:
        logger.error(f"Error in create_or_update_review for {data.faculty_email}: {str(e)}")
        logger.error(traceback.format_exc())
        raise

# --- Form Section Definition ---
async def get_section_definitions(db: AsyncSession, form_family: Optional[str] = None) -> List[FormSectionDefinition]:
    try:
        query = select(FormSectionDefinition)
        if form_family:
            query = query.where(FormSectionDefinition.form_family == form_family)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error fetching section definitions: {str(e)}")
        raise
