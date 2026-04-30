from sqlalchemy import Column, Integer, String, ForeignKey, Text, Double
from sqlalchemy.orm import relationship
from src.setup.database import Base
from src.models.Part_B.faculty import Faculty  # Import Faculty model for relationship

class SelfDevelopmentFDP(Base):
    __tablename__ = "self_development_fdp"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    program_name = Column(String(255), nullable=False)
    duration_days = Column(Integer, nullable=False)
    organizer = Column(String(255), nullable=False)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty", back_populates="self_development_fdp_entries")
