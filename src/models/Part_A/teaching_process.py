from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship
from ...setup.database import Base

class TeachingProcess(Base):
    __tablename__ = "teaching_process"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    sr_no = Column(Integer, nullable=True)
    semester = Column(String(50), nullable=False)
    course_code_name = Column(String(255), nullable=False)
    planned_classes = Column(Integer, nullable=False)
    conducted_classes = Column(Integer, nullable=False)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    signature = Column(Boolean, default=False)

    faculty = relationship("Faculty")
