from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Double, Date
from sqlalchemy.orm import relationship
from ....setup.database import Base
from ..faculty import Faculty  # Import Faculty model for relationship

class ConferencePaper(Base):
    __tablename__ = "conference_papers"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    event_title = Column(Text, nullable=False)
    event_date = Column(Date, nullable=False)
    activity_type = Column(String(50), nullable=False) # Lecture / Resource Person / Paper / Proceedings
    hosting_organization = Column(String(255), nullable=False)
    event_level = Column(String(50), nullable=False) # International / National
    research_score_faculty = Column(Double, default=0.0)
    research_score_hod = Column(Double, default=0.0)
    research_score_director = Column(Double, default=0.0)

    faculty = relationship("Faculty", back_populates="conference_papers")
