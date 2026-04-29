from sqlalchemy import Column, Integer, String, ForeignKey, Text, Double
from sqlalchemy.orm import relationship
from ....setup.database import Base
from ..faculty import Faculty  # Import Faculty model for relationship

class IndustrialTraining(Base):
    __tablename__ = "industrial_trainings"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    company_industry = Column(String(255), nullable=False)
    duration_days = Column(Integer, nullable=False)
    nature_of_training = Column(Text, nullable=False)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)

    faculty = relationship("Faculty", back_populates="industrial_trainings")
