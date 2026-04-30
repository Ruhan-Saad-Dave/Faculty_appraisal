from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Double, Date
from sqlalchemy.orm import relationship
from src.setup.database import Base
from src.models.Part_B.faculty import Faculty  # Import Faculty model for relationship

class ResearchGuidance(Base):
    __tablename__ = "research_guidance"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    degree = Column(String(20), nullable=False) # ME / PhD
    student_name = Column(String(255), nullable=False)
    submission_status = Column(String, nullable=False) # e.g., "Submitted", "Awarded"
    award_date = Column(Date, nullable=True) # Date of award, if applicable
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty", back_populates="research_guidance_entries")
