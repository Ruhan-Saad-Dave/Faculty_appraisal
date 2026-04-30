from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from src.setup.database import Base

class Enclosure(Base):
    __tablename__ = "enclosure_text_block"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id"))
    enclosure_text = Column(Text)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty")

class Declaration(Base):
    __tablename__ = "enclosure_declaration"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id"), unique=True)
    designation = Column(String)
    place = Column(String)
    submission_date = Column(Date, default=datetime.utcnow)
    faculty_signature = Column(String, nullable=True)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty")
