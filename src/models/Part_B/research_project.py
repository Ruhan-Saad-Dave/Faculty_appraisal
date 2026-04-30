from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Double, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.setup.database import Base

class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id"))
    project_name = Column(Text, nullable=False)
    funding_agency = Column(String(255), nullable=False)
    date_of_sanction = Column(Date, nullable=False)
    funding_amount = Column(Double, nullable=False)
    role = Column(String(50), nullable=False) # PI / Co-PI / Consultant
    project_status = Column(String(50), nullable=False) # Ongoing / Completed
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty", back_populates="research_projects")
