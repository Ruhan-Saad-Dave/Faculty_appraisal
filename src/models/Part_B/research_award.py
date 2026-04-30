from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Double, Date
from sqlalchemy.orm import relationship
from src.setup.database import Base
from src.models.Part_B.faculty import Faculty  # Import Faculty model for relationship

class ResearchAward(Base):
    __tablename__ = "research_awards"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    award_name = Column(Text, nullable=False)
    award_date = Column(Date, nullable=False)
    awarding_agency = Column(String(255), nullable=False)
    level = Column(String(50), nullable=False) # International / National
    research_score_faculty = Column(Double, default=0.0)
    research_score_hod = Column(Double, default=0.0)
    research_score_director = Column(Double, default=0.0)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty", back_populates="research_awards")
