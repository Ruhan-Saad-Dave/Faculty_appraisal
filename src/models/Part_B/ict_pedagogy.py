from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Double
from sqlalchemy.orm import relationship
from ....setup.database import Base
from ..faculty import Faculty  # Import Faculty model for relationship

class ICTPedagogy(Base):
    __tablename__ = "ict_pedagogies"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    pedagogy_type = Column(String(100), nullable=False) # ENUM / String
    quadrants = Column(Integer, nullable=False)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)

    faculty = relationship("Faculty", back_populates="ict_pedagogies")
