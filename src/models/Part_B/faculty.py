from sqlalchemy import Column, Integer, String, ForeignKey
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
    role = Column(String, default="faculty") # Roles: faculty, hod, director, dean, vc, admin
    
    school_id = Column(UUID(as_uuid=True), ForeignKey("school.id"), nullable=True)

    # Relationships
    school = relationship("School", back_populates="faculties")

    # Part B Relationships
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

    # Part A Relationships
    teaching_processes = relationship("TeachingProcess", back_populates="faculty")
    course_files = relationship("CourseFile", back_populates="faculty")
    teaching_methods = relationship("TeachingMethods", back_populates="faculty")
    projects_part_a = relationship("ProjectPartA", back_populates="faculty")
    qualification_enhancements = relationship("QualificationEnhancement", back_populates="faculty")
    student_feedbacks = relationship("StudentFeedback", back_populates="faculty")
    departmental_activities = relationship("DepartmentalActivity", back_populates="faculty")
    university_activities = relationship("UniversityActivity", back_populates="faculty")
    social_contributions = relationship("SocialContribution", back_populates="faculty")
    industry_connections = relationship("IndustryConnect", back_populates="faculty")
    acr_entries = relationship("ACR", back_populates="faculty")
