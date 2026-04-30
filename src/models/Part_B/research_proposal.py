from sqlalchemy import Column, Integer, String, ForeignKey, Text, Double
from sqlalchemy.orm import relationship
from src.setup.database import Base
from src.models.Part_B.faculty import Faculty  # Import Faculty model for relationship

class ResearchProposal(Base):
    __tablename__ = "research_proposals"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    proposal_title = Column(Text, nullable=False)
    duration = Column(String(50), nullable=False) # Project duration (e.g., "6 months", "1 year")
    funding_agency = Column(String(255), nullable=False)
    grant_amount = Column(Double, nullable=False)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    faculty = relationship("Faculty", back_populates="research_proposals")
