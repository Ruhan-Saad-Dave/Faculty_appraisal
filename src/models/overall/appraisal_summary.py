from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Double, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from src.setup.database import Base

class AppraisalStatus(str, enum.Enum):
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    HOD_APPROVED = "HOD Approved"
    DIRECTOR_APPROVED = "Director Approved"
    DEAN_APPROVED = "Dean Approved"
    FINALIZED = "Finalized"

class AppraisalSummary(Base):
    __tablename__ = "appraisal_summary_tracking"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id"), unique=True)
    academic_year = Column(String(20), nullable=False) # e.g., "2025-26"
    
    status = Column(Enum(AppraisalStatus), default=AppraisalStatus.PENDING)
    
    overall_score = Column(Double, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    faculty = relationship("Faculty")
