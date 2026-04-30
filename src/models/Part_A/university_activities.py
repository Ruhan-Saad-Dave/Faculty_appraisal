from sqlalchemy import Column, Integer, String, Text, ForeignKey, Double
from sqlalchemy.orm import relationship
from ...setup.database import Base

class UniversityActivity(Base):
    __tablename__ = "university_activities"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    sr_no = Column(Integer, nullable=True)
    activity = Column(String(255), nullable=False)
    nature_of_activity = Column(Text, nullable=False)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)

    faculty = relationship("Faculty")
