from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Double, Date
from sqlalchemy.orm import relationship
from ....setup.database import Base
from ..faculty import Faculty  # Import Faculty model for relationship

class IPR(Base):
    __tablename__ = "ipr_entries"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    title = Column(Text, nullable=False)
    scope = Column(String(20), nullable=False) # National / International
    filing_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False) # Published / Granted
    patent_file_no = Column(String(100), nullable=False)
    research_score_faculty = Column(Double, default=0.0)
    research_score_hod = Column(Double, default=0.0)
    research_score_director = Column(Double, default=0.0)

    faculty = relationship("Faculty", back_populates="ipr_entries")
