from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.setup.database import Base

class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String, index=True)
    role = Column(String, default="faculty")

    journal_publications = relationship("JournalPublication", back_populates="faculty")
    book_publications = relationship("BookPublication", back_populates="faculty")
    ict_pedagogies = relationship("ICTPedagogy", back_populates="faculty")
    research_guidance_entries = relationship("ResearchGuidance", back_populates="faculty")
    research_projects = relationship("ResearchProject", back_populates="faculty")
    ipr_entries = relationship("IPR", back_populates="faculty")
    research_awards = relationship("ResearchAward", back_populates="faculty")
    conference_papers = relationship("ConferencePaper", back_populates="faculty")
    research_proposals = relationship("ResearchProposal", back_populates="faculty")
    product_developments = relationship("ProductDevelopment", back_populates="faculty")
    self_development_fdp_entries = relationship("SelfDevelopmentFDP", back_populates="faculty")
    industrial_trainings = relationship("IndustrialTraining", back_populates="faculty")
