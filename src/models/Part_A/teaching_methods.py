from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship
from ...setup.database import Base

class TeachingMethods(Base):
    __tablename__ = "teaching_methods"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    sr_no = Column(Integer, nullable=True)
    short_description = Column(String(255), nullable=False)
    details_proof = Column(Boolean, default=False)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    signature = Column(Boolean, default=False)

    faculty = relationship("Faculty")
