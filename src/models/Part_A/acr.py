from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship
from ...setup.database import Base

class ACR(Base):
    __tablename__ = "acr"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    sr_no = Column(Integer, nullable=True)
    subject = Column(String(255), nullable=False)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)
    signature = Column(Boolean, default=False)

    faculty = relationship("Faculty")
