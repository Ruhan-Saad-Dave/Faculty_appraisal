from sqlalchemy import Column, Integer, String, Text, ForeignKey, Double
from sqlalchemy.orm import relationship
from ...setup.database import Base

class SocialContribution(Base):
    __tablename__ = "social_contributions"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    sr_no = Column(Integer, nullable=True)
    activity_type = Column(String(255), nullable=False)
    details_of_activity = Column(Text, nullable=False)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)

    faculty = relationship("Faculty")
