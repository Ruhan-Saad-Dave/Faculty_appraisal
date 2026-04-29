from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Double, Date
from sqlalchemy.orm import relationship
from ....setup.database import Base
from ..faculty import Faculty  # Import Faculty model for relationship

class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    project_name = Column(Text, nullable=False)
    funding_agency = Column(String(255), nullable=False)
    date_of_sanction = Column(Date, nullable=False)
    funding_amount = Column(Double, nullable=False)
    role = Column(String(50), nullable=False) # PI / Co-PI / Consultant
    project_status = Column(String(50), nullable=False) # Ongoing / Completed
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)

    faculty = relationship("Faculty", back_populates="research_projects")
