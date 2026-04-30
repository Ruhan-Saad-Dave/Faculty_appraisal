from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Double, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from src.setup.database import Base

class AppraisalRemarks(Base):
    __tablename__ = "appraisal_remarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id"))
    remarks = Column(String, nullable=True)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty")

class HODRemarks(Base):
    __tablename__ = "hod_remarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id"))
    hod_remark = Column(String, nullable=True)
    hod_approved_score = Column(Double, default=0.0)
    hod_signature = Column(String, nullable=True)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty")

class DirectorRemarks(Base):
    __tablename__ = "director_remarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id"))
    director_remark = Column(String, nullable=True)
    director_approved_score = Column(Double, default=0.0)
    director_signature = Column(String, nullable=True)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty")

class DeanRemarks(Base):
    __tablename__ = "dean_remarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id"))
    dean_remark = Column(String, nullable=True)
    dean_approved_score = Column(Double, default=0.0)
    dean_signature = Column(String, nullable=True)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty")

class FinalApproval(Base):
    __tablename__ = "final_approval"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id"))
    final_score = Column(Double, default=0.0)
    final_grade = Column(String, nullable=True)
    vc_approval = Column(String, nullable=True) # or Boolean as per schema
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty")
